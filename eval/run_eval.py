"""Eval harness: score each detector against ground truth and write a side-by-side report.

Detectors compared (all use the same top-N cutoff): plain z-score, risk-adjusted, combined list.
Reads reports/flagged.csv (from flagging.py) and the answer key (eval/answer_key/ground_truth.json; eval only).
Optionally reads a guardrail output file for citation accuracy.

Usage:
    python eval/run_eval.py FLAGGED_CSV GROUND_TRUTH_JSON OUT_MD [--top-n 25] [--checked-summaries FILE]
"""
import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from score import score  # noqa: E402

DETECTORS = [("Plain z-score", "rank_zscore"), ("Risk-adjusted", "rank_riskadj"), ("Combined list", "rank")]


def evaluate(flagged_rows, truth, top_n=25):
    roles = {p: v["role"] for p, v in truth["providers"].items()}
    out = {}
    for name, col in DETECTORS:
        ranks = {r["provider_id"]: int(float(r[col])) for r in flagged_rows}
        flagged = [p for p, k in ranks.items() if k <= top_n]
        s = score(flagged, truth)
        out[name] = {
            "upcoders_found": s["upcoder"]["flagged"], "upcoders_total": s["upcoder"]["total"],
            "hard_neg_flagged": s["hard_negative"]["flagged"], "hard_neg_total": s["hard_negative"]["total"],
            "normal_flagged": s["normal"]["flagged"], "normal_total": s["normal"]["total"],
            "upcoder_ranks": sorted(ranks[p] for p in roles if roles[p] == "upcoder"),
            "hard_neg_ranks": sorted(ranks[p] for p in roles if roles[p] == "hard_negative"),
            "precision": s["upcoder"]["flagged"] / top_n,
        }
    return out


def citation_stats(path):
    if not path or not os.path.exists(path):
        return None
    rec = [json.loads(line) for line in open(path) if line.strip()]
    cited = sum(r["citation_check"]["n_cited"] for r in rec)
    valid = sum(r["citation_check"]["n_valid"] for r in rec)
    return {"summaries": len(rec), "passed": sum(r["citation_check"]["passed"] for r in rec),
            "accuracy": (valid / cited) if cited else None, "cited": cited, "valid": valid}


def render(res, top_n, cit):
    z, ra, comb = (res[n] for n, _ in DETECTORS)
    lines = [f"# Eval report (top {top_n} flagged)", "",
             "| Metric | Plain z-score | Risk-adjusted | Combined list | Target |", "|---|---|---|---|---|"]

    def row(label, f, target):
        lines.append(f"| {label} | " + " | ".join(f(res[n]) for n, _ in DETECTORS) + f" | {target} |")
    row("Upcoders found", lambda r: f"{r['upcoders_found']} / {r['upcoders_total']}", ">= 7 / 8")
    row("Hard negatives falsely flagged", lambda r: f"{r['hard_neg_flagged']} / {r['hard_neg_total']}",
        "lower than plain z-score")
    row("Normal providers falsely flagged", lambda r: f"{r['normal_flagged']} / {r['normal_total']}", "-")
    row("Precision (upcoders / flagged)", lambda r: f"{r['precision']:.0%}", "-")
    row("Upcoder ranks", lambda r: ",".join(map(str, r["upcoder_ranks"])), "-")
    row("Hard-negative ranks", lambda r: ",".join(map(str, r["hard_neg_ranks"])), "-")
    lines += ["", "## LLM summary metrics"]
    if cit:
        acc = "n/a" if cit["accuracy"] is None else f"{cit['accuracy']:.1%}"
        lines += [f"- Citation accuracy: {acc} ({cit['valid']}/{cit['cited']}); "
                  f"{cit['passed']}/{cit['summaries']} summaries passed the guardrail. Target: 100%."]
    else:
        lines += ["- Citation accuracy: pending (needs the live summary run). Target: 100%."]
    lines += ["- Summary usefulness (1-5, see eval/rubric.md): pending. Target: average >= 4.", "",
              "## Target check"]
    lines += [f"- Recall >= 7/8: {'met' if comb['upcoders_found'] >= 7 else 'NOT met'} (combined list)"]
    better = comb["hard_neg_flagged"] < z["hard_neg_flagged"]
    lines += [f"- Hard-negative false flags lower than plain z-score: {'met' if better else 'NOT met'} "
              f"({comb['hard_neg_flagged']} vs {z['hard_neg_flagged']})", "",
              "## Caveats",
              "- Synthetic data. Billed level depends on patient complexity by construction, so the risk-adjusted "
              "detector is helped by how the data was built; results do not transfer directly to real claims.",
              "- One seed, 8 upcoders and 8 hard negatives: small counts, so one provider moves a rate a lot.",
              "- The CMS file hides small cells; the synthetic data is calibrated to it only in the upper tail "
              "(see docs/synthetic_data.md)."]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("flagged_csv")
    ap.add_argument("truth_json")
    ap.add_argument("out_md")
    ap.add_argument("--top-n", type=int, default=25)
    ap.add_argument("--checked-summaries")
    a = ap.parse_args()
    with open(a.flagged_csv) as f:
        rows = list(csv.DictReader(f))
    res = evaluate(rows, json.load(open(a.truth_json)), a.top_n)
    md = render(res, a.top_n, citation_stats(a.checked_summaries))
    os.makedirs(os.path.dirname(os.path.abspath(a.out_md)), exist_ok=True)
    open(a.out_md, "w").write(md)
    print(md)
