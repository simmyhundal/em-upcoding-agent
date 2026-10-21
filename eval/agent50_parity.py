"""Parity check of agent v5.0's environment with workflow v4.0 (issue 128): a scripted agent that does exactly what the advice says (ask where ASK, one random sample of 30 charts and a follow-up,
hybrid_review on every provider with records, submit the review's leanings) is run on a development seed, and its asked set and called set are compared with the stored frozen workflow v4.0 run
(`wlh8_<seed>`). No model is called (hybrid_review without a model; the rules decide). Free."""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent_tools as at  # noqa: E402
import summary_rules as sr  # noqa: E402


def scripted(seed):
    code = f"d4_{seed}"
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    env = at.Environment(data, os.path.join(data, "view"), seed=1, version="5.0", records_budget=22)
    table = env.call("screen_providers", {"method": "eb_upper_t", "top_pct": 10})["table"]
    asked = [r[0] for r in table["rows"] if r[-1] == "ASK"]
    for pid in asked:
        r = env.call("request_records", {"provider_id": pid, "sample": {"kind": "random", "n": 30}})
        if r.get("deficiencies") and r.get("rounds_left", 0) > 0:
            env.call("follow_up_records", {"provider_id": pid, "addressed_codes": [d["code"] for d in r["deficiencies"]]})
        env.call("close_records", {"provider_id": pid, "reason": "advice: STOP after the first sample"})
    with_records = [p for p in asked if env.office.state[p]["usable"]]
    leanings = {}
    for i in range(0, len(with_records), 20):
        for x in env.call("hybrid_review", {"provider_ids": with_records[i:i + 20]})["results"] if with_records else []:
            leanings[x["provider"]] = x["leaning"] or sr.INCONCLUSIVE
    findings = [{"provider_id": p, "leaning": l, "headline": f"{p}: review", "interpretation": "Scripted review."} for p, l in leanings.items()]
    aside = [{"provider_id": c, "reason": "scripted: not asked"} for c in sorted(env.screen_candidates) if c not in leanings]
    res = env.call("submit_findings", {"findings": findings, "set_aside": aside})
    for _ in range(3):                                    # a real agent would soften a call the lint does not support (chart-rule calls the pooled evidence does not carry)
        bad = (res.get("problems") or {}) if "error" in res else {}
        if not bad:
            break
        findings = [{**f, "leaning": sr.INCONCLUSIVE} if f["provider_id"] in bad else f for f in findings]
        res = env.call("submit_findings", {"findings": findings, "set_aside": aside})
    called = {p for p, s in env.findings.items() if s["leaning"] == sr.UPCODING}
    return set(asked), called, res


def workflow(seed):
    rid = f"wlh8_{seed}"
    asked = {json.loads(x)["provider_id"] for x in open(os.path.join(ROOT, "experiments", rid, "office_transcript.jsonl")) if '"send_request"' in x}
    recs = [json.loads(x) for x in open(os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")) if x.strip()]
    called = {r["provider_id"] for r in recs if r["summary"]["leaning"] == sr.UPCODING}
    return asked, called


if __name__ == "__main__":
    for seed in [int(a) for a in sys.argv[1:]] or [1515, 1616, 1717]:
        a_asked, a_called, res = scripted(seed)
        w_asked, w_called = workflow(seed)
        print(seed, "asked equal:", a_asked == w_asked, f"({len(a_asked)} vs {len(w_asked)})", "| called: agent", sorted(a_called), "workflow", sorted(w_called), "| submit:", str(res)[:120])
