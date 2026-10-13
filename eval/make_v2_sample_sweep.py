"""Records-request sample-size sweep on v2 data: rules baselines (free) for two seeds, and the views the AI sweep runs read.

For each sample size, requests that many charts per flagged provider (same response model as the main runs), writes a view
folder `data/synthetic_v2_<run>/view_n<size>/` (symlinks to the shared tables plus its own documentation.csv and
records_requests.csv), and scores the two rules baselines against the answer key. Writes `experiments/sample_size_sweep/rules.json`.
The AI half of the sweep is run by `eval/make_v2_ai_runs.py` (runs 261012_15..18_api, seed 42); `eval/sample_size_sweep.py`
turns everything into `docs/sample_size_sweep.md`.

Usage:
    python eval/make_v2_sample_sweep.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import records  # noqa: E402

SIZES = [10, 20, 30, 60, 100]
SOURCES = {"seed 42": "261012_1_code", "seed 101": "261012_2_code"}
RULES = {"documented_below_billed": 0.15, "data_without_tests": 0.12}
MIN_DOCS = 8
SEEDS = {"261012_1_code": 42, "261012_2_code": 101}   # the records-request seeds used by make_v2_runs.py
LINKED = ("claims.csv", "patients.csv", "providers.csv")


def make_view(src, size):
    data = os.path.join(ROOT, "data", f"synthetic_v2_{src}")
    base = os.path.join(data, "view")
    view = base if size == 30 else os.path.join(data, f"view_n{size}")
    if size != 30:
        os.makedirs(view, exist_ok=True)
        for name in LINKED:
            dst = os.path.join(view, name)
            if not os.path.exists(dst):
                os.symlink(os.path.join(base, name), dst)
    flagged = os.path.join(ROOT, "experiments", src, "flagged_threshold.csv")
    docs, st = records.run_requests(data, view, flagged, sample_n=size, seed=SEEDS[src])
    return view, st


if __name__ == "__main__":
    out = {}
    for label, src in SOURCES.items():
        truth = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{src}.json")))["providers"]
        for size in SIZES:
            view, st = make_view(src, size)
            asked = {r["provider_id"] for r in st if r["kind"] == "flagged"}
            req = sum(r["requested"] for r in st if r["kind"] == "flagged")
            got = sum(r["received"] for r in st if r["kind"] == "flagged")
            row = {"requested": req, "returned": got, "returned_per_provider": got / max(len(asked), 1), "rules": {}}
            for rule, thr in RULES.items():
                sel = records.rules_flags(view, rule, thr, MIN_DOCS, asked)
                row["rules"][rule] = {"upcoders": sum(truth[p]["role"] == "upcoder" for p in sel),
                                      "honest": sum(truth[p]["role"] != "upcoder" for p in sel)}
            out[f"{label}|{size}"] = row
            print(label, size, row, flush=True)
    os.makedirs(os.path.join(ROOT, "experiments", "sample_size_sweep"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "experiments", "sample_size_sweep", "rules.json"), "w"), indent=1)
