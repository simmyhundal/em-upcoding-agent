"""Score the candidate screen methods (src/screen_methods.py) against the answer key, per method and per dataset (issue 88).

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
    lines = [f"| Method | Upcoders in top 25 (of {n_up}) | Datasets with every upcoder in the top 25 (of {len(rs)}) | Honest in top 25: hard negatives | Honest in top 25: ordinary | "
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


def choice(results):
    """The selection rule, fixed before looking at the table: most upcoders in the top 25 across the 14 datasets among methods whose
    honest doctors in the top 25 (hard negatives plus ordinary) do not exceed `riskadj`'s. Ties go to the simpler method."""
    t = totals(results)
    base = t["riskadj"]["hn"] + t["riskadj"]["normal"]
    ok = [m for m in sm.METHODS if t[m]["hn"] + t[m]["normal"] <= base]
    return max(ok, key=lambda m: (t[m]["found"], -sm.METHODS.index(m)))


CAVEATS = """
## What this does and does not show

- **The target is not met.** The aim of issue 88 is every planted upcoder in the top 25. The best method here still leaves upcoders out on
  6 of 14 datasets. Most misses sit at ranks 26 to 55 (a longer list reaches them; see the tables above), and one upcoder (seed 1010) bills 99215 at
  only 1.2 times expected, so no 99215-only score ranks it high.
- **At 600 doctors `eb_ratio` ties `riskadj` in the top 25** (15 of 21 each); its gain there appears in a longer list (18 of 21 at 30, 20 at 40,
  against 15 and 17) and in AUPRC (0.48 against 0.31). With 3 to 12 upcoders per dataset and one draw each, this is one doctor either way.
- **`eb_ratio` helps by shrinking small panels, not by a new kind of evidence.** It is `riskadj`'s expectation (observed over expected 99215
  claims) pulled toward 1 in proportion to how little data a doctor has, so a 250-claim practice at 3x expected outranks a 60-claim practice at 3x.
  The gain over `riskadj` is a handful of upcoders over 14 datasets from one generator and one draw each: treat it as a promising direction,
  not a confirmed improvement, until the release 2 evaluation's fresh seeds.
- **The whole-distribution scores failed on this data** (`level_z`, `rich_level`, `eb_upper`, `eb_two`). Honest doctors differ in coding style
  (the generator's provider-level effects shift every threshold), and that moves the mean billed level and the 99214-or-higher share as much as an
  upcoder's one-level upgrades do. Only the 99215 count is a clean enough signal. Real claims have style differences too, so do not read this as
  "levels never help"; it says that with this much style noise a simple level score does not.
- **Patient-level features add nothing here, by construction.** The justified level depends on the member's chronic-condition count only (age is drawn
  from it; new versus established is not modeled), so `rich_logit` is essentially `riskadj`. On real data richer patient-level adjustment may matter; this
  data cannot show it.
- **Everything on data 2.0/2.1 is easier than real claims.** Honest providers bill exactly the justified level there. On the one data 2.2
  dataset (seed 42, honest coding noise) the picture is mixed: `riskadj` and `priority` have all 7 counted upcoders in their top 25 (the last at rank 25) and `eb_ratio`
  6 of 7 (the same doctor at rank 26), while `eb_ratio` ranks the whole list better (AUPRC 0.75 against 0.46 for `riskadj` and 0.65 for `priority`). One dataset, one doctor: it does not
  support or reject the choice, it only says the 5-upcoder gain from the 14 older datasets is not guaranteed to carry over.
- **Selection on seen data.** The 14 datasets are all development data now. Picking a method by this table is tuning; the choice is confirmed or
  rejected on the release 2 evaluation's fresh seeds, which have not been generated.
- **`ensemble` is a rank average that includes the weak `level_z`**, so it is dragged down; it is reported because it was a named candidate, not because it
  is a fair best-of-the-rest ensemble.
"""


def data22_section():
    """Seed 42 on data 2.2 (issue 74): the same table, one dataset, plus where each planted upcoder ranks. Empty if the data is absent."""
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
    lines = ["| Planted upcoder | Kind | Upcode rate | Counted as upcoder | " + " | ".join(f"`{m}` rank" for m in methods) + " |", "|---|---|---|---|" + "---|" * len(methods)]
    for p, v in sorted(planted.items(), key=lambda kv: -kv[1]["upcode_rate"]):
        lines.append(f"| {p} | {'subtle' if v['subtle'] else 'obvious'}, {'cloned' if v['clones_notes'] else 'honest'} notes | {v['upcode_rate']:.1%} "
                     f"| {'yes' if v['role'] == 'upcoder' else 'no (below the margin)'} | " + " | ".join(str(full[m][p]) for m in methods) + " |")
    return ("\n## Seed 42 on data 2.2 (honest coding noise, issue 74)\n\n"
            "One development dataset (run `261016_1_code`: 216 doctors, 8 planted upcoders of which %d count under the margin rule; honest baseline upcoding rate %.1f%%, "
            "margin %.0f points). One draw, so a single doctor moves any count here. Same columns as above.\n\n" % (
                r["upcoders"], 100 * truth["honest_baseline_upcode_rate"], 100 * truth["upcoder_margin"])
            + table([r]) + "\n\nWhere each planted upcoder ranks:\n\n" + "\n".join(lines) + "\n")


def report(results, extra=CAVEATS):
    low = lambda r: r["providers"] > 300
    s216 = lambda r: r["providers"] <= 300
    show = ["riskadj", "eb_ratio", "priority", "ensemble", "zscore"]
    return ("# Screen methods: can every upcoder reach the top 25? (issue 88)\n\n[Back to the README](../README.md)\n\n"
            "Generated by `python eval/screen_methods_eval.py --write`; methods in `src/screen_methods.py`, ranking metrics in "
            "`eval/screen_metrics.py`. Free: claims and patients only, no model. `riskadj` is the frozen screen of v2.1 and v3.1 "
            "(`src/baseline_riskadj.py`); the others are candidates built beside it.\n\n"
            "**Data.** The 14 release-1 datasets: development seed 42 plus the 13 datasets of the release 1 evaluation (#61). All of them "
            "have been seen, so they count as development data now; picking a method here is tuning on them, and the choice must be "
            "confirmed on the fresh seeds of the release 2 evaluation. Data 2.0/2.1: honest providers bill exactly the justified level "
            "and the justified level depends on the member's chronic-condition count by construction, which flatters every "
            "risk-adjusted method and makes the extra patient-level features useless (`rich_logit` is essentially `riskadj`: the same upcoders in every top 25). "
            "Issue 74 (data 2.2) adds honest coding noise; the table for seed 42 on data 2.2 is added when that data exists.\n\n"
            "## All 14 datasets\n\n" + table(results) + "\n\n"
            "## 216 doctors, 3.7% upcoders (11 datasets)\n\n" + table(results, s216) + "\n\n"
            "## 600 doctors, 0.5%, 1% and 2% upcoders (3 datasets, one draw each)\n\n" + table(results, low) + "\n\n"
            "## Per dataset (selected methods)\n\n" + per_dataset(results) + "\n\n"
            "Paired by dataset, `eb_ratio` finds more upcoders in the top 25 than `riskadj` on %d datasets, the same on %d and fewer on %d; "
            "`priority` against `riskadj`: %d, %d, %d.\n\n" % (paired(results, "eb_ratio", "riskadj") + paired(results, "priority", "riskadj"))
            + "## A longer list (600-doctor datasets, 21 upcoders)\n\n" + capacity_table([r for r in results if r["providers"] > 300]) + "\n\n"
            "## All 14 datasets, a longer list (109 upcoders)\n\n" + capacity_table(results) + "\n\n"
            "## Choice (rule stated after a first look at the table, so not blind)\n\n"
            "The rule (written down here after I had seen the ten-method table once, so it is not a blind pre-registration): most upcoders in the top 25 over the 14 datasets, among methods that put no more honest doctors in the top 25 than `riskadj` "
            "(%d). Ties go to the simpler method. The rule picks **`%s`**: %d of %d upcoders in the top 25 against %d for `riskadj`, with %d "
            "hard-negative doctors in the top 25 against %d.\n\n" % ((totals(results)["riskadj"]["hn"] + totals(results)["riskadj"]["normal"], choice(results),
            totals(results)[choice(results)]["found"], sum(r["upcoders"] for r in results), totals(results)["riskadj"]["found"],
            totals(results)[choice(results)]["hn"], totals(results)["riskadj"]["hn"]))
            + "## Where `riskadj` misses go\n\n" + misses_table(results, show[1:4]) + "\n" + data22_section() + extra)


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
        print("->", path)
