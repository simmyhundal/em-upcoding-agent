"""Agent v3.5 (issues 111 to 113): the advice inside tool results equals the workflow v2.5 policy, rule-decided leanings are binding unless a reason names a fact, status is shown.
Run: python tests/test_agent_35.py   (needs the gitignored data of development seed 1515; skipped otherwise)"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
DATA = os.path.join(ROOT, "data", "synthetic_v2_r2_1515")


def _env(version="3.5"):
    import agent_tools as at
    return at.Environment(DATA, os.path.join(DATA, "view"), seed=1, version=version)


def _sample(env, pid):
    resp = env.call("request_records", {"provider_id": pid, "sample": {"kind": "random", "n": 30}})
    if resp.get("deficiencies") and resp.get("rounds_left", 0) > 0:
        resp = env.call("follow_up_records", {"provider_id": pid, "addressed_codes": [d["code"] for d in resp["deficiencies"]]})
    return resp


def test_advice_equals_the_workflow_policy_and_is_only_in_v35():
    import agent
    import make_v2_office_workflow_runs as mw
    view, office, flagged = mw.build_view("a35test_1515", "r2_1515", "eb_ratio_t_10", version="2.5", tier1_n=11)
    asked = {p for p, st in office.state.items() if st["round"] > 0}
    env, env34 = _env(), _env("3.4")
    assert "Version 3.5" in agent.SYSTEM_35 and agent.SYSTEM_35.startswith(agent.SYSTEM_34)
    for pid in env.rows:                                                                       # ask-or-skip advice for the whole panel equals who the workflow asks
        assert (env.call("advise_next_step", {"provider_id": pid})["recommended"] == "ASK") == (pid in asked), pid
    table = env.call("screen_providers", {"method": "eb_ratio_t", "top_pct": 10})["table"]
    assert table["cols"][-1] == "ask_advice" and all(r[-1] in ("ASK", "SKIP") for r in table["rows"])
    for pid in list(office.policy_log)[:4]:
        resp = _sample(env, pid)
        assert resp["advice"]["recommended"] == office.policy_log[pid][1], (pid, resp["advice"], office.policy_log[pid])
        assert "advice" not in _sample(env34, pid)
    assert env.advice_summary()["actions"] >= 4


def test_rules_are_binding_unless_a_reason_names_a_fact():
    env = _env()
    for pid in sorted(env.rows, key=lambda p: -float(env.rows[p]["share_99215"])):
        _sample(env, pid)
        if not env.office.state[pid]["usable"]:
            continue
        out = env.call("hybrid_review", {"provider_ids": [pid]})
        if env.rule_result[pid][1] in ("summary_rule", "chart_rule"):
            break
    else:
        print("no rule-decided provider found"); return
    rules = env.rule_result[pid][0]
    other = "inconclusive" if rules != "inconclusive" else "pattern_consistent_with_upcoding"
    f = {"provider_id": pid, "leaning": other, "headline": "h", "interpretation": "i"}
    got = env.call("submit_findings", {"findings": [f]})
    assert "binding" in got["error"] and pid in got["refused"]
    got = env.call("submit_findings", {"findings": [{**f, "override_reason": "I just think the doctor is fine, nothing else to add here."}]})
    assert "binding" in got["error"]
    claim = env.claims[pid][0]["claim_id"]
    got = env.call("submit_findings", {"findings": [{**f, "override_reason": f"claim {claim} shows a note the rules do not read as upcoding"}]})
    assert "binding" not in got.get("error", "") and env.overrides and env.overrides[0]["provider"] == pid
    same = _env()
    assert "binding" not in same.call("submit_findings", {"findings": []}).get("error", "")


def test_status_is_shown_and_earlier_versions_are_unchanged():
    env = _env()
    pid = next(iter(env.rows))
    _sample(env, pid)
    text = env.practice_status()
    assert "Rounds sent so far" in text and pid in text
    e34 = _env("3.4")
    assert e34.v34 and not e34.v35 and "ask_advice" not in e34.call("screen_providers", {"method": "eb_ratio_t", "top_pct": 10})["table"]["cols"]


if __name__ == "__main__":
    if not os.path.isdir(DATA):
        print("skipped (no development data)")
    else:
        test_advice_equals_the_workflow_policy_and_is_only_in_v35()
        test_rules_are_binding_unless_a_reason_names_a_fact()
        test_status_is_shown_and_earlier_versions_are_unchanged()
        print("ok")
