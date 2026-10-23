"""Score 4.2 (S4.2) pricing (docs/score_42.md; payer-visible, no answer key). S4.0 and S4.1 stay frozen; this module wraps their parameters and adds two things:

1. The commercial profile is the default (records copy fee $0, as S4.1's `commercial_no_copy`).
2. A sampled claim for which the office reports NO_RECORD (it has no record of the visit) is treated as overpaid at its full paid amount, in the same estimate (netting, error gate, 90% lower bound).
   Source: Program Integrity Manual ch. 8, section 8.4.5: sampling units whose records were not provided are treated as overpayments (the manual's wording is the same line S4.0 left as "not modeled").
   Only an office that answers and reports NO_RECORD counts; silence (no response) is not evidence and counts for nothing.

`recovery_stratified` prices a random sample drawn WITHIN a stratum of the provider's claims (for example the claims dated on a day the provider billed an impossible number of visits): stratified random
sampling supports extrapolation to that stratum only, and the estimate is the stratum total, not the provider's.
"""
import math

import recovery_40 as r4
import recovery_41 as r41

PROFILE = "commercial_no_copy"


def params42(**over):
    """Score 4.2's parameter dict: score 4.0's with the commercial profile (copy fee $0) and any overrides."""
    return r41.params41(PROFILE, **over)


def _estimate(vals_by_stratum, frame_sizes, flat, p):
    err = sum(1 for v in flat if v > 0) / len(flat)
    if p["GATE"] and err < p["GATE_ERROR_RATE"]:
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


def _sample_values(by, ids, level_of, no_record, p, fees, amounts):
    """(values by billed code, flat values, number of no-record claims) for the sampled claims that were reviewed or reported NO_RECORD."""
    vals, flat, nr = {}, [], 0
    for c in ids:
        if c not in by:
            continue
        b = by[c]["cpt"]
        if c in no_record and c in amounts:
            v = amounts[c][1]                                   # records not provided: the whole paid amount is an overpayment (PIM 8.4.5)
            nr += 1
        elif c in level_of:
            v = r4.overpay_signed(b, r4.CODES[level_of[c]], fees, amounts.get(c))
            if not p["NETTING"]:
                v = max(v, 0.0)
        else:
            continue
        vals.setdefault(b, []).append(v)
        flat.append(v)
    return vals, flat, nr


def recovery(claim_rows, random_ids, level_of, p, no_record=frozenset()):
    """S4.2's recovery from a provider's random sample: S4.0's estimate with NO_RECORD claims counted at their paid amount. Returns the S4.0 dict plus `no_record` (how many sampled claims)."""
    by = {r["claim_id"]: r for r in claim_rows}
    ids = [c for c in sorted(random_ids) if c in by]
    fees, amounts = r4.allowed(), r4.claim_amounts(claim_rows)
    vals, flat, nr = _sample_values(by, ids, level_of, no_record, p, fees, amounts)
    if not flat:
        return {"value": 0.0, "point": 0.0, "mode": "none", "sample_error_rate": 0.0, "reviewed": 0, "no_record": 0}
    from collections import Counter
    out = _estimate(vals, dict(Counter(r["cpt"] for r in claim_rows)), flat, p)
    out["no_record"] = nr
    return out


def recovery_stratified(stratum_rows, sample_ids, level_of, p, no_record=frozenset()):
    """Recovery from a random sample drawn within `stratum_rows` (the provider's claims in the stratum): the estimate is for the stratum only, one stratum (no strata by billed code)."""
    by = {r["claim_id"]: r for r in stratum_rows}
    ids = [c for c in sorted(sample_ids) if c in by]
    fees, amounts = r4.allowed(), r4.claim_amounts(stratum_rows)
    vals, flat, nr = _sample_values(by, ids, level_of, no_record, p, fees, amounts)
    if not flat:
        return {"value": 0.0, "point": 0.0, "mode": "none", "sample_error_rate": 0.0, "reviewed": 0, "no_record": 0}
    one = {"stratum": [v for vs in vals.values() for v in vs]}
    out = _estimate(one, {"stratum": len(stratum_rows)}, flat, p)
    out["no_record"] = nr
    return out
