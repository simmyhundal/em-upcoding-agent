"""Score the candidate screen methods (src/screen_methods.py) against the answer key, per method and per dataset (issue 88). Writes the page and its chart.

Free: claims and patients only. Evaluation only (uses the answer key). Writes docs/screen_methods.md with --write.

Per method and dataset it reports: upcoders in the top 25 (recall), honest doctors in the top 25 (hard negatives and
ordinary doctors separately), AUPRC, ROC AUC, precision at 10 and 25 (eval/screen_metrics.py), and the recall of a
matched-volume cutoff: the top K where K is how many doctors the suspicion >= 5 rule flags on that dataset. Methods on the
z_adj scale also get their own z >= 5 recall.

Usage:
    python eval/screen_methods_eval.py                       # release-1 datasets, print
    python eval/screen_methods_eval.py --write               # also write docs/screen_methods.md
    python eval/screen_methods_eval.py --view DIR --truth FILE --label NAME    # one dataset
"""
import json
import os
import sys
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import screen_methods as sm  # noqa: E402
import screen_metrics as mt  # noqa: E402

ZSCALE = ("riskadj", "level_z", "rich_logit", "rich_level", "zscore")
TOP = 25


def evaluate_dataset(view, truth, label, rate_key=None):
    S = sm.score_all(view)
    roles = {p: v["role"] for p, v in truth["providers"].items()}
    ids = sorted(S["riskadj"])
    labels = [1 if roles[p] == "upcoder" else 0 for p in ids]
    n_up = sum(labels)
    k5 = sum(1 for p in ids if S["riskadj"][p] >= 5) or TOP
    res = {"label": label, "providers": len(ids), "upcoders": n_up, "k5": k5, "methods": {}}
    for m in sm.METHODS:
        s = S[m]
        sc = [s[p] for p in ids]
        order = sorted(ids, key=lambda p: (-s[p], p))
        top = order[:TOP]
        matched = order[:k5]
        entry = {
            "found": sum(roles[p] == "upcoder" for p in top),
            "hn": sum(roles[p] == "hard_negative" for p in top),
            "normal": sum(roles[p] == "normal" for p in top),
            "matched_found": sum(roles[p] == "upcoder" for p in matched),
            "auprc": mt.average_precision(sc, labels), "roc_auc": mt.roc_auc(sc, labels),
            "p10": mt.precision_at_k(sc, labels, 10, ids), "p25": mt.precision_at_k(sc, labels, 25, ids),
            "ranks": {p: order.index(p) + 1 for p in ids if roles[p] == "upcoder"},
        }
        if m in ZSCALE:
            hits = [p for p in ids if s[p] >= 5]
            entry["z5_found"] = sum(roles[p] == "upcoder" for p in hits)
            entry["z5_flagged"] = len(hits)
        res["methods"][m] = entry
    res["eb_shape"] = S["_meta"]["eb_shape"]
    return res


def run(keys=None):
    reg = json.load(open(os.path.join(ROOT, "experiments", "runs.json")))
    out = []
    for k in keys or mt.RELEASE1:
        d = reg["datasets"][k]
        truth = json.load(open(os.path.join(ROOT, d["truth"])))
        out.append(evaluate_dataset(os.path.join(ROOT, d["view"]), truth, k))
        print("scored", k, file=sys.stderr)
    return out


def totals(results):
    t = {}
    for m in sm.METHODS:
        e = [r["methods"][m] for r in results]
        t[m] = {"found": sum(x["found"] for x in e), "hn": sum(x["hn"] for x in e), "normal": sum(x["normal"] for x in e),
                "matched": sum(x["matched_found"] for x in e), "auprc": sum(x["auprc"] for x in e) / len(e),
                "roc": sum(x["roc_auc"] for x in e) / len(e), "p10": sum(x["p10"] for x in e) / len(e),
                "p25": sum(x["p25"] for x in e) / len(e),
                "z5": sum(x.get("z5_found", 0) for x in e) if m in ZSCALE else None,
                "z5_flagged": sum(x.get("z5_flagged", 0) for x in e) if m in ZSCALE else None,
                "perfect": sum(1 for r, x in zip(results, e) if x["found"] == r["upcoders"])}
    return t


def table(results, group=None):
    rs = [r for r in results if group is None or group(r)]
    n_up = sum(r["upcoders"] for r in rs)
    t = totals(rs)
    lines = [f"| Method | Upcoders in top 25 (of {n_up}) | Datasets with every upcoder in the top 25 (of {len(rs)}) | High-acuity panels in top 25 | Other honest in top 25 | "
             "Upcoders at matched volume (same K as z >= 5) | z >= 5 (found / flagged) | AUPRC (mean) | ROC AUC (mean) | Precision at 10 | Precision at 25 |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in sm.METHODS:
        x = t[m]
        z5 = f"{x['z5']} / {x['z5_flagged']}" if x["z5"] is not None else "n/a"
        lines.append(f"| `{m}` | {x['found']} ({x['found'] / n_up:.0%}) | {x['perfect']} | {x['hn']} | {x['normal']} | {x['matched']} | {z5} "
                     f"| {x['auprc']:.3f} | {x['roc']:.3f} | {x['p10']:.2f} | {x['p25']:.2f} |")
    return "\n".join(lines)


def per_dataset(results, methods=("riskadj", "eb_ratio", "priority", "ensemble")):
    lines = ["| Dataset | Providers | Upcoders | " + " | ".join(f"`{m}` in top 25" for m in methods) + " | `riskadj` z >= 5 |", "|---|---|---|" + "---|" * (len(methods) + 1)]
    for r in results:
        cells = " | ".join(str(r["methods"][m]["found"]) for m in methods)
        lines.append(f"| {r['label']} | {r['providers']} | {r['upcoders']} | {cells} | {r['methods']['riskadj']['z5_found']} |")
    return "\n".join(lines)


def misses(results, methods):
    """Where each method ranks the upcoders `riskadj` leaves outside its top 25."""
    rows = []
    for r in results:
        for p, rk in r["methods"]["riskadj"]["ranks"].items():
            if rk > TOP:
                rows.append((r["label"], p, rk, {m: r["methods"][m]["ranks"][p] for m in methods}))
    return rows


def misses_table(results, methods):
    rows = misses(results, methods)
    lines = ["| Dataset | Upcoder | `riskadj` rank | " + " | ".join(f"`{m}` rank" for m in methods) + " |", "|---|---|---|" + "---|" * len(methods)]
    for lab, p, rk, rs in rows:
        lines.append(f"| {lab} | {p} | {rk} | " + " | ".join(str(rs[m]) for m in methods) + " |")
    recovered = {m: sum(1 for *_, rs in rows if rs[m] <= TOP) for m in methods}
    lines += ["", f"Of these {len(rows)} upcoders that `riskadj` leaves outside its top 25, the top 25 of each method holds: "
              + ", ".join(f"`{m}` {recovered[m]}" for m in methods) + "."]
    return "\n".join(lines)


def paired(results, a, b):
    """Datasets where method `a` finds more, equal or fewer upcoders in the top 25 than method `b`."""
    d = [r["methods"][a]["found"] - r["methods"][b]["found"] for r in results]
    return sum(x > 0 for x in d), sum(x == 0 for x in d), sum(x < 0 for x in d)


def capacity_table(results, methods=("riskadj", "priority", "eb_ratio"), ks=(25, 30, 40, 50, 75)):
    """Upcoders reached if the investigators' list were longer: pooled over the given datasets."""
    n_up = sum(r["upcoders"] for r in results)
    lines = [f"| Method | " + " | ".join(f"top {k}" for k in ks) + " |", "|---|" + "---|" * len(ks)]
    for m in methods:
        cells = [sum(sum(1 for rk in r["methods"][m]["ranks"].values() if rk <= k) for r in results) for k in ks]
        lines.append(f"| `{m}` | " + " | ".join(f"{c} of {n_up}" for c in cells) + " |")
    return "\n".join(lines)


def percent_table(results, methods=("zscore", "riskadj", "priority", "eb_ratio"), pcts=(5, 10)):
    """Payers flag a percentile of the panel, not a fixed count (CMS comparative billing reports, the OIG's top 1%). Upcoders reached when the top PCT
    percent of providers (rounded up) is flagged, and the honest providers that costs. A fixed 25 is 11.6% of 216 doctors and 4.2% of 600."""
    import math
    n_up = sum(r["upcoders"] for r in results)
    lines = ["| Method | " + " | ".join(f"top {p}%: upcoders found / honest flagged" for p in pcts) + " |", "|---|" + "---|" * len(pcts)]
    for m in methods:
        cells = []
        for p in pcts:
            found = flagged = 0
            for r in results:
                k = max(1, math.ceil(r["providers"] * p / 100))
                found += sum(1 for rk in r["methods"][m]["ranks"].values() if rk <= k)
                flagged += k
            cells.append(f"{found} of {n_up} / {flagged - found:,}")
        lines.append(f"| `{m}` | " + " | ".join(cells) + " |")
    ks = sorted({math.ceil(r["providers"] * pcts[0] / 100) for r in results})
    return "\n".join(lines) + f"\n\nThe top {pcts[0]}% is {', '.join(map(str, ks))} providers on these datasets (216 and 600 providers); the top {pcts[1]}% is double that."


def choice(results):
    """The selection rule, fixed before looking at the table: most upcoders in the top 25 across the 14 datasets among methods whose
    honest doctors in the top 25 (hard negatives plus ordinary) do not exceed `riskadj`'s. Ties go to the simpler method."""
    t = totals(results)
    base = t["riskadj"]["hn"] + t["riskadj"]["normal"]
    ok = [m for m in sm.METHODS if t[m]["hn"] + t[m]["normal"] <= base]
    return max(ok, key=lambda m: (t[m]["found"], -sm.METHODS.index(m)))


ISSUE = "https://github.com/simmyhundal/em-upcoding-agent/issues/"

# Results computed by other scripts, quoted here so the history reads in one place (sources in the comments).
R2_TOP5 = {"zscore": 28, "riskadj": 30, "priority": 33, "eb_ratio": 34}     # docs/release2_screen_choice.md: 8 fresh data 2.2 seeds, 62 upcoders
R2_UPCODERS = 62
R3_TOP5 = {"eb_ratio": 44, "eb_ratio_t": 47}                                # docs/dev_release3.md and src/screen_methods.eb_ratio_t: ten release 2 seeds, 78 upcoders, in sample
R3_UPCODERS = 78
V4 = json.load(open(os.path.join(ROOT, "experiments", "screen_methods_v4.json")))   # data 4.0 (11 development seeds, 88 upcoders): written from eval/screens_v4_eval.py's scores; see docs/screens_v4.md
V4_N = V4["eb_ratio_t"]["n"]["all"]

METHOD_ROWS = [  # method, family, what it scores (one line), where it is used
    ("zscore", "z-score", "share of visits billed 99215 against all providers; no adjustment for how sick the patients are", "screen of v1 and v2.0; reference"),
    ("riskadj", "z-score, risk-adjusted", "observed against expected 99215 count, the expectation from each patient's chronic-condition count (logistic fit), rescaled by the typical spread", "screen of v2.1 and v3.1 (frozen); reference"),
    ("priority", "rank average", "average of the ranks by ratio to expected and by excess 99215 claims", "ordering in v3.1; release 2 candidate"),
    ("eb_ratio", "empirical Bayes", "`riskadj`'s observed over expected 99215 count, shrunk toward 1 for small panels (see below)", "screen of v2.2 and v3.2"),
    ("eb_ratio_t", "empirical Bayes", "`eb_ratio` with one more input to the expected count: whether the claim has a lab or test line", "screen of v2.3 to v2.5 and v3.3 to v3.5 (frozen)"),
    ("eb_upper_t", "empirical Bayes", "the same shrinkage on the share billed 99214 or 99215, with the lab or test line as an input, so 99213-to-99214 upgrades count (data 4.0)", "**current screen** (workflow v4.0, agent v5.0)"),
    ("eb_upper_c", "empirical Bayes", "`eb_upper_t` without the test line (chronic-condition count only)", "candidate only; does not lean on the lab-line link"),
    ("eb_prob", "empirical Bayes", "probability that the true 99215 rate is more than 1.5 times expected", "candidate only"),
    ("eb_excess", "empirical Bayes", "shrunk extra 99215 claims: expected count x (shrunk ratio - 1)", "candidate only"),
    ("eb_upper", "empirical Bayes", "the same shrinkage on the share billed 99214 or 99215, so 99213-to-99214 upgrades count", "candidate only"),
    ("eb_two", "rank average", "`eb_ratio` and `eb_upper`", "candidate only"),
    ("level_z", "whole distribution", "mean billed level (99211 to 99215) against the level expected from the chronic-condition count", "candidate only"),
    ("rich_logit", "regression", "`riskadj` with more patient features (each condition, age band, risk score, first visit)", "candidate only"),
    ("rich_level", "regression", "`level_z` with the same patient features", "candidate only"),
    ("ensemble", "rank average", "`riskadj`, `eb_ratio` and `level_z`", "candidate only"),
]


def methods_table():
    lines = ["| Method | Family | What it scores | Used in |", "|---|---|---|---|"]
    lines += [f"| `{m}` | {f} | {w} | {u} |" for m, f, w, u in METHOD_ROWS]
    return "\n".join(lines)


def top_pct_found(results, method, pct=5):
    import math
    return sum(sum(1 for rk in r["methods"][method]["ranks"].values() if rk <= max(1, math.ceil(r["providers"] * pct / 100))) for r in results)


def headline_table(results, group=None):
    rs = [r for r in results if group is None or group(r)]
    n_up = sum(r["upcoders"] for r in rs)
    t = totals(rs)
    lines = [f"| Method | Upcoders in the top 25 (of {n_up}) | High-acuity panels in the top 25 | Other honest providers in the top 25 | AUPRC |", "|---|---|---|---|---|"]
    for m in sm.METHODS:
        x = t[m]
        lines.append(f"| `{m}` | {x['found']} ({x['found'] / n_up:.0%}) | {x['hn']} | {x['normal']} | {x['auprc']:.2f} |")
    return "\n".join(lines)


LEGEND = ("Columns: **upcoders in the top 25**, summed over the datasets; **datasets with every upcoder in the top 25**; honest providers in the top 25, split into "
          "**high-acuity panels** (honest providers whose sicker patients justify more 99215s, the hard cases) and **ordinary** ones; **matched volume**: upcoders in the top K, "
          "where K is how many providers `riskadj`'s suspicion score of 5 or more flags on that dataset; **z >= 5**: upcoders found / providers flagged by that cutoff "
          "(z-score methods only); **AUPRC** and **ROC AUC**: how well the whole ranking separates upcoders from honest providers (1.0 is perfect; AUPRC is the stricter "
          "one when upcoders are rare); **precision at 10 and 25**: the share of upcoders among the first 10 and 25 providers listed. Means are over datasets.")


def details(summary, body):
    """A folded section: GitHub renders <details>; the blank lines let the Markdown inside render."""
    return f"<details>\n<summary><b>{summary}</b></summary>\n\n{body}\n\n</details>\n"


def chart_svg(results):
    """Small multiples: share of upcoders in the top 5% of providers, by data version. One hue; the screen chosen at each step in blue."""
    INK, MUTED, GRID, BAR, HI = "#1f2937", "#6b7280", "#e5e7eb", "#9ca3af", "#2563eb"
    n1 = sum(r["upcoders"] for r in results)
    panels = [
        (f"Data 2.0 and 2.1: 14 datasets, {n1} upcoders", [(m, top_pct_found(results, m), n1) for m in ("zscore", "riskadj", "priority", "eb_ratio")], "eb_ratio"),
        (f"Data 2.2: 8 fresh release 2 seeds, {R2_UPCODERS} upcoders", [(m, R2_TOP5[m], R2_UPCODERS) for m in ("zscore", "riskadj", "priority", "eb_ratio")], "eb_ratio"),
        (f"Data 2.2: 10 release 2 seeds, {R3_UPCODERS} upcoders (in sample)", [(m, R3_TOP5[m], R3_UPCODERS) for m in ("eb_ratio", "eb_ratio_t")], "eb_ratio_t"),
        (f"Data 4.0: 11 development seeds, {V4_N} upcoders (in sample)", [(m, V4[m]["top5"]["all"], V4_N) for m in ("eb_ratio_t", "eb_upper_c", "eb_upper_t")], "eb_upper_t"),
    ]
    W, left, right, bar_h, gap, x0 = 760, 120, 150, 18, 8, 0
    plot_w = W - left - right
    y = 78
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} HEIGHT" width="{W}" height="HEIGHT" font-family="Helvetica, Arial, sans-serif" role="img" '
         f'aria-label="Share of upcoders each screen puts in the top 5% of providers, by data version">',
         '<rect width="100%" height="100%" fill="#ffffff"/>',
         f'<text x="20" y="32" font-size="18" font-weight="bold" fill="{INK}">Upcoders in the top 5% of providers, by screen and data version</text>',
         f'<text x="20" y="54" font-size="12.5" fill="{MUTED}">Blue: the screen chosen at that step. Each panel has its own seeds, so compare bars within a panel.</text>']
    for title, rows, chosen in panels:
        s.append(f'<text x="20" y="{y + 4}" font-size="13.5" font-weight="bold" fill="{INK}">{escape(title)}</text>')
        y += 16
        for frac in (0, 0.25, 0.5, 0.75, 1.0):
            gx = left + frac * plot_w
            s.append(f'<line x1="{gx:.1f}" y1="{y}" x2="{gx:.1f}" y2="{y + len(rows) * (bar_h + gap) - gap}" stroke="{GRID}" stroke-width="1"/>')
        for m, found, n in rows:
            w = plot_w * found / n
            col = HI if m == chosen else BAR
            s.append(f'<text x="{left - 8}" y="{y + bar_h - 5}" text-anchor="end" font-size="12.5" fill="{INK}">{m}</text>')
            s.append(f'<path d="M{left},{y} h{w - 4:.1f} a4,4 0 0 1 4,4 v{bar_h - 8} a4,4 0 0 1 -4,4 h-{w - 4:.1f} z" fill="{col}"><title>{m}: {found} of {n} ({found / n:.0%})</title></path>')
            s.append(f'<text x="{left + w + 6:.1f}" y="{y + bar_h - 5}" font-size="12" fill="{MUTED}">{found} of {n} ({found / n:.0%})</text>')
            y += bar_h + gap
        y += 4
        for frac in (0, 0.5, 1.0):
            s.append(f'<text x="{left + frac * plot_w:.1f}" y="{y + 8}" text-anchor="middle" font-size="11" fill="{MUTED}">{frac:.0%}</text>')
        y += 36
    s.append("</svg>")
    return "\n".join(s).replace("HEIGHT", str(y))


def chart_rows(results):
    n1 = sum(r["upcoders"] for r in results)
    lines = ["| Data and seeds | Screen | Upcoders in the top 5% |", "|---|---|---|"]
    for m in ("zscore", "riskadj", "priority", "eb_ratio"):
        lines.append(f"| 2.0 and 2.1, 14 datasets | `{m}` | {top_pct_found(results, m)} of {n1} |")
    for m in ("zscore", "riskadj", "priority", "eb_ratio"):
        lines.append(f"| 2.2, 8 fresh release 2 seeds | `{m}` | {R2_TOP5[m]} of {R2_UPCODERS} |")
    for m in ("eb_ratio", "eb_ratio_t"):
        lines.append(f"| 2.2, 10 release 2 seeds (in sample) | `{m}` | {R3_TOP5[m]} of {R3_UPCODERS} |")
    for m in ("eb_ratio_t", "eb_upper_c", "eb_upper_t"):
        lines.append(f"| 4.0, 11 development seeds (in sample) | `{m}` | {V4[m]['top5']['all']} of {V4_N} |")
    return "\n".join(lines)


CAVEATS = """## Caveats (read before using any number here)

- **Synthetic data from one generator.** Data 2.0 and 2.1 are easier than real claims: honest providers bill exactly the justified level, and the justified
  level depends on the patient's chronic-condition count by construction. That flatters every risk-adjusted method and makes extra patient features useless
  (`rich_logit` is essentially `riskadj`). Data 2.2 adds honest coding noise; real claims have more.
- **The first choice was not blind.** The rule that picked `eb_ratio` on the 14 datasets was written down after one look at the table, so that step was
  tuning. The release 2 check on 8 fresh seeds used a rule fixed before any result ([release2_screen_choice.md](release2_screen_choice.md)); `eb_ratio`
  won it by 1 upcoder over `priority` and 4 over `riskadj` of 62, a small margin. `eb_ratio_t`'s gain (47 against 44 of 78) is in sample.
- **The target is not met.** The aim was every upcoder in the top 25; the best method still misses upcoders on 6 of 14 datasets. Most misses sit at ranks
  26 to 55 (a longer list reaches them), and one upcoder (seed 1010) bills 99215 at only 1.2 times expected, so no 99215-only score ranks it high.
- **`eb_ratio` helps by shrinking small panels, not by a new kind of evidence.** Its gain over `riskadj` is a handful of upcoders. At 600 providers it ties
  `riskadj` in the top 25 (15 of 21 each) and gains only in a longer list and in AUPRC; with 3 to 12 upcoders per dataset, that is one provider either way.
- **Whole-distribution scores failed on this data** (`level_z`, `rich_level`, `eb_upper`, `eb_two`). Honest providers differ in coding style, which moves
  the mean billed level and the 99214-or-higher share as much as an upcoder's one-level upgrades. That says a simple level score is too noisy here, not that
  levels never help; data 4.0 plants 99213-to-99214 habits on purpose, so they are tested again there.
- **Data 4.0 is easier for `eb_upper_t` by construction.** The generator draws a visit's lab line from the true complexity, so a screen that uses the test line has a planted input;
  `hi_no_test` (visits billed 99214 or 99215 with no test line) finds 88 of 88 upcoders from that link alone, and the habits are the ones these screens look for.
  `eb_upper_c` leaves the test line out and finds 70 of 88 in the top 10%. A systematic upcoder also carries a planted panel shift, so its gain is checked against honest providers
  with a similar provider effect ([screens_v4.md](screens_v4.md)); `eb_upper_t` outscores them (about 1.00). The 11 seeds are development data: the screen's real test is the fresh seeds.
- **`ensemble` includes the weak `level_z`**, so it is dragged down; it is reported because it was a named candidate.
"""


def data40_section():
    """Data 4.0 per habit, from experiments/screen_methods_v4.json (the full table, all screens and the matched-honest check are in docs/screens_v4.md)."""
    habits = ("all", "systematic", "opportunistic", "template")
    lines = [f"Upcoders in the top 10% of providers (22 of 216), by habit, 11 development seeds ({V4_N} upcoders):", "",
             "| Screen | All | Systematic | Opportunistic | Template-driven | Honest in list | AUPRC |", "|---|---|---|---|---|---|---|"]
    for m in ("eb_ratio_t", "eb_upper_c", "eb_upper_t"):
        v = V4[m]
        lines.append(f"| `{m}` | " + " | ".join(f"{v['top10'][h]} of {v['n'][h]}" for h in habits) + f" | {v['honest10']} | {v['auprc']:.3f} |")
    lines += ["", "`eb_ratio_t` is the frozen screen of v2.3 to v2.5; it looks at 99215 only, and data 4.0's systematic habit moves 99213 to 99214. "
              "[screens_v4.md](screens_v4.md) has every candidate screen, dollar-weighted capture and the check against honest providers with a similar provider effect; "
              "[screens_v4_pipeline.md](screens_v4_pipeline.md) has the pipeline after the list."]
    return "\n".join(lines)


def data22_section():
    """Seed 42 on data 2.2: the same table, one dataset, plus where each planted upcoder ranks. Empty if the data is absent."""
    view = os.path.join(ROOT, "data", "synthetic_v2_261016_1_code", "view")
    key = os.path.join(ROOT, "eval", "answer_key", "ground_truth_v2_261016_1_code.json")
    if not (os.path.exists(view) and os.path.exists(key)):
        return ""
    truth = json.load(open(key))
    r = evaluate_dataset(view, truth, "s42_data22")
    planted = {p: v for p, v in truth["providers"].items() if v.get("planted") == "upcoder"}
    methods = ["riskadj", "priority", "eb_ratio"]
    full = {m: {p: None for p in planted} for m in methods}
    S = sm.score_all(view)
    for m in methods:
        order = sorted(S[m], key=lambda p: (-S[m][p], p))
        for p in planted:
            full[m][p] = order.index(p) + 1
    lines = ["| Planted upcoder | Kind | True rate / realised rate | Counted as upcoder | " + " | ".join(f"`{m}` rank" for m in methods) + " |", "|---|---|---|---|" + "---|" * len(methods)]
    for p, v in sorted(planted.items(), key=lambda kv: -kv[1]["true_upcode_rate"]):
        lines.append(f"| {p} | {'subtle' if v['subtle'] else 'obvious'}, {'cloned' if v['clones_notes'] else 'honest'} notes | {v['true_upcode_rate']:.1%} / {v['upcode_rate']:.1%} "
                     f"| {'yes' if v['role'] == 'upcoder' else 'no (below the line)'} | " + " | ".join(str(full[m][p]) for m in methods) + " |")
    body = ("One development dataset (run `261016_1_code`: 216 providers, 8 planted upcoders of which %d count under the payer-based definition; honest mean true rate %.1f%%, "
            "95th percentile %.1f%%, margin %.0f points). One draw, so a single provider moves any count. `riskadj` and `priority` have all 8 upcoders in their top 25, "
            "`eb_ratio` 7, while `eb_ratio` ranks the whole list better (higher AUPRC).\n\n" % (
                r["upcoders"], 100 * truth["honest_baseline_true_rate"], 100 * truth["honest_p95_true_rate"], 100 * truth["upcoder_margin"])
            + headline_table([r]) + "\n\nWhere each planted upcoder ranks:\n\n" + "\n".join(lines) + "\n\n"
            "**Fresh seeds on data 2.2.** The release 2 check (8 fresh seeds, rule fixed in advance) chose `eb_ratio`: [release2_screen_choice.md](release2_screen_choice.md). "
            "Release 3 added the test-line input (`eb_ratio_t`, 47 against 44 of 78 upcoders in the top 5% on the ten release 2 seeds, in sample): [dev_release3.md](dev_release3.md).")
    return details("Data 2.2: seed 42 here; fresh seeds in the release 2 and 3 pages", body)


def report(results, extra=CAVEATS):
    low = lambda r: r["providers"] > 300
    s216 = lambda r: r["providers"] <= 300
    show = ["riskadj", "eb_ratio", "priority", "ensemble", "zscore"]
    t = totals(results)
    n_up = sum(r["upcoders"] for r in results)
    pick = choice(results)
    wins = paired(results, "eb_ratio", "riskadj")
    i = ISSUE
    d1 = ("**How the first choice was made (rule stated after a first look, so not blind):** most upcoders in the top 25 over the 14 datasets, among methods "
          f"that put no more honest providers in the top 25 than `riskadj` ({t['riskadj']['hn'] + t['riskadj']['normal']}); ties go to the simpler method. It picks "
          f"**`{pick}`**: {t[pick]['found']} of {n_up} upcoders against {t['riskadj']['found']} for `riskadj`, with {t[pick]['hn']} high-acuity panels in the top 25 "
          f"against {t['riskadj']['hn']}. Paired by dataset, `eb_ratio` finds more upcoders than `riskadj` on {wins[0]} datasets, the same on {wins[1]} and fewer on {wins[2]}.\n\n"
          + headline_table(results) + "\n\n"
          + details("Full table, all 14 datasets (11 columns, with a legend)", LEGEND + "\n\n" + table(results))
          + details("216 providers, 3.7% upcoders (11 datasets)", table(results, s216))
          + details("600 providers, 0.5%, 1% and 2% upcoders (3 datasets, one draw each)", table(results, low))
          + details("Per dataset (selected methods)", per_dataset(results))
          + details("Flagging a percentile of providers (how payers do it)", percent_table(results))
          + details("A longer list", "600-provider datasets (21 upcoders):\n\n" + capacity_table([r for r in results if r["providers"] > 300])
                    + "\n\nAll 14 datasets (109 upcoders):\n\n" + capacity_table(results))
          + details("Where `riskadj`'s misses rank under the other screens", misses_table(results, show[1:4])))
    data_rows = "\n".join([
        "| Data | What changed for the screen | Screen results |",
        "|---|---|---|",
        "| 1 | Stored chronic-condition count; a records sample handed over up front | plain z-score only; not compared here ([archive](archive-version-1.md)) |",
        "| 2.0 | Plan-shaped tables; conditions derived from claims; half the upcoders clone notes | the 14 datasets below |",
        "| 2.1 | Adds the note package; claims are identical to 2.0 for a seed, so the screens score them the same | the 14 datasets below |",
        "| 2.2 | Honest coding noise in both directions; an upcoder must bill above the honest baseline by a margin; group billing and data defects | seed 42 below; fresh seeds on the release 2 and 3 pages |",
        "| 4.0 | Every provider has an upcoding rate; upcoders get a habit (systematic 99213-to-99214, opportunistic borderline-only, EHR template); wider honest noise | 11 development seeds below; [screens_v4.md](screens_v4.md) |",
    ])
    return ("# Screen methods: which screen ranks upcoders highest\n\n[Back to the README](../README.md) · [glossary](glossary.md)\n\n"
            "## In short\n\n"
            "- **Current screen: `eb_upper_t`** (workflow v4.0, agent v5.0). It shrinks the share of visits billed 99214 or 99215 against what the patients and the test line predict, "
            f"so upgrades into 99214 count. On the 11 data 4.0 development seeds it put {V4['eb_upper_t']['top10']['all']} of {V4_N} upcoders in the top 10% of providers against {V4['eb_ratio_t']['top10']['all']} "
            f"for `eb_ratio_t`, which looks only at 99215 and cannot see the systematic habit ({V4['eb_ratio_t']['top10']['systematic']} of {V4['eb_ratio_t']['n']['systematic']} against {V4['eb_upper_t']['top10']['systematic']} of {V4['eb_upper_t']['n']['systematic']}). "
            "The test line is a planted input (see the caveats), and these seeds are development data.\n"
            f"- **Before that: `eb_ratio_t`** (workflow v2.3 to v2.5, agent v3.3 to v3.5), `eb_ratio` with the test line as one more input to the expected 99215 count: "
            f"{R3_TOP5['eb_ratio_t']} of {R3_UPCODERS} upcoders in the top 5% on the ten release 2 seeds against {R3_TOP5['eb_ratio']} for `eb_ratio` (in sample).\n"
            f"- **How it got there.** On the 14 datasets of data 2.0 and 2.1, `eb_ratio` put {t['eb_ratio']['found']} of {n_up} upcoders in the top 25 against "
            f"{t['riskadj']['found']} for the risk-adjusted z-score (`riskadj`), and never fewer on any dataset. Release 2 confirmed it on 8 fresh data 2.2 seeds by a rule fixed in advance "
            f"({R2_TOP5['eb_ratio']} of {R2_UPCODERS} upcoders in the top 5% against {R2_TOP5['riskadj']}).\n"
            "- **Not solved.** No screen puts every upcoder in the top 25, and the gains are a few upcoders on synthetic data (see the caveats).\n"
            f"- **Next.** Whether `eb_upper_t` holds on a second fresh set of seeds ([issue]({i}132)); the opportunistic habit is the weakest ({V4['eb_upper_t']['top10']['opportunistic']} of {V4['eb_upper_t']['n']['opportunistic']} in the top 10%) ([issue]({i}134)).\n\n"
            "Generated by `python eval/screen_methods_eval.py --write` (also writes the chart); methods in `src/screen_methods.py`, ranking metrics in "
            "`eval/screen_metrics.py`. Free: claims and patients only, no model; the answer key only scores.\n\n"
            "![Share of upcoders each screen puts in the top 5% of providers, by data version](images/screen_methods_top5.svg)\n\n"
            + details("The numbers behind the chart", "Top 5% because the release 2 rule used it and it scales with the number of providers (11 of 216, 30 of 600).\n\n" + chart_rows(results))
            + "\n" + extra + "\n"
            "## The methods\n\n" + methods_table() + "\n\n"
            "**How the empirical Bayes screens work.** A provider's 99215 count is modeled as Poisson with mean θ x expected, where the expected count comes from the "
            "patients' chronic conditions (as in `riskadj`) and θ is the provider's true billing ratio. θ gets a Gamma prior with mean 1, its spread fitted by maximum "
            "likelihood on providers that are not already extreme, so the upcoders do not widen it. The score is the posterior mean, (a + observed) / (a + expected): a "
            "provider with few expected 99215s is pulled toward 1 (billing as the case mix predicts) more than one with many, so a small panel is less likely to top "
            "the list by chance. Shrinkage toward a prior fitted to all providers is common to every empirical Bayes method; this Gamma-Poisson form, its target of 1 "
            "and the trimmed fit are our choices. `eb_prob` and `eb_excess` read the same posterior differently.\n\n"
            "## Data versions\n\n" + data_rows + "\n\n"
            "## Results by data version\n\n"
            + details(f"Data 2.0 and 2.1: 14 datasets ({n_up} upcoders): `eb_ratio` {t['eb_ratio']['found']} in the top 25, `riskadj` {t['riskadj']['found']}", d1)
            + "\n" + data22_section() + "\n"
            + details(f"Data 4.0: 11 development seeds ({V4_N} upcoders): `eb_upper_t` {V4['eb_upper_t']['top10']['all']} in the top 10%, `eb_ratio_t` {V4['eb_ratio_t']['top10']['all']}", data40_section()) + "\n"
            "## Decisions so far\n\n"
            "- **Release 2:** Simmy chose `eb_ratio` and `priority` as candidates for both designs, with `riskadj` (frozen) and `zscore` as comparisons; the fresh-seed check "
            "picked `eb_ratio` ([release2_plan.md](release2_plan.md), [release2_screen_choice.md](release2_screen_choice.md)). Wired in as `flagging.py --method` and the "
            "agent's `screen_providers` method.\n"
            "- **Release 3:** `eb_ratio_t` adds the test-line input and becomes the screen of both designs ([dev_release3.md](dev_release3.md)).\n"
            "- **Workflow v4.0 and agent v5.0:** `eb_upper_t` replaces `eb_ratio_t` in both designs, chosen on the 11 development seeds ([screens_v4.md](screens_v4.md), [screens_v4_pipeline.md](screens_v4_pipeline.md)). "
            "The screen gets the right providers onto the list; rules 4.0 and the ask model decide what happens next, and the fresh-seed result shows the list is no longer the limit ([v4_v5_results.md](v4_v5_results.md)).\n")


def write_chart(results):
    with open(os.path.join(ROOT, "docs", "images", "screen_methods_top5.svg"), "w") as f:
        f.write(chart_svg(results) + "\n")


if __name__ == "__main__":
    if "--view" in sys.argv:
        a = sys.argv
        view, truth, label = a[a.index("--view") + 1], a[a.index("--truth") + 1], a[a.index("--label") + 1]
        r = [evaluate_dataset(view, json.load(open(truth)), label)]
        print(table(r))
        sys.exit()
    cache = os.path.join(ROOT, "experiments", "screen_methods_release1.json")
    if "--cached" in sys.argv:
        res = json.load(open(cache))
    else:
        res = run()
        json.dump(res, open(cache, "w"), indent=1)
    print(table(res))
    print()
    print(misses_table(res, ["eb_ratio", "priority", "ensemble"]))
    if "--write" in sys.argv:
        path = os.path.join(ROOT, "docs", "screen_methods.md")
        open(path, "w").write(report(res))
        write_chart(res)
        print("->", path)
