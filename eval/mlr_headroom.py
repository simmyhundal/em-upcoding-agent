"""Headroom above the ACA minimum medical loss ratio, by insurer group, from the CMS MLR public use file (issue-free exploration, market sizing).

Source: https://www.cms.gov/files/zip/mlr-public-use-file-2024.zip (reporting year 2024, as of 2025-09-12); unzip it and pass the folder.
Uses Part3_MLR_Rebate_Calculation.csv (rows MLR_NUMERATOR and MLR_DENOMINATOR, current-year columns, markets individual, small group and large group) and the template header
(company, state, NAIC group). Rows whose business_state is 'Grand Total' are dropped (they repeat the state rows). The MLR is numerator over denominator, before the credibility
adjustment and before the three-year averaging, so it is not the figure that sets a rebate. Headroom of a submission-market = denominator x (MLR - floor) when positive;
floors: 80% individual and small group, 85% large group (state floors can be higher; not applied).

Usage: python eval/mlr_headroom.py FOLDER [--top N] [--csv OUT]
"""
import collections
import csv
import sys

FLOOR = {"individual": 0.80, "small_group": 0.80, "large_group": 0.85}
MARKETS = list(FLOOR)


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def load(folder):
    hdr = {r["mr_submission_template_id"]: r for r in csv.DictReader(open(folder + "/MR_Submission_Template_Header.csv"))}
    rows = collections.defaultdict(dict)
    for r in csv.DictReader(open(folder + "/Part3_MLR_Rebate_Calculation.csv")):
        if r["row_lookup_code"] in ("MLR_NUMERATOR", "MLR_DENOMINATOR"):
            rows[r["mr_submission_template_id"]][r["row_lookup_code"]] = r
    return hdr, rows


def by_group(folder):
    hdr, rows = load(folder)
    out = collections.defaultdict(lambda: {m: {"prem": 0.0, "num": 0.0, "head": 0.0, "below": 0.0} for m in MARKETS})
    label = {}
    for t, d in rows.items():
        h = hdr.get(t)
        if not h or h["business_state"] == "Grand Total" or "MLR_DENOMINATOR" not in d:
            continue
        g = h["naic_group_code"] or h["group_affiliation"] or h["company_name"]
        label.setdefault(g, h["group_affiliation"] or h["company_name"])
        for m in MARKETS:
            den, num = f(d["MLR_DENOMINATOR"].get(f"cmm_{m}_cy")), f(d["MLR_NUMERATOR"].get(f"cmm_{m}_cy"))
            if den <= 0:
                continue
            a = out[g][m]
            a["prem"] += den
            a["num"] += num
            if num / den > FLOOR[m]:
                a["head"] += den * (num / den - FLOOR[m])
            else:
                a["below"] += den * (FLOOR[m] - num / den)
    return out, label


if __name__ == "__main__":
    folder = sys.argv[1]
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 10
    out, label = by_group(folder)
    tot = lambda g, k: sum(out[g][m][k] for m in MARKETS)
    ranked = sorted(out, key=lambda g: -tot(g, "prem"))
    print(f"{'group':34}{'premium $B':>11}" + "".join(f"{m[:5]+' MLR':>12}" for m in MARKETS) + f"{'headroom $B':>13}{'below floor $B':>16}")
    for g in ranked[:top]:
        mlr = [out[g][m]["num"] / out[g][m]["prem"] if out[g][m]["prem"] else float("nan") for m in MARKETS]
        print(f"{label[g][:33]:34}{tot(g, 'prem') / 1e9:11.1f}" + "".join(f"{x:12.1%}" for x in mlr) + f"{tot(g, 'head') / 1e9:13.2f}{tot(g, 'below') / 1e9:16.2f}")
    allp, allh, allb = (sum(tot(g, k) for g in out) for k in ("prem", "head", "below"))
    print(f"{'ALL INSURERS':34}{allp / 1e9:11.1f}{'':36}{allh / 1e9:13.2f}{allb / 1e9:16.2f}")
    top_p, top_h = (sum(tot(g, k) for g in ranked[:top]) for k in ("prem", "head"))
    print(f"top {top}: premium {top_p / 1e9:.1f}B ({top_p / allp:.0%} of all), headroom {top_h / 1e9:.2f}B ({top_h / allh:.0%} of all)")
    for m in MARKETS:
        p = sum(out[g][m]["prem"] for g in out); n = sum(out[g][m]["num"] for g in out); h = sum(out[g][m]["head"] for g in out)
        print(f"  {m}: premium {p / 1e9:.1f}B, aggregate MLR {n / p:.1%}, headroom {h / 1e9:.2f}B")
    if "--csv" in sys.argv:
        with open(sys.argv[sys.argv.index("--csv") + 1], "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["group", "market", "premium", "numerator", "mlr", "floor", "headroom", "below_floor"])
            for g in ranked:
                for m in MARKETS:
                    a = out[g][m]
                    if a["prem"]:
                        w.writerow([label[g], m, round(a["prem"]), round(a["num"]), round(a["num"] / a["prem"], 4), FLOOR[m], round(a["head"]), round(a["below"])])
