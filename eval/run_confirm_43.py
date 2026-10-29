"""The pre-declared confirm read of workflow v4.3 (docs/w43_freeze.md): W4.3 (H33), workflow v4.1 (W41), workflow v4.2 (W42) and the ask-nobody control (H0) on the 100 data 4.3 confirm seeds,
read once, scored with score 4.3. Free, API-free. Writes experiments/w43_confirm_results.json. Usage: python eval/run_confirm_43.py [--approved]"""
import json
import os
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v43 as pool  # noqa: E402
import seed_registry as sreg  # noqa: E402
import w_loop  # noqa: E402
import w_loop_43 as w  # noqa: E402

OUT = os.path.join(ROOT, "experiments", "w43_confirm_results.json")
ARMS = {"W43": "H33", "W41": "W41", "W42": "W42", "H0": "H0"}

if __name__ == "__main__":
    if os.path.exists(OUT):
        sys.exit("the confirm pool was already read once: " + OUT)
    seeds = list(pool.CONFIRM)
    for arm in ARMS.values():
        sreg.check_run("4.3", seeds, arm, "confirm")
    res = {}
    for name, ver in ARMS.items():
        res[name] = {str(s): w._run((ver, s))[1] for s in seeds}
    json.dump(res, open(OUT, "w"), indent=0)
    sc = {n: [res[n][str(s)]["score"] for s in seeds] for n in ARMS}
    for n in ARMS:
        print(n, "per seed", round(st.mean(sc[n])), "median", round(st.median(sc[n])), "above zero", sum(x > 0 for x in sc[n]), "charts", round(st.mean(res[n][str(s)]["charts"] for s in seeds)))
    for a, b in (("W43", "W41"), ("W43", "H0"), ("W43", "W42")):
        d = [x - y for x, y in zip(sc[a], sc[b])]
        print(a, "-", b, round(st.mean(d)), "sd", round(st.stdev(d)), "wins", sum(x > 0 for x in d), "of", len(d), "p", round(w_loop.perm_p(d), 4))
