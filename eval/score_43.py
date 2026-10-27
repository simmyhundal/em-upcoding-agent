"""Score 4.3 on data 4.0 and later (docs/score_43.md; issue 200): dollars COLLECTED minus staff cost minus provider abrasion, per seed. EVALUATION ONLY: reads the answer key.
Score 4.2's rules plus (src/recovery_43.py): a dollar-based error gate, appeals then collection applied to each demand's lower bound, a volume-lane provider priced as a REFERRAL (referral cost, lower collection rate),
and the payer's expected cost of handling appeals. Works on data 4.0 stored runs (no fraud claims) and on data 4.2 and later. Never import this from an arm or a model.
"""
import csv
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import eval61_recovery as rec  # noqa: E402
import recovery_40 as r4  # noqa: E402
import recovery_43 as r43  # noqa: E402
import score_40 as s4  # noqa: E402
import score_42 as s42  # noqa: E402

VERSION = "4.3"
FRAUD_KINDS = ("not_rendered", "impossible_days")
_CTX = {}


def context(code):
    """(claims by provider, answer key, total true rate by provider) for one dataset of any version (cached for one dataset)."""
    if code not in _CTX:
        _CTX.clear()
        data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
        claims = {}
        for r in csv.DictReader(open(os.path.join(data, "view", "claims.csv"))):
            claims.setdefault(r["provider_id"], []).append(r)
        key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))
        fraud = {c: k for c, k in key.get("fraud_claims", {}).items() if k in FRAUD_KINDS}
        allowed = rec.allowed()
        rate = {}
        for pid, rows in claims.items():
            t = s4.provider_truth([r for r in rows if r["claim_id"] not in fraud], key["justified_cpt_by_claim"], allowed)
            ph = sum(1 for r in rows if r["claim_id"] in fraud)
            rate[pid] = (t["upcoded"] - t["downcoded"] + ph) / max(t["claims"] + ph, 1)
        _CTX[code] = (claims, key, rate)
    return _CTX[code]


def seed_result(rid, code, p=None, inputs=None, lane_data=None, no_record=None):
    p = p or r43.params43()
    claims, key, rate = context(code)
    i = inputs or s4.run_inputs(rid, code)
    ln = (lane_data if lane_data is not None else s42.lane(rid))["providers"]
    nr = no_record if no_record is not None else s42.no_record_ids(rid)
    referral = {pid for pid, v in ln.items() if v.get("demand")} | {pid for pid in i["called"] if nr.get(pid)}     # a demand that rests on claims for visits that never happened is a fraud referral
    ordinary = set(i["called"]) - referral
    rounds, charts = Counter(i["rounds"]), Counter(i["charts"])
    for pid, v in ln.items():
        rounds[pid] += v.get("rounds", 0)
        charts[pid] += v.get("charts", 0)
    listed = i["listed"] + len(ln)
    lower, got = {}, {}
    for pid in ordinary | referral:
        rows = claims.get(pid, [])
        v = ln.get(pid) if pid in referral else None
        strat = set(v["stratum_ids"]) if v else set()
        lb = 0.0
        if pid in i["called"]:
            outside = [r for r in rows if r["claim_id"] not in strat]
            ids = {c for c in i["random"].get(pid, set()) if c not in strat}
            lb += r43.recovery(outside, ids, i["level"], p, no_record=nr.get(pid, frozenset()))["value"]
        if strat:
            lb += r43.recovery_stratified([r for r in rows if r["claim_id"] in strat], v["sample_ids"], {c: int(l) for c, l in v.get("levels", {}).items()}, p, no_record=set(v.get("no_record", [])))["value"]
        lower[pid] = lb
        got[pid] = r43.collected(lb, p, referral=pid in referral)
    cost, parts = r43.staff_cost(listed, sum(rounds.values()), sum(charts.values()), len(ordinary), len(referral), i["api"], p)
    called = ordinary | referral
    abrasion = sum(s4.abrasion_weight(rate[pid], p) * (rounds.get(pid, 0) * p["C_BURDEN"] + (p["C_DEMAND_ABRASION"] if pid in called else 0.0)) for pid in set(rounds) | called if pid in rate)
    collected = sum(got.values())
    return {"score": collected - cost - abrasion, "collected": collected, "lower_bounds": sum(lower.values()), "staff_cost": cost, "staff_parts": parts, "abrasion": abrasion,
            "demands": len(ordinary), "referrals": len(referral), "rounds": sum(rounds.values()), "charts": sum(charts.values()), "listed": listed}, i


if __name__ == "__main__":
    c, _ = seed_result(sys.argv[1], sys.argv[2])
    print(json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in c.items()}, indent=1))
