"""Agent v5.0 (issue 128): mirrors workflow v4.0 in the tool environment. Needs the data 4.0 development seeds (skipped otherwise). Run: python tests/test_agent_50.py"""
import csv
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent  # noqa: E402
import agent_tools as at  # noqa: E402
import policy_40  # noqa: E402
import summary_rules as sr  # noqa: E402

DATA = os.path.join(ROOT, "data", "synthetic_v2_d4_1616")


def _env(version="5.0"):
    return at.Environment(DATA, os.path.join(DATA, "view"), seed=1, version=version, records_budget=22)


def _sample(env, pid):
    r = env.call("request_records", {"provider_id": pid, "sample": {"kind": "random", "n": 30}})
    if r.get("deficiencies") and r.get("rounds_left", 0) > 0:
        r = env.call("follow_up_records", {"provider_id": pid, "addressed_codes": [d["code"] for d in r["deficiencies"]]})
    return r


def test_prompt_and_tools():
    assert "Version 5.0" in agent.SYSTEM_50 and agent.SYSTEM_50.startswith(agent.SYSTEM_35)
    if not os.path.isdir(DATA):
        print("skipped (no data 4.0 development seed)")
        return
    env, old = _env(), _env("3.5")
    enum = next(t for t in env.tool_schemas() if t["name"] == "screen_providers")["input_schema"]["properties"]["method"]["enum"]
    assert "eb_upper_t" in enum and "eb_upper_t" not in next(t for t in old.tool_schemas() if t["name"] == "screen_providers")["input_schema"]["properties"]["method"]["enum"]


def test_screen_list_and_ask_advice_equal_workflow_v40():
    if not os.path.isdir(DATA):
        return
    env = _env()
    table = env.call("screen_providers", {"method": "eb_upper_t", "top_pct": 10})["table"]
    flagged = [r for r in csv.DictReader(open(os.path.join(ROOT, "experiments", "d4_1616", "flagged_eb_upper_t_10.csv"))) if r["flagged"] == "True"]
    model = policy_40.load_ask()
    want = {r["provider_id"]: "ASK" if policy_40.ask_linear(model, r) else "SKIP" for r in flagged}
    assert {r[0]: r[-1] for r in table["rows"]} == want and len(want) == 22
    assert env.call("advise_next_step", {"provider_id": next(iter(want))})["recommended"] in ("ASK", "SKIP")


def test_stop_advice_after_the_first_sample_and_rules_decide():
    if not os.path.isdir(DATA):
        return
    env = _env()
    table = env.call("screen_providers", {"method": "eb_upper_t", "top_pct": 10})["table"]
    pid = next(r[0] for r in table["rows"] if r[-1] == "ASK")
    got = _sample(env, pid)
    assert got["advice"]["recommended"] == "STOP"
    env.call("hybrid_review", {"provider_ids": [pid]})
    assert env.rule_result[pid][1] != "chart_rule"                                   # no separate chart-rule call: the rules decide, as in the workflow


def test_demand_floor_withdraws_a_call_whose_estimate_is_below_the_cost_of_a_demand():
    data = os.path.join(ROOT, "data", "synthetic_v2_d4_1515")
    if not os.path.isdir(data):
        return
    pid = "1000000033"                                                               # called by rules 4.0 in the frozen workflow on this seed
    for estimate, kept in ((10.0, False), (5000.0, True)):
        env = at.Environment(data, os.path.join(data, "view"), seed=1, version="5.0", records_budget=22)
        _sample(env, pid)
        assert env.call("hybrid_review", {"provider_ids": [pid]})["results"][0]["leaning"] == sr.UPCODING
        env._demand_estimate = lambda p, e=estimate: (e, 276.0)
        res = env.call("submit_findings", {"findings": [{"provider_id": pid, "leaning": sr.UPCODING, "headline": "x", "interpretation": "y"}],
                                           "set_aside": [{"provider_id": c, "reason": "test"} for c in sorted(env.screen_candidates) if c != pid]})
        assert "error" not in res, res
        assert (env.findings[pid]["leaning"] == sr.UPCODING) == kept and (pid in res.get("withdrawn_below_the_demand_floor", {})) == (not kept)


def test_style_repair_is_applied_to_findings():
    if not os.path.isdir(DATA):
        return
    env = _env()
    table = env.call("screen_providers", {"method": "eb_upper_t", "top_pct": 10})["table"]
    pid = next(r[0] for r in table["rows"] if r[-1] == "ASK")
    _sample(env, pid)
    env.call("hybrid_review", {"provider_ids": [pid]})
    res = env.call("submit_findings", {"findings": [{"provider_id": pid, "leaning": sr.INCONCLUSIVE, "headline": "A headline quoting 77% and 12 of 15 charts nowhere in the rationale", "interpretation": "Scripted."}],
                                       "set_aside": [{"provider_id": c, "reason": "test"} for c in sorted(env.screen_candidates) if c != pid]})
    assert "error" not in res, res
    import summary_lint
    assert summary_lint.style_defects(env.findings[pid]) == []


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
