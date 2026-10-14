"""Which ordering of providers makes records requests most efficient? A free analysis of screening-order scores (issue 48).

Every records request costs burden, so with a budget of B requests the best ordering puts upcoders first: its precision-recall curve (as the
budget grows from 1 to 25) encloses the most area. This compares candidate orderings by AP (average precision, the area under the
precision-recall curve for the ordering) and by precision and recall at budgets 5, 10, 15 and 25. The ordering is chosen on the DEVELOPMENT
seed only (42); the other datasets (seeds 101, 7, 202, 303) are reported alongside as validation and were not used to choose. Orderings use only
what a payer has before asking for charts. Writes docs/priority_score.md.

Usage:
    python eval/priority_analysis.py
"""
import csv
import json
import math
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))

DATASETS = [("seed 42 (development)", "261012_1_code", True), ("seed 101", "261012_2_code", False), ("seed 202", "261013_4_code", False),
            ("seed 303", "261013_5_code", False), ("seed 7, 0.5% upcoders", "261012_3_code", False), ("seed 7, 1% upcoders", "261012_4_code", False),
            ("seed 7, 2% upcoders", "261012_5_code", False)]
BUDGETS = [5, 10, 15, 25]
FEES = None


def features(code):
    """Per-provider claims-only features from a v2 detector view and the screen output."""
    view = os.path.join(ROOT, "data", f"synthetic_v2_{code}", "view")
    flag = {r["provider_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "experiments", code, "flagged.csv")))}
    chronic = {r["patient_id"]: int(r["chronic_condition_count"]) for r in csv.DictReader(open(os.path.join(view, "patients.csv")))}
    n215, low215 = defaultdict(int), defaultdict(int)
    for r in csv.DictReader(open(os.path.join(view, "claims.csv"))):
        if r["cpt"] == "99215":
            n215[r["provider_id"]] += 1
            low215[r["provider_id"]] += chronic.get(r["patient_id"], 0) <= 1
    fees = {c: v["allowed_amount"] for c, v in json.load(open(os.path.join(ROOT, "data", "baselines", "allowed_amounts_ga_fp.json")))["codes"].items()}
    out = {}
    for p, r in flag.items():
        n, share, exp = int(r["n_claims"]), float(r["share_99215"]), float(r["expected_share"])
        excess = (share - exp) * n
        out[p] = {"z_adj": float(r["z_adj"]), "z": float(r["z"]), "mean_rank": float(r["mean_rank"]), "n": n,
                  "ratio": share / exp if exp else 0.0, "excess": excess,
                  "low": (low215[p] / n215[p]) if n215[p] else 0.0,
                  "excess_usd": max(excess, 0) * (fees["99215"] - fees["99214"]) * 0.8}
    return out


def rank_avg(feats, keys):
    """Average of per-feature ranks (higher feature = better rank): robust, no fitted weights."""
    ranks = defaultdict(float)
    for k in keys:
        order = sorted(feats, key=lambda p: -feats[p][k])
        for i, p in enumerate(order):
            ranks[p] += i
    return {p: -v / len(keys) for p, v in ranks.items()}


SCORES = {
    "z_adj (the screen's score)": lambda f: {p: v["z_adj"] for p, v in f.items()},
    "combined rank (workflow top 25)": lambda f: {p: -v["mean_rank"] for p, v in f.items()},
    "ratio to expected": lambda f: {p: v["ratio"] for p, v in f.items()},
    "excess 99215 claims": lambda f: {p: v["excess"] for p, v in f.items()},
    "low-complexity share of 99215": lambda f: {p: v["low"] for p, v in f.items()},
    "excess dollars": lambda f: {p: v["excess_usd"] for p, v in f.items()},
    "priority: rank average of z_adj, ratio and low-complexity share": lambda f: rank_avg(f, ["z_adj", "ratio", "low"]),
    "priority: rank average of z_adj, excess claims and low-complexity share": lambda f: rank_avg(f, ["z_adj", "excess", "low"]),
    "priority: rank average of ratio and excess claims": lambda f: rank_avg(f, ["ratio", "excess"]),
}


def curve(order, up, kmax=25):
    tp, pts = 0, []
    for k, p in enumerate(order[:kmax], 1):
        tp += p in up
        pts.append((tp / len(up), tp / k, tp))
    return pts


def ap(order, up, kmax=None):
    """Average precision over the ordering (area under the precision-recall curve), over the first kmax providers."""
    tp, s = 0, 0.0
    for k, p in enumerate(order[:kmax] if kmax else order, 1):
        if p in up:
            tp += 1
            s += tp / k
    return s / len(up)


def main():
    truth_of = lambda code: {p: v["role"] == "upcoder" for p, v in json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))["providers"].items()}
    results = {}
    for label, code, dev in DATASETS:
        f = features(code)
        up = {p for p, v in truth_of(code).items() if v}
        results[label] = {name: [ap(sorted(sc(f), key=lambda p: -sc(f)[p]), up, 25)] + [curve(sorted(sc(f), key=lambda p: -sc(f)[p]), up)[b - 1] for b in BUDGETS]
                          for name, sc in SCORES.items()}
    out = ["# Ordering providers for records requests", "",
           "Generated by `python eval/priority_analysis.py`. Free: uses only claims-side features and the answer key to score the ordering. "
           "The ordering was chosen on seed 42 (development); the other seeds are validation and were not used to choose. **AP** is average precision over the "
           "first 25 providers (the area under the precision-recall curve as the records budget grows from 1 to 25). Cells show `recall / precision` at a budget of 5, 10, 15 and 25 requests.", ""]
    for label, code, dev in DATASETS:
        out += [f"## {label}", "", "| Ordering | AP | budget 5 | budget 10 | budget 15 | budget 25 |", "|---|---|---|---|---|---|"]
        for name, r in sorted(results[label].items(), key=lambda kv: -kv[1][0]):
            out.append(f"| {name} | {r[0]:.2f} | " + " | ".join(f"{x[0]:.2f} / {x[1]:.2f}" for x in r[1:]) + " |")
        out.append("")
    # mean AP across validation datasets
    out += ["## Mean AP across the six validation datasets", "", "| Ordering | AP on seed 42 (chosen on) | mean AP on the other six |", "|---|---|---|"]
    dev_label = DATASETS[0][0]
    others = [d[0] for d in DATASETS[1:]]
    for name in SCORES:
        out.append(f"| {name} | {results[dev_label][name][0]:.2f} | {sum(results[o][name][0] for o in others) / len(others):.2f} |")
    open(os.path.join(ROOT, "docs", "priority_score.md"), "w").write("\n".join(out) + "\n")
    print("\n".join(out[-14:]))
    return results


if __name__ == "__main__":
    main()
