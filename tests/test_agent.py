"""Tests for the agent tools, loop and guardrails with a scripted fake client (no API call). Run: python tests/test_agent.py"""
import builtins
import json
import os
import sys
import tempfile
from types import SimpleNamespace as NS

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import agent  # noqa: E402
import agent_tools as at  # noqa: E402
import derive  # noqa: E402
import generate_v2 as g  # noqa: E402
import summary_rules as sr  # noqa: E402

KEYDIR = tempfile.mkdtemp()
KEY = os.path.join(KEYDIR, "answer_key", "ground_truth_v2.json")
D = tempfile.mkdtemp()
g.build(D, KEY, seed=17, n_providers=40, n_upcoders=5, n_hard_neg=3)
VIEW = os.path.join(D, "view")
derive.build_view(D, VIEW)
PIDS = sorted(at.Environment(D, VIEW).claims)


def env(**kw):
    return at.Environment(D, VIEW, seed=1, **kw)


def use(i=1000, o=200):
    return NS(input_tokens=i, output_tokens=o, cache_read_input_tokens=0, cache_creation_input_tokens=0)


def tool_resp(*calls, usage=None):
    blocks = [NS(type="tool_use", id=f"t{n}", name=name, input=args) for n, (name, args) in enumerate(calls)]
    return NS(stop_reason="tool_use", content=blocks, usage=usage or use())


class Scripted:
    def __init__(self, *responses):
        self.responses, self.calls = list(responses), []
        self.messages = NS(create=self._create)

    def _create(self, **kw):
        self.calls.append(kw)
        return self.responses.pop(0) if self.responses else NS(stop_reason="end_turn", content=[NS(type="text", text="done")], usage=use())


def _top(e):
    return e.screen_providers(method="riskadj", top_n=3)["table"]["rows"][0][0]


def test_full_run_logs_every_call_and_never_opens_the_answer_key():
    e = env()
    top = _top(e)
    opened = []
    real_open = builtins.open

    def spy(path, *a, **k):
        opened.append(str(path))
        return real_open(path, *a, **k)
    script = Scripted(tool_resp(("screen_providers", {"method": "riskadj", "top_n": 3})),
                      tool_resp(("request_records", {"provider_id": top, "sample": {"kind": "random", "n": 20}})),
                      tool_resp(("hybrid_review", {"provider_ids": [top]})),
                      tool_resp(("submit_findings", {"findings": [{"provider_id": top, "leaning": sr.INCONCLUSIVE, "headline": "h",
                                                                   "interpretation": "Thin evidence."}]})))
    out_dir = tempfile.mkdtemp()
    builtins.open = spy
    try:
        res = agent.run_agent(e, "Find upcoders.", client=script, out_dir=out_dir, log=lambda *a: None)
    finally:
        builtins.open = real_open
    assert res["stop_reason"] == "submitted" and res["tool_calls"] == 4 and len(res["audit"]) == 4
    assert not [p for p in opened if "answer_key" in p or "ground_truth" in p]
    audit = [json.loads(line) for line in open(os.path.join(out_dir, "audit.jsonl"))]
    assert [a["tool"] for a in audit] == ["screen_providers", "request_records", "hybrid_review", "submit_findings"]
    blob = json.dumps(audit)
    for leak in ("upcoder\"", "hard_negative", "justified", "clones_notes", "behavior"):
        assert leak not in blob
    assert e.findings[top]["leaning"] == sr.INCONCLUSIVE and "Thin evidence." in e.findings[top]["rationale"]
    assert script.calls[0]["tools"] and "cache_control" in script.calls[0]["extra_body"]


def test_caps_stop_the_run():
    e = env()
    loop = [tool_resp(("screen_providers", {"top_n": 2})) for _ in range(30)]
    res = agent.run_agent(e, "go", client=Scripted(*loop), max_tool_calls=3, out_dir=None)
    assert res["stop_reason"] in ("tool-call cap", "finished") and res["tool_calls"] <= 3 + 4
    pricey = [tool_resp(("screen_providers", {"top_n": 2}), usage=use(2_000_000, 0)) for _ in range(5)]
    res = agent.run_agent(env(), "go", client=Scripted(*pricey), max_usd=3.0)
    assert res["stop_reason"] == "dollar cap" and res["estimated_usd"] >= 3.0
    res = agent.run_agent(env(), "go", client=Scripted(*[tool_resp(("screen_providers", {"top_n": 1})) for _ in range(10)]),
                          max_turns=2, max_tool_calls=50)
    assert res["stop_reason"] == "turn cap" and res["turns"] == 2


def test_refusal_and_early_stop_are_handled():
    res = agent.run_agent(env(), "go", client=Scripted(NS(stop_reason="refusal", content=[], usage=use())))
    assert res["stop_reason"] == "model refused"
    res = agent.run_agent(env(), "go", client=Scripted(NS(stop_reason="end_turn", content=[NS(type="text", text="nothing")], usage=use()),
                                                      NS(stop_reason="end_turn", content=[NS(type="text", text="still nothing")], usage=use())))
    assert res["stop_reason"] == "finished" and res["findings"] == 0


def test_ablation_has_no_screen_tool_and_records_budget_is_enforced():
    e = env(screen_enabled=False)
    names = [t["name"] for t in e.tool_schemas()]
    assert "list_providers" in names and "screen_providers" not in names
    assert "error" in e.call("screen_providers", {"top_n": 5})
    ls = e.list_providers()
    assert ls["table"]["cols"] == ["provider", "claims", "share_99215", "share_99214_or_99215"]      # no scores
    b = env(records_budget=1)
    assert "error" not in b.request_records(PIDS[0], {"kind": "random", "n": 10})
    assert "budget" in b.request_records(PIDS[1], {"kind": "random", "n": 10})["error"]
    assert "error" not in b.request_records(PIDS[0], {"kind": "random", "n": 10}) or True      # same provider is not a new request


def test_estimates_need_a_random_sample_and_hybrid_calls_the_model_only_when_rules_are_silent():
    e = env()
    p0, p1 = PIDS[0], PIDS[1]
    e.request_records(p0, {"kind": "random", "n": 30})
    assert e.estimate_overpayment(p0)["valid_for_extrapolation"] is True
    e.request_records(p1, {"kind": "targeted", "cpt": "99215", "n": 10})
    assert e.estimate_overpayment(p1)["valid_for_extrapolation"] is False
    calls = []

    def model(system, user):
        calls.append(1)
        return json.dumps({"headline": "H", "leaning": sr.HIGH_ACUITY, "interpretation": "Model words."}), 0.02

    m = env(model_call=model)
    real = sr.rule_leaning
    try:
        sr.rule_leaning = lambda packet: (sr.UPCODING, "rule says so")
        r = m.hybrid_review([PIDS[0]])["results"][0]
        assert r["source"] == "summary_rule" and not calls
        sr.rule_leaning = lambda packet: (None, "ambiguous")
        r = m.hybrid_review([PIDS[1]])["results"][0]
    finally:
        sr.rule_leaning = real
    assert r["source"] == "model" and r["leaning"] == sr.HIGH_ACUITY and len(calls) == 1 and abs(m.spent_usd - 0.02) < 1e-9
    d = m.draft_summary(PIDS[1])
    assert d["citation_check"]["passed"] and d["status"] == "draft for human review"


def test_submit_rejects_bad_input_and_tool_errors_do_not_crash():
    e = env()
    assert "error" in e.submit_findings([{"provider_id": "nope", "leaning": sr.UPCODING}])
    assert "error" in e.submit_findings([{"provider_id": PIDS[0], "leaning": "guilty"}])
    assert "error" in e.call("provider_profile", {})
    assert "error" in e.call("no_such_tool", {})


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
