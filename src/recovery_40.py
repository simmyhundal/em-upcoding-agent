"""Payer-visible pricing of score 4.0 (issue 125; docs/score_40.md): the parameters, the level-difference price of a claim, the recovery a payer can demand from a random sample, and the staff cost of an
activity. Nothing here reads the answer key: workflow v4.0's demand floor (eval/make_v2_office_workflow_runs.py) and agent v5.0 (src/agent_tools.py) import it, and eval/score_40.py re-exports
it and adds the parts that need the truth (provider truth, abrasion, the per-seed score)."""
import json
import math
import os
from collections import Counter

import pi_estimate as pe

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODES = pe.CODES
LEVEL = pe.LEVEL
_ALLOWED = None


def allowed():
    """Fee-schedule allowed amounts by E/M code (the same file as eval/eval61_recovery.allowed)."""
    global _ALLOWED
    if _ALLOWED is None:
        _ALLOWED = {c: v["allowed_amount"] for c, v in json.load(open(os.path.join(ROOT, "data", "baselines", "allowed_amounts_ga_fp.json")))["codes"].items()}
    return _ALLOWED


# ---- parameters (every one is documented, with its source or "assumption", in docs/score_40.md) -------------------------------------------------------------------------------
PARAMS = {
    "NETTING": True,                 # PIM ch. 8 (verified, Rev. 13762)
    "GATE": True,                    # SSA 1893(f)(3)
    "GATE_ERROR_RATE": 0.15,         # ASSUMPTION: the manual gives no number; sweep 0.10, 0.25, 0.40
    "FULL_DENIAL": False,
    "BOUND": "two_sided_90",         # release 5's lower limit; "one_sided_90" is the manual's wording
    "BENEFIT_FACTOR": 1.4,           # ASSUMPTION (BLS wage and salary plus roughly 30% benefits); sweep 1.3 to 1.5
    "HOURS_PER_YEAR": 2080,
    "WAGES": {                       # BLS Occupational Outlook Handbook, median annual wage, May 2025 (quoted in docs/score_40.md)
        "analyst": 78000,            # claims adjusters, examiners and investigators (SOC 13-1031): PROXY for a PI analyst
        "admin": 45930,              # medical secretaries and administrative assistants (SOC 43-6013)
        "coder": 51140,              # medical records specialists (SOC 29-2072): PROXY for a certified coder (no certification premium)
        "investigator": 78000,       # claims adjusters, examiners and investigators (SOC 13-1031)
        "nurse": 97550,              # registered nurses (SOC 29-1141)
    },
    "MINUTES": {"triage_per_listed": 15, "admin_per_round": 30, "coder_per_chart": 15, "investigator_per_demand": 240, "nurse_per_demand": 60},      # ASSUMPTIONS (plan)
    "REVIEW_COST_MODEL": "bls",      # "bls": coder minutes x wage; "gao_per_claim": $158 per chart reviewed (GAO-16-394, a Recovery Auditor's average cost per CLAIM review, 2013-14)
    "GAO_PER_CLAIM_REVIEW": 158.0,
    "C_COPY": 90.0,                  # per round (release 5: CMS Transmittal 786 page fees)
    "C_BURDEN": 43.84,               # per round to a provider (release 5: Premier 2022)
    "C_DEMAND_ABRASION": 2000.0,     # per demand (release 5 ASSUMPTION); sensitivity 0 and 10,000
    "W_FLOOR": 0.15,                 # w(r) reaches 0 here: the upcoder floor of data 4.0 (assumption)
}

# Student t, one-sided 90% (two-sided 80%), df 1..30, for BOUND = "one_sided_90"; z beyond 30.
T_ONE_SIDED_90 = [3.078, 1.886, 1.638, 1.533, 1.476, 1.440, 1.415, 1.397, 1.383, 1.372, 1.363, 1.356, 1.350, 1.345, 1.341, 1.337, 1.333, 1.330, 1.328, 1.325, 1.323, 1.321,
                  1.319, 1.318, 1.316, 1.315, 1.314, 1.313, 1.311, 1.310]


def params(**over):
    p = {k: (dict(v) if isinstance(v, dict) else v) for k, v in PARAMS.items()}
    p.update(over)
    return p


def t_value(df, bound):
    if bound == "one_sided_90":
        return T_ONE_SIDED_90[df - 1] if 1 <= df <= 30 else 1.282
    return pe.t_crit(df, 0.90)


def hourly(role, p):
    return p["WAGES"][role] / p["HOURS_PER_YEAR"] * p["BENEFIT_FACTOR"]


# ---- pricing -------------------------------------------------------------------------------------------------------------------------------------------------------------------
def overpay_signed(billed, supported, allowed, amounts=None):
    """Overpayment of one claim, negative when the supported level is above the billed one. Same arithmetic as pi_estimate.overpay (share of the allowed amount the plan paid)."""
    if billed == supported:
        return 0.0
    if amounts and amounts[0] > 0:
        claim_allowed, paid = amounts
        return (claim_allowed - allowed[supported]) * (paid / claim_allowed)
    return allowed[billed] - allowed[supported]


def claim_amounts(rows):
    return {r["claim_id"]: (float(r["allowed_amount"]), float(r["paid_amount"])) for r in rows if r.get("allowed_amount")}


# ---- recovery ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def recovery(claim_rows, random_ids, level_of, p, uncurable=()):
    """What an arm demands from one provider: dict(value, point, mode, sample_error_rate, reviewed). value is never negative and is not capped at the true overpayment."""
    by = {r["claim_id"]: r for r in claim_rows}
    ids = [c for c in sorted(random_ids) if c in by and c in level_of]
    if not ids:
        return {"value": 0.0, "point": 0.0, "mode": "none", "sample_error_rate": 0.0, "reviewed": 0}
    fees = allowed()
    amounts = claim_amounts(claim_rows)
    vals = {}
    flat = []
    for c in ids:
        b = by[c]["cpt"]
        v = overpay_signed(b, CODES[level_of[c]], fees, amounts.get(c))
        if not p["NETTING"]:
            v = max(v, 0.0)
        if p["FULL_DENIAL"] and c in uncurable and c in amounts:
            v = max(v, amounts[c][1])
        vals.setdefault(b, []).append(v)
        flat.append(v)
    err = sum(1 for v in flat if v > 0) / len(flat)
    if p["GATE"] and err < p["GATE_ERROR_RATE"]:
        s = sum(flat)
        return {"value": max(s, 0.0), "point": s, "mode": "sampled claims only", "sample_error_rate": err, "reviewed": len(flat)}
    frame = dict(Counter(r["cpt"] for r in claim_rows))
    total = var = 0.0
    n_all = k = 0
    for code, N in frame.items():
        v = vals.get(code, [])
        n = len(v)
        if not n:
            continue
        mean = sum(v) / n
        s2 = (sum((x - mean) ** 2 for x in v) / (n - 1)) if n > 1 else 0.0
        total += N * mean
        var += N * N * (1 - n / N) * s2 / n
        n_all += n
        k += 1
    half = t_value(max(n_all - k, 1), p["BOUND"]) * math.sqrt(var)
    return {"value": max(0.0, total - half), "point": total, "mode": "extrapolated", "sample_error_rate": err, "reviewed": len(flat)}


# ---- staff-hours cost -----------------------------------------------------------------------------------------------------------------------------------------------------------
def staff_cost(listed, rounds, charts, demands, api_usd, p):
    """(total, parts). listed: providers triaged; rounds: request rounds sent; charts: E/M charts received; demands: demands sent; api_usd: the arm's model dollars."""
    m = p["MINUTES"]
    parts = {"triage": listed * m["triage_per_listed"] / 60 * hourly("analyst", p),
             "request admin": rounds * m["admin_per_round"] / 60 * hourly("admin", p),
             "chart review": (charts * p["GAO_PER_CLAIM_REVIEW"]) if p["REVIEW_COST_MODEL"] == "gao_per_claim" else charts * m["coder_per_chart"] / 60 * hourly("coder", p),
             "demand work": demands * (m["investigator_per_demand"] / 60 * hourly("investigator", p) + m["nurse_per_demand"] / 60 * hourly("nurse", p)),
             "copy fees": rounds * p["C_COPY"], "API": api_usd}
    return sum(parts.values()), parts


