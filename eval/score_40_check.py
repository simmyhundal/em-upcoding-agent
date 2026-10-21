"""Free check (issue 126): score 4.0 on every stored arm run of releases 2 to 5, side by side with the release 5 score, using the data 2.2 answer keys.
No model, no new seeds. Writes docs/score_40_check.md and experiments/score_40_check.json. Usage: python eval/score_40_check.py [--rerun]

Arms are the stored run folders (workflow and agent); the release 5 baseline also re-ran some arms (G, L, GL on releases 2 and 3), which are not stored runs and are not scored here.
Definitions of demand, listed, rounds, charts and API dollars: docs/score_40.md. Release 5's score is recomputed here from the same stored runs (eval/dollar_reward.py, unchanged)."""
import json
import multiprocessing as mp
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dollar_reward as dr  # noqa: E402
import score_40 as s4  # noqa: E402

OUT = os.path.join(ROOT, "experiments", "score_40_check.json")
DOC = os.path.join(ROOT, "docs", "score_40_check.md")
SETS = {"r2": ("Release 2", list(range(1515, 2425, 101)), [("W2.2", "r2w"), ("A3.2", "r2a")]),
        "r3": ("Release 3", list(range(2525, 3435, 101)), [("W2.2", "r3w2"), ("W2.3", "r3w"), ("A3.3", "r3a")]),
        "r4": ("Release 4", list(range(3535, 4445, 101)), [("W2.3", "r4w23"), ("G", "r4g"), ("L", "r4l"), ("GL", "r4gl"), ("A3.4", "r4a")]),
        "r5": ("Release 5", list(range(4545, 5455, 101)), [("W2.3", "r5w23"), ("GL", "r5gl"), ("W2.5", "r5w25"), ("A3.5", "r5a")])}
VARIANTS = {"base": {}, "review at $158 per chart (GAO)": {"REVIEW_COST_MODEL": "gao_per_claim"}, "one-sided 90% bound (manual)": {"BOUND": "one_sided_90"},
            "no gate, no netting (release 5 recovery basis)": {"GATE": False, "NETTING": False}, "no gate": {"GATE": False}, "no netting": {"NETTING": False},
            "gate at 10%": {"GATE_ERROR_RATE": 0.10}, "gate at 25%": {"GATE_ERROR_RATE": 0.25}, "gate at 40%": {"GATE_ERROR_RATE": 0.40},
            "demand charge $0": {"C_DEMAND_ABRASION": 0.0}, "demand charge $10,000": {"C_DEMAND_ABRASION": 10000.0}}
KEEP = ("recovered", "staff_cost", "abrasion", "score", "found", "upcoders", "demands", "honest_called", "recovered_from_non_upcoders", "abrasion_from_non_upcoders",
        "estimate_over_truth", "true_overpay_called", "true_overpay_all", "rounds", "charts", "over_n_up", "over_d_up", "over_n_non", "over_d_non")


def work(job):
    rel, seed = job
    code = f"{rel}_{seed}"
    rows = []
    reading = {}                                                   # how a returned chart reads against the billed and the true level, over the distinct charts of all arms on this seed
    claims0, key0, _ = s4.context(code)
    billed_of = {r["claim_id"]: r["cpt"] for rs in claims0.values() for r in rs}
    seen_charts = {}
    for arm, pre in SETS[rel][2]:
        rid = f"{pre}_{seed}"
        try:
            inputs = s4.run_inputs(rid, code)
            seen_charts.update(inputs["level"])
            r5 = dr.from_run(rid, code)
        except (FileNotFoundError, KeyError) as e:
            rows.append({"set": rel, "seed": seed, "arm": arm, "error": repr(e)})
            continue
        row = {"set": rel, "seed": seed, "arm": arm, "r5_value": r5["value"], "r5_net": dr.net(r5), "r5_found": r5["found"], "r5_honest_called": r5["honest_called"]}
        for name, over in VARIANTS.items():
            c = s4.from_run(rid, code, s4.params(**over), inputs)
            row[name] = {k: c[k] for k in KEEP}
            if name == "base":
                row["bands"], row["modes"], row["staff_parts"] = c["bands"], c["modes"], c["staff_parts"]
        rows.append(row)
    for cid, lvl in seen_charts.items():
        b, j = billed_of.get(cid), key0["justified_cpt_by_claim"].get(cid)
        if b is None or j is None:
            continue
        cls = "correct" if b == j else ("upcoded" if s4.LEVEL[b] > s4.LEVEL[j] else "downcoded")
        how = "reads higher than billed" if lvl > s4.LEVEL[b] else ("reads as billed" if lvl == s4.LEVEL[b] else "reads lower than billed")
        reading[f"{cls}|{how}"] = reading.get(f"{cls}|{how}", 0) + 1
    rows.append({"set": rel, "seed": seed, "arm": "_reading", "reading": reading})
    return rows


def collect():
    jobs = [(rel, seed) for rel, (_, seeds, _) in SETS.items() for seed in seeds]
    with mp.Pool(4) as pool:
        rows = [r for part in pool.map(work, jobs, chunksize=1) for r in part]
    json.dump(rows, open(OUT, "w"))
    return rows


def pooled(rows, rel, arm, variant="base"):
    rs = [r for r in rows if r["set"] == rel and r["arm"] == arm and "error" not in r]
    c = {k: sum(r[variant][k] for r in rs) for k in KEEP}
    c["n"] = len(rs)
    c["r5_net"] = sum(r["r5_net"] for r in rs)
    c["bands"] = {b: sum(r["bands"][b] for r in rs) for b, _, _ in s4.BANDS}
    c["chart_review"] = sum(r["staff_parts"]["chart review"] for r in rs)
    return c


def order(vals):
    return [a for a, _ in sorted(vals.items(), key=lambda kv: -kv[1])]


def discordant(v1, v2):
    arms = list(v1)
    return [(a, b) for i, a in enumerate(arms) for b in arms[i + 1:] if (v1[a] - v1[b]) * (v2[a] - v2[b]) < 0]


def money(x):
    return f"${x:,.0f}" if x >= 0 else f"-${-x:,.0f}"


def render(rows, rows_all=None):
    rows_all = rows_all or rows
    L = ["# Score 4.0 on the stored release 2 to 5 runs (issue 126)", "", "[Back to the README](../README.md) · [score 4.0 parameters](score_40.md) · [the v4/v5 plan](v4_v5_plan.md)", "",
         "Generated by `python eval/score_40_check.py`. **Free:** no model, no new seed. Every stored arm run of releases 2 to 5 (ten seeds each, development data) re-scored with score 4.0 on its data 2.2 answer key, "
         "beside release 5's score recomputed on the same runs. Per seed (pooled over ten seeds, divided by ten). Data 2.2 has no habits and a narrower honest noise than data 4.0, so this isolates the **score**, not the data. "
         "Parameters are assumptions with sensitivity ranges ([score_40.md](score_40.md)); `role` is data 2.2's binary label (8 to 11 upcoders per seed because of its relabeling rule).", ""]
    pub = {}
    for r in json.load(open(os.path.join(ROOT, "experiments", "release5_dollar_results.json"))):
        pub.setdefault((r["set"], r["arm"]), []).append(r)
    L += ["## Reconciliation with the release 5 baseline", "", "Release 5's net recomputed on the stored runs here, against the published baseline table (`docs/release5_dollar_baseline.md`). Arms the baseline re-ran from the screen lists (W2.2 and W2.3 on "
          "releases 2 and 3) can differ from the stored folders; the cause was not traced. This page uses the stored folders for both scores, so the comparison is like for like.", "",
          "| Release | Arm | Published net per seed | Recomputed here |", "|---|---|---|---|"]
    for rel, (title, seeds, arms) in SETS.items():
        for a, _ in arms:
            if (rel, a) in pub:
                rr = pub[(rel, a)]
                L.append(f"| {title} | {a} | {money(dr.net(dr.add(rr)) / len(rr))} | {money(pooled(rows, rel, a)['r5_net'] / len(seeds))} |")
    L.append("")
    verdicts = []
    for rel, (title, seeds, arms) in SETS.items():
        names = [a for a, _ in arms]
        P = {a: pooled(rows, rel, a) for a in names}
        n = P[names[0]]["n"]
        r5 = {a: P[a]["r5_net"] / n for a in names}
        s4v = {a: P[a]["score"] / n for a in names}
        L += [f"## {title} (seeds {seeds[0]} to {seeds[-1]})", "",
              "| Arm | Release 5 net | **Score 4.0** | Recovered | Staff-hours cost | of which chart review | Abrasion | Break-even scale | Upcoders found | Demands | Honest called |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for a in names:
            c = P[a]
            L.append(f"| {a} | {money(r5[a])} | **{money(s4v[a])}** | {money(c['recovered'] / n)} | {money(c['staff_cost'] / n)} | {money(c['chart_review'] / n)} | {money(c['abrasion'] / n)} | {(c['staff_cost'] + c['abrasion']) / max(c['recovered'], 1):.1f}x | {c['found']} of {c['upcoders']} | {c['demands']} | {c['honest_called']} |")
        flips = discordant(r5, s4v)
        verdicts.append((title, order(r5), order(s4v), flips))
        L += ["", f"Order by release 5 net: {', '.join(order(r5))}. Order by score 4.0: {', '.join(order(s4v))}. " + ("**Pairs whose order flips:** " + "; ".join(f"{a} and {b}" for a, b in flips) + "." if flips else "No pair flips."), "",
              "Non-upcoders and truth (per seed): ", "", "| Arm | Recovered from non-upcoders | Abrasion from non-upcoders | Demands with the estimate above the true overpayment: upcoders (dollars above) | same, non-upcoders (dollars above) | Estimates minus truth, all demands, netted | Dollar-weighted recall | Demands by true net rate: <0 / 0-5% / 5-15% / 15%+ |", "|---|---|---|---|---|---|---|---|"]
        for a in names:
            c = P[a]
            L.append(f"| {a} | {money(c['recovered_from_non_upcoders'] / n)} | {money(c['abrasion_from_non_upcoders'] / n)} | {c['over_n_up']} ({money(c['over_d_up'] / n)}) | {c['over_n_non']} ({money(c['over_d_non'] / n)}) | {money(c['estimate_over_truth'] / n)} | "
                     f"{c['true_overpay_called'] / c['true_overpay_all']:.0%} | {' / '.join(str(c['bands'][b]) for b, _, _ in s4.BANDS)} |")
        L += ["", "Recovered from non-upcoders per seed, by recovery rule: " + "; ".join(f"{v}: " + ", ".join(f"{a} {money(pooled(rows, rel, a, v)['recovered_from_non_upcoders'] / n)}" for a in names) for v in ("base", "no netting", "no gate, no netting (release 5 recovery basis)")) + ".",
              "", "Score 4.0 per seed under each sensitivity:", "", "| Variant | " + " | ".join(names) + " | Order |", "|---|" + "---|" * (len(names) + 1)]
        for v in VARIANTS:
            sv = {a: pooled(rows, rel, a, v)["score"] / n for a in names}
            L.append(f"| {v} | " + " | ".join(money(sv[a]) for a in names) + f" | {' > '.join(order(sv))} |")
        L.append("")
    flipped = [v for v in verdicts if v[3]]
    L += ["## Does score 4.0 reorder the arms?", ""]
    for title, o5, o4, fl in verdicts:
        L.append(f"- **{title}:** release 5 order {' > '.join(o5)}; score 4.0 order {' > '.join(o4)}" + (f"; flips: {', '.join(f'{a}/{b}' for a, b in fl)}." if fl else "; unchanged."))
    allarms = [(rel, a) for rel, (_, _, arms) in SETS.items() for a, _ in arms]
    neg = [(rel, a) for rel, a in allarms if pooled(rows, rel, a)["score"] < 0]
    rec_per_found = sum(pooled(rows, rel, a)["recovered"] for rel, a in allarms) / max(sum(pooled(rows, rel, a)["found"] for rel, a in allarms), 1)
    cost_share = sum(pooled(rows, rel, a)["staff_cost"] for rel, a in allarms) / max(sum(pooled(rows, rel, a)["recovered"] for rel, a in allarms), 1)
    chart_share = sum(pooled(rows, rel, a)["chart_review"] for rel, a in allarms) / max(sum(pooled(rows, rel, a)["staff_cost"] for rel, a in allarms), 1)
    L += ["", f"**Level.** Under the base assumptions {len(neg)} of {len(allarms)} arm-sets score below zero, and asking nobody scores 0. Two things cause it. (1) Recovery: on the level-difference basis it averages ${rec_per_found:,.0f} per upcoder found; the extrapolation gate and netting cut it further "
          "(the 'no gate, no netting' variant is the release 5 recovery basis). (2) The new staff-hours term: it is " + f"{cost_share:.1f} times what is recovered, and chart review is {chart_share:.0%} of it (the variant with every recovery rule off stays negative for most arms). "
          "The simulated provider has about 240 claims a year, so the recoverable amount is small beside fixed labor: read the scores as a **ranking** and the break-even scale column as how many times larger recoveries would have to be. "
          "Release 5's option 2 (denying cloned notes in full) is what made its arms positive.", ""]
    reading = {}
    for r in rows_all:
        if r["arm"] == "_reading":
            reading.setdefault(r["set"], {})
            for k_, v_ in r["reading"].items():
                reading[r["set"]][k_] = reading[r["set"]].get(k_, 0) + v_
    L += ["## How a returned chart reads against the truth (why netting matters)", "",
          "Distinct charts returned to any arm, by whether the claim was billed correctly, above or below the true level, and how the chart reads (the supported level by the time-or-decision-making rule, as the arms' estimates use it). "
          "Netting counts a chart that reads **higher** than billed as an underpayment, so it partly measures this documentation noise in data 2.2 (a correctly billed claim whose time statement is one level up reads as underpaid).", "",
          "| Release | Billed correctly: chart reads higher | as billed | lower | Billed above the true level: chart reads higher | as billed | lower |", "|---|---|---|---|---|---|---|"]
    for rel, (title, _, _) in SETS.items():
        d = reading.get(rel, {})
        def share(cls, how):
            tot = sum(v for k_, v in d.items() if k_.startswith(cls + "|"))
            return f"{d.get(f'{cls}|{how}', 0) / tot:.0%}" if tot else "-"
        L.append(f"| {title} | " + " | ".join(share("correct", h) for h in ("reads higher than billed", "reads as billed", "reads lower than billed")) + " | "
                 + " | ".join(share("upcoded", h) for h in ("reads higher than billed", "reads as billed", "reads lower than billed")) + " |")
    L += ["", "Data 4.0's reviewer-disagreement design must report this rate as a parameter: with netting on it drives recovery directly.", ""]
    L += ["", ("Yes, in " + ", ".join(v[0] for v in flipped) + "; see the pairs above and the sensitivity table (the order within a release moves with the assumptions)." if flipped else
               "No: the order of arms is the same in every release under both scores (the sensitivity tables show how stable that is)."), ""]
    open(DOC, "w").write("\n".join(L) + "\n")
    return verdicts


if __name__ == "__main__":
    rows = json.load(open(OUT)) if os.path.exists(OUT) and "--rerun" not in sys.argv else collect()
    errs = [r for r in rows if "error" in r]
    render([r for r in rows if "error" not in r and r["arm"] != "_reading"], rows)
    print("rows", len(rows), "errors", len(errs), errs[:3])
