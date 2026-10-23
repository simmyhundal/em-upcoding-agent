"""How many extra charts would turn a withdrawn near-miss into a demand, and is it worth it? (docs/ceiling_benchmarks_w41.md). Free (no model calls).

For workflow v4.0 (H8) runs on development batches 5 to 10: asked upcoders with a random sample that the rules did not demand, in two groups: the rules called them but the demand floor withdrew the call, or the rules did not call
them. From the stored sample, the extrapolated estimate, its variance and df are recomputed as recovery_40.recovery does; the 90% lower bound at n charts is taken as point - t * se * sqrt(n0 / n) (variance falls with
the sample size; the point estimate stays). Net value of extending to n charts = (new bound - demand cost if the bound clears the cost) - (extra charts + one more round). The extension is selected on a high point estimate,
so a new sample's estimate would regress toward the mean: the figures are optimistic. Usage: python eval/near_miss_charts_41.py
"""
import json
import math
import os
import statistics as st
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v4 as dp  # noqa: E402
import recovery_40 as r4  # noqa: E402
import score_40 as s4  # noqa: E402

P = r4.PARAMS
SEEDS = [s for t in range(5, 11) for s in dp.BATCHES[t - 1]]
COST = r4.staff_cost(0, 0, 0, 1, 0, P)[0]
CH = r4.staff_cost(0, 0, 1, 0, 0, P)[0]
RD = r4.staff_cost(0, 1, 0, 0, 0, P)[0]


def stats(rows, ids, level_of):
    by = {r["claim_id"]: r for r in rows}
    ids = [c for c in sorted(ids) if c in by and c in level_of]
    fees, amounts, vals = r4.allowed(), r4.claim_amounts(rows), {}
    for c in ids:
        b = by[c]["cpt"]
        vals.setdefault(b, []).append(r4.overpay_signed(b, r4.CODES[level_of[c]], fees, amounts.get(c)))
    frame = Counter(r["cpt"] for r in rows)
    total = var = 0.0
    n_all = k = 0
    for code, N in frame.items():
        v = vals.get(code, [])
        n = len(v)
        if not n:
            continue
        mean = sum(v) / n
        s2 = (sum((x - mean) ** 2 for x in v) / (n - 1)) if n > 1 else 0.0
        total += N * mean
        var += N * N * (1 - n / N) * s2 / n
        n_all += n
        k += 1
    return total, var, n_all, k


def main():
    groups = {"floor-withdrawn (rules called, bound below cost)": [], "not called by the rules": []}
    for s in SEEDS:
        code = f"d4_{s}"
        claims, key, truth = s4.context(code)
        inp = s4.run_inputs(f"wlh8_{s}", code)
        wd = json.load(open(os.path.join(ROOT, "experiments", f"wlh8_{s}", "demand_floor.json")))["withdrawn"]
        for pid, v in key["providers"].items():
            if v["role"] != "upcoder" or inp["rounds"].get(pid, 0) == 0 or not inp["random"].get(pid) or pid in inp["called"]:
                continue
            if r4.recovery(claims[pid], inp["random"][pid], inp["level"], P)["mode"] != "extrapolated":
                continue
            tot, var, n, k = stats(claims[pid], inp["random"][pid], inp["level"])
            groups["floor-withdrawn (rules called, bound below cost)" if pid in wd else "not called by the rules"].append(
                dict(h=v["habit"], n=n, pt=tot, se=math.sqrt(var), t=r4.t_value(max(n - k, 1), P["BOUND"])))
    print(f"demand cost ${COST:.0f}; chart ${CH:.2f}; round ${RD:.2f}")
    for g, L in groups.items():
        feas = [o for o in L if o["pt"] > COST]
        print(f"\n{g}: {len(L)} asked upcoders (extrapolated); point estimate above the demand cost: {len(feas)}; by habit {dict(Counter(o['h'] for o in L))}")
        needs = sorted(o["n"] * (o["t"] * o["se"] / (o["pt"] - COST)) ** 2 for o in feas)
        if not needs:
            continue
        print("  total charts needed for the bound to just clear the cost: median %.0f, quartiles %.0f / %.0f; up to 60: %.0f%%, up to 90: %.0f%%, up to 150: %.0f%%, up to 300: %.0f%%"
              % (st.median(needs), needs[len(needs) // 4], needs[3 * len(needs) // 4], *[100 * sum(x <= k for x in needs) / len(needs) for k in (60, 90, 150, 300)]))
        for n2 in (60, 90, 150, 300):
            net = gain = 0
            for o in feas:
                lb2 = max(o["pt"] - o["t"] * o["se"] * math.sqrt(o["n"] / n2), 0)
                extra = (n2 - o["n"]) * CH + RD
                if lb2 >= COST:
                    net += lb2 - COST - extra
                    gain += 1
                else:
                    net -= extra
            print(f"  extend all {len(feas)} to {n2} charts: demands gained {gain}, net ${net:,.0f} over {len(SEEDS)} seeds (${net / len(SEEDS):,.0f} per seed)")


if __name__ == "__main__":
    main()
