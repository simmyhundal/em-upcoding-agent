"""Leave-one-batch-out choice of one parameter on batches 1 to 4 (H20): for each held-out batch, take the setting with the best mean on the other three (ties to the smaller) and record its score on the
held-out batch; the final choice is the best mean over all four (ties to the smaller). Free. Usage: python eval/sweep_select_41.py PREFIX v1,v2,...   (version names PREFIX<v>)"""
import json
import os
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v4 as pool  # noqa: E402


def select(prefix, values, suffix=""):
    tab = {}
    for v in values:
        d = json.load(open(os.path.join(ROOT, "experiments", "w_loop", f"{prefix}{v}{suffix}.json")))
        tab[v] = [st.mean(d[str(s)]["score"] for s in pool.BATCHES[b]) for b in range(4)]
    mean = {v: st.mean(x) for v, x in tab.items()}
    best = lambda cand: min(cand, key=lambda v: (-cand[v], float(v)))
    folds = []
    for f in range(4):
        sub = {v: st.mean(x for i, x in enumerate(tab[v]) if i != f) for v in values}
        c = best(sub)
        folds.append({"held_out_batch": f + 1, "chosen": c, "realized": tab[c][f]})
    return {"batch_means": tab, "mean": mean, "chosen": best(mean), "folds": folds, "lobo_mean": st.mean(x["realized"] for x in folds)}


if __name__ == "__main__":
    suffix = sys.argv[3] if len(sys.argv) > 3 else ""
    r = select(sys.argv[1], sys.argv[2].split(","), suffix)
    json.dump(r, open(os.path.join(ROOT, "experiments", "w_loop", f"{sys.argv[1]}_select{suffix}.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in r.items() if k != "batch_means"}, indent=1))
