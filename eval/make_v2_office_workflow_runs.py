"""The frozen v2.0 workflow on the same simulated provider office the agent uses (the fair baseline arms of the M6 comparison).

Policy (fixed, no judgment): for every provider the screen flags, send a random request for 30 charts (30-day deadline); if the response
had deficiencies, send ONE follow-up naming them; then close. The usable charts plus a control sample of earlier reviews feed the same
summary step as every other v2.0 run (rules, then Claude Opus 5.5 via the Batch API where the rules are silent), the citation check and the
judge. Two screens: suspicion >= 5 (the v2.0 default) and the top 25 (the agent's likely choice). This spends real money (about $0.25 a
run); get the user's OK first.

Usage:
    python eval/make_v2_office_workflow_runs.py [--only 261013_12_api ...]
"""
import argparse
import csv
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import make_v2_ai_runs as ai  # noqa: E402
import provider_sim  # noqa: E402
import records  # noqa: E402
import run_office_baseline as rob  # noqa: E402
import workflow_policy_23 as wp23  # noqa: E402
import workflow_policy_24 as wp24  # noqa: E402
import workflow_policy_25 as wp25  # noqa: E402
import workflow_policy_40 as wp40  # noqa: E402
import workflow_policy_v21 as wp  # noqa: E402

RUNS = [("261013_12_api", "261013_4_code", "threshold", "reserved seed 202; screen suspicion >= 5; fixed office policy"),
        ("261013_13_api", "261013_5_code", "threshold", "reserved seed 303; screen suspicion >= 5; fixed office policy"),
        ("261013_14_api", "261013_4_code", "top25", "reserved seed 202; screen top 25; fixed office policy"),
        ("261013_15_api", "261013_5_code", "top25", "reserved seed 303; screen top 25; fixed office policy")]


def build_view(rid, src, screen, version="2.0", tier1_n=None, policy24=None, w40=None):
    """version "2.1": office 2.1 and the fixed v2.1 policy (eval/workflow_policy_v21.py) on data 2.1; the notes go into documentation.csv.
    version "2.2": the same, with the screen named by `screen` (eb_ratio or priority: experiments/<src>/flagged_<screen>.csv, top 25) and the data-quality pre-flight."""
    data = os.path.join(ROOT, "data", f"synthetic_v2_{src}")
    base = os.path.join(data, "view")
    view = os.path.join(data, f"view_{rid}")
    os.makedirs(view, exist_ok=True)
    for name in ("claims.csv", "patients.csv", "providers.csv"):
        dst = os.path.join(view, name)
        if not os.path.exists(dst):
            os.symlink(os.path.join(base, name), dst)
    flagged_file = os.path.join(ROOT, "experiments", src, {"threshold": "flagged_threshold.csv", "top25": "flagged.csv"}.get(screen, f"flagged_{screen}.csv"))
    flagged = [r["provider_id"] for r in csv.DictReader(open(flagged_file)) if r["flagged"] == "True"]
    if version in ("2.1", "2.2", "2.3", "2.4", "2.5", "4.0"):        # 2.2: the same office and policy as 2.1; the screen is eb_ratio or priority (top 25)
        office = provider_sim.Office(data, base, seed=1, version="2.1")
        by_provider = {}
        for r in csv.DictReader(open(os.path.join(base, "claims.csv"))):
            by_provider.setdefault(r["provider_id"], []).append(r)
        if version == "4.0":                           # 4.0 (issue 131): policy options in w40, rules 4.0, API-free
            ratio = {}
            for r in csv.DictReader(open(flagged_file)):
                exp = float(r["expected_share"])
                ratio[r["provider_id"]] = float(r["share_99215"]) / exp if exp else 0.0
            wp40.run_policy_40(office, flagged, by_provider, flagged_file, ratio, w40)
        elif version == "2.5":                           # 2.5 (issue 109): learned ask-or-skip and learned escalation, fitted on net dollars
            ratio = {}
            for r in csv.DictReader(open(flagged_file)):
                exp = float(r["expected_share"])
                ratio[r["provider_id"]] = float(r["share_99215"]) / exp if exp else 0.0
            wp25.run_policy_25(office, flagged, by_provider, flagged_file, ratio)
        elif version == "2.4":                           # 2.4 candidates (development, issue 102): policy 2.3 plus a ratio gate and a stop for silent offices
            ratio = {}
            for r in csv.DictReader(open(flagged_file)):
                exp = float(r["expected_share"])
                ratio[r["provider_id"]] = float(r["share_99215"]) / exp if exp else 0.0
            wp24.run_policy_24(office, flagged, by_provider, tier1_n or len(flagged), ratio, **(policy24 or {}))
        elif version == "2.3":                         # 2.3: two tiers on the top-10% list (workflow_policy_23.py)
            wp23.run_policy_23(office, flagged, by_provider, tier1_n or len(flagged))
        else:
            wp.run_policy_v21(office, flagged, by_provider)
    else:
        office = provider_sim.Office(data, base, seed=1)
        rob.run_policy(office, flagged)
    write_view(view, base, office, flagged)
    return view, office, flagged_file


def write_view(view, base, office, flagged):
    """Write the view's documentation.csv and records_requests.csv from the office's current state (called again after a second pass of requests).
    The control sample = earlier reviews of providers outside the flagged list."""
    req = list(csv.DictReader(open(os.path.join(base, "records_requests.csv"))))
    control = {r["provider_id"] for r in req if r["kind"] == "control"} - set(flagged)
    owner = {r["claim_id"]: r["provider_id"] for r in csv.DictReader(open(os.path.join(base, "claims.csv")))}
    docs = [r for r in csv.DictReader(open(os.path.join(base, "documentation.csv"))) if owner.get(r["claim_id"]) in control]
    docs += office.documentation_rows()
    records.write_docs(os.path.join(view, "documentation.csv"), docs)
    with open(os.path.join(view, "records_requests.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["provider_id", "kind", "requested", "received", "late", "no_response"])
        for p in sorted(control):
            w.writerow([p, "control", 0, 0, 0, 0])
        for p in flagged:
            st = office._st(p)
            w.writerow([p, "flagged", len(st["requested"]), len(st["usable"]), 0, 0])


def run(rid, src, screen, note, version="2.0", tier1_n=None, policy24=None, no_model=None, w40=None):
    """no_model None: on for workflow 2.5 only (older versions keep their frozen behavior); pass True to run an older arm API-free on future tests."""
    view, office, flagged_file = build_view(rid, src, screen, version, **({} if tier1_n is None else {"tier1_n": tier1_n}), **({} if policy24 is None else {"policy24": policy24}), **({} if w40 is None else {"w40": w40}))
    name = os.path.basename(view)

    def summaries():
        # 2.2: rules 2.2 decide more summaries without the model, and no LLM usefulness judge (the rule judge runs after; issues 91 and 93)
        ai.run(rid, src, note, view_name=name, flagged_name=os.path.basename(flagged_file), v21=version in ("2.1", "2.2", "2.3", "2.4", "2.5", "4.0"), preflight=version in ("2.2", "2.3", "2.4", "2.5", "4.0"),
               v22=version in ("2.2", "2.3", "2.4", "2.5", "4.0"), v23=version in ("2.3", "2.4", "2.5", "4.0"), llm_judge=version not in ("2.2", "2.3", "2.4", "2.5", "4.0"),
               no_model=(version in ("2.5", "4.0")) if no_model is None else no_model, rules40=version == "4.0", rules41=version == "4.0" and (w40 or {}).get("rules") == "4.1",       # 2.5 onward: no API call at all
               rules40_opts=(w40 or {}).get("rules40_opts"))
    summaries()
    if version == "4.0" and (w40 or {}).get("extend"):
        if extend_near_misses(rid, src, view, office, flagged_file, w40["extend"]):
            summaries()
    office.write_transcript(os.path.join(ROOT, "experiments", rid, "office_transcript.jsonl"))
    if getattr(office, "probe_log", None):
        json.dump(office.probe_log, open(os.path.join(ROOT, "experiments", rid, "probe_log.json"), "w"))
    if version == "4.0" and (w40 or {}).get("demand_floor") is not None:
        apply_demand_floor(rid, src, view, office, w40["demand_floor"])


def extend_near_misses(rid, src, view, office, flagged_file, opts):
    """Workflow v4.1 option `extend` (H16): a provider the rules call upcoding whose payer-visible point estimate of the recovery is at least c times the cost of a demand but whose 90% lower bound
    is below it gets a second RANDOM request of `more` charts; the view is rewritten and the summaries are rebuilt by the caller. Returns the list of providers extended. No answer key."""
    import dollar_reward as dr
    import recovery_40 as s4
    import summary_rules as sr
    import workflow_policy_v21 as v21
    cost = s4.staff_cost(0, 0, 0, 1, 0, s4.PARAMS)[0]
    base = os.path.join(ROOT, "data", f"synthetic_v2_{src}", "view")
    claims = {}
    for r in csv.DictReader(open(os.path.join(base, "claims.csv"))):
        claims.setdefault(r["provider_id"], []).append(r)
    level = dr.level_of_rows(list(csv.DictReader(open(os.path.join(view, "documentation.csv")))))
    recs = [json.loads(x) for x in open(os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")) if x.strip()]
    log, done = {}, []
    for r in recs:
        if r["summary"]["leaning"] != sr.UPCODING:
            continue
        pid = r["provider_id"]
        e = s4.recovery(claims.get(pid, []), office.random_claim_ids(pid), level, s4.PARAMS)
        if e["mode"] == "extrapolated" and e["point"] >= opts["c"] * cost and e["value"] < cost:
            resp = v21._follow(office, pid, office.send_request(pid, {"kind": "random", "n": opts["more"]}, deadline=30))
            log[pid] = {"point": round(e["point"], 2), "lower_bound": round(e["value"], 2), "blocked": "error" in resp}
            if "error" not in resp:
                done.append(pid)
            office.close_request(pid, "workflow v4.1 near-miss extension")
    if done:
        flagged = [r["provider_id"] for r in csv.DictReader(open(flagged_file)) if r["flagged"] == "True"]
        write_view(view, base, office, flagged)
    json.dump(log, open(os.path.join(ROOT, "experiments", rid, "extension_log.json"), "w"))
    return done


def apply_demand_floor(rid, src, view, office, floor):
    """Workflow v4.0 option `demand_floor` (issue 131): a provider the rules call upcoding is demanded from only when the payer's own estimate of the recovery (the 90% lower bound from the
    provider's random sample, recovery_40.recovery: no answer key) is at least `floor` dollars ("cost" = the staff cost of a demand); below it the call is withdrawn: leaning inconclusive."""
    import dollar_reward as dr
    import recovery_40 as s4
    import summary_rules as sr
    if isinstance(floor, str) and floor.startswith("cost"):             # "cost" = the staff cost of a demand; "cost2" = twice that
        floor = s4.staff_cost(0, 0, 0, 1, 0, s4.PARAMS)[0] * (float(floor[4:]) if floor[4:] else 1.0)
    claims = {}
    for r in csv.DictReader(open(os.path.join(view, "claims.csv"))):
        claims.setdefault(r["provider_id"], []).append(r)
    level = dr.level_of_rows(list(csv.DictReader(open(os.path.join(view, "documentation.csv")))))
    path = os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")
    recs = [json.loads(x) for x in open(path) if x.strip()]
    dropped = {}
    for r in recs:
        if r["summary"]["leaning"] != sr.UPCODING:
            continue
        pid = r["provider_id"]
        lb = s4.recovery(claims.get(pid, []), office.random_claim_ids(pid), level, s4.PARAMS)["value"]
        if lb < floor:
            dropped[pid] = round(lb, 2)
            r["summary"] = {**r["summary"], "leaning": sr.INCONCLUSIVE, "headline": f"{pid}: estimated recovery below the cost of a demand",
                            "rationale": r["summary"]["rationale"] + f" No demand is sent: the estimated recovery (lower bound ${lb:,.0f}) is below the staff cost of a demand (${floor:,.0f})."}
            r["demand_floor"] = True
    with open(path, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in recs)
    json.dump({"floor": floor, "withdrawn": dropped}, open(os.path.join(ROOT, "experiments", rid, "demand_floor.json"), "w"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    for rid, src, screen, note in RUNS:
        if not a.only or rid in a.only:
            print("start", rid, flush=True)
            run(rid, src, screen, note)
            print("done", rid, flush=True)
