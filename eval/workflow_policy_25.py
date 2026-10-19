"""Workflow v2.5 records policy (issue 109): learned ask-or-skip, then learned stop-or-escalate, both fitted on net dollars (src/policy_25.json, src/policy_25.py).

A fixed workflow: the same two formulas run every time and nothing is learned during a run. Practices the ask model skips get no request at all.
"""
import csv

import escalation_policy as ep
import policy_25 as p25
import workflow_policy_23 as p23
import workflow_policy_v21 as v21


def run_policy_25(office, provider_ids, claims_by_provider, flagged_file, ratio, policy=None):
    policy = policy or p25.load()
    rows = {r["provider_id"]: r for r in csv.DictReader(open(flagged_file))}
    office.policy_log = {}
    for rank, pid in enumerate(provider_ids):
        if not p25.ask(policy, p25.ask_vector(rows[pid])):
            continue
        resp = v21._follow(office, pid, office.send_request(pid, {"kind": "random", "n": p23.RANDOM_N}, deadline=30))
        if "error" in resp:
            continue
        st = office.state[pid]
        x = ep.state_vector(list(st["usable"].values()), claims_by_provider.get(pid, []), rank + 1, ratio.get(pid, 0.0), st["round"])
        branch = p25.choose(policy, x)
        office.policy_log[pid] = (x, branch)
        if branch in ("TARG", "BOTH") and st["round"] < office.max_rounds:
            v21._follow(office, pid, office.send_request(pid, {"kind": "targeted", "cpt": "99215", "n": p23.TARGETED_N}, deadline=30))
        audit_rows = [r for c, r in st["usable"].items() if r.get("note_id")]
        if branch in ("AUD", "BOTH") and audit_rows and st["round"] < office.max_rounds:
            office.request_audit_trail(pid, [r["claim_id"] for r in audit_rows][:p23.AUDIT_MAX])
        office.close_request(pid, f"learned policy 2.5: {branch}")
