"""Flagging step: decide which providers go to case review.

Two modes:
  * default (top-N): combined rank = average of the plain z-score rank and the risk-adjusted rank (ties broken by the
    risk-adjusted rank); the top N are flagged.
  * suspicion threshold (--min-suspicion S): flag every provider whose suspicion score is at least S. The suspicion score
    is the risk-adjusted score (observed minus expected 99215 count, in units of typical variation across providers).
    --max-flagged caps the number (keeps the highest scores) and --min-claims ignores tiny practices. The review list is
    then ordered by suspicion, highest first.
The output records each detector's own rank and top-N flag so the eval can compare them, plus a `suspicion` column.

Reads only agent-visible files. Never touches ground truth.

Usage:
    python src/flagging.py DATA_DIR OUT_CSV [--top-n 25] [--min-suspicion S] [--max-flagged N] [--min-claims K]
"""
import argparse
import csv
import os

import baseline_riskadj as ra
import baseline_zscore as bz


def flag(data_dir, top_n=25, min_suspicion=None, max_flagged=None, min_claims=0):
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
            "suspicion": r[pid]["z_adj"],
        })
    if min_suspicion is None:
        rows.sort(key=lambda x: (x["mean_rank"], x["rank_riskadj"], x["provider_id"]))
        for i, row in enumerate(rows, 1):
            row["rank"] = i
            row["flagged"] = i <= top_n
            by = [n for n, k in (("zscore", "flagged_zscore"), ("riskadj", "flagged_riskadj")) if row[k]]
            row["flagged_by"] = "+".join(by)
        return rows
    rows.sort(key=lambda x: (-x["suspicion"], x["provider_id"]))
    eligible = [r for r in rows if r["suspicion"] >= min_suspicion and r["n_claims"] >= min_claims]
    if max_flagged is not None:
        eligible = eligible[:max_flagged]
    chosen = {r["provider_id"] for r in eligible}
    for i, row in enumerate(rows, 1):
        row["rank"] = i
        row["flagged"] = row["provider_id"] in chosen
        row["flagged_by"] = f"suspicion>={min_suspicion:g}" if row["flagged"] else ""
    return rows


COLUMNS = ["rank", "provider_id", "n_claims", "share_99215", "expected_share", "z", "z_adj", "suspicion",
           "rank_zscore", "rank_riskadj", "mean_rank", "flagged_zscore", "flagged_riskadj", "flagged", "flagged_by"]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir")
    ap.add_argument("out_csv")
    ap.add_argument("--top-n", type=int, default=25)
    ap.add_argument("--min-suspicion", type=float, help="flag every provider at or above this suspicion score instead of a top N")
    ap.add_argument("--max-flagged", type=int, help="with --min-suspicion: keep at most this many (highest scores)")
    ap.add_argument("--min-claims", type=int, default=0, help="with --min-suspicion: ignore providers with fewer claims")
    a = ap.parse_args()
    rows = flag(a.data_dir, a.top_n, a.min_suspicion, a.max_flagged, a.min_claims)
    os.makedirs(os.path.dirname(os.path.abspath(a.out_csv)), exist_ok=True)
    with open(a.out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    n = sum(r["flagged"] for r in rows)
    how = f"suspicion >= {a.min_suspicion:g}" if a.min_suspicion is not None else f"top {a.top_n}"
    print(f"{len(rows)} providers ranked; {n} flagged ({how}) -> {a.out_csv}")
