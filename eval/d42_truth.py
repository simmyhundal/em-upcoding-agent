"""Data 4.2 truth for evaluation code (issue 173; docs/data_v4_2.md, sections c and e). EVALUATION ONLY: this module reads the answer key; never import it from anything an arm or a model sees.

The data 4.2 answer key has no `role`. Score 4.0 (eval/score_40.py, untouched) needs `key[pid]["role"]` in `seed_result`, so this adapter builds, at evaluation time, a DERIVED key whose `role` is
"upcoder" when the provider's true overpayment (level plus fraud, waste and abuse) is at least `m` times the cost of pursuing it, and "honest" otherwise. That label is labelled as derived
(`role_derived_at`), is never written to a file and never reaches a generator or an arm. It also computes the level truth on RENDERED claims only (a phantom claim is justified at its billed level, so it
cannot change the level truth, but it would dilute the net rate's denominator), and passes it to `seed_result(..., truth=...)`.
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import eval61_recovery as rec  # noqa: E402
import recovery_40 as r4  # noqa: E402
import score_40 as s4  # noqa: E402

P = r4.PARAMS
N_CHARTS = 30                                   # the first sample of workflow v4.0 and v4.1
M_SWEEP = (0.0, 0.5, 1.0, 2.0, 4.0)             # the justification threshold as a multiple of the cost of pursuing a provider; 1.0 is the primary view
FORBIDDEN_KEY_FIELDS = ("role", "planted", "above_margin", "above_p95", "subtle", "planted_below_line", "upcoder_definition", "upcoder_margin")


def unit_costs(p=None):
    """(chart, round, demand, triage) staff costs in dollars under score 4.0's prices."""
    p = p or P
    return tuple(r4.staff_cost(*a, p)[0] for a in ((0, 0, 1, 0, 0), (0, 1, 0, 0, 0), (0, 0, 0, 1, 0), (1, 0, 0, 0, 0)))


def pursuit_cost(n_charts=N_CHARTS, p=None):
    """Staff cost of pursuing one provider with a random sample of n charts, two request rounds, one demand, and its triage (score 4.0's prices)."""
    ch, rd, dm, tr = unit_costs(p)
    return n_charts * ch + 2 * rd + dm + tr


def abrasion_price(p=None):
    """What pursuing a provider costs the provider's relationship at full weight: two rounds of burden and one demand."""
    p = p or P
    return 2 * p["C_BURDEN"] + p["C_DEMAND_ABRASION"]


def load_key(code):
    """The raw data 4.2 answer key (eval/answer_key/ground_truth_v2_<code>.json)."""
    return json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))


def totals(key):
    """{provider_id: true overpayment available to recover (level net floored at 0, plus the three fraud kinds), in dollars}."""
    return {pid: v["true_overpay_total"] for pid, v in key["providers"].items()}


def justified(key, m, cost=None):
    """Providers whose true overpayment is at least m times the cost of pursuing them (m = 0: any positive amount). An evaluation-time label."""
    cost = pursuit_cost() if cost is None else cost
    thr = m * cost
    return {pid for pid, t in totals(key).items() if (t > 0 if thr <= 0 else t >= thr)}


def derived_key(key, m=1.0, cost=None):
    """A key in score 4.0's shape with a DERIVED role (see the module docstring)."""
    j = justified(key, m, cost)
    return {pid: {"role": "upcoder" if pid in j else "honest", "role_derived_at": f"true_overpay_total >= {m} x pursuit cost", "habit": v["habit"]} for pid, v in key["providers"].items()}


_CTX = {}


def context(code):
    """(claims by provider from the view, raw key, level truth per provider on rendered claims only). Cached for one dataset at a time."""
    if code not in _CTX:
        _CTX.clear()
        data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
        claims = {}
        for r in csv.DictReader(open(os.path.join(data, "view", "claims.csv"))):
            claims.setdefault(r["provider_id"], []).append(r)
        key = load_key(code)
        fraud = key["fraud_claims"]
        allowed = rec.allowed()
        truth = {pid: s4.provider_truth([r for r in rows if r["claim_id"] not in fraud], key["justified_cpt_by_claim"], allowed) for pid, rows in claims.items()}
        _CTX[code] = (claims, key, truth)
    return _CTX[code]


def seed_result(rid, code, m=1.0, p=None, inputs=None):
    """Score 4.0's components for a stored run on a data 4.2 dataset, through the adapter: derived role at threshold m, level truth on rendered claims. Score 4.0 itself is not changed."""
    p = p or P
    claims, key, truth = context(code)
    i = inputs or s4.run_inputs(rid, code)
    return s4.seed_result(i["called"], i["listed"], derived_key(key, m), claims, key["justified_cpt_by_claim"], lambda pid: i["random"].get(pid, set()), i["level"], i["rounds"], i["charts"],
                          i["api"], p, truth=truth), i
