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
import workflow_policy_v21 as wp  # noqa: E402

RUNS = [("261013_12_api", "261013_4_code", "threshold", "reserved seed 202; screen suspicion >= 5; fixed office policy"),
        ("261013_13_api", "261013_5_code", "threshold", "reserved seed 303; screen suspicion >= 5; fixed office policy"),
        ("261013_14_api", "261013_4_code", "top25", "reserved seed 202; screen top 25; fixed office policy"),
        ("261013_15_api", "261013_5_code", "top25", "reserved seed 303; screen top 25; fixed office policy")]


def build_view(rid, src, screen, version="2.0"):
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
    if version in ("2.1", "2.2"):                      # 2.2: the same office and policy as 2.1; the screen is eb_ratio or priority (top 25)
        office = provider_sim.Office(data, base, seed=1, version="2.1")
        by_provider = {}
        for r in csv.DictReader(open(os.path.join(base, "claims.csv"))):
            by_provider.setdefault(r["provider_id"], []).append(r)
        wp.run_policy_v21(office, flagged, by_provider)
    else:
        office = provider_sim.Office(data, base, seed=1)
        rob.run_policy(office, flagged)
    # control sample = earlier reviews of providers outside the flagged list
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
            st = office.state[p]
            w.writerow([p, "flagged", len(st["requested"]), len(st["usable"]), 0, 0])
    return view, office, flagged_file


def run(rid, src, screen, note, version="2.0"):
    view, office, flagged_file = build_view(rid, src, screen, version)
    name = os.path.basename(view)
    ai.run(rid, src, note, view_name=name, flagged_name=os.path.basename(flagged_file), v21=version in ("2.1", "2.2"), preflight=version == "2.2")
    office.write_transcript(os.path.join(ROOT, "experiments", rid, "office_transcript.jsonl"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    for rid, src, screen, note in RUNS:
        if not a.only or rid in a.only:
            print("start", rid, flush=True)
            run(rid, src, screen, note)
            print("done", rid, flush=True)
