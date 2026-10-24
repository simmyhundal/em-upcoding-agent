"""One yardstick for the README table: score 4.2's formula on every version of the v4 and v5 line, from the stored runs. Free; reads the answer keys (evaluation only).

Data 4.0 test seeds (5555 + 101j): workflow v4.0 (fr40), workflow v4.1 (fr41), agent v5.0 (fra50), agent v5.1 (fra51) re-scored by score 4.2. On data 4.0 nothing is fraudulent and nothing is unrendered, so score 4.2 there is
score 4.0 with the copy fee at $0 (score 4.1's commercial profile), abrasion on the true level rate, as before. The runs themselves are unchanged; only the price list differs.
Data 4.2 test seeds (4700 + 37j): workflow v4.1 (re-run), workflow v4.2, agent v5.2, scored by score 4.2 (experiments/v42_test_results.json).
Measures per arm: upcoders found = providers whose true net level rate is at least 15% that were sent a demand (data 4.0: the 8 planted per dataset; data 4.2: about 9 per dataset), and, on data 4.2,
providers with impossible-day billing that were sent a demand. Writes experiments/yardstick_s42.json.
Usage: python eval/yardstick_s42.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import d42_truth as dt  # noqa: E402
import dev_pool_v42 as pool  # noqa: E402
import recovery_42 as r42  # noqa: E402
import score_40 as s4  # noqa: E402
import score_42 as s42  # noqa: E402

OUT = os.path.join(ROOT, "experiments", "yardstick_s42.json")
D40_SEEDS = [5555 + 101 * j for j in range(10)]
D40 = [("Workflow v4.0", "fr40"), ("Workflow v4.1", "fr41"), ("Agent v5.0", "fra50"), ("Agent v5.1", "fra51")]
D42 = [("Workflow v4.1", "d42t_h23_n4_"), ("Workflow v4.2", "d42t_h28_"), ("Agent v5.2", "fra52_")]


def d40_rows():
    p = r42.params42()
    out = []
    for label, pre in D40:
        sc = found = up = demands = 0
        for s in D40_SEEDS:
            c = s4.from_run(f"{pre}_{s}", f"f4_{s}", p)
            sc += c["score"]; found += c["found"]; up += c["upcoders"]; demands += c["demands"]
        out.append({"arm": label, "data": "4.0, test", "score": round(sc), "found": found, "upcoders": up, "lane_found": None, "lane_total": None, "demands": demands})
    return out


def d42_rows():
    out = []
    for label, pre in D42:
        sc = found = up = lf = lt = demands = 0
        for s in pool.TEST:
            code, rid = f"d42_{s}", (f"{pre}{s}" if pre.endswith("_") else f"{pre}_{s}")
            c, i = s42.seed_result(rid, code)
            key = dt.load_key(code)["providers"]
            r15 = {pid for pid, v in key.items() if v["net_rate"] >= 0.15}
            imp = {pid for pid, v in key.items() if v["true_overpay_fwa"].get("impossible_days", 0) > 0}
            ln = s42.lane(rid)["providers"]
            called = set(i["called"]) | {pid for pid, v in ln.items() if v.get("demand")}
            sc += c["score"]; found += len(called & r15); up += len(r15); lf += len(called & imp); lt += len(imp); demands += len(called)
        out.append({"arm": label, "data": "4.2, test", "score": round(sc), "found": found, "upcoders": up, "lane_found": lf, "lane_total": lt, "demands": demands})
    return out


if __name__ == "__main__":
    rows = d40_rows() + d42_rows()
    json.dump(rows, open(OUT, "w"), indent=1)
    for r in rows:
        print(r)
