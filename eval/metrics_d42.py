"""Evaluation on data 4.2 without a planted role (issue 173; docs/data_v4_2.md, section d). EVALUATION ONLY: reads the answer key through eval/d42_truth.py.

Dollar-weighted measures of what an arm did (recovery, staff cost and abrasion as in score 4.0, true overpayment pursued over available, the share of pursued providers and of recovered
dollars that were justified at a stated threshold, abrasion on the rate basis of score 4.0 and on a dollar basis), graded ranking metrics for screens (NDCG on true overpayment) and the oracle
with triage. Any binary view ("justified") is derived here from the answer key's dollars at a threshold m x the cost of pursuing a provider and never reaches a generator or an arm.

Usage: python eval/metrics_d42.py RUN_ID CODE        (prints the metrics of one stored workflow run)
"""
import csv
import json
import math
import os
import random
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import d42_truth as dt  # noqa: E402
import records as rcd  # noqa: E402
import recovery_40 as r4  # noqa: E402
import score_40 as s4  # noqa: E402

P = r4.PARAMS
FWA = ("not_rendered", "impossible_days", "unbundling")


def w_dollar(t, threshold):
    """Abrasion weight on a dollar basis: 1 when the provider's true overpayment is zero or less, falling linearly to 0 at the threshold (the cost of pursuing it)."""
    if threshold <= 0:
        return 0.0 if t > 0 else 1.0
    return 1.0 if t <= 0 else max(0.0, 1.0 - t / threshold)


def listed_ids(rid):
    return {json.loads(x)["provider_id"] for x in open(os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")) if x.strip()}


def run_metrics(rid, code, ms=dt.M_SWEEP, inputs=None):
    """Everything for one stored workflow run on one data 4.2 dataset. Keys: score components (score 4.0 as is), the dollar-basis abrasion and score, available and pursued dollars, and a table by threshold."""
    comp, i = dt.seed_result(rid, code, m=1.0, inputs=inputs)
    claims, key, truth = dt.context(code)
    cost = dt.pursuit_cost()
    price = dt.abrasion_price()
    T = dt.totals(key)
    prov = key["providers"]
    A = sum(T.values())
    lvl = {pid: max(v["true_overpay_level_net"], 0.0) for pid, v in prov.items()}
    fwa = {pid: sum(v["true_overpay_fwa"].values()) for pid, v in prov.items()}
    called, asked, listed = i["called"], set(i["rounds"]), listed_ids(rid)
    rec_by = {pid: r4.recovery(claims.get(pid, []), i["random"].get(pid, set()), i["level"], P)["value"] for pid in called}
    abr_dollar = sum(w_dollar(T[pid], cost) * (i["rounds"].get(pid, 0) * P["C_BURDEN"] + (P["C_DEMAND_ABRASION"] if pid in called else 0.0)) for pid in set(i["rounds"]) | called if pid in T)
    out = {"rid": rid, "code": code, "pursuit_cost": cost,
           "recovered": comp["recovered"], "staff_cost": comp["staff_cost"], "abrasion_s40": comp["abrasion"], "abrasion_dollar": abr_dollar,
           "score_s40": comp["score"], "score_dollar": comp["recovered"] - comp["staff_cost"] - abr_dollar,
           "demands": len(called), "asked": len(asked), "listed": len(listed), "rounds": comp["rounds"], "charts": comp["charts"],
           "available": A, "available_level": sum(lvl.values()), "available_fwa": sum(fwa.values()),
           "available_fwa_by_kind": {k: sum(v["true_overpay_fwa"][k] for v in prov.values()) for k in FWA},
           "pursued": sum(T[p] for p in called), "pursued_level": sum(lvl[p] for p in called), "pursued_fwa": sum(fwa[p] for p in called),
           "asked_dollars": sum(T[p] for p in asked if p in T), "listed_dollars": sum(T[p] for p in listed if p in T),
           "fwa_providers": sum(1 for v in prov.values() if any(v["intent"][k] for k in ("not_rendered", "impossible_days", "unbundling"))),
           "fwa_providers_pursued": sum(1 for p in called if any(prov[p]["intent"][k] for k in ("not_rendered", "impossible_days", "unbundling"))),
           "by_m": {}}
    for m in ms:
        J = dt.justified(key, m, cost)
        rj = sum(v for p, v in rec_by.items() if p in J)
        out["by_m"][str(m)] = {"justified": len(J), "justified_dollars": sum(T[p] for p in J), "called_justified": len(called & J), "called_not_justified": len(called - J),
                               "precision": len(called & J) / len(called) if called else None, "recall": len(called & J) / len(J) if J else None,
                               "recovered_from_justified": rj, "recovered_from_not_justified": sum(rec_by.values()) - rj,
                               "share_recovered_justified": rj / sum(rec_by.values()) if sum(rec_by.values()) > 0 else None}
    return out


# ---- graded ranking metrics for screens ---------------------------------------------------------------------------------------------------------------------------------------
def ndcg_at_k(order, gain, k):
    """NDCG at k with linear gain: order is a list of provider ids, best first; gain {provider_id: true overpayment}."""
    dcg = sum(gain.get(p, 0.0) / math.log2(i + 2) for i, p in enumerate(order[:k]))
    ideal = sorted(gain.values(), reverse=True)
    idcg = sum(g / math.log2(i + 2) for i, g in enumerate(ideal[:k]))
    return dcg / idcg if idcg > 0 else 0.0


def dollar_share_at_k(order, gain, k):
    tot = sum(max(g, 0.0) for g in gain.values())
    return sum(max(gain.get(p, 0.0), 0.0) for p in order[:k]) / tot if tot > 0 else 0.0


def screen_ranking(code, screen_file):
    """The ranked provider ids of an experiments/<code>/flagged_*.csv file (rank order)."""
    rows = list(csv.DictReader(open(os.path.join(ROOT, "experiments", code, screen_file))))
    return [r["provider_id"] for r in sorted(rows, key=lambda r: int(r["rank"]))] if "rank" in rows[0] else [r["provider_id"] for r in rows]


def screen_metrics(code, screen_file, ks=(10, 22, 50), kinds=("total", "level", "fwa")):
    claims, key, truth = dt.context(code)
    prov = key["providers"]
    gains = {"total": dt.totals(key), "level": {p: max(v["true_overpay_level_net"], 0.0) for p, v in prov.items()},
             "fwa": {p: sum(v["true_overpay_fwa"].values()) for p, v in prov.items()}}
    order = screen_ranking(code, screen_file)
    return {kind: {f"ndcg@{k}": ndcg_at_k(order, gains[kind], k) for k in ks} | {f"share@{k}": dollar_share_at_k(order, gains[kind], k) for k in ks} for kind in kinds}


# ---- the oracle with triage ---------------------------------------------------------------------------------------------------------------------------------------------------------------
NS = (30, 60, 90, 150)


def oracle(code, seed=11, draws=6, p=None):
    """The best conceivable score on one dataset under score 4.0's prices, with triage (eval/ceiling_benchmarks_41.py, now with the abrasion term it lacked).
    For each provider: the expected 90% lower bound of a random chart sample of n charts (a phantom claim returns no chart), minus the cost of the charts received, two rounds, a demand and triage, minus
    abrasion. It pursues a provider (at its best n) only when that is positive. Two abrasion bases: score 4.0's (the provider's level net rate on rendered claims) and the dollar basis.
    Recovery from a chart sample reaches the level dollars only, so the FWA dollars are available but not reachable by this oracle (by construction)."""
    p = p or P
    claims, key, truth = dt.context(code)
    fraud = key["fraud_claims"]
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    level = {}
    for r in csv.DictReader(open(os.path.join(data, "records", "records_universe.csv"))):
        mins = r["documented_minutes"] if r["documented_minutes"] != "" else None
        level[r["claim_id"]] = max(rcd.mdm_level(int(r["problems_level"]), int(r["data_level"]), int(r["risk_level"])), rcd.level_from_minutes(mins))
    ch, rd, dm, tr = dt.unit_costs(p)
    T = dt.totals(key)
    cost = dt.pursuit_cost()
    price = dt.abrasion_price(p)
    rng = random.Random(seed)
    res = {"s40": {"score": 0.0, "pursued": 0, "recovered": 0.0, "cost": 0.0, "abrasion": 0.0}, "dollar": {"score": 0.0, "pursued": 0, "recovered": 0.0, "cost": 0.0, "abrasion": 0.0}}
    for pid, cl in claims.items():
        ids = [r["claim_id"] for r in cl]
        if len(ids) < 50:
            continue
        best = {}
        for n in NS:
            vals, got = [], []
            for _ in range(draws):
                sample = rng.sample(ids, min(n, len(ids)))
                rendered = {c for c in sample if c not in fraud}
                vals.append(r4.recovery(cl, rendered, level, p)["value"])
                got.append(len(rendered))
            best[n] = (st.mean(vals), st.mean(got))
        for basis, w in (("s40", s4.abrasion_weight(truth[pid]["net_rate"], p)), ("dollar", w_dollar(T[pid], cost))):
            top = None
            for n, (lb, got) in best.items():
                c = got * ch + 2 * rd + dm + tr
                v = lb - c - w * price
                if top is None or v > top[0]:
                    top = (v, lb, c, w * price)
            if top[0] > 0:
                r = res[basis]
                r["score"] += top[0]
                r["pursued"] += 1
                r["recovered"] += top[1]
                r["cost"] += top[2]
                r["abrasion"] += top[3]
    return res


if __name__ == "__main__":
    print(json.dumps(run_metrics(sys.argv[1], sys.argv[2]), indent=1, default=float))
