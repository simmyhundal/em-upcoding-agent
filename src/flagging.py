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


SCREEN_METHODS = ("riskadj", "eb_ratio", "priority")


def top_n_from_pct(n_providers, pct):
    """Number of providers in the top `pct` percent of a panel (rounded up, at least 1): payers flag by percentile, not by a fixed count."""
    import math
    return max(1, math.ceil(n_providers * pct / 100.0))


def flag(data_dir, top_n=25, min_suspicion=None, max_flagged=None, min_claims=0, method="riskadj", top_pct=None):
    """method "riskadj" (default) is the frozen screen of v2.0 to v3.1: combined rank, or a suspicion threshold. "eb_ratio" and "priority" (release 2,
    src/screen_methods.py) rank by their own score and flag the top N; they have no suspicion threshold. Rows gain screen_method and screen_score."""
    if top_pct is not None:                            # a percentile cutoff replaces the fixed count (release 2; the frozen default stays top 25)
        top_n = top_n_from_pct(len(bz.rank(data_dir, 1)[0]), top_pct)
    if method != "riskadj":
        return _flag_by_method(data_dir, method, top_n, min_suspicion, max_flagged, min_claims)
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


def add_preflight(rows, report):
    """Workflow v2.2: add a data_quality column (empty, or the data caveat for providers whose findings the pre-flight puts on hold)."""
    import data_quality as dq
    for r in rows:
        r["data_quality"] = dq.hold_decision(report, r["provider_id"])["caveat"]
    return rows


def _flag_by_method(data_dir, method, top_n, min_suspicion, max_flagged, min_claims):
    if method not in SCREEN_METHODS:
        raise ValueError(f"method must be one of {SCREEN_METHODS}")
    if min_suspicion is not None:
        raise ValueError("a suspicion threshold is defined only for the riskadj score; use top_n with eb_ratio or priority")
    import screen_methods as sm
    rows = flag(data_dir, top_n)
    score = sm.score_core(data_dir)[method]
    rows.sort(key=lambda r: (-score[r["provider_id"]], r["provider_id"]))
    eligible = [r for r in rows if r["n_claims"] >= min_claims][:int(max_flagged or top_n)]
    chosen = {r["provider_id"] for r in eligible}
    for i, r in enumerate(rows, 1):
        r["rank"], r["flagged"] = i, r["provider_id"] in chosen
        r["flagged_by"] = method if r["flagged"] else ""
        r["screen_method"], r["screen_score"] = method, round(float(score[r["provider_id"]]), 5)
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
    ap.add_argument("--top-pct", type=float, help="flag the top PCT percent of providers (rounded up) instead of --top-n, e.g. 5")
    ap.add_argument("--method", default="riskadj", choices=list(SCREEN_METHODS),
                    help="screen score: riskadj (frozen default), or the release 2 candidates eb_ratio and priority (top N only)")
    ap.add_argument("--preflight", metavar="V2_DIR", help="workflow v2.2: run the data-quality pre-flight on the plan tables in V2_DIR first, write "
                    "data_quality.json next to OUT_CSV, add a data_quality column, and stop on a block")
    ap.add_argument("--continue-on-block", action="store_true", help="with --preflight: carry on even if the pre-flight blocks")
    a = ap.parse_args()
    rows = flag(a.data_dir, a.top_n, a.min_suspicion, a.max_flagged, a.min_claims, a.method, a.top_pct)
    cols = COLUMNS + (["screen_method", "screen_score"] if a.method != "riskadj" else [])
    os.makedirs(os.path.dirname(os.path.abspath(a.out_csv)), exist_ok=True)
    if a.preflight:
        import data_quality as dq
        report = dq.run_checks(a.preflight)
        print(f"data-quality pre-flight: {report['status']} -> {dq.write_report(report, os.path.dirname(os.path.abspath(a.out_csv)))}")
        for line in report["global_flags"]:
            print("  warning:", line)
        if report["status"] == "block" and not a.continue_on_block:
            raise SystemExit("pre-flight blocked the run (rerun with --continue-on-block to override)")
        rows = add_preflight(rows, report)
        cols = cols + ["data_quality"]
    with open(a.out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    n = sum(r["flagged"] for r in rows)
    how = f"suspicion >= {a.min_suspicion:g}" if a.min_suspicion is not None else f"top {a.top_n}"
    print(f"{len(rows)} providers ranked; {n} flagged ({how}) -> {a.out_csv}")
