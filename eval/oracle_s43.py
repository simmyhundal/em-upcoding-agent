"""The oracle under score 4.3 (src/recovery_43.py; values signed off 2026-10-27): the best conceivable score on one dataset, with triage. An UPPER BOUND, not an arm and not a target.
Revised 2026-10-27 after a second review (the first draft is kept in experiments/oracle_s43_v1_first_draft.json).

Per provider the oracle knows which claims are for visits that never happened and the true supported level, but it is held to what a payer can do under the score's rules:
  * Chart reads carry the reviewer's disagreement (records.CODER_NOISE, 15% of reads off by one level), drawn afresh for every sampled chart; `coder_noise=0` gives the separately labelled "perfect reading" ceiling.
  * Level option: a random sample of n charts (n = 30, 60, 90, 150 or all); a sampled claim for a visit that never happened returns no record and counts at its paid amount; a draw whose sample contains one is
    collected as a fraud referral, otherwise as an ordinary demand.
  * Lane option (providers with a day of 30 or more visits): a random sample of claims on those days only (a stratum a payer can define from claims, as the lane does); same no-record rule; always a referral.
  * It commits to a request before seeing the sample (charts, rounds, triage and the abrasion of the requests are sunk) but drops the demand when the sample's value does not cover its cost, as arms do.
  * Choice and report use separate draws: n and the option are chosen on `draws` selection draws, the value reported is the mean over `report_draws` independent draws of the chosen policy; a provider is pursued only when that mean is positive.
It assumes every office answers and the screen is perfect, so it is an expected value over samples: a single-seed arm can exceed it by luck; compare totals.
Usage: python eval/oracle_s43.py [--write]   -> experiments/oracle_s43.json
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
import recovery_43 as r43  # noqa: E402
import records as rcd  # noqa: E402
import score_40 as s4  # noqa: E402

LEVEL_NS = (30, 60, 90, 150)
STRATUM_NS = (30, 60, 90)
FRAUD = ("not_rendered", "impossible_days")
OUT = os.path.join(ROOT, "experiments", "oracle_s43.json")


def oracle(code, seed=11, draws=20, over=None, report_draws=100, coder_noise=rcd.CODER_NOISE):
    p = r43.params43(**(over or {}))
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))
    fraud = {c: k for c, k in key.get("fraud_claims", {}).items() if k in FRAUD}
    claims = {}
    for r in csv.DictReader(open(os.path.join(data, "view", "claims.csv"))):
        claims.setdefault(r["provider_id"], []).append(r)
    allowed = rec.allowed()
    mdm, tlev = {}, {}
    for r in csv.DictReader(open(os.path.join(data, "records", "records_universe.csv"))):
        mins = r["documented_minutes"] if r["documented_minutes"] != "" else None
        mdm[r["claim_id"]] = rcd.mdm_level(int(r["problems_level"]), int(r["data_level"]), int(r["risk_level"]))
        tlev[r["claim_id"]] = rcd.level_from_minutes(mins)
    chart = r4.staff_cost(0, 0, 1, 0, 0, p)[0]
    rnd, tri = r4.staff_cost(0, 1, 0, 0, 0, p)[0], r4.staff_cost(1, 0, 0, 0, 0, p)[0]
    appeal_cost = p["P_APPEAL"] * p["APPEAL_HANDLING_HOURS"] * r4.hourly("coder", p)
    dem = r4.staff_cost(0, 0, 0, 1, 0, p)[0] + appeal_cost           # an ordinary demand: its work and its expected appeal handling
    ref = p["REFERRAL_COST"] + appeal_cost                          # a referral replaces a demand's work
    rng = random.Random(seed)
    rng_report = random.Random(seed + 1000)

    def read(sample, rg):
        """The reviewer's level for each sampled chart: the MDM level with coder disagreement, or the time level if higher"""
        d = {}
        for c in sample:
            if c not in mdm:
                continue
            m = mdm[c]
            if coder_noise and rg.random() < coder_noise:
                m = max(0, min(4, m + rg.choice([-1, 1])))
            d[c] = max(m, tlev[c])
        return d

    tot = {"_ids": [], "score": 0.0, "recovered": 0.0, "recovered_level_only": 0.0, "recovered_impossible_day_providers": 0.0, "recovered_other_phantom_providers": 0.0, "staff": 0.0, "abrasion": 0.0, "pursued": 0, "level_only": 0, "stratum_only": 0, "both": 0, "pursued_with_rate_below_5pct": 0}
    for pid, cl in claims.items():
        ids = [r["claim_id"] for r in cl]
        rendered_rows = [r for r in cl if r["claim_id"] not in fraud]
        t = s4.provider_truth(rendered_rows, key["justified_cpt_by_claim"], allowed)
        ph_all = sum(1 for r in cl if r["claim_id"] in fraud)
        rate = (t["upcoded"] - t["downcoded"] + ph_all) / max(t["claims"] + ph_all, 1)
        w = s4.abrasion_weight(rate, p)
        CB, CD = p["C_BURDEN"], p["C_DEMAND_ABRASION"]
        hot = fwa_lane.flag({pid: cl}, max_flagged=1)
        hot_ids = fwa_lane.stratum_ids(cl, hot[0][2]) if hot else []
        hot_rows = [r for r in cl if r["claim_id"] in set(hot_ids)]

        def one(kind, n, rg):
            """one draw: (sunk cost, value of the demand if made); the demand is dropped when its value is negative"""
            if kind == "L":
                sample = ids if n == len(ids) else rg.sample(ids, n)
                nr = {c for c in sample if c in fraud}
                lb = r43.recovery(cl, set(sample), read(sample, rg), p, no_record=nr)["value"]
                hit = bool(nr)
                rounds = 2
            else:
                sample = hot_ids if n == len(hot_ids) else rg.sample(hot_ids, n)
                nr = {c for c in sample if c in fraud}
                lb = r43.recovery_stratified(hot_rows, sample, read(sample, rg), p, no_record=nr)["value"]
                hit = True
                rounds = 1
            got = len(sample) - len(nr)
            sunk = got * chart + rounds * rnd + tri + w * rounds * CB
            coll = r43.collected(lb, p, referral=hit)
            dcost = ref if hit else dem
            opt = coll - dcost - w * CD
            return sunk, opt, rounds, coll, dcost

        def mean_value(kind, n, k, rg):
            vals, rs = [], []
            for _ in range(1 if n == (len(ids) if kind == "L" else len(hot_ids)) and not coder_noise else k):
                sunk, opt, rounds, coll, dcost = one(kind, n, rg)
                vals.append(max(opt, 0.0) - sunk)
                rs.append((sunk, opt, rounds, coll, dcost))
            return st.mean(vals), rs

        cands = []
        for n in LEVEL_NS + (len(ids),):
            n = min(n, len(ids))
            if n > 0:
                cands.append(("L", n))
        if hot_ids:
            for n in STRATUM_NS + (len(hot_ids),):
                n = min(n, len(hot_ids))
                cands.append(("S", n))
        best = {}
        for kind, n in cands:                                       # choose on the selection draws
            v, _ = mean_value(kind, n, draws, rng)
            if kind not in best or v > best[kind][0]:
                best[kind] = (v, n)
        pick = max(best.items(), key=lambda kv: kv[1][0])
        kind, (_, n) = pick
        v, rs = mean_value(kind, n, report_draws, rng_report)         # report on independent draws
        if v <= 0:
            continue
        made = [x for x in rs if x[1] > 0]                       # draws in which the demand was made
        rec_total = sum(x[3] for x in made) / len(rs)
        rounds = rs[0][2]
        ab = w * rounds * CB + w * CD * len(made) / len(rs)
        stf = st.mean(x[0] for x in rs) - w * rounds * CB + sum(x[4] for x in made) / len(rs)
        tot["_ids"].append(pid)
        tot["score"] += v; tot["recovered"] += rec_total; tot["pursued"] += 1
        tot["abrasion"] += ab
        tot["staff"] += stf
        tot["level_only" if kind == "L" else "stratum_only"] += 1
        imp = any(fraud.get(c) == "impossible_days" for c in hot_ids)
        tot["recovered_level_only" if kind == "L" else "recovered_impossible_day_providers" if imp else "recovered_other_phantom_providers"] += rec_total
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
