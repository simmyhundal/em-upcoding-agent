"""Parity check of agent v5.1's environment with workflow v4.1 (H23 at N = 4, stored runs `wlh23_n4_<seed>`): a scripted agent that does exactly what the advice says (ask where ASK, one random sample of
30 charts and a follow-up, hybrid_review, a second random request of 30 for a near-miss, hybrid_review again, submit the review's leanings) is run on data 4.0 DEVELOPMENT seeds only (below 5555), and its
asked set, extended set, called set and score 4.0 are compared with the stored workflow run. No model is called. Free.
The score is computed twice for the agent: with its natural triage (a finding for each provider it asked) and with the workflow's triage (the 4 listed providers), so the difference
between the two designs' triage is not mistaken for a difference in judgment.
Usage: python3 eval/agent51_parity.py [SEED ...]   (default: batches 5 and 6 of eval/dev_pool_v4.py)"""
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent_tools as at  # noqa: E402
import dev_pool_v4 as pool  # noqa: E402
import dollar_reward as dr  # noqa: E402
import score_40 as s4  # noqa: E402
import summary_rules as sr  # noqa: E402


def _sample(env, pid, n=30):
    r = env.call("request_records", {"provider_id": pid, "sample": {"kind": "random", "n": n}})
    if r.get("deficiencies") and r.get("rounds_left", 0) > 0:
        r = env.call("follow_up_records", {"provider_id": pid, "addressed_codes": [d["code"] for d in r["deficiencies"]]})
    return r


def scripted(seed, extend=True, trace=None):
    code = f"d4_{seed}"
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    env = at.Environment(data, os.path.join(data, "view"), seed=1, version="5.1", records_budget=22)
    if trace is not None:                                # record every tool call, so eval/agent51_replay_check.py can feed the same calls through the real loop
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
            if extend and (x.get("demand_check") or {}).get("near_miss"):
                extended.append(x["provider"])
    for pid in extended:
        if "error" in _sample(env, pid):
            continue
        env.call("close_records", {"provider_id": pid, "reason": "near-miss extension done"})
        x = env.call("hybrid_review", {"provider_ids": [pid]})["results"][0]
        leanings[pid] = x["leaning"] or sr.INCONCLUSIVE
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
    return env, set(asked), set(extended), called, res


def agent_score(env, code, called, listed_n):
    claims, k, truth = s4.context(code)
    st = env.office.state
    rounds, seen = Counter(), {}
    for e in env.office.transcript:
        if e.get("action") in ("send_request", "follow_up", "audit_trail") and "error" not in e:
            rounds[e["provider_id"]] += 1
            seen.setdefault(e["provider_id"], set()).update(e.get("usable_claim_ids", []))
    level = dr.level_of_rows(env.office.documentation_rows())
    c = s4.seed_result(called, listed_n, k["providers"], claims, k["justified_cpt_by_claim"], lambda pid: set(env.office.random_claim_ids(pid)), level, dict(rounds),
                       {p: len(v) for p, v in seen.items()}, 0.0, s4.PARAMS, truth=truth)
    return c


def workflow(seed):
    rid = f"wlh23_n4_{seed}"
    asked = {json.loads(x)["provider_id"] for x in open(os.path.join(ROOT, "experiments", rid, "office_transcript.jsonl")) if '"send_request"' in x}
    ext = json.load(open(os.path.join(ROOT, "experiments", rid, "extension_log.json")))
    recs = [json.loads(x) for x in open(os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")) if x.strip()]
    called = {r["provider_id"] for r in recs if r["summary"]["leaning"] == sr.UPCODING}
    return asked, {p for p, v in ext.items() if not v["blocked"]}, called, s4.from_run(rid, f"d4_{seed}")


if __name__ == "__main__":
    seeds = [int(a) for a in sys.argv[1:]] or pool.BATCHES[4] + pool.BATCHES[5]
    assert all(s < 5555 for s in seeds), "development seeds only"
    tot = Counter()
    sw = sa = sa4 = 0.0
    for seed in seeds:
        env, a_asked, a_ext, a_called, res = scripted(seed)
        w_asked, w_ext, w_called, w_sc = workflow(seed)
        code = f"d4_{seed}"
        ca, ca4 = agent_score(env, code, a_called, len(env.findings)), agent_score(env, code, a_called, 4)
        eq = (a_asked == w_asked, a_ext == w_ext, a_called == w_called, abs(ca4["score"] - w_sc["score"]) < 0.5)
        for name, v in zip(("asked", "extended", "called", "score"), eq):
            tot[name] += v
        tot["n"] += 1
        sw, sa, sa4 = sw + w_sc["score"], sa + ca["score"], sa4 + ca4["score"]
        print(seed, "asked", len(a_asked), "=" if eq[0] else f"!= wf {len(w_asked)}", "| extended", sorted(a_ext) if a_ext or w_ext else "-", "=" if eq[1] else f"!= wf {sorted(w_ext)}",
              "| called", len(a_called), "=" if eq[2] else f"!= wf {sorted(w_called)} vs {sorted(a_called)}", f"| score wf {w_sc['score']:+,.0f} agent(4 listed) {ca4['score']:+,.0f} agent(natural) {ca['score']:+,.0f}",
              "| submit:", "ok" if "error" not in res else str(res)[:100])
    n = tot["n"]
    print(f"\n{n} seeds: asked set equal {tot['asked']}, extended set equal {tot['extended']}, called set equal {tot['called']}, score (agent with the workflow's 4 listed) equal {tot['score']}")
    print(f"mean score per seed: workflow {sw / n:+,.0f}, agent with 4 listed {sa4 / n:+,.0f}, agent natural triage {sa / n:+,.0f}")
