"""The oracle under score 4.2: the best conceivable score on one dataset, with triage, from the answer key (evaluation only). An UPPER BOUND, not an arm and not a target.

For each provider the oracle knows the true supported level of every claim and which claims are for visits that never happened, and takes the better of two options (not added together):
  level option: pursue with a random chart sample of n charts (n = 30, 60, 90 or 150, the best); value = the expected 90% lower bound of the level overpayment (averaged over `draws` random samples) minus
    the staff cost of the charts received, two request rounds, a demand and triage, minus abrasion (weight w on the provider's total true rate);
  lane option (providers with a day of 30 or more visits): a random sample of 30 claims on those days; claims for visits that never happened return no record (counted at their paid amount), the rest are
    priced by the true level; value = the expected stratum lower bound minus the cost of the charts received, one round, a demand and triage (abrasion weight 0: the provider overbilled).
It pursues a provider only when the value is positive. It pays triage like a tuned arm, assumes every office answers (no silence), and assumes perfect screening: the gap between it and an arm is the whole
distance from the arm to what the data allow. Works on data 4.0 test datasets (no fraud claims) and on data 4.2.
Usage: python eval/oracle_s42.py [--write]   -> experiments/oracle_s42.json
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
import dev_pool_v42 as pool  # noqa: E402
import eval61_recovery as rec  # noqa: E402
import fwa_lane  # noqa: E402
import recovery_40 as r4  # noqa: E402
import recovery_42 as r42  # noqa: E402
import records as rcd  # noqa: E402
import score_40 as s4  # noqa: E402

NS = (30, 60, 90, 150)
FRAUD = ("not_rendered", "impossible_days")
OUT = os.path.join(ROOT, "experiments", "oracle_s42.json")


def oracle(code, seed=11, draws=6):
    p = r42.params42()
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))
    fraud = {c: k for c, k in key.get("fraud_claims", {}).items() if k in FRAUD}
    claims = {}
    for r in csv.DictReader(open(os.path.join(data, "view", "claims.csv"))):
        claims.setdefault(r["provider_id"], []).append(r)
    allowed = rec.allowed()
    level = {}
    for r in csv.DictReader(open(os.path.join(data, "records", "records_universe.csv"))):
        mins = r["documented_minutes"] if r["documented_minutes"] != "" else None
        level[r["claim_id"]] = max(rcd.mdm_level(int(r["problems_level"]), int(r["data_level"]), int(r["risk_level"])), rcd.level_from_minutes(mins))
    chart = r4.staff_cost(0, 0, 1, 0, 0, p)[0]
    rnd, dem, tri = r4.staff_cost(0, 1, 0, 0, 0, p)[0], r4.staff_cost(0, 0, 0, 1, 0, p)[0], r4.staff_cost(1, 0, 0, 0, 0, p)[0]
    price = 2 * p["C_BURDEN"] + p["C_DEMAND_ABRASION"]
    rng = random.Random(seed)
    total = {"score": 0.0, "pursued": 0, "recovered": 0.0, "lane_pursued": 0}
    for pid, cl in claims.items():
        ids = [r["claim_id"] for r in cl]
        if len(ids) < 50:
            continue
        rendered_rows = [r for r in cl if r["claim_id"] not in fraud]
        t = s4.provider_truth(rendered_rows, key["justified_cpt_by_claim"], allowed)
        ph = sum(1 for r in cl if r["claim_id"] in fraud)
        rate = (t["upcoded"] - t["downcoded"] + ph) / max(t["claims"] + ph, 1)
        w = s4.abrasion_weight(rate, p)
        best = None
        for n in NS:                                                   # level option
            vals, got = [], []
            for _ in range(draws):
                sample = rng.sample(ids, min(n, len(ids)))
                rendered = {c for c in sample if c not in fraud}
                vals.append(r42.recovery(cl, rendered, level, p)["value"])
                got.append(len(rendered))
            lb, g = st.mean(vals), st.mean(got)
            v = lb - (g * chart + 2 * rnd + dem + tri) - w * price
            if best is None or v > best[0]:
                best = (v, lb, False)
        days = {}
        for r in cl:
            days[r["service_date"]] = days.get(r["service_date"], 0) + 1
        hot = {d for d, k in days.items() if k >= fwa_lane.DAY_MAX}
        if hot:                                                        # lane option
            stratum = [r for r in cl if r["service_date"] in hot]
            sids = [r["claim_id"] for r in stratum]
            vals, got = [], []
            for _ in range(draws):
                sample = rng.sample(sids, min(fwa_lane.SAMPLE_N, len(sids)))
                nr = {c for c in sample if c in fraud}
                vals.append(r42.recovery_stratified(stratum, sample, level, p, no_record=nr)["value"])
                got.append(len(sample) - len(nr))
            lb, g = st.mean(vals), st.mean(got)
            v = lb - (g * chart + rnd + dem + tri)
            if v > best[0]:
                best = (v, lb, True)
        if best[0] > 0:
            total["score"] += best[0]; total["pursued"] += 1; total["recovered"] += best[1]; total["lane_pursued"] += int(best[2])
    return total


def run():
    out = {}
    for name, codes in (("4.0, test", [f"f4_{5555 + 101 * j}" for j in range(10)]), ("4.2, test", [f"d42_{s}" for s in pool.TEST])):
        tot = {"score": 0.0, "pursued": 0, "recovered": 0.0, "lane_pursued": 0}
        for c in codes:
            o = oracle(c)
            for k in tot:
                tot[k] += o[k]
        out[name] = {k: round(v, 2) for k, v in tot.items()}
        print(name, out[name], flush=True)
    return out


if __name__ == "__main__":
    res = run()
    if "--write" in sys.argv:
        json.dump(res, open(OUT, "w"), indent=1)
