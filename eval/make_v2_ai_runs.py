"""Run the AI step on the v2 code-only datasets: summaries (rules plus model), citation check, judge, packets.

Each run folder (`YYMMDD_X_api`) is self-contained and reuses the screen and records request from the matching code-only run
(`experiments/<code run>/`). Model calls use the Batch API with a response cache inside the run folder. This spends real money
(see usage_writer.jsonl and usage_judge.jsonl in each folder); get the user's OK first.

Usage:
    python eval/make_v2_ai_runs.py [--only 261012_8_api ...]
"""
import argparse
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
RUNS = [("261012_8_api", "261012_1_code", "v2 seed 42, half of the upcoders clone their notes"),
        ("261012_9_api", "261012_2_code", "v2 held-out seed 101, half clone; code frozen before this seed was looked at"),
        ("261012_10_api", "261012_6_code", "v2 seed 42, nobody clones notes"),
        ("261012_11_api", "261012_7_code", "v2 seed 42, every upcoder clones notes"),
        ("261012_12_api", "261012_3_code", "v2 seed 7, 0.5% upcoders (3 of 600), half clone notes"),
        ("261012_13_api", "261012_4_code", "v2 seed 7, 1% upcoders (6 of 600), half clone notes"),
        ("261012_14_api", "261012_5_code", "v2 seed 7, 2% upcoders (12 of 600), half clone notes"),
        ("261013_6_api", "261013_4_code", "v2 reserved seed 202, half clone; frozen v2.0 workflow"),
        ("261013_7_api", "261013_5_code", "v2 reserved seed 303, half clone; frozen v2.0 workflow"),
        ("261012_15_api", "261012_1_code", "v2 seed 42, half clone; records request of 10 charts per flagged provider", "view_n10"),
        ("261012_16_api", "261012_1_code", "v2 seed 42, half clone; records request of 20 charts per flagged provider", "view_n20"),
        ("261012_17_api", "261012_1_code", "v2 seed 42, half clone; records request of 60 charts per flagged provider", "view_n60"),
        ("261012_18_api", "261012_1_code", "v2 seed 42, half clone; records request of 100 charts per flagged provider", "view_n100")]


def sh(*args):
    r = subprocess.run([PY, *args], cwd=ROOT, capture_output=True, text=True)
    print(r.stdout.strip()[-600:], flush=True)
    if r.returncode:
        print(r.stderr[-1500:], flush=True)
        raise SystemExit(f"failed: {' '.join(args[:2])}")


def run(rid, src, note, view_name="view", flagged_name="flagged_threshold.csv", v21=False, preflight=False, v22=False, llm_judge=True, v23=False, no_model=False):
    """view_name: a folder under the data dir holding documentation.csv and records_requests.csv from a different records request
    (the sample-size sweep); the screen always comes from the code-only run `src`. v21: version 2.1 summaries (conditional next steps,
    lint and repair). v22: workflow v2.2 summaries (the 2.1 summaries with rules 2.2, issue 91). llm_judge=False skips the LLM usefulness
    judge (release 2 uses the rule judge only, issue 93); the run then has no usefulness.jsonl and the scoreboard leaves that eval unscored."""
    out = os.path.join(ROOT, "experiments", rid)
    os.makedirs(out, exist_ok=True)
    s = os.path.join(ROOT, "experiments", src)
    view = os.path.join(ROOT, "data", f"synthetic_v2_{src}", view_name)
    for name in ("flagged.csv", "flagged_threshold.csv", flagged_name):
        shutil.copy(os.path.join(s, name), os.path.join(out, name))
    for name in ("documentation.csv", "records_requests.csv"):
        shutil.copy(os.path.join(view if view_name != "view" else s, name), os.path.join(out, name))
    flagged = os.path.join(out, flagged_name)
    summaries, checked = os.path.join(out, "case_summaries.jsonl"), os.path.join(out, "case_summaries_checked.jsonl")
    sh("src/case_summary.py", view, flagged, summaries, "--cache-dir", os.path.join(out, "llm_cache"),
       "--usage-jsonl", os.path.join(out, "usage_writer.jsonl"), *(["--v23"] if v23 else ["--v22"] if v22 else ["--v21"] if v21 else []), *(["--no-model"] if no_model else []))
    sh("src/guardrail.py", view, summaries, checked)
    if preflight:                                      # workflow v2.2: data-quality pre-flight on the plan tables, then hold affected summaries
        import csv
        import json
        import data_quality as dq
        report = dq.run_checks(os.path.join(ROOT, "data", f"synthetic_v2_{src}"))
        dq.write_report(report, out)
        owner = {r["claim_id"]: r["provider_id"] for r in csv.DictReader(open(os.path.join(view, "claims.csv")))}
        charts = {}
        for r in csv.DictReader(open(os.path.join(out, "documentation.csv"))):
            charts[owner.get(r["claim_id"])] = charts.get(owner.get(r["claim_id"]), 0) + 1
        recs = [json.loads(x) for x in open(checked) if x.strip()]
        recs, held = dq.apply_holds(recs, report, charts)
        with open(checked, "w") as f:
            f.writelines(json.dumps(x) + "\n" for x in recs)
        print(f"data-quality pre-flight {report['status']}: {sum(1 for x in recs if x.get('data_quality_hold'))} summaries carry the data caveat, {len(held)} held", flush=True)
    if llm_judge:
        sh("eval/judge_usefulness.py", view, flagged, checked, os.path.join(out, "usefulness.jsonl"),
           "--cache-dir", os.path.join(out, "llm_cache_judge"), "--usage-jsonl", os.path.join(out, "usage_judge.jsonl"))
    sh("src/finalize_run.py", out, view, flagged, checked)
    open(os.path.join(out, "README.md"), "w").write(
        f"# {rid}\n\nv2 data, the full pipeline with the AI step{' (workflow v2.2 summaries: rules 2.2)' if v22 else ' (workflow v2.1 summaries)' if v21 else ''}. {note}.\n\n"
        f"- Screen from `experiments/{src}/` (`flagged_threshold.csv`); records request in `documentation.csv` and `records_requests.csv`.\n"
        "- Summaries: obvious cases decided and written by rules (`src/summary_rules.py`), the rest by Claude Opus 5.5 through the Batch API "
        "(headline, leaning and interpretation only). Each record says which (`source`) and what the rule said (`rule_leaning`).\n"
        + ("- Judge: Claude Sonnet 5.5 through the Batch API, with a deterministic number check; templating is no longer checked.\n" if llm_judge else
           "- Judge: no LLM usefulness judge (release 2 uses the deterministic rule judge only, `usefulness_rules.jsonl`).\n") +
        f"- Cost: `usage_writer.jsonl` and `usage_judge.jsonl` (estimated from list prices, batch at half). Answer key: "
        f"`eval/answer_key/ground_truth_v2_{src}.json` (gitignored).\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    for rid, src, note, *view in RUNS:
        if not a.only or rid in a.only:
            print("start", rid, flush=True)
            run(rid, src, note, *view)
            print("done", rid, flush=True)
