"""Ceiling test on data 4.0 (issue 117): how much score 4.0 is left in the upcoders a workflow arm misses? Free (API-free workflow runs; answer key read only to score).

Frozen workflow v2.4 (GL) and v2.5 on the data 4.0 development seeds (d4_42, d4_1515 to d4_2424) with the frozen `eb_ratio_t` list, and v2.5 on the chosen `eb_upper_t` list. For each arm:
  the funnel of the planted upcoders: not in the list, listed but never asked, asked but no usable chart came back (silent), charts back but not called, called;
  the ceiling ladder: an oracle turns misses into finds, cumulatively, at their value and with the extra work costed (score 4.0 prices):
    A  every asked-but-not-called upcoder is called (silent or inconclusive): its own estimate where it has a random sample, else the mean of the called upcoders; plus demand work
    B  A plus the listed-but-never-asked upcoders: mean value, plus the mean rounds and charts of an asked provider, plus demand work
    C  B plus the upcoders outside the list (as B, plus triage)
  each rung twice: valued at the estimate (what score 4.0 would recover) and at the true overpayment (a payer with a perfect extrapolation).
Writes docs/ceiling_v4.md. Usage: python eval/ceiling_v4.py [--rerun]
"""
import csv
import json
import multiprocessing as mp
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_release3 as dev  # noqa: E402
import make_d4_dev as md  # noqa: E402
import make_v2_office_workflow_runs as ow  # noqa: E402
import run_release2 as r2  # noqa: E402
import score_40 as s4  # noqa: E402
import workflow_policy_24 as p24  # noqa: E402

ARMS = [("W2.4 (GL) on eb_ratio_t", "ceilgl", "2.4", p24.ARMS["GL"], "eb_ratio_t"), ("W2.5 on eb_ratio_t", "ceil25", "2.5", None, "eb_ratio_t"), ("W2.5 on eb_upper_t", "ceil25u", "2.5", None, "eb_upper_t")]
DOC = os.path.join(ROOT, "docs", "ceiling_v4.md")
CACHE = os.path.join(ROOT, "experiments", "ceiling_v4.json")


def run_arm(job):
    label, pre, version, opts, screen, seed = job
    code = f"d4_{seed}"
    name = dev.write_flagged(code, screen, 10)
    rid = f"{pre}_{seed}"
    if not r2.done(rid, "case_summaries_checked.jsonl"):
        kw = {"policy24": opts} if opts is not None else {}
        ow.run(rid, code, name, f"frozen {label} on data 4.0 development seed {seed} (issue 117)", version=version, tier1_n=11, no_model=True, **kw)
    claims, key, truth = s4.context(code)
    inp = s4.run_inputs(rid, code)
    listed = {r["provider_id"] for r in csv.DictReader(open(os.path.join(ROOT, "experiments", code, f"flagged_{name}.csv"))) if r["flagged"] == "True"}
    base = s4.from_run(rid, code)
    P = key["providers"]
    rows = []
    for pid, v in P.items():
        if v["role"] != "upcoder":
            continue
        rec = s4.recovery(claims.get(pid, []), inp["random"].get(pid, set()), inp["level"], s4.PARAMS) if pid in inp["random"] and inp["random"][pid] else None
        rows.append({"pid": pid, "habit": v["habit"], "cloner": v["clones_notes"], "listed": pid in listed, "asked": inp["rounds"].get(pid, 0) > 0, "charts": inp["charts"].get(pid, 0),
                     "called": pid in inp["called"], "est": rec["value"] if rec else None, "true": max(truth[pid]["net_overpay"], 0.0), "rounds": inp["rounds"].get(pid, 0)})
    return {"arm": label, "seed": seed, "base": {k: base[k] for k in ("score", "recovered", "staff_cost", "abrasion", "found", "demands", "honest_called", "rounds", "charts")}, "ups": rows}


def build():
    jobs = [(a[0], a[1], a[2], a[3], a[4], s) for a in ARMS for s in md.SEEDS]
    with mp.get_context("spawn").Pool(4) as pool:
        res = pool.map(run_arm, jobs, chunksize=1)
    json.dump(res, open(CACHE, "w"))
    return res


def ladder(runs, label):
    rs = [r for r in runs if r["arm"] == label]
    n = len(rs)
    ups = [u for r in rs for u in r["ups"]]
    called = [u for u in ups if u["called"]]
    mean_est = sum(u["est"] or 0.0 for u in called) / max(len(called), 1)
    mean_true = sum(u["true"] for u in called) / max(len(called), 1)
    asked = [u for u in ups if u["asked"]]
    mean_rounds = sum(u["rounds"] for u in asked) / max(len(asked), 1)
    mean_charts = sum(u["charts"] for u in asked) / max(len(asked), 1)
    p = s4.PARAMS
    demand = s4.staff_cost(0, 0, 0, 1, 0, p)[0]
    ask = s4.staff_cost(0, mean_rounds, mean_charts, 0, 0, p)[0]
    triage = s4.staff_cost(1, 0, 0, 0, 0, p)[0]

    def value(u, how):
        return (u["est"] if u["est"] is not None else mean_est) if how == "est" else u["true"]
    out = {"base": sum(r["base"]["score"] for r in rs) / n, "found": sum(r["base"]["found"] for r in rs)}
    for how in ("est", "true"):
        gainA = sum(value(u, how) - demand for u in ups if u["asked"] and not u["called"])
        gainB = sum((mean_est if how == "est" else value(u, how)) - ask - demand for u in ups if u["listed"] and not u["asked"])
        gainC = sum((mean_est if how == "est" else value(u, how)) - ask - demand - triage for u in ups if not u["listed"])
        out[how] = {"A": out["base"] + gainA / n, "B": out["base"] + (gainA + gainB) / n, "C": out["base"] + (gainA + gainB + gainC) / n}
    cnt = Counter()
    for u in ups:
        cnt["called" if u["called"] else "asked, charts back, not called" if u["asked"] and u["charts"] else "asked, no usable chart" if u["asked"] else "listed, never asked" if u["listed"] else "not in the list"] += 1
    return out, cnt, len(ups), ups


def main():
    runs = json.load(open(CACHE)) if os.path.exists(CACHE) and "--rerun" not in sys.argv else build()
    L = ["# The ceiling on data 4.0: how much score is left in the upcoders a workflow misses? (issue 117)", "", "[Back to the README](../README.md) · [v4/v5 plan](v4_v5_plan.md) · [screens on data 4.0](screens_v4.md)", "",
         "Generated by `python eval/ceiling_v4.py`. **Free:** frozen workflow arms (API-free) on the 11 data 4.0 development seeds, score 4.0. The oracle is an upper bound, not a plan: it ignores that some misses are unfindable with what an office returns. "
         "The frozen arms were fitted on data 2.2 and score 99215 evidence, so their funnel here shows what the new data and screens ask of v4.0, not how a v4.0 arm would do.", ""]
    outs = {}
    for label, *_ in ARMS:
        out, cnt, n_up, ups = ladder(runs, label)
        outs[label] = (out, cnt, n_up)
        L += [f"## {label}", "", f"Score 4.0 per seed as run: **${out['base']:,.0f}**; upcoders found {out['found']} of {n_up}.", "", "Where the 88 upcoders drop out:", "", "| Step | Upcoders | Systematic | Opportunistic | Template-driven | Cloners |", "|---|---|---|---|---|---|"]
        for step in ("not in the list", "listed, never asked", "asked, no usable chart", "asked, charts back, not called", "called"):
            def sel(u):
                return (u["called"] if step == "called" else (not u["called"] and u["asked"] and u["charts"] and step == "asked, charts back, not called")
                        or (not u["called"] and u["asked"] and not u["charts"] and step == "asked, no usable chart") or (not u["called"] and not u["asked"] and u["listed"] and step == "listed, never asked")
                        or (not u["called"] and not u["asked"] and not u["listed"] and step == "not in the list"))
            row = [u for u in ups if sel(u)]
            L.append(f"| {step} | {len(row)} | " + " | ".join(str(sum(u["habit"] == h for u in row)) for h in ("systematic", "opportunistic", "template")) + f" | {sum(u['cloner'] for u in row)} |")
        L += ["", "Score 4.0 per seed up the ladder:", "", "| Rung | Valued at the estimate | Valued at the true overpayment |", "|---|---|---|", f"| As run | ${out['base']:,.0f} | ${out['base']:,.0f} |"]
        for r, name in (("A", "A: every asked upcoder called"), ("B", "B: A plus the listed but never asked"), ("C", "C: B plus those outside the list")):
            L.append(f"| {name} | ${out['est'][r]:,.0f} | ${out['true'][r]:,.0f} |")
        L.append("")
    o_f, o_u = outs["W2.5 on eb_ratio_t"][0], outs["W2.5 on eb_upper_t"][0]
    rv = {k: 0.0 for k in ("base", "no netting", "one-sided", "all three", "true")}
    for sd in md.SEEDS:
        code = f"d4_{sd}"
        inp = s4.run_inputs(f"ceil25u_{sd}", code)
        for k, o in (("base", {}), ("no netting", {"NETTING": False}), ("one-sided", {"BOUND": "one_sided_90"}), ("all three", {"GATE": False, "NETTING": False, "BOUND": "one_sided_90"})):
            rv[k] += s4.from_run(f"ceil25u_{sd}", code, s4.params(**o), inp)["recovered"] / len(md.SEEDS)
        rv["true"] += s4.from_run(f"ceil25u_{sd}", code, None, inp)["true_overpay_called"] / len(md.SEEDS)
    L += ["## Reading", "",
          f"- **The frozen screen is the first ceiling.** With the 99215-share list, 70 of the 88 upcoders never reach the list and the frozen arms find 3 to 4. Even rung C valued at the estimate stays far below zero (${o_f['est']['C']:,.0f} per seed for W2.5): "
          "finding more upcoders at today's recovery prices does not pay. Valued at the true overpayment rung C would be "
          f"${o_f['true']['C']:,.0f}, so the money is there but not at the price score 4.0 collects it.",
          f"- **With the chosen screen the next ceiling is the decision layer.** On the `eb_upper_t` list 81 upcoders are listed, 40 of them asked with charts back and **not called** (21 systematic, 16 template-driven: the frozen rules read 99215 evidence). "
          f"Calling them all (rung A) is worth ${o_u['est']['A'] - o_u['base']:,.0f} per seed at the estimate and **${o_u['true']['A'] - o_u['base']:,.0f} at the true overpayment**.",
          f"- **The largest gap is recovery, not detection.** Of the true overpayment of the providers W2.5 called on the `eb_upper_t` list (${rv['true']:,.0f} per seed), the base score recovers ${rv['base']:,.0f}. Dropping the netting of underpayments (12% of correctly billed charts read higher than billed) lifts it to ${rv['no netting']:,.0f}, "
          f"the manual's one-sided 90% bound to ${rv['one-sided']:,.0f}, all three to ${rv['all three']:,.0f}; the rest is the sample (30 charts spread over every billed level) and the lower bound. A recovery that samples where the overpayment is (the 99213-to-99214 stratum for the systematic and template habits) and handles reviewer noise is worth more than any list. "
          "This is the lever for the W arm's RL loop.",
          "- **Silent offices are few.** 'Asked, no usable chart' is 1 to 6 of 88 upcoders in every arm: not worth building for beside the above. Clean-looking cloners are 1 to 2 per arm.",
          "- Not tested here: a second targeted request for silent offices (#103) and the cost of non-response (#68); the counts above say they are small."]
    open(DOC, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
