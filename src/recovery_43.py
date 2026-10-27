"""Score 4.3 pricing (docs/score_43.md; issue 200; signed off by Simmy 2026-10-27): score 4.2 plus a referral class, a collection rate, an appeal reduction, a dollar-based error gate and a payer cost of handling appeals.
Every value is the one in docs/score_43_proposal.md with its status (sourced or assumption). Payer-visible, no answer key.

Changes from score 4.2 (frozen, unchanged):
  GATE_UNIT "dollar": extrapolate only when the sample's NET DOLLAR error rate (net overpayment over paid dollars of the reviewed claims) is at least GATE_DOLLAR_RATE; "claim" is score 4.2's share of claims overpaid.
  A demand's value is what the payer expects to COLLECT: the lower bound times (1 - APPEAL_REDUCTION) times the collection rate (appeals first, then collection on what remains); a REFERRAL's rate is already net of appeals, so no separate reduction applies.
  A volume-lane provider is a REFERRAL: its cost is REFERRAL_COST in place of the demand's staff cost, its collection rate is COLLECTION_REFERRAL.
  The payer pays APPEAL_HANDLING_HOURS of coder time for the share P_APPEAL of demands that are appealed (expected cost).
"""
import math

import recovery_40 as r4
import recovery_42 as r42

DEFAULTS = {"GATE_UNIT": "dollar", "GATE_DOLLAR_RATE": 0.05, "APPEAL_REDUCTION": 0.15, "COLLECTION_DEMAND": 0.68, "COLLECTION_REFERRAL": 0.25, "REFERRAL_COST": 4000.0,
            "APPEAL_HANDLING_HOURS": 3.0, "P_APPEAL": 0.17}


def params43(**over):
    """Score 4.3's parameter dict: score 4.2's with the proposal's defaults and any overrides."""
    base = r42.params42()
    base.update(DEFAULTS)
    base.update(over)
    return base


def _paid_of(claim_rows, ids):
    amounts = r4.claim_amounts(claim_rows)
    return sum(amounts[c][1] for c in ids if c in amounts)


def _estimate43(vals_by_stratum, frame_sizes, flat, paid_sum, p):
    if p["GATE_UNIT"] == "dollar":
        err = (sum(flat) / paid_sum) if paid_sum else 0.0
        gated = err < p["GATE_DOLLAR_RATE"]
    else:
        err = sum(1 for v in flat if v > 0) / len(flat)
        gated = p["GATE"] and err < p["GATE_ERROR_RATE"]
    if gated:
        s = sum(flat)
        return {"value": max(s, 0.0), "point": s, "mode": "sampled claims only", "sample_error_rate": err, "reviewed": len(flat)}
    total = var = 0.0
    n_all = k = 0
    for key, N in frame_sizes.items():
        v = vals_by_stratum.get(key, [])
        n = len(v)
        if not n:
            continue
        mean = sum(v) / n
        s2 = (sum((x - mean) ** 2 for x in v) / (n - 1)) if n > 1 else 0.0
        total += N * mean
        var += N * N * (1 - n / N) * s2 / n
        n_all += n
        k += 1
    half = r4.t_value(max(n_all - k, 1), p["BOUND"]) * math.sqrt(var)
    return {"value": max(0.0, total - half), "point": total, "mode": "extrapolated", "sample_error_rate": err, "reviewed": len(flat)}


def recovery(claim_rows, random_ids, level_of, p, no_record=frozenset()):
    """Level recovery before appeals and collection (the lower bound), with the dollar-based gate."""
    from collections import Counter
    by = {r["claim_id"]: r for r in claim_rows}
    ids = [c for c in sorted(random_ids) if c in by]
    fees, amounts = r4.allowed(), r4.claim_amounts(claim_rows)
    vals, flat, nr = r42._sample_values(by, ids, level_of, no_record, p, fees, amounts)
    if not flat:
        return {"value": 0.0, "point": 0.0, "mode": "none", "sample_error_rate": 0.0, "reviewed": 0, "no_record": 0}
    used = [c for c in ids if c in no_record or c in level_of]
    out = _estimate43(vals, dict(Counter(r["cpt"] for r in claim_rows)), flat, _paid_of(claim_rows, used), p)
    out["no_record"] = nr
    return out


def recovery_stratified(stratum_rows, sample_ids, level_of, p, no_record=frozenset()):
    by = {r["claim_id"]: r for r in stratum_rows}
    ids = [c for c in sorted(sample_ids) if c in by]
    fees, amounts = r4.allowed(), r4.claim_amounts(stratum_rows)
    vals, flat, nr = r42._sample_values(by, ids, level_of, no_record, p, fees, amounts)
    if not flat:
        return {"value": 0.0, "point": 0.0, "mode": "none", "sample_error_rate": 0.0, "reviewed": 0, "no_record": 0}
    used = [c for c in ids if c in no_record or c in level_of]
    out = _estimate43({"stratum": [v for vs in vals.values() for v in vs]}, {"stratum": len(stratum_rows)}, flat, _paid_of(stratum_rows, used), p)
    out["no_record"] = nr
    return out


def collected(value, p, referral=False):
    """What the payer expects to collect from a lower bound: appeals first, then collection on what remains."""
    if referral:                                   # the sourced referral rates (16% to 24%) already count appealed and overturned dollars as uncollected (docs/score_43_sources_addendum.md)
        return value * p["COLLECTION_REFERRAL"]
    return value * (1 - p["APPEAL_REDUCTION"]) * p["COLLECTION_DEMAND"]


def staff_cost(listed, rounds, charts, demands, referrals, api_usd, p):
    """(total, parts): score 4.2's staff cost for `demands` ordinary demands, REFERRAL_COST for each referral in place of a demand's work, and the expected cost of handling appeals."""
    base, parts = r4.staff_cost(listed, rounds, charts, demands, api_usd, p)
    parts = dict(parts)
    parts["referrals"] = referrals * p["REFERRAL_COST"]
    parts["appeal handling"] = (demands + referrals) * p["P_APPEAL"] * p["APPEAL_HANDLING_HOURS"] * r4.hourly("coder", p)
    return base + parts["referrals"] + parts["appeal handling"], parts
