"""Agent v5.1 (A5.1) mirrors workflow v4.1 (H23, N = 4): a list of the first 4, the loosened rules 4.0 chart test, the near-miss extension (once, 30 random charts), the demand floor kept.
Needs the data 4.0 development seeds (skipped otherwise). Free: no model is called. Run: python tests/test_agent_51.py"""
import builtins
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent  # noqa: E402
import agent_tools as at  # noqa: E402
import summary_rules as sr  # noqa: E402

D17 = os.path.join(ROOT, "data", "synthetic_v2_d4_1717")
D15 = os.path.join(ROOT, "data", "synthetic_v2_d4_1515")
NEAR = "1000000174"        # d4_1717: the frozen rules 4.0 say inconclusive, the loosened test calls upcoding, and the estimate is a near-miss (stored workflow run wlh23_n4_1717)


def _env(data=D17, version="5.1"):
    return at.Environment(data, os.path.join(data, "view"), seed=1, version=version, records_budget=22)


def _sample(env, pid, n=30):
    r = env.call("request_records", {"provider_id": pid, "sample": {"kind": "random", "n": n}})
    if r.get("deficiencies") and r.get("rounds_left", 0) > 0:
        r = env.call("follow_up_records", {"provider_id": pid, "addressed_codes": [d["code"] for d in r["deficiencies"]]})
    return r


def _have():
    return os.path.isdir(D17)


def test_prompt_flag_and_v50_unchanged():
    assert "Version 5.1" in agent.SYSTEM_51 and agent.SYSTEM_51.startswith(agent.SYSTEM_50) and "Version 5.1" not in agent.SYSTEM_50
    if not _have():
        print("skipped (no data 4.0 development seed)")
        return
    e51, e50 = _env(), _env(version="5.0")
    assert e51.v51 and e51.v50 and e51.v35 and not e50.v51
    t50 = e50.call("screen_providers", {"method": "eb_upper_t", "top_pct": 10})
    assert "list_note" not in t50 and len(t50["table"]["rows"]) == 22
    d50 = {t["name"]: t["description"] for t in e50.tool_schemas()}
    assert "near-miss" not in d50["request_records"] and "demand_check" not in d50["hybrid_review"]
    assert "near-miss" in {t["name"]: t["description"] for t in e51.tool_schemas()}["request_records"]


def test_the_loop_sends_system_51_for_v51_and_system_50_for_v50():
    if not _have():
        return
    from types import SimpleNamespace as NS
    seen = []

    class Client:
        class messages:
            @staticmethod
            def create(**kw):
                seen.append(kw["system"])
                return NS(content=[NS(type="text", text="done")], stop_reason="end_turn", usage=NS(input_tokens=1, output_tokens=1, cache_read_input_tokens=0, cache_creation_input_tokens=0))
    for v, want in (("5.1", agent.SYSTEM_51), ("5.0", agent.SYSTEM_50)):
        agent.run_agent(_env(version=v), "task", client=Client, max_turns=3)
        assert seen[-1] == want


def test_ask_advice_only_for_the_first_four_and_equals_the_workflow_list():
    if not _have():
        return
    env = _env()
    res = env.call("screen_providers", {"method": "eb_upper_t", "top_pct": 10})
    rows = res["table"]["rows"]
    assert "first 4" in res["list_note"] and len(rows) == 22
    ask = [r[0] for r in rows if r[-1] == "ASK"]
    assert len(ask) <= 4 and all(r[-1] == "SKIP" for r in rows[4:])                  # rows come in rank order; beyond the 4th is outside the list
    import csv
    top4 = [r["provider_id"] for r in csv.DictReader(open(os.path.join(ROOT, "experiments", "d4_1717", "flagged_eb_upper_t_10_top4.csv"))) if r["flagged"] == "True"]
    assert [r[0] for r in rows[:4]] == top4 and set(ask) <= set(top4)
    w50 = _env(version="5.0").call("screen_providers", {"method": "eb_upper_t", "top_pct": 10})["table"]["rows"]
    assert {r[0] for r in w50 if r[-1] == "ASK"} >= set(ask)                           # the 5.1 list is the part of the 5.0 ask list that sits in the first four


def test_loosened_rules_call_where_the_frozen_rules_are_silent():
    if not _have():
        return
    e51, e50 = _env(), _env(version="5.0")
    for e in (e51, e50):
        _sample(e, NEAR)
    r51 = e51.call("hybrid_review", {"provider_ids": [NEAR]})["results"][0]
    r50 = e50.call("hybrid_review", {"provider_ids": [NEAR]})["results"][0]
    assert r51["leaning"] == sr.UPCODING and r50["leaning"] != sr.UPCODING
    assert r51["leaning"] == sr.rule_leaning_40(e51._packet(NEAR), at.RULES_51)[0] and "demand_check" not in r50
    dc = r51["demand_check"]
    assert dc["near_miss"] and dc["point_estimate"] >= 2 * dc["demand_cost"] > dc["lower_bound"] and "NEAR-MISS" in dc["advice"]


def test_extension_allowed_once_for_a_near_miss_only_and_review_goes_stale():
    if not _have():
        return
    env = _env()
    _sample(env, NEAR)
    assert "error" in env.call("request_records", {"provider_id": NEAR, "sample": {"kind": "random", "n": 30}})        # before hybrid_review: refused
    env.call("close_records", {"provider_id": NEAR, "reason": "first sample done"})
    env.call("hybrid_review", {"provider_ids": [NEAR]})
    rounds0 = env.office.state[NEAR]["round"]
    assert "error" in env.call("request_records", {"provider_id": NEAR, "sample": {"kind": "random", "n": 80}})           # more than 30 charts is refused, not cut (audit replay)
    got = env.call("request_records", {"provider_id": NEAR, "sample": {"kind": "random", "n": 30}})
    assert "error" not in got, got
    assert env.advice_log[-1]["action"] == "EXT" and env.advice_log[-1]["match"] is True
    assert env.office.state[NEAR]["round"] == rounds0 + 1 and len(env.office.random_claim_ids(NEAR)) <= 60 and got["advice"]["recommended"] == "STOP"
    assert NEAR in env.extended and NEAR not in env.reviewed
    assert "error" in env.call("request_records", {"provider_id": NEAR, "sample": {"kind": "random", "n": 30}})        # once only
    res = env.call("submit_findings", {"findings": [{"provider_id": NEAR, "leaning": sr.INCONCLUSIVE, "headline": "x", "interpretation": "y"}], "set_aside": []})
    assert "error" in res and NEAR in res["missing"]                                                                  # the stale review must be redone
    env.call("hybrid_review", {"provider_ids": [NEAR]})
    assert NEAR in env.reviewed
    # a provider the review did not call upcoding (or not a near-miss) is refused
    other = next(r[0] for r in env.call("screen_providers", {"method": "eb_upper_t", "top_pct": 10})["table"]["rows"][:4] if r[0] != NEAR)
    _sample(env, other)
    env.call("hybrid_review", {"provider_ids": [other]})
    assert "error" in env.call("request_records", {"provider_id": other, "sample": {"kind": "random", "n": 30}}) or env.rule_result[other][0] == sr.UPCODING


def test_extension_and_loosened_calls_match_the_stored_workflow_run():
    if not _have():
        return
    log = json.load(open(os.path.join(ROOT, "experiments", "wlh23_n4_1717", "extension_log.json")))
    env = _env()
    _sample(env, NEAR)
    dc = env.call("hybrid_review", {"provider_ids": [NEAR]})["results"][0]["demand_check"]
    assert NEAR in log and round(dc["point_estimate"], 2) == log[NEAR]["point"] and round(dc["lower_bound"], 2) == log[NEAR]["lower_bound"]


def test_demand_floor_still_withdraws_a_call_below_the_cost_of_a_demand():
    if not os.path.isdir(D15):
        return
    pid = "1000000033"                                                               # called by rules 4.0 on d4_1515 (as in tests/test_agent_50.py)
    for estimate, kept in ((10.0, False), (5000.0, True)):
        env = _env(D15)
        _sample(env, pid)
        assert env.call("hybrid_review", {"provider_ids": [pid]})["results"][0]["leaning"] == sr.UPCODING
        env._demand_estimate = lambda p, e=estimate: (e, 276.0)
        res = env.call("submit_findings", {"findings": [{"provider_id": pid, "leaning": sr.UPCODING, "headline": "x", "interpretation": "y"}],
                                           "set_aside": [{"provider_id": c, "reason": "test"} for c in sorted(env.screen_candidates) if c != pid]})
        assert "error" not in res, res
        assert (env.findings[pid]["leaning"] == sr.UPCODING) == kept and (pid in res.get("withdrawn_below_the_demand_floor", {})) == (not kept)


def test_binding_rule_of_v35_is_kept():
    if not _have():
        return
    env = _env()
    _sample(env, NEAR)
    r = env.call("hybrid_review", {"provider_ids": [NEAR]})["results"][0]
    assert r["leaning"] == sr.UPCODING
    if env.rule_result[NEAR][2]:                                                     # chart rule also supports it: binding
        res = env.call("submit_findings", {"findings": [{"provider_id": NEAR, "leaning": sr.INCONCLUSIVE, "headline": "x", "interpretation": "y"}],
                                           "set_aside": [{"provider_id": c, "reason": "t"} for c in sorted(env.screen_candidates) if c != NEAR]})
        assert "error" in res and "refused" in res


def test_everything_the_agent_sees_is_payer_visible():
    if not _have():
        return
    opened, real = [], builtins.open

    def spy(path, *a, **k):
        opened.append(str(path))
        return real(path, *a, **k)
    builtins.open = spy
    try:
        env = _env()
        out = [env.call("screen_providers", {"method": "eb_upper_t", "top_pct": 10})]
        out.append(_sample(env, NEAR))
        out.append(env.call("hybrid_review", {"provider_ids": [NEAR]}))
        out.append(env.practice_status())
    finally:
        builtins.open = real
    text = json.dumps(out)
    assert not [p for p in opened if "answer_key" in p or "ground_truth" in p]
    assert not any(w in text for w in ("hard_negative", "ground_truth", "answer_key", '"role"', "true_net_rate", "justified"))


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
