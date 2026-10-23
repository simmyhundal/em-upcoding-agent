"""Ceiling benchmarks for the v4.1 loop (docs/ceiling_benchmarks_w41.md): how much of D4.0's true overpayment can a chart-based arm recover under S4.0, and at what cost? Free (no model calls).

For the 480 planted upcoders of development batches 5 to 10 (60 seeds): the true net overpayment (answer key), what reading EVERY chart would find (documented levels from records_universe.csv, S4.0 pricing with netting),
the expected 90% lower bound of a random chart sample of n charts (recovery_40.recovery, 6 seeded draws per upcoder), the cost of asking and demanding (charts, two rounds, demand work), an oracle that pursues only the
upcoders whose expected bound beats that cost, and the actual recovery and cost of workflow v4.0 (H8) and the W4.1 candidate (H23, N = 4) from experiments/w_loop/*.json.
Usage: python eval/ceiling_benchmarks_41.py
"""
import csv
import json
import os
import random
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v4 as dp  # noqa: E402
import records as rcd  # noqa: E402
import recovery_40 as r4  # noqa: E402
import score_40 as s4  # noqa: E402

P = r4.PARAMS
NS = (30, 60, 90, 150)
SEEDS = [s for t in range(5, 11) for s in dp.BATCHES[t - 1]]
CH, RD, DM, TRIAGE = (r4.staff_cost(*a, P)[0] for a in ((0, 0, 1, 0, 0), (0, 1, 0, 0, 0), (0, 0, 0, 1, 0), (1, 0, 0, 0, 0)))


def ask_cost(n):
    return n * CH + 2 * RD + DM


def main():
    rng = random.Random(11)
    per = {n: [] for n in NS}
    by_h = {}
    tot_true = tot_audit = 0.0
    claims_n = []
    for s in SEEDS:
        code = f"d4_{s}"
        claims, key, truth = s4.context(code)
        level = {}
        for r in csv.DictReader(open(os.path.join(ROOT, "data", f"synthetic_v2_{code}", "records", "records_universe.csv"))):
            mins = r["documented_minutes"] if r["documented_minutes"] != "" else None
            level[r["claim_id"]] = max(rcd.mdm_level(int(r["problems_level"]), int(r["data_level"]), int(r["risk_level"])), rcd.level_from_minutes(mins))
        fees = r4.allowed()
        for pid, v in key["providers"].items():
            if v["role"] != "upcoder":
                continue
            cl = claims[pid]
            ids = [r["claim_id"] for r in cl if r["claim_id"] in level]
            if len(ids) < 50:
                continue
            amt = r4.claim_amounts(cl)
            audit = max(sum(r4.overpay_signed(r["cpt"], r4.CODES[level[r["claim_id"]]], fees, amt.get(r["claim_id"])) for r in cl if r["claim_id"] in level), 0)
            t = truth[pid]
            true = max(t["net_overpay"], 0)
            tot_true += true
            tot_audit += audit
            claims_n.append(t["claims"])
            hi = [r for r in cl if r["cpt"] in ("99214", "99215")]
            uns = sum(1 for r in hi if r4.LEVEL.get(key["justified_cpt_by_claim"].get(r["claim_id"]), 9) < r4.LEVEL[r["cpt"]])
            h = by_h.setdefault(v["habit"], dict(n=0, true=[], audit=0.0, lb30=0.0, up=[], claims=[], per_visit=[], uns=[]))
            h["n"] += 1
            h["true"].append(true)
            h["audit"] += audit
            h["up"].append(t["upcoded"])
            h["claims"].append(t["claims"])
            h["per_visit"].append(t["gross_overpay"] / max(t["upcoded"], 1))
            h["uns"].append(uns / max(len(hi), 1))
            for n in NS:
                vals = [r4.recovery(cl, set(rng.sample(ids, min(n, len(ids)))), level, P)["value"] for _ in range(6)]
                per[n].append(st.mean(vals))
                if n == 30:
                    h["lb30"] += st.mean(vals)
    N = len(per[30])
    print(f"{N} upcoders, development batches 5 to 10 ({len(SEEDS)} seeds); unit costs: chart {CH:.2f}, round {RD:.2f}, demand {DM:.2f}")
    print(f"true net overpayment ${tot_true:,.0f}; full chart audit ${tot_audit:,.0f}")
    print("\nBy habit (true net overpayment per upcoder, upcoded visits, per upcoded visit, share of 99214/99215 visits unsupported, audit and 30-chart bound as a share of true):")
    for hn, h in sorted(by_h.items()):
        print(f"  {hn}: n={h['n']} mean ${st.mean(h['true']):,.0f} median ${st.median(h['true']):,.0f}; upcoded {st.mean(h['up']):.0f} of {st.mean(h['claims']):.0f}; ${st.mean(h['per_visit']):.0f} per visit; unsupported {st.mean(h['uns']):.0%}; "
              f"audit {h['audit'] / sum(h['true']):.0%}; 30-chart bound {h['lb30'] / sum(h['true']):.0%}")
    allt = [x for h in by_h.values() for x in h["true"]]
    print(f"  all: mean ${st.mean(allt):,.0f} median ${st.median(allt):,.0f}")
    print("\n| Row | Recovery | Cost side | Net | Net per seed |\n|---|---|---|---|---|")
    f = lambda x: "n/a" if x is None else f"${x:,.0f}"
    rows = [("True net overpayment (answer key)", tot_true, None, None),
            ("Full chart audit, every chart read", tot_audit, st.mean(claims_n) * N * CH, tot_audit - st.mean(claims_n) * N * CH)]
    for n in NS:
        rows.append((f"Ask and demand all {N} upcoders, {n} charts", sum(per[n]), N * ask_cost(n), sum(per[n]) - N * ask_cost(n)))
    for n in NS:
        k = sum(1 for x in per[n] if x > ask_cost(n))
        net = sum(max(x - ask_cost(n), 0) for x in per[n])
        tri = k * TRIAGE                      # the oracle lists, and so triages, the providers it pursues (Simmy, 2026-10-22: an oracle pays the same score costs as a tuned arm)
        rows.append((f"Oracle: only the {k} worth pursuing, {n} charts (triage included)", net + k * ask_cost(n), k * ask_cost(n) + tri, net - tri))
    for lab, name in (("Workflow v4.0 (H8), actual", "H8"), ("W4.1 candidate (H23, N = 4), actual", "H23_n4")):
        d = json.load(open(os.path.join(ROOT, "experiments", "w_loop", f"{name}.json")))
        rows.append((lab, sum(d[str(s)]["recovered"] for s in SEEDS), sum(d[str(s)]["staff_cost"] + d[str(s)]["abrasion"] for s in SEEDS), sum(d[str(s)]["score"] for s in SEEDS)))
    for lab, rec, c, net in rows:
        print(f"| {lab} | {f(rec)} | {f(c)} | {f(net)} | {f(None if net is None else net / len(SEEDS))} |")
    print("\nMean lower bound per upcoder and cost per upcoder:", {n: (round(st.mean(per[n])), round(ask_cost(n))) for n in NS})


if __name__ == "__main__":
    main()
