"""Write a run's reviewer-facing materials inside the run's own folder, so a later run cannot overwrite them.

For one run (its data, flagged list and guardrail-checked summaries) this builds, under RUN_DIR:
  charts/       one evidence chart (SVG) per flagged provider
  cases/        one readable case page per provider plus an index (the review queue for SIU reviewers)
  pi_packets/   Payment Integrity packets for the providers whose summaries lean "upcoding" (with a simulated worked example)
All links are relative inside RUN_DIR, so the folder is self-contained. No API calls and no answer key.

Usage:
    python src/finalize_run.py RUN_DIR DATA_DIR FLAGGED_CSV CHECKED_SUMMARIES_JSONL [--allowed data/baselines/allowed_amounts_ga_fp.json]
"""
import argparse
import os

import case_report
import evidence_chart
import pi_packet

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_ALLOWED = os.path.join(ROOT, "data", "baselines", "allowed_amounts_ga_fp.json")


def finalize(run_dir, data_dir, flagged_csv, checked_path, allowed_path=DEFAULT_ALLOWED):
    charts = os.path.join(run_dir, "charts")
    evidence_chart.make_charts(data_dir, flagged_csv, charts)
    n_cases = case_report.build(checked_path, charts, os.path.join(run_dir, "cases"))
    packets = pi_packet.build(data_dir, flagged_csv, checked_path, charts, allowed_path,
                              os.path.join(run_dir, "pi_packets"), example=True)
    return n_cases, packets


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for n in ("run_dir", "data_dir", "flagged_csv", "checked_summaries"):
        ap.add_argument(n)
    ap.add_argument("--allowed", default=DEFAULT_ALLOWED)
    a = ap.parse_args()
    cases, packets = finalize(a.run_dir, a.data_dir, a.flagged_csv, a.checked_summaries, a.allowed)
    print(f"{cases} case pages and {len(packets)} recovery packets written under {a.run_dir}")
