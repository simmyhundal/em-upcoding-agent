"""Build the v2 code-only runs (no AI): generate data, derive the detector view, screen, request records, apply rules baselines.

Each run folder under experiments/ is self-contained: flagged.csv (top 25 by combined rank), flagged_threshold.csv (the
suspicion-at-or-above-5 list that gets a records request), documentation.csv and records_requests.csv (what the request
returned), the rules-baseline selections, and a README. Data folders and answer keys are gitignored.

The rules thresholds (documented level below billed in more than 15% of returned charts; note claims moderate-or-higher data
reviewed with no lab or test line on more than 12%; at least 8 returned charts) were set by looking at seed 42 and then FROZEN;
every other seed here is untouched by that choice.

Usage:
    python eval/make_v2_runs.py [--only 261012_1_code ...]
"""
import argparse
import csv
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import derive  # noqa: E402
import generate_v2  # noqa: E402
import records  # noqa: E402

MIN_SUSPICION = 5
MAX_FLAGGED = 25
RULES = {"documented_below_billed": 0.15, "data_without_tests": 0.12}
MIN_DOCS = 8
RUNS = [
    # id, seed, providers, upcoders, hard negatives, clone share, note
    ("261012_1_code", 42, 216, 8, 8, 0.5, "seed 42, 3.7% upcoders, half of them clone their notes"),
    ("261012_2_code", 101, 216, 8, 8, 0.5, "held-out seed 101, 3.7% upcoders, half clone their notes"),
    ("261012_3_code", 7, 600, 3, 18, 0.5, "0.5% upcoders (3 of 600), half clone"),
    ("261012_4_code", 7, 600, 6, 18, 0.5, "1% upcoders (6 of 600), half clone"),
    ("261012_5_code", 7, 600, 12, 18, 0.5, "2% upcoders (12 of 600), half clone"),
    ("261012_6_code", 42, 216, 8, 8, 0.0, "seed 42, nobody clones notes"),
    ("261012_7_code", 42, 216, 8, 8, 1.0, "seed 42, every upcoder clones notes"),
    # reserved seeds for the Milestone 6 evaluation (docs/versioning.md): same settings as 261012_1_code, never tuned on
    ("261013_4_code", 202, 216, 8, 8, 0.5, "reserved seed 202, 3.7% upcoders, half clone notes"),
    ("261013_5_code", 303, 216, 8, 8, 0.5, "reserved seed 303, 3.7% upcoders, half clone notes"),
]


def run(spec, data_version="2.0", **v22):
    """data_version "2.1" also writes the note package; claims and the records universe are identical to 2.0 for the same seed.
    data_version "2.2" accepts the data 2.2 options of generate_v2.build (honest noise, group billing, defects, ...) as keyword arguments."""
    rid, seed, n, n_up, n_hn, clone, note = spec
    data = os.path.join(ROOT, "data", f"synthetic_v2_{rid}")
    key = os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{rid}.json")
    out = os.path.join(ROOT, "experiments", rid)
    os.makedirs(out, exist_ok=True)
    generate_v2.build(data, key, seed=seed, n_providers=n, n_upcoders=n_up, n_hard_neg=n_hn, clone_share=clone, data_version=data_version, **v22)
    view = os.path.join(data, "view")
    derive.build_view(data, view)
    py = sys.executable
    flag = os.path.join(ROOT, "src", "flagging.py")
    subprocess.run([py, flag, view, os.path.join(out, "flagged.csv")], check=True, capture_output=True)
    subprocess.run([py, flag, view, os.path.join(out, "flagged_threshold.csv"), "--min-suspicion", str(MIN_SUSPICION),
                    "--max-flagged", str(MAX_FLAGGED)], check=True, capture_output=True)
    docs, st = records.run_requests(data, view, os.path.join(out, "flagged_threshold.csv"), seed=seed)
    for name in ("documentation.csv", "records_requests.csv"):
        open(os.path.join(out, name), "w").write(open(os.path.join(view, name)).read())
    asked = {r["provider_id"] for r in st if r["kind"] == "flagged"}
    for rule, thr in RULES.items():
        sel = records.rules_flags(view, rule, thr, MIN_DOCS, asked)
        with open(os.path.join(out, f"rules_{rule}.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["provider_id", "rate", "returned_charts"])
            for p, (rate, k) in sorted(sel.items()):
                w.writerow([p, round(rate, 3), k])
    flagged_n = len(asked)
    got = sum(r["received"] for r in st if r["kind"] == "flagged")
    req = sum(r["requested"] for r in st if r["kind"] == "flagged")
    open(os.path.join(out, "README.md"), "w").write(
        f"# {rid}\n\nv2 data ({data_version}), code only (no AI step). {note}.\n\n"
        f"- Screen: `flagged.csv` (top 25 by combined rank) and `flagged_threshold.csv` (suspicion at or above {MIN_SUSPICION}, at most "
        f"{MAX_FLAGGED}); {flagged_n} providers flagged by the threshold.\n"
        f"- Records request for those providers plus a 30-provider control sample: {got} of {req} requested charts for the flagged "
        f"providers came back in time (`documentation.csv`, `records_requests.csv`).\n"
        f"- Rules baselines on that evidence: `rules_documented_below_billed.csv` (documented level below billed in more than "
        f"{RULES['documented_below_billed']:.0%} of returned charts) and `rules_data_without_tests.csv` (note claims moderate-or-higher data "
        f"reviewed but the claim has no lab or test line, more than {RULES['data_without_tests']:.0%}); at least {MIN_DOCS} returned charts.\n"
        f"- Rule thresholds were chosen by looking at seed 42 and frozen before the other seeds were generated.\n"
        f"- Nothing here is an AI result. Answer key: `eval/answer_key/ground_truth_v2_{rid}.json` (gitignored).\n")
    return rid


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    for spec in RUNS:
        if not a.only or spec[0] in a.only:
            print("built", run(spec), flush=True)
