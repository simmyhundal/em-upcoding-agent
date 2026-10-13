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
        ("261012_11_api", "261012_7_code", "v2 seed 42, every upcoder clones notes")]


def sh(*args):
    r = subprocess.run([PY, *args], cwd=ROOT, capture_output=True, text=True)
    print(r.stdout.strip()[-600:], flush=True)
    if r.returncode:
        print(r.stderr[-1500:], flush=True)
        raise SystemExit(f"failed: {' '.join(args[:2])}")


def run(rid, src, note):
    out = os.path.join(ROOT, "experiments", rid)
    os.makedirs(out, exist_ok=True)
    s = os.path.join(ROOT, "experiments", src)
    for name in ("flagged.csv", "flagged_threshold.csv", "documentation.csv", "records_requests.csv"):
        shutil.copy(os.path.join(s, name), os.path.join(out, name))
    view = os.path.join(ROOT, "data", f"synthetic_v2_{src}", "view")
    flagged = os.path.join(out, "flagged_threshold.csv")
    summaries, checked = os.path.join(out, "case_summaries.jsonl"), os.path.join(out, "case_summaries_checked.jsonl")
    sh("src/case_summary.py", view, flagged, summaries, "--cache-dir", os.path.join(out, "llm_cache"),
       "--usage-jsonl", os.path.join(out, "usage_writer.jsonl"))
    sh("src/guardrail.py", view, summaries, checked)
    sh("eval/judge_usefulness.py", view, flagged, checked, os.path.join(out, "usefulness.jsonl"),
       "--cache-dir", os.path.join(out, "llm_cache_judge"), "--usage-jsonl", os.path.join(out, "usage_judge.jsonl"))
    sh("src/finalize_run.py", out, view, flagged, checked)
    open(os.path.join(out, "README.md"), "w").write(
        f"# {rid}\n\nv2 data, the full pipeline with the AI step. {note}.\n\n"
        f"- Screen and records request: copied from `experiments/{src}/` (`flagged_threshold.csv`, `documentation.csv`, `records_requests.csv`).\n"
        "- Summaries: obvious cases decided and written by rules (`src/summary_rules.py`), the rest by Claude Opus 5.5 through the Batch API "
        "(headline, leaning and interpretation only). Each record says which (`source`) and what the rule said (`rule_leaning`).\n"
        "- Judge: Claude Sonnet 5.5 through the Batch API, with a deterministic number check; templating is no longer checked.\n"
        f"- Cost: `usage_writer.jsonl` and `usage_judge.jsonl` (estimated from list prices, batch at half). Answer key: "
        f"`eval/answer_key/ground_truth_v2_{src}.json` (gitignored).\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    for rid, src, note in RUNS:
        if not a.only or rid in a.only:
            print("start", rid, flush=True)
            run(rid, src, note)
            print("done", rid, flush=True)
