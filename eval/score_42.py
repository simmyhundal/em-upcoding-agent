"""Score 4.2 (S4.2) on data 4.2: dollars recovered - staff-hours cost - provider abrasion, per seed (docs/score_42.md). EVALUATION ONLY: reads the answer key (through eval/d42_truth.py).

Differences from score 4.0 (which stays frozen), all on data 4.2:
  * the commercial profile: copy fee $0 (src/recovery_42.py, S4.1's `commercial_no_copy`);
  * records not provided: a sampled claim for which the office reported NO_RECORD counts as overpaid at its paid amount (PIM 8.4.5);
  * the claims-data lane (src/fwa_lane.py): a run may carry `fwa_lane.json`, the providers it flagged from claims alone, a random sample within the claims on their impossible days, and
    whether it sent a demand. Its recovery is the stratum estimate (recovery_stratified); a provider with both a level demand and a lane demand gets one demand and both estimates, the level one on
    the claims outside the stratum;
  * abrasion weights use the provider's TOTAL true net rate: (visits billed above - below the justified level + claims billed for services never rendered) over (rendered + never-rendered claims).
    Under score 4.0's weight a provider whose only fault is billing for visits that never happened has a true rate of 0 and would count as an honest provider.
Never import this from an arm or a model.
"""
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import d42_truth as dt  # noqa: E402
import recovery_40 as r4  # noqa: E402
import recovery_42 as r42  # noqa: E402
import score_40 as s4  # noqa: E402

VERSION = "4.2"
FRAUD_KINDS = ("not_rendered", "impossible_days")
_TOT = {}


def total_truth(code):
    """{pid: level truth dict with net_rate replaced by the total rate, plus 'phantom'} for one dataset (cached)."""
    if code not in _TOT:
        _TOT.clear()
        claims, key, truth = dt.context(code)
        fraud = key["fraud_claims"]
        out = {}
        for pid, t in truth.items():
            ph = sum(1 for r in claims.get(pid, []) if fraud.get(r["claim_id"]) in FRAUD_KINDS)
            n = t["claims"]
            out[pid] = {**t, "phantom": ph, "net_rate": (t["upcoded"] - t["downcoded"] + ph) / max(n + ph, 1)}
        _TOT[code] = out
    return _TOT[code]


def lane(rid):
    path = os.path.join(ROOT, "experiments", rid, "fwa_lane.json")
    return json.load(open(path)) if os.path.exists(path) else {"providers": {}}


def no_record_ids(rid):
    """Claim ids the office reported NO_RECORD, from the run's office transcripts (main and lane): payer-visible facts."""
    out = {}
    for name in ("office_transcript.jsonl", "fwa_office_transcript.jsonl"):
        path = os.path.join(ROOT, "experiments", rid, name)
        if not os.path.exists(path):
            continue
        for line in open(path):
            e = json.loads(line)
            for d in e.get("deficiencies", []):
                if d["code"] == "NO_RECORD":
                    out.setdefault(e["provider_id"], set()).update(d["claim_ids"])
    return out


def seed_result(rid, code, m=1.0, p=None, inputs=None, lane_data=None, no_record=None, gate2=None):
    """lane_data / no_record: the lane record and NO_RECORD ids of a live environment (a parity check); None reads the run folder."""
    p = p or r42.params42()
    claims, key, _lvl = dt.context(code)
    truth = total_truth(code)
    i = inputs or s4.run_inputs(rid, code)
    ln = (lane_data if lane_data is not None else lane(rid))["providers"]
    nr = no_record if no_record is not None else no_record_ids(rid)
    dkey = dt.derived_key(key, m)
    lane_demand = {pid for pid, v in ln.items() if v.get("demand")}
    called = set(i["called"]) | lane_demand
    rounds = Counter(i["rounds"])
    charts = Counter(i["charts"])
    for pid, v in ln.items():
        rounds[pid] += v.get("rounds", 0)
        charts[pid] += v.get("charts", 0)
    listed = i["listed"] + len(ln)
    rec_level, rec_fwa, modes = {}, {}, Counter()
    for pid in called:
        rows = claims.get(pid, [])
        v = ln.get(pid)
        strat = set(v["stratum_ids"]) if v and v.get("demand") else set()
        if pid in i["called"]:
            outside = [r for r in rows if r["claim_id"] not in strat]
            ids = {c for c in i["random"].get(pid, set()) if c not in strat}
            e = r42.recovery(outside, ids, i["level"], p, no_record=nr.get(pid, frozenset()))
            rec_level[pid] = e["value"]
            modes[e["mode"]] += 1
        if strat:
            e = r42.recovery_stratified([r for r in rows if r["claim_id"] in strat], v["sample_ids"], {c: int(l) for c, l in v.get("levels", {}).items()}, p, no_record=set(v.get("no_record", [])))
            rec_fwa[pid] = e["value"]
            modes["stratum:" + e["mode"]] += 1
    rejected = set()
    if gate2 is not None:                                  # evaluation mode (gate 2): a person signs off each demand; a rejected demand is not sent (docs/evaluation_modes.md)
        for pid in sorted(called):
            if not gate2(pid, rec_level.get(pid, 0.0) + rec_fwa.get(pid, 0.0)):
                rejected.add(pid)
        called = called - rejected
        for pid in rejected:
            rec_level.pop(pid, None)
            rec_fwa.pop(pid, None)
    recovered = sum(rec_level.values()) + sum(rec_fwa.values())
    cost, parts = r4.staff_cost(listed, sum(rounds.values()), sum(charts.values()), len(called), i["api"], p)
    wt = lambda pid: s4.abrasion_weight(truth[pid]["net_rate"], p)
    abrasion = sum(wt(pid) * (rounds.get(pid, 0) * p["C_BURDEN"] + (p["C_DEMAND_ABRASION"] if pid in called else 0.0)) for pid in set(rounds) | called if pid in truth)
    imp = {pid for pid, v in key["providers"].items() if v.get("true_overpay_fwa", {}).get("impossible_days", 0) > 0}
    found_just = sum(dkey[pid]["role"] == "upcoder" for pid in called)
    return {"recovered": recovered, "recovered_level": sum(rec_level.values()), "recovered_fwa": sum(rec_fwa.values()), "staff_cost": cost, "staff_parts": parts, "abrasion": abrasion,
            "score": recovered - cost - abrasion, "demands": len(called), "lane_flagged": len(ln), "lane_demands": len(lane_demand), "lane_true": len(lane_demand & imp), "lane_false": len(set(ln) - imp),
            "impossible_providers": len(imp), "justified_called": found_just, "justified": sum(v["role"] == "upcoder" for v in dkey.values()), "rounds": sum(rounds.values()), "charts": sum(charts.values()),
            "listed": listed, "rejected_demands": len(rejected), "modes": dict(modes), "true_overpay_all": sum(dt.totals(key).values()), "true_overpay_called": sum(dt.totals(key)[pid] for pid in called if pid in truth)}, i


if __name__ == "__main__":
    c, _ = seed_result(sys.argv[1], sys.argv[2])
    print(json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in c.items()}, indent=1))
