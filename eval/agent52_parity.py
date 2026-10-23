"""Parity check of agent v5.2's environment with workflow v4.2 (H28, stored runs `d42wlh28_<seed>`): a scripted agent that does exactly what the advice says (agent v5.1's script for the level review, then volume_screen,
request_stratum for every provider listed, send_demand where the tool says DEMAND) runs on data 4.2 DEVELOPMENT seeds; its asked set, lane set, demands and score 4.2 are compared with the stored workflow run.
No model is called. Free. Usage: python3 eval/agent52_parity.py [SEED ...]   (default: the first 20 development seeds)"""
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent_tools as at  # noqa: E402
import dev_pool_v42 as pool  # noqa: E402
import dollar_reward as dr  # noqa: E402
import score_40 as s4  # noqa: E402
import score_42 as s42  # noqa: E402
import summary_rules as sr  # noqa: E402


def _sample(env, pid, n=30):
    r = env.call("request_records", {"provider_id": pid, "sample": {"kind": "random", "n": n}})
    if r.get("deficiencies") and r.get("rounds_left", 0) > 0:
        r = env.call("follow_up_records", {"provider_id": pid, "addressed_codes": [d["code"] for d in r["deficiencies"] if d["code"] != "NO_RECORD"]})
    return r


def scripted(seed, trace=None):
    code = f"d42_{seed}"
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    env = at.Environment(data, os.path.join(data, "view"), seed=1, version="5.2", records_budget=22, office=at.make_office(data, os.path.join(data, "view"), "5.2", seed=1))
    if trace is not None:
        call0 = env.call
        env.call = lambda name, args: (trace.append((name, dict(args))), call0(name, args))[1]
    table = env.call("screen_providers", {"method": "eb_upper_t", "top_pct": 10})["table"]
    asked = [r[0] for r in table["rows"] if r[-1] == "ASK"]
    for pid in asked:
        _sample(env, pid)
        env.call("close_records", {"provider_id": pid, "reason": "advice: STOP after the first sample"})
    with_records = [p for p in asked if env.office.state[p]["usable"]]
    leanings, extended = {}, []
    for i in range(0, len(with_records), 20):
        for x in env.call("hybrid_review", {"provider_ids": with_records[i:i + 20]})["results"]:
            leanings[x["provider"]] = x["leaning"] or sr.INCONCLUSIVE
            if (x.get("demand_check") or {}).get("near_miss"):
                extended.append(x["provider"])
    for pid in extended:
        if "error" in _sample(env, pid):
            continue
        env.call("close_records", {"provider_id": pid, "reason": "near-miss extension done"})
        x = env.call("hybrid_review", {"provider_ids": [pid]})["results"][0]
        leanings[pid] = x["leaning"] or sr.INCONCLUSIVE
    lane_set, demands = [], []
    for row in env.call("volume_screen", {})["table"]:
        pid = row["provider_id"]
        r = env.call("request_stratum", {"provider_id": pid})
        lane_set.append(pid)
        if r.get("recommended") == "DEMAND" and "error" not in env.call("send_demand", {"provider_id": pid}):
            demands.append(pid)
    findings = [{"provider_id": p, "leaning": l, "headline": f"{p}: review", "interpretation": "Scripted review."} for p, l in leanings.items()]
    aside = [{"provider_id": c, "reason": "scripted: not asked"} for c in sorted(env.screen_candidates) if c not in leanings]
    res = env.call("submit_findings", {"findings": findings, "set_aside": aside})
    for _ in range(3):
        bad = (res.get("problems") or {}) if "error" in res else {}
        if not bad:
            break
        findings = [{**f, "leaning": sr.INCONCLUSIVE} if f["provider_id"] in bad else f for f in findings]
        res = env.call("submit_findings", {"findings": findings, "set_aside": aside})
    called = {p for p, s in env.findings.items() if s["leaning"] == sr.UPCODING}
    return env, set(asked), set(extended), called, set(lane_set), set(demands), res


def agent_score(env, code, called, listed_n):
    rounds, seen = Counter(), {}
    nr = {}
    for e in env.office.transcript:
        if e.get("action") in ("send_request", "follow_up", "audit_trail") and "error" not in e:
            rounds[e["provider_id"]] += 1
            seen.setdefault(e["provider_id"], set()).update(e.get("usable_claim_ids", []))
        for d in e.get("deficiencies", []):
            if d["code"] == "NO_RECORD":
                nr.setdefault(e["provider_id"], set()).update(d["claim_ids"])
    level = dr.level_of_rows(env.office.documentation_rows())
    inputs = {"called": called, "listed": listed_n, "random": {p: set(env.office.random_claim_ids(p)) for p in env.office.state}, "level": level, "rounds": dict(rounds),
              "charts": {p: len(v) for p, v in seen.items()}, "api": 0.0}
    return s42.seed_result("scripted", code, inputs=inputs, lane_data=env.lane_record(), no_record=nr)[0]


def workflow(seed):
    rid = f"d42wlh28_{seed}"
    asked = {json.loads(x)["provider_id"] for x in open(os.path.join(ROOT, "experiments", rid, "office_transcript.jsonl")) if '"send_request"' in x}
    recs = [json.loads(x) for x in open(os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")) if x.strip()]
    called = {r["provider_id"] for r in recs if r["summary"]["leaning"] == sr.UPCODING}
    ln = s42.lane(rid)["providers"]
    return asked, called, set(ln), {p for p, v in ln.items() if v["demand"]}, s42.seed_result(rid, f"d42_{seed}")[0]


if __name__ == "__main__":
    seeds = [int(a) for a in sys.argv[1:]] or pool.DEV[:20]
    tot, sw, sa4 = Counter(), 0.0, 0.0
    for seed in seeds:
        env, a_asked, a_ext, a_called, a_lane, a_dem, res = scripted(seed)
        w_asked, w_called, w_lane, w_dem, w_sc = workflow(seed)
        ca4 = agent_score(env, f"d42_{seed}", a_called | a_dem, 4)
        eq = (a_asked == w_asked, a_called == w_called, a_lane == w_lane, a_dem == w_dem, abs(ca4["score"] - w_sc["score"]) < max(100.0, 0.01 * abs(w_sc["score"])))
        for name, v in zip(("asked", "called", "lane", "demands", "score"), eq):
            tot[name] += v
        tot["n"] += 1
        sw, sa4 = sw + w_sc["score"], sa4 + ca4["score"]
        print(seed, "asked", "=" if eq[0] else "!=", "| called", "=" if eq[1] else "!=", "| lane", len(a_lane), "=" if eq[2] else f"!= wf {len(w_lane)}", "| lane demands", len(a_dem), "=" if eq[3] else f"!= wf {len(w_dem)}",
              f"| S4.2 wf {w_sc['score']:+,.0f} agent {ca4['score']:+,.0f}", "| submit:", "ok" if "error" not in res else str(res)[:80], flush=True)
    n = tot["n"]
    print(f"\n{n} seeds: asked equal {tot['asked']}, called equal {tot['called']}, lane providers equal {tot['lane']}, lane demands equal {tot['demands']}, score equal {tot['score']}")
    print(f"mean S4.2 per seed: workflow {sw / n:+,.0f}, scripted agent {sa4 / n:+,.0f}")
