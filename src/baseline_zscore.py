"""Baseline 1: plain z-score of each provider's 99215 share against peers.

No risk adjustment: it ignores how sick a provider's patients are. This is the
number the risk-adjusted baseline and the rest of the pipeline have to beat.

Reads only the agent-visible files (claims.csv). It never touches ground truth.

Usage:
    python src/baseline_zscore.py DATA_DIR OUT_CSV [--top-n 25]
"""
import argparse
import csv
import os
import statistics
from collections import Counter, defaultdict

TARGET_CODE = "99215"


def zscores(claims_path):
    totals, hits = Counter(), Counter()
    with open(claims_path) as f:
        for row in csv.DictReader(f):
            totals[row["provider_id"]] += 1
            if row["cpt"] == TARGET_CODE:
                hits[row["provider_id"]] += 1
    share = {p: hits[p] / totals[p] for p in totals}
    mean = statistics.fmean(share.values())
    sd = statistics.stdev(share.values())
    return [
        {"provider_id": p, "n_claims": totals[p], "n_99215": hits[p],
         "share_99215": round(share[p], 5), "z": round((share[p] - mean) / sd, 4)}
        for p in totals
    ], mean, sd


def rank(data_dir, top_n=25):
    rows, mean, sd = zscores(os.path.join(data_dir, "claims.csv"))
    rows.sort(key=lambda r: (-r["z"], r["provider_id"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
        r["flagged"] = i <= top_n
    return rows, mean, sd


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir")
    ap.add_argument("out_csv")
    ap.add_argument("--top-n", type=int, default=25)
    a = ap.parse_args()
    rows, mean, sd = rank(a.data_dir, a.top_n)
    os.makedirs(os.path.dirname(os.path.abspath(a.out_csv)), exist_ok=True)
    with open(a.out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["rank", "provider_id", "n_claims", "n_99215", "share_99215", "z", "flagged"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} providers; mean share {mean:.4f}, sd {sd:.4f}; top {a.top_n} flagged -> {a.out_csv}")
