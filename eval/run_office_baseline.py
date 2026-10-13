"""No-API run: the fixed-policy workflow against the simulated provider office (issue 47).

Policy (the baseline the agent is compared with in #42): for every provider the screen flags, send a random request for 30 charts
with a 30-day deadline; if the response had deficiencies, send ONE follow-up naming them; then close. The result is scored with the
chart rule on whatever usable charts came back. Honest-doctor burden (requests, rounds and days spent on honest doctors) is
counted from the answer key, which only this evaluation script reads.

Usage:
    python eval/run_office_baseline.py RUN_ID CODE_RUN [--correlation 0.0] [--seed 1]
e.g. python eval/run_office_baseline.py 261013_1_code 261012_1_code
"""
import argparse
import csv
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import provider_sim  # noqa: E402
import records  # noqa: E402

SAMPLE = {"kind": "random", "n": 30}


def run_policy(office, provider_ids):
    for pid in provider_ids:
        resp = office.send_request(pid, SAMPLE, deadline=30)
        if resp.get("deficiencies") and resp["rounds_left"] > 0:
            office.follow_up(pid, [d["code"] for d in resp["deficiencies"]], deadline=30)
        office.close_request(pid, "fixed policy: one follow-up, then close")


def main(run_id, code_run, correlation=0.0, seed=1):
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code_run}")
    view = os.path.join(data, "view")
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code_run}.json")))["providers"]
    roles = {p: v["role"] for p, v in key.items()}
    flagged = [r["provider_id"] for r in csv.DictReader(open(os.path.join(ROOT, "experiments", code_run, "flagged_threshold.csv")))
               if r["flagged"] == "True"]
    office = provider_sim.Office(data, view, seed=seed, correlation=correlation, roles=roles)
    run_policy(office, flagged)
    out = os.path.join(ROOT, "experiments", run_id)
    os.makedirs(out, exist_ok=True)
    office.write_transcript(os.path.join(out, "transcript.jsonl"))
    docs = office.documentation_rows()
    with open(os.path.join(out, "documentation.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=records.DOC_COLS)
        w.writeheader()
        w.writerows(docs)
    tmp = os.path.join(data, f"view_{run_id}")
    os.makedirs(tmp, exist_ok=True)
    for name in ("claims.csv", "patients.csv", "providers.csv"):
        dst = os.path.join(tmp, name)
        if not os.path.exists(dst):
            os.symlink(os.path.join(view, name), dst)
    open(os.path.join(tmp, "documentation.csv"), "w").write(open(os.path.join(out, "documentation.csv")).read())
    sel = records.rules_flags(tmp, "documented_below_billed", 0.15, 8, set(flagged))
    st = office.state
    honest = [p for p in flagged if roles[p] != "upcoder"]
    ends = {k: sum(v["closed"] == k for v in st.values()) for k in ("complete", "partial", "non_responsive")}
    res = {"run": run_id, "screen_run": code_run, "correlation": correlation, "providers_requested": len(flagged),
           "end_states": ends, "mean_usable_charts": statistics.mean(len(v["usable"]) for v in st.values()),
           "mean_rounds": statistics.mean(v["round"] for v in st.values()), "mean_days": statistics.mean(v["day"] for v in st.values()),
           "requests_to_honest": len(honest), "rounds_on_honest": sum(st[p]["round"] for p in honest),
           "chart_rule_upcoders_found": sum(roles[p] == "upcoder" for p in sel),
           "chart_rule_honest_accused": sum(roles[p] != "upcoder" for p in sel)}
    json.dump(res, open(os.path.join(out, "results.json"), "w"), indent=1)
    open(os.path.join(out, "README.md"), "w").write(
        f"# {run_id}\n\nNo AI. The frozen v2.0 workflow's fixed policy against the simulated provider office "
        f"(`src/provider_sim.py`): for each provider the screen flagged in `experiments/{code_run}/`, send a random request for 30 "
        f"charts (30-day deadline), send one follow-up if the response had deficiencies, then close. Office behavior is drawn "
        f"independently of upcoder status (correlation {correlation}).\n\n```\n{json.dumps(res, indent=1)}\n```\n\n"
        f"Compare with the single-draw request in `experiments/{code_run}/` (about 18 usable charts per provider). "
        f"Documentation is generated from the same hidden truth that defines an upcoded visit; the office behaviors and their "
        f"probabilities are illustrative assumptions. Answer key: `eval/answer_key/ground_truth_v2_{code_run}.json` (gitignored).\n")
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("run_id")
    ap.add_argument("code_run")
    ap.add_argument("--correlation", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    print(json.dumps(main(a.run_id, a.code_run, a.correlation, a.seed), indent=1))
