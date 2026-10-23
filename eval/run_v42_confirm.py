"""The pre-declared confirm read of workflow v4.2 (docs/w42_freeze.md): W4.2 (H28) against workflow v4.1 (H23_n4) on the confirm pool of data 4.2 (seeds 1002 + 37j, 100 seeds), once.
Writes docs/w42_confirm_result.md and experiments/w_loop_42/ caches. Free. Usage: python eval/run_v42_confirm.py [--first N]"""
import json
import os
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v42 as pool  # noqa: E402
import seed_registry as sreg  # noqa: E402
import w_loop  # noqa: E402
import w_loop_42 as wl  # noqa: E402


def main(n=100):
    seeds = pool.CONFIRM[:n]
    for arm in ("H28", "H23_n4"):
        sreg.check_run("4.2", seeds, arm, "confirm")
    a, b = wl.evaluate("H28", seeds), wl.evaluate("H23_n4", seeds)
    diffs = [a[s]["score"] - b[s]["score"] for s in seeds]
    p = w_loop.perm_p(diffs)
    imp = sum(a[s]["impossible_providers"] for s in seeds)
    right = sum(a[s]["lane_true"] for s in seeds)
    wrong = sum(a[s]["lane_false"] for s in seeds)
    crit = {"gain >= +$500 per seed with p < 0.0125": st.mean(diffs) >= 500 and p < 0.0125,
            "lane demands >= 70% of impossible-day providers": right >= 0.7 * imp,
            "lane takes <= 0.5 providers per seed without impossible-day billing": wrong / len(seeds) <= 0.5}
    out = {"n": len(seeds), "W4.2_mean": st.mean(a[s]["score"] for s in seeds), "W4.2_median": st.median(a[s]["score"] for s in seeds), "W4.1_mean": st.mean(b[s]["score"] for s in seeds),
           "W4.1_median": st.median(b[s]["score"] for s in seeds), "diff_mean": st.mean(diffs), "diff_sd": st.stdev(diffs), "p": p, "wins": sum(d > 0 for d in diffs), "above_zero_W4.2": sum(a[s]["score"] > 0 for s in seeds),
           "above_zero_W4.1": sum(b[s]["score"] > 0 for s in seeds), "impossible": imp, "lane_right": right, "lane_wrong": wrong, "criteria": crit, "passed": all(crit.values())}
    json.dump(out, open(os.path.join(ROOT, "experiments", "w_loop_42", "confirm_result.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main(int(sys.argv[sys.argv.index("--first") + 1]) if "--first" in sys.argv else 100)
