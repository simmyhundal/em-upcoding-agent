"""Flagging step: combine both detectors into one ranked review list.

Combined rank = average of the plain z-score rank and the risk-adjusted rank
(ties broken by the risk-adjusted rank). The top N go to case review. The output
records each detector's own rank and flag so the eval can compare them.

Reads only agent-visible files. Never touches ground truth.

Usage:
    python src/flagging.py DATA_DIR OUT_CSV [--top-n 25]
"""
import argparse
import csv
import os

import baseline_riskadj as ra
import baseline_zscore as bz


def flag(data_dir, top_n=25):
    z_rows, _, _ = bz.rank(data_dir, top_n)
    r_rows, _, _ = ra.rank(data_dir, top_n)
    z = {r["provider_id"]: r for r in z_rows}
    r = {x["provider_id"]: x for x in r_rows}
    rows = []
    for pid in z:
        rows.append({
            "provider_id": pid,
            "n_claims": z[pid]["n_claims"],
            "share_99215": z[pid]["share_99215"],
            "expected_share": r[pid]["expected_share"],
            "z": z[pid]["z"],
            "z_adj": r[pid]["z_adj"],
            "rank_zscore": z[pid]["rank"],
            "rank_riskadj": r[pid]["rank"],
            "flagged_zscore": z[pid]["flagged"],
            "flagged_riskadj": r[pid]["flagged"],
            "mean_rank": (z[pid]["rank"] + r[pid]["rank"]) / 2,
        })
    rows.sort(key=lambda x: (x["mean_rank"], x["rank_riskadj"], x["provider_id"]))
    for i, row in enumerate(rows, 1):
        row["rank"] = i
        row["flagged"] = i <= top_n
        by = [n for n, k in (("zscore", "flagged_zscore"), ("riskadj", "flagged_riskadj")) if row[k]]
        row["flagged_by"] = "+".join(by)
    return rows


COLUMNS = ["rank", "provider_id", "n_claims", "share_99215", "expected_share", "z", "z_adj",
           "rank_zscore", "rank_riskadj", "mean_rank", "flagged_zscore", "flagged_riskadj", "flagged", "flagged_by"]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir")
    ap.add_argument("out_csv")
    ap.add_argument("--top-n", type=int, default=25)
    a = ap.parse_args()
    rows = flag(a.data_dir, a.top_n)
    os.makedirs(os.path.dirname(os.path.abspath(a.out_csv)), exist_ok=True)
    with open(a.out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} providers ranked; top {a.top_n} flagged -> {a.out_csv}")
