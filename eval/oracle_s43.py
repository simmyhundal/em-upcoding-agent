"""The oracle under score 4.3 (src/recovery_43.py; values signed off 2026-10-27): the best conceivable score on one dataset, with triage, from the answer key (evaluation only). An UPPER BOUND, not an arm and not a target.

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
import recovery_43 as r43  # noqa: E402
import records as rcd  # noqa: E402
import score_40 as s4  # noqa: E402

LEVEL_NS = (30, 60, 90, 150)
STRATUM_NS = (30, 60, 90)
FRAUD = ("not_rendered", "impossible_days")
OUT = os.path.join(ROOT, "experiments", "oracle_s43.json")


def oracle(code, seed=11, draws=20, over=None):
    """Perfect knowledge of the answer key, inside score 4.2's recovery rules. Per provider the oracle may use two recovery channels and pays for what it uses:
      level channel (L): a random sample of n of the provider's claims (n = 30, 60, 90, 150 or all of them); sampled claims for visits that never happened return no record and count at their paid amount;
      stratum channel (S): a stratified sample drawn within the provider's claims for visits that never happened (the oracle knows which they are); n = 30, 60, 90 or all of them.
    A pursuit is one of L, S or L plus S (on the claims outside the stratum); it pays the charts received, the request rounds (2 for L, 1 for S, 2 for both), one demand, one triage, and abrasion
    w x (2 rounds x $43.84 + $2,000) with w from the provider's TOTAL true rate. It pursues a provider (honest or not) only when the value is positive, at its best n. Values are expected 90% lower bounds
    averaged over `draws` random samples (a census has no sampling error). It assumes every office answers and the screen is perfect: an upper bound, not an arm. Returns totals and a breakdown."""
    p = r43.params43(**(over or {}))
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
    rnd, tri = r4.staff_cost(0, 1, 0, 0, 0, p)[0], r4.staff_cost(1, 0, 0, 0, 0, p)[0]
    appeal_cost = p["P_APPEAL"] * p["APPEAL_HANDLING_HOURS"] * r4.hourly("coder", p)
    dem = r4.staff_cost(0, 0, 0, 1, 0, p)[0] + appeal_cost           # an ordinary demand: its work and its expected appeal handling
    ref = p["REFERRAL_COST"] + appeal_cost                          # a referral replaces a demand's work
    price = 2 * p["C_BURDEN"] + p["C_DEMAND_ABRASION"]
    price1 = p["C_BURDEN"] + p["C_DEMAND_ABRASION"]           # one request round (the stratum channel alone)
    rng = random.Random(seed)
    tot = {"_ids": [], "score": 0.0, "recovered": 0.0, "recovered_level_only": 0.0, "recovered_impossible_day_providers": 0.0, "recovered_other_phantom_providers": 0.0, "staff": 0.0, "abrasion": 0.0, "pursued": 0, "level_only": 0, "stratum_only": 0, "both": 0, "pursued_with_rate_below_5pct": 0}
    for pid, cl in claims.items():
        ids = [r["claim_id"] for r in cl]
        rendered_rows = [r for r in cl if r["claim_id"] not in fraud]
        t = s4.provider_truth(rendered_rows, key["justified_cpt_by_claim"], allowed)
        ph = sum(1 for r in cl if r["claim_id"] in fraud)
        rate = (t["upcoded"] - t["downcoded"] + ph) / max(t["claims"] + ph, 1)
        w = s4.abrasion_weight(rate, p)
        sids = [c for c in ids if c in fraud]
        stratum = [r for r in cl if r["claim_id"] in set(sids)]
        outside = [r for r in cl if r["claim_id"] not in set(sids)]
        oids = [r["claim_id"] for r in outside]

        fraud_case = bool(sids)                                  # a provider with claims for visits that never happened is pursued as a fraud referral, whatever sample is used

        def level_opt(rows, pool_ids, referral=False):
            """best (lower bound, charts received) over n for the level channel on `rows`"""
            best = None
            for n in LEVEL_NS + (len(pool_ids),):
                n = min(n, len(pool_ids))
                if n <= 0:
                    continue
                vals, got = [], []
                for _ in range(1 if n == len(pool_ids) else draws):
                    sample = pool_ids if n == len(pool_ids) else rng.sample(pool_ids, n)
                    nr = {c for c in sample if c in fraud}
                    vals.append(r43.recovery(rows, set(sample), level, p, no_record=nr)["value"])
                    got.append(len(sample) - len(nr))
                lb, g = st.mean(vals), st.mean(got)
                lb = r43.collected(lb, p, referral=referral)
                cand = (lb - g * chart, lb, g)
                if best is None or cand[0] > best[0]:
                    best = cand
            return best
        L = level_opt(cl, ids, referral=fraud_case)                                               # (lb - chart cost, lb, charts)
        opts = []
        if L:
            opts.append((L[0] - 2 * rnd - (ref if fraud_case else dem) - tri - w * price, L[1], "L"))
        S = None
        if sids:
            for n in STRATUM_NS + (len(sids),):
                n = min(n, len(sids))
                vals = []
                for _ in range(1 if n == len(sids) else draws):
                    sample = sids if n == len(sids) else rng.sample(sids, n)
                    vals.append(r43.recovery_stratified(stratum, sample, level, p, no_record=set(sample))["value"])
                lb = r43.collected(st.mean(vals), p, referral=True)            # every sampled claim is a visit that never happened: no chart is received; a referral is collected at its own rate
                if S is None or lb > S[1]:
                    S = (lb, lb, 0)
            opts.append((S[1] - rnd - ref - tri - w * price1, S[1], "S"))
            LO = level_opt(outside, oids) if oids else None
            if LO:
                lo = LO[1] * p["COLLECTION_REFERRAL"] / p["COLLECTION_DEMAND"]                # the level part of a referral is collected at the referral rate
                opts.append((S[1] + lo - LO[2] * chart - 2 * rnd - ref - tri - w * price, S[1] + lo, "LS"))
        if not opts:
            continue
        v, lb, kind = max(opts, key=lambda o: o[0])
        if v > 0:
            tot["_ids"].append(pid)
            tot["score"] += v; tot["recovered"] += lb; tot["pursued"] += 1
            ab = w * (price1 if kind == "S" else price)
            tot["abrasion"] += ab
            tot["staff"] += lb - v - ab
            tot[{"L": "level_only", "S": "stratum_only", "LS": "both"}[kind]] += 1
            imp = any(fraud.get(c) == "impossible_days" for c in sids)
            tot["recovered_level_only" if kind == "L" else "recovered_impossible_day_providers" if imp else "recovered_other_phantom_providers"] += lb
            tot["pursued_with_rate_below_5pct"] += int(rate < 0.05)
    return tot


def run():
    out = {}
    for name, codes in (("4.0, test", [f"f4_{5555 + 101 * j}" for j in range(10)]), ("4.2, test", [f"d42_{s}" for s in pool.TEST])):
        tot, per = {}, {}
        for c in codes:
            o = oracle(c)
            per[c] = round(o["score"], 2)
            for k, v in o.items():
                if not k.startswith("_"):
                    tot[k] = tot.get(k, 0) + v
        out[name] = {k: round(v, 2) for k, v in tot.items()} | {"per_seed": per}
        print(name, {k: v for k, v in out[name].items() if k != "per_seed"}, flush=True)
    return out


if __name__ == "__main__":
    res = run()
    if "--write" in sys.argv:
        json.dump(res, open(OUT, "w"), indent=1)
