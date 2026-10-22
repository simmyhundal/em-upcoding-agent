"""H23 (H22 with a shorter list) analysis: leave-one-batch-out choice of N on batches 1 to 4 and paired comparisons (declared in eval/w_loop_v41_decl.py). Free.
Usage: python eval/w_loop_h23.py lobo | python eval/w_loop_h23.py cmp N BATCHES   e.g. cmp 8 5,6"""
import os
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v4 as pool  # noqa: E402
import score_40 as s4  # noqa: E402
import w_loop as wl  # noqa: E402

NS = (4, 6, 8, 11, 15, 22)
TRIAGE = 13.125


def name(n):
    return "H22" if n == 22 else f"H23_n{n}"


def seeds_of(batches):
    return sum([pool.BATCHES[b - 1] for b in batches], [])


def lobo():
    res = {n: wl.evaluate(name(n), seeds_of([1, 2, 3, 4])) for n in NS}
    mean = lambda n, bs: st.mean(res[n][s]["score"] for b in bs for s in pool.BATCHES[b - 1])
    print("| N | " + " | ".join(f"batch {b}" for b in (1, 2, 3, 4)) + " | mean of 40 | found of 320 | honest called |\n|---|---|---|---|---|---|---|---|")
    for n in NS:
        print(f"| {n} | " + " | ".join(f"{mean(n, [b]):,.0f}" for b in (1, 2, 3, 4)) + f" | {mean(n, [1, 2, 3, 4]):,.0f} | {sum(r['found'] for r in res[n].values())} | {sum(r['honest_called'] for r in res[n].values())} |")
    tot = 0
    for h in (1, 2, 3, 4):
        rest = [b for b in (1, 2, 3, 4) if b != h]
        best = max(NS, key=lambda n: (mean(n, rest), n))      # ties to the larger list
        print(f"held out batch {h}: N = {best} chosen on the other three, realized {mean(best, [h]):,.0f} (H22 {mean(22, [h]):,.0f})")
        tot += mean(best, [h])
    print(f"leave-one-batch-out mean {tot / 4:,.0f}; H22 {mean(22, [1, 2, 3, 4]):,.0f}")
    print("final N (best mean of 40, ties to the larger):", max(NS, key=lambda n: (round(mean(n, [1, 2, 3, 4]), 6), n)))


def detail(n, ref, seeds):
    a, b = wl.evaluate(name(n), seeds), wl.evaluate(ref, seeds)
    d = [a[s]["score"] - b[s]["score"] for s in seeds]
    return a, b, d


def inputs(nm, seeds):
    out = {}
    for s in seeds:
        i = s4.run_inputs(f"wl{nm.lower()}_{s}", f"d4_{s}")
        out[s] = (i["listed"], sorted(i["random"]), i["called"])
    return out


def cmp(n, batches):
    seeds = seeds_of(batches)
    nm = name(n)
    for ref in ("H22", "H8"):
        a, b, d = detail(n, ref, seeds)
        c = wl.compare(nm, ref, seeds)
        k = len(seeds)
        print(f"\n{nm} vs {ref} on {k} seeds: {c['mean_a']:,.0f} vs {c['mean_b']:,.0f}, difference {c['mean_diff']:+,.0f} (sd {c['sd_diff']:,.0f}), p = {c['p']:.4f}, "
              f"better {sum(x > 1e-9 for x in d)} worse {sum(x < -1e-9 for x in d)} same {sum(abs(x) <= 1e-9 for x in d)}; found {c['found_a']} vs {c['found_b']}; rounds {c['rounds_a']} vs {c['rounds_b']}; honest called {c['hc_a']} vs {c['hc_b']}")
        for key in ("recovered", "staff_cost", "abrasion", "demands", "charts"):
            print(f"  {key} per seed: {sum(a[s][key] for s in seeds) / k:,.0f} vs {sum(b[s][key] for s in seeds) / k:,.0f}")
        ia, ib = inputs(nm, seeds), inputs(ref, seeds)
        la, lb = sum(v[0] for v in ia.values()) / k, sum(v[0] for v in ib.values()) / k
        asked_a = sum(len(v[1]) for v in ia.values()) / k
        asked_b = sum(len(v[1]) for v in ib.values()) / k
        saved = (lb - la) * TRIAGE
        print(f"  listed per seed {la:.1f} vs {lb:.1f}; triage per seed ${la * TRIAGE:,.0f} vs ${lb * TRIAGE:,.0f}; triage saved ${saved:,.0f}; asked per seed {asked_a:.2f} vs {asked_b:.2f}")
        print(f"  gain {c['mean_diff']:+,.0f} = triage saved {saved:+,.0f} + other (asking/recall) {c['mean_diff'] - saved:+,.0f}")
        dropped = sum(len(set(ib[s][1]) - set(ia[s][1])) for s in seeds)
        extra = sum(len(set(ia[s][1]) - set(ib[s][1])) for s in seeds)
        print(f"  providers asked by {ref} but not by {nm}: {dropped}; asked by {nm} only: {extra}; demands called by {ref} not by {nm}: {sum(len(ib[s][2] - ia[s][2]) for s in seeds)}")


if __name__ == "__main__":
    if sys.argv[1] == "lobo":
        lobo()
    else:
        cmp(int(sys.argv[2]), [int(x) for x in sys.argv[3].split(",")])
