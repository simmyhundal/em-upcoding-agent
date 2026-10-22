"""Workflow v4.0 records policy (issue 131; the RL loop on data 4.0 and score 4.0). Built on policy 2.5 (eval/workflow_policy_25.py); every option off reproduces policy 2.5.

Options (a dict; all default to the policy 2.5 behavior):
  sample_cpts  None, or a list of billed codes: the first sample is a random sample drawn WITHIN that frame (for example ["99214", "99215"]); a stratified audit universe whose strata
               are sampled at random, so the estimate stays valid for those strata
  n            charts in the first sample (30)
  ask          "policy25" (the learned ask-or-skip of workflow v2.5), "linear" (ask-or-skip refitted on score 4.0: a ridge model of the net value of asking, file `ask_model`, default src/policy_40_ask.json),
               "all" (every listed provider), or an integer K (the first K of the list)
  escalate     "policy25" (the learned stop-or-escalate), "stop" (no second request: the first sample and its follow-up decide)
The rules are chosen separately (summary_rules.rule_leaning_40 when the run is built as version 4.0).
"""
import csv
import json
import os

import escalation_policy as ep
import policy_25 as p25
import policy_40 as pol40
import workflow_policy_23 as p23
import workflow_policy_v21 as v21

# Workflow v4.0 as frozen after the RL loop of issue 131 (version H8 in eval/w_loop.py): screen eb_upper_t (top 10%), rules 4.0, a first sample of 30 random charts, the ask-or-skip refitted on score 4.0
# (src/policy_40_ask.json, fitted on development batches 1 to 4), no escalation, and a demand only when the payer's estimate of the recovery covers the staff cost of a demand.
FROZEN_V40 = {"screen": "eb_upper_t", "w40": {"ask": "linear", "escalate": "stop", "demand_floor": "cost"}}
DEFAULTS = {"sample_cpts": None, "n": p23.RANDOM_N, "ask": "policy25", "escalate": "policy25", "ask_model": None}
ASK_MODEL = pol40.ASK_MODEL
ask_linear = pol40.ask_linear


def run_policy_40(office, provider_ids, claims_by_provider, flagged_file, ratio, opts=None):
    o = {**DEFAULTS, **(opts or {})}
    policy = p25.load()
    model = json.load(open(o["ask_model"] or ASK_MODEL)) if o["ask"] == "linear" else None
    rows = {r["provider_id"]: r for r in csv.DictReader(open(flagged_file))}
    office.policy_log = {}
    for rank, pid in enumerate(provider_ids):
        if o["ask"] == "policy25":
            if not p25.ask(policy, p25.ask_vector(rows[pid])):
                continue
        elif o["ask"] == "linear":
            if not ask_linear(model, rows[pid], claims_by_provider.get(pid, [])):
                continue
        elif isinstance(o["ask"], int) and rank >= o["ask"]:
            continue
        sample = {"kind": "random", "n": o["n"]}
        if o["sample_cpts"]:
            sample["cpts"] = list(o["sample_cpts"])
        resp = v21._follow(office, pid, office.send_request(pid, sample, deadline=30))
        if "error" in resp:
            continue
        st = office.state[pid]
        branch = "STOP"
        if o["escalate"] == "policy25":
            x = ep.state_vector(list(st["usable"].values()), claims_by_provider.get(pid, []), rank + 1, ratio.get(pid, 0.0), st["round"])
            branch = p25.choose(policy, x)
            office.policy_log[pid] = (x, branch)
        if branch in ("TARG", "BOTH") and st["round"] < office.max_rounds:
            v21._follow(office, pid, office.send_request(pid, {"kind": "targeted", "cpt": "99215", "n": p23.TARGETED_N}, deadline=30))
        audit_rows = [r for c, r in st["usable"].items() if r.get("note_id")]
        if branch in ("AUD", "BOTH") and audit_rows and st["round"] < office.max_rounds:
            office.request_audit_trail(pid, [r["claim_id"] for r in audit_rows][:p23.AUDIT_MAX])
        office.close_request(pid, f"policy 4.0: {branch}")
