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
BANDS = [("below 0", -9, 0.0), ("0 to 5%", 0.0, 0.05), ("5 to 15%", 0.05, 0.15), ("15% and above", 0.15, 9)]


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


# ---- recovery ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def recovery(claim_rows, random_ids, level_of, p, uncurable=()):
    """What an arm demands from one provider: dict(value, point, mode, sample_error_rate, reviewed). value is never negative and is not capped at the true overpayment."""
    by = {r["claim_id"]: r for r in claim_rows}
    ids = [c for c in sorted(random_ids) if c in by and c in level_of]
    if not ids:
        return {"value": 0.0, "point": 0.0, "mode": "none", "sample_error_rate": 0.0, "reviewed": 0}
    allowed = rec.allowed()
    amounts = claim_amounts(claim_rows)
    vals = {}
    flat = []
    for c in ids:
        b = by[c]["cpt"]
        v = overpay_signed(b, CODES[level_of[c]], allowed, amounts.get(c))
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


# ---- one seed -----------------------------------------------------------------------------------------------------------------------------------------------------------------
def seed_result(called, listed_n, key, claims_by_provider, justified, random_ids_of, level_of, rounds_of, charts_of, api_usd, p=None, uncurable_of=None):
    """Components of score 4.0 for one seed. called: provider ids sent a demand; key: answer-key providers (role); justified: {claim_id: justified cpt}."""
    p = p or PARAMS
    allowed = rec.allowed()
    truth = {pid: provider_truth(rows, justified, allowed) for pid, rows in claims_by_provider.items()}
    rec_by = {pid: recovery(claims_by_provider.get(pid, []), random_ids_of(pid), level_of, p, (uncurable_of or (lambda _: ()))(pid)) for pid in called}
    recovered = sum(v["value"] for v in rec_by.values())
    non_up = [pid for pid in called if key[pid]["role"] != "upcoder"]
    cost, parts = staff_cost(listed_n, sum(rounds_of.values()), sum(charts_of.values()), len(called), api_usd, p)
    abrasion = sum(abrasion_weight(truth[pid]["net_rate"], p) * (rounds_of.get(pid, 0) * p["C_BURDEN"] + (p["C_DEMAND_ABRASION"] if pid in called else 0.0))
                   for pid in set(rounds_of) | set(called) if pid in truth)
    pos = {pid: max(t["net_overpay"], 0.0) for pid, t in truth.items()}
    bands = {name: sum(1 for pid in called if lo <= truth[pid]["net_rate"] < hi) for name, lo, hi in BANDS}
    return {"recovered": recovered, "staff_cost": cost, "staff_parts": parts, "abrasion": abrasion, "score": recovered - cost - abrasion,
            "found": sum(key[pid]["role"] == "upcoder" for pid in called), "upcoders": sum(v["role"] == "upcoder" for v in key.values()), "demands": len(called),
            "honest_called": len(non_up), "recovered_from_non_upcoders": sum(rec_by[pid]["value"] for pid in non_up),
            "abrasion_from_non_upcoders": sum(abrasion_weight(truth[pid]["net_rate"], p) * (rounds_of.get(pid, 0) * p["C_BURDEN"] + p["C_DEMAND_ABRASION"]) for pid in non_up if pid in truth),
            "estimate_over_truth": sum(rec_by[pid]["value"] - max(truth[pid]["net_overpay"], 0.0) for pid in called if pid in truth),
            "true_overpay_called": sum(pos[pid] for pid in called if pid in pos), "true_overpay_all": sum(pos.values()),
            "bands": bands, "modes": dict(Counter(v["mode"] for v in rec_by.values())), "rounds": sum(rounds_of.values()), "charts": sum(charts_of.values())}


def add(parts):
    """Sum components over seeds."""
    out = {}
    for k in ("recovered", "staff_cost", "abrasion", "score", "found", "upcoders", "demands", "honest_called", "recovered_from_non_upcoders", "abrasion_from_non_upcoders",
              "estimate_over_truth", "true_overpay_called", "true_overpay_all", "rounds", "charts"):
        out[k] = sum(x[k] for x in parts)
    out["bands"] = {b: sum(x["bands"][b] for x in parts) for b, _, _ in BANDS}
    return out


def dollar_weighted_recall(c):
    return c["true_overpay_called"] / c["true_overpay_all"] if c["true_overpay_all"] else 0.0


# ---- stored runs ------------------------------------------------------------------------------------------------------------------------------------------------------------
def load_key(code):
    return json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))


def from_run(rid, code, p=None, key=None):
    """Score 4.0 components for a stored run folder (workflow or agent) on its data-2.2 answer key. Definitions (docs/score_40.md):
    demand = called upcoding in case_summaries_checked.jsonl; listed = providers with a checked summary; rounds and charts from the office transcript (as release 5);
    API dollars = the run's recorded model spend (writer, judge, agent)."""
    p = p or PARAMS
    k = key or load_key(code)
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    claims = {}
    for r in csv.DictReader(open(os.path.join(data, "view", "claims.csv"))):
        claims.setdefault(r["provider_id"], []).append(r)
    docs = list(csv.DictReader(open(os.path.join(data, f"view_{rid}", "documentation.csv"))))
    level = dr.level_of_rows(docs)
    summaries = [json.loads(x) for x in open(os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")) if x.strip()]
    called = {x["provider_id"] for x in summaries if x["summary"]["leaning"] == "pattern_consistent_with_upcoding"}
    rnd = rec.random_ids(rid)
    rounds, seen = Counter(), {}
    for line in open(os.path.join(ROOT, "experiments", rid, "office_transcript.jsonl")):
        e = json.loads(line)
        if e.get("action") in ("send_request", "follow_up", "audit_trail") and "error" not in e:
            rounds[e["provider_id"]] += 1
            seen.setdefault(e["provider_id"], set()).update(e.get("usable_claim_ids", []))
    charts = {pid: len(ids) for pid, ids in seen.items()}                    # distinct charts received (a follow-up can list the same chart again)
    import run_release2 as r2
    return seed_result(called, len(summaries), k["providers"], claims, k["justified_cpt_by_claim"], lambda pid: rnd.get(pid, set()), level, dict(rounds), dict(charts), r2.cost(rid), p)


if __name__ == "__main__":
    c = from_run(sys.argv[1], sys.argv[2])
    print(json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in c.items()}, indent=1))
