"""Score 4.0: dollars recovered - staff-hours cost - provider abrasion, per seed (issue 125; spec docs/v4_v5_plan.md, parameters docs/score_40.md).

A new versioned module. The release 5 score (eval/dollar_reward.py) stays frozen and is only imported from (its note-sign and extrapolation helpers are not reused: score 4.0
prices every provider on the level-difference basis).

  recovered   Every provider an arm sends a demand to (called upcoding in its checked summaries), whatever its `role`. Value = the 90% lower bound of the overpayment
              extrapolated from that provider's RANDOM sample on the level-difference basis, NOT capped at the true overpayment (a payer has no answer key). Parameters:
                NETTING     sampled claims whose supported level is above the billed level count as negative overpayments (Program Integrity Manual ch. 8: "Sampling units that are
                            found to be underpayments ... are recorded as negative overpayments and shall be used in calculating the estimated overpayment").
                GATE        extrapolation applies only when the sample shows a sustained or high error rate (statute: Social Security Act 1893(f)(3); the manual gives no number,
                            so GATE_ERROR_RATE is an assumption); below it only the sampled claims' own (netted) overpayment is recovered.
                FULL_DENIAL a sampled claim denied in full for an uncurable documentation failure (off: no data 2.2 chart has one, see docs/score_40.md).
                BOUND       "two_sided_90" is the release 5 lower limit (t for a two-sided 90% interval, i.e. a one-sided 95% bound); "one_sided_90" is what the manual asks for.
  staff cost  activity counts x minutes x loaded hourly wage (BLS medians x 1.4) plus cash: $90 per request round and the arm's API dollars.
  abrasion    w(r) x (rounds x $43.84 + $2,000 if a demand was sent), r = the provider's TRUE net upcoding rate; w = 1 at r <= 0, falling linearly to 0 at r >= 15%.

Truth comes from the answer key's `justified_cpt_by_claim` against the billed claims, priced by the same function as the estimate, so "estimate minus truth" measures the estimate.
Never import this module from anything an arm or a model sees: it reads the answer key.

Usage: python eval/score_40.py RUN_ID CODE        (prints the components for one stored run)
"""
import csv
import json
import math
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dollar_reward as dr  # noqa: E402  (frozen; read only)
import eval61_recovery as rec  # noqa: E402
import pi_estimate as pe  # noqa: E402

VERSION = "4.0"
CODES = pe.CODES
LEVEL = pe.LEVEL

import recovery_40  # noqa: E402
from recovery_40 import (PARAMS, T_ONE_SIDED_90, claim_amounts, hourly, overpay_signed, params, recovery, staff_cost, t_value)  # noqa: E402,F401  (payer-visible pricing: src/recovery_40.py)

BANDS = [("below 0", -9, 0.0), ("0 to 5%", 0.0, 0.05), ("5 to 15%", 0.05, 0.15), ("15% and above", 0.15, 9)]


# ---- truth (answer key; eval only) -----------------------------------------------------------------------------------------------------------------------------------------
def provider_truth(claim_rows, justified, allowed):
    """True net upcoding rate and true overpayment dollars of one provider from its claims and the justified level of every claim."""
    amounts = claim_amounts(claim_rows)
    up = down = 0
    net = gross = 0.0
    for r in claim_rows:
        j = justified.get(r["claim_id"])
        if j is None:
            continue
        b = r["cpt"]
        up += LEVEL[b] > LEVEL[j]
        down += LEVEL[b] < LEVEL[j]
        v = overpay_signed(b, j, allowed, amounts.get(r["claim_id"]))
        net += v
        gross += max(v, 0.0)
    n = max(len(claim_rows), 1)
    return {"claims": len(claim_rows), "upcoded": up, "downcoded": down, "net_rate": (up - down) / n, "net_overpay": net, "gross_overpay": gross}


def abrasion_weight(r, p=None):
    floor = (p or PARAMS)["W_FLOOR"]
    return 1.0 if r <= 0 else max(0.0, 1.0 - r / floor)


# ---- one seed -----------------------------------------------------------------------------------------------------------------------------------------------------------------
def seed_result(called, listed_n, key, claims_by_provider, justified, random_ids_of, level_of, rounds_of, charts_of, api_usd, p=None, uncurable_of=None, truth=None):
    """Components of score 4.0 for one seed. called: provider ids sent a demand; key: answer-key providers (role); justified: {claim_id: justified cpt}."""
    p = p or PARAMS
    allowed = rec.allowed()
    truth = truth or {pid: provider_truth(rows, justified, allowed) for pid, rows in claims_by_provider.items()}
    rec_by = {pid: recovery(claims_by_provider.get(pid, []), random_ids_of(pid), level_of, p, (uncurable_of or (lambda _: ()))(pid)) for pid in called}
    recovered = sum(v["value"] for v in rec_by.values())
    non_up = [pid for pid in called if key[pid]["role"] != "upcoder"]
    cost, parts = staff_cost(listed_n, sum(rounds_of.values()), sum(charts_of.values()), len(called), api_usd, p)
    abrasion = sum(abrasion_weight(truth[pid]["net_rate"], p) * (rounds_of.get(pid, 0) * p["C_BURDEN"] + (p["C_DEMAND_ABRASION"] if pid in called else 0.0))
                   for pid in set(rounds_of) | set(called) if pid in truth)
    pos = {pid: max(t["net_overpay"], 0.0) for pid, t in truth.items()}
    over = {"up": [0, 0.0], "non": [0, 0.0]}                      # demands whose estimate is ABOVE the provider's true overpayment: count and dollars above (the uncapped cases)
    for pid in called:
        if pid in pos and rec_by[pid]["value"] > pos[pid] + 1e-9:
            o = over["up" if key[pid]["role"] == "upcoder" else "non"]
            o[0] += 1
            o[1] += rec_by[pid]["value"] - pos[pid]
    bands = {name: sum(1 for pid in called if lo <= truth[pid]["net_rate"] < hi) for name, lo, hi in BANDS}
    return {"recovered": recovered, "staff_cost": cost, "staff_parts": parts, "abrasion": abrasion, "score": recovered - cost - abrasion,
            "found": sum(key[pid]["role"] == "upcoder" for pid in called), "upcoders": sum(v["role"] == "upcoder" for v in key.values()), "demands": len(called),
            "honest_called": len(non_up), "recovered_from_non_upcoders": sum(rec_by[pid]["value"] for pid in non_up),
            "abrasion_from_non_upcoders": sum(abrasion_weight(truth[pid]["net_rate"], p) * (rounds_of.get(pid, 0) * p["C_BURDEN"] + p["C_DEMAND_ABRASION"]) for pid in non_up if pid in truth),
            "estimate_over_truth": sum(rec_by[pid]["value"] - max(truth[pid]["net_overpay"], 0.0) for pid in called if pid in truth),
            "true_overpay_called": sum(pos[pid] for pid in called if pid in pos), "true_overpay_all": sum(pos.values()),
            "over_n_up": over["up"][0], "over_d_up": over["up"][1], "over_n_non": over["non"][0], "over_d_non": over["non"][1],
            "bands": bands, "modes": dict(Counter(v["mode"] for v in rec_by.values())), "rounds": sum(rounds_of.values()), "charts": sum(charts_of.values())}


def per_provider(rid, code, p=None, inputs=None):
    """Score 4.0 split by provider for one stored run (issue 131): {provider_id: {value, staff, abrasion, net, called, role, rounds, charts, true_overpay, net_rate}} for every provider the run listed,
    asked or called. The triage of a listed provider is counted in its staff cost (every summary the run wrote); the run's API dollars are not split."""
    p = p or PARAMS
    claims, key, truth = context(code)
    i = inputs or run_inputs(rid, code)
    out = {}
    for pid in set(i["rounds"]) | i["called"]:
        called = pid in i["called"]
        rec_v = recovery(claims.get(pid, []), i["random"].get(pid, set()), i["level"], p)["value"] if called else 0.0
        rounds, charts = i["rounds"].get(pid, 0), i["charts"].get(pid, 0)
        staff = staff_cost(0, rounds, charts, 1 if called else 0, 0.0, p)[0]
        r = truth[pid]["net_rate"]
        abr = abrasion_weight(r, p) * (rounds * p["C_BURDEN"] + (p["C_DEMAND_ABRASION"] if called else 0.0))
        out[pid] = {"value": rec_v, "staff": staff, "abrasion": abr, "net": rec_v - staff - abr, "called": called, "role": key["providers"][pid]["role"], "rounds": rounds, "charts": charts,
                    "true_overpay": max(truth[pid]["net_overpay"], 0.0), "net_rate": r, "habit": key["providers"][pid].get("habit")}
    return out


def add(parts):
    """Sum components over seeds."""
    out = {}
    for k in ("recovered", "staff_cost", "abrasion", "score", "found", "upcoders", "demands", "honest_called", "recovered_from_non_upcoders", "abrasion_from_non_upcoders",
              "estimate_over_truth", "true_overpay_called", "true_overpay_all", "rounds", "charts", "over_n_up", "over_d_up", "over_n_non", "over_d_non"):
        out[k] = sum(x[k] for x in parts)
    out["bands"] = {b: sum(x["bands"][b] for x in parts) for b, _, _ in BANDS}
    return out


def dollar_weighted_recall(c):
    return c["true_overpay_called"] / c["true_overpay_all"] if c["true_overpay_all"] else 0.0


# ---- stored runs ------------------------------------------------------------------------------------------------------------------------------------------------------------
def load_key(code):
    return json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))


_CTX = {}


def context(code):
    """Claims by provider, the answer key and each provider's truth for one dataset (cached: truth does not depend on the arm or the parameters)."""
    if code not in _CTX:
        _CTX.clear()
        data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
        claims = {}
        for r in csv.DictReader(open(os.path.join(data, "view", "claims.csv"))):
            claims.setdefault(r["provider_id"], []).append(r)
        k = load_key(code)
        allowed = rec.allowed()
        _CTX[code] = (claims, k, {pid: provider_truth(rows, k["justified_cpt_by_claim"], allowed) for pid, rows in claims.items()})
    return _CTX[code]


def run_inputs(rid, code):
    """What a stored run folder holds that scoring needs: demands, listed count, random ids, supported levels, rounds, distinct charts, API dollars."""
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    docs = list(csv.DictReader(open(os.path.join(data, f"view_{rid}", "documentation.csv"))))
    summaries = [json.loads(x) for x in open(os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")) if x.strip()]
    called = {x["provider_id"] for x in summaries if x["summary"]["leaning"] == "pattern_consistent_with_upcoding"}
    rounds, seen = Counter(), {}
    for line in open(os.path.join(ROOT, "experiments", rid, "office_transcript.jsonl")):
        e = json.loads(line)
        if e.get("action") in ("send_request", "follow_up", "audit_trail") and "error" not in e:
            rounds[e["provider_id"]] += 1
            seen.setdefault(e["provider_id"], set()).update(e.get("usable_claim_ids", []))      # a follow-up can list the same chart again
    import run_release2 as r2
    return {"called": called, "listed": len(summaries), "random": rec.random_ids(rid), "level": dr.level_of_rows(docs), "rounds": dict(rounds),
            "charts": {pid: len(ids) for pid, ids in seen.items()}, "api": r2.cost(rid)}


def from_run(rid, code, p=None, inputs=None):
    """Score 4.0 components for a stored run folder (workflow or agent) on its data-2.2 answer key. Definitions (docs/score_40.md):
    demand = called upcoding in case_summaries_checked.jsonl; listed = providers with a checked summary; rounds from the office transcript, charts = distinct charts received;
    API dollars = the run's recorded model spend (writer, judge, agent)."""
    claims, k, truth = context(code)
    i = inputs or run_inputs(rid, code)
    return seed_result(i["called"], i["listed"], k["providers"], claims, k["justified_cpt_by_claim"], lambda pid: i["random"].get(pid, set()), i["level"], i["rounds"], i["charts"], i["api"],
                       p or PARAMS, truth=truth)


if __name__ == "__main__":
    c = from_run(sys.argv[1], sys.argv[2])
    print(json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in c.items()}, indent=1))
