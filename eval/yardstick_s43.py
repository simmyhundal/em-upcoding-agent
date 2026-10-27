"""One yardstick under score 4.3 for the README table and docs/score_43_rescored.md: every version of the v4 and v5 line re-scored from the stored runs (free), beside the oracle of its data.
Rows: data 4.0 test seeds (5555 + 101j): workflow v4.0, agent v5.0, workflow v4.1, agent v5.1; data 4.2 test seeds (4700 + 37j): workflow v4.1 (re-run), workflow v4.2, agent v5.2.
Writes experiments/yardstick_s43.json (needs experiments/oracle_s43.json from eval/oracle_s43.py --write). Usage: python eval/yardstick_s43.py [--write]"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v42 as pool  # noqa: E402
import score_43 as s43  # noqa: E402

OUT = os.path.join(ROOT, "experiments", "yardstick_s43.json")
D40_SEEDS = [5555 + 101 * j for j in range(10)]
D40 = [("Workflow v4.0", "fr40"), ("Agent v5.0", "fra50"), ("Workflow v4.1", "fr41"), ("Agent v5.1", "fra51")]       # development order
D42 = [("Workflow v4.1", "d42t_h23_n4_"), ("Workflow v4.2", "d42t_h28_"), ("Agent v5.2", "fra52_")]


def rows():
    orc = json.load(open(os.path.join(ROOT, "experiments", "oracle_s43.json")))
    out = []
    for data, arms, seeds, codef, ridf in (("4.0, test", D40, D40_SEEDS, lambda s: f"f4_{s}", lambda pre, s: f"{pre}_{s}"),
                                           ("4.2, test", D42, pool.TEST, lambda s: f"d42_{s}", lambda pre, s: f"{pre}{s}" if pre.endswith("_") else f"{pre}_{s}")):
        for arm, pre in arms:
            per = {}
            for s in seeds:
                c, _ = s43.seed_result(ridf(pre, s), codef(s))
                per[codef(s)] = c
            score = sum(c["score"] for c in per.values())
            o = orc[data]
            beats = [k for k, c in per.items() if c["score"] > o["per_seed"][k] + 1e-6]
            out.append({"arm": arm, "data": data, "score": round(score), "oracle": round(o["score"]), "share": score / o["score"], "collected": round(sum(c["collected"] for c in per.values())),
                        "staff": round(sum(c["staff_cost"] for c in per.values())), "abrasion": round(sum(c["abrasion"] for c in per.values())), "demands": sum(c["demands"] for c in per.values()),
                        "referrals": sum(c["referrals"] for c in per.values()), "seeds_above_oracle": beats})
    return out


if __name__ == "__main__":
    r = rows()
    for x in r:
        print(x["arm"], x["data"], x["score"], x["oracle"], f"{100 * x['share']:.0f}%", x["seeds_above_oracle"])
    if "--write" in sys.argv:
        json.dump(r, open(OUT, "w"), indent=1)
