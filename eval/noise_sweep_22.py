"""Data 2.2 honest-noise sweep on the development seed 42 only (issue 74): how the screen and the chart rule change as honest
miscoding grows. Free (no model). The defaults in `generate_v2.V22_DEFAULTS` were chosen for plausibility, not to make a result
look good; this table is the check that honest noise stays below the upcoder margin and does not break the screen outright.

Usage:
    python eval/noise_sweep_22.py [--write]      # --write puts the table into docs/data_v2_2.md between the sweep markers
"""
import json
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import derive  # noqa: E402
import generate_v2  # noqa: E402
import records  # noqa: E402
import screen_methods as sm  # noqa: E402

RATES = [0.0, 0.04, 0.08, 0.16]
SEED = 42


def one(rate):
    tmp = tempfile.mkdtemp()
    data, key = os.path.join(tmp, "d"), os.path.join(tmp, "k", "key.json")
    generate_v2.build(data, key, seed=SEED, n_providers=216, n_upcoders=8, n_hard_neg=8, clone_share=0.5, data_version="2.2",
                      honest_miscode_rate=rate)
    view = os.path.join(data, "view")
    derive.build_view(data, view)
    truth = json.load(open(key))
    roles = {p: v["role"] for p, v in truth["providers"].items()}
    S = sm.score_all(view)
    out = {"rate": rate, "n_up": sum(r == "upcoder" for r in roles.values()), "baseline": truth["honest_baseline_upcode_rate"]}
    for m in ("riskadj", "eb_ratio"):
        top = sorted(S[m], key=lambda p: (-S[m][p], p))[:25]
        out[m] = (sum(roles[p] == "upcoder" for p in top), sum(roles[p] != "upcoder" for p in top))
    # chart rule on the charts of the doctors the suspicion >= 5 screen sends (the v2.0 single-draw request, as in make_v2_runs)
    import csv
    import flagging
    rows = flagging.flag(view, 25, min_suspicion=5, max_flagged=25)
    flagged_csv = os.path.join(tmp, "flagged_threshold.csv")
    with open(flagged_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=flagging.COLUMNS)
        w.writeheader()
        w.writerows(rows)
    sent = {r["provider_id"] for r in rows if r["flagged"]}
    _, st = records.run_requests(data, view, flagged_csv, seed=SEED)
    asked = {r["provider_id"] for r in st if r["kind"] == "flagged"}
    sel = records.rules_flags(view, "documented_below_billed", 0.15, 8, asked)
    out["rule"] = (sum(roles[p] == "upcoder" for p in sel), sum(roles[p] != "upcoder" for p in sel), len(sent))
    return out


def table(res):
    lines = ["| Honest miscode rate | Counted upcoders (of 8 planted) | Honest baseline upcoding | `riskadj` top 25: upcoders / honest | `eb_ratio` top 25: upcoders / honest | Chart rule on screened doctors: upcoders / honest accused |",
             "|---|---|---|---|---|---|"]
    for r in res:
        lines.append(f"| {r['rate']:.0%} | {r['n_up']} | {r['baseline']:.1%} | {r['riskadj'][0]} / {r['riskadj'][1]} | {r['eb_ratio'][0]} / {r['eb_ratio'][1]} "
                     f"| {r['rule'][0]} / {r['rule'][1]} (of {r['rule'][2]} sent) |")
    return "\n".join(lines)


if __name__ == "__main__":
    res = [one(r) for r in RATES]
    t = table(res)
    print(t)
    if "--write" in sys.argv:
        path = os.path.join(ROOT, "docs", "data_v2_2.md")
        text = open(path).read()
        text = re.sub(r"(<!-- sweep:start -->).*?(<!-- sweep:end -->)", lambda m: m.group(1) + "\n" + t + "\n" + m.group(2), text, flags=re.S)
        open(path, "w").write(text)
