"""Tests for the agent v3.2 cost changes (issue 92), with a scripted fake client (no API call). Run: python tests/test_agent_cost.py"""
import json
import os
import shutil
import sys
import tempfile
from types import SimpleNamespace as NS

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent  # noqa: E402
import agent_tools as at  # noqa: E402
import derive  # noqa: E402
import generate_v2 as g  # noqa: E402

D = tempfile.mkdtemp()
KEY = os.path.join(tempfile.mkdtemp(), "k.json")
g.build(D, KEY, seed=21, n_providers=40, n_upcoders=5, n_hard_neg=3, data_version="2.1", clone_signal_strength=1.0)
VIEW = os.path.join(D, "view")
derive.build_view(D, VIEW)


def use():
    return NS(input_tokens=900, output_tokens=150, cache_read_input_tokens=4000, cache_creation_input_tokens=300)


class Scripted:
    """Two turns with no tool use: the loop nudges once, then stops."""
    def __init__(self):
        self.messages = NS(create=lambda **kw: NS(stop_reason="end_turn", content=[NS(type="text", text="done")], usage=use()))


def test_turn_usage_is_logged_for_32_only():
    for version, logged in (("3.1", False), ("3.2", True)):
        out = tempfile.mkdtemp()
        agent.run_agent(at.Environment(D, VIEW, seed=1, version=version), "task", client=Scripted(), out_dir=out, log=lambda *a: None)
        path = os.path.join(out, "turn_usage.jsonl")
        assert os.path.exists(path) == logged, version
        if logged:
            rows = [json.loads(x) for x in open(path)]
            assert [r["turn"] for r in rows] == [1, 2]
            assert rows[0]["cache_read_input_tokens"] == 4000 and rows[0]["output_tokens"] == 150


def _fake_root():
    """run_agent.main reads data/ and eval/answer_key/ under its ROOT: point it at a folder holding the test data."""
    root = tempfile.mkdtemp()
    os.makedirs(os.path.join(root, "data"))
    os.symlink(D, os.path.join(root, "data", "synthetic_v2_c"))
    os.makedirs(os.path.join(root, "eval", "answer_key"))
    shutil.copy(KEY, os.path.join(root, "eval", "answer_key", "ground_truth_v2_c.json"))
    return root


class Stop(Exception):
    pass


def test_run_agent_caps_and_model_by_version():
    import run_agent
    seen = {}

    def capture(env, task, **kw):
        seen.update(kw)
        raise Stop
    real_root, real_run = run_agent.ROOT, agent.run_agent
    run_agent.ROOT, agent.run_agent = _fake_root(), capture
    try:
        for version, cap in (("3.0", 3.0), ("3.1", 3.0), ("3.2", run_agent.EVAL_MAX_USD_32)):
            seen.clear()
            try:
                run_agent.main("r", "c", version=version)
            except Stop:
                pass
            assert seen["max_usd"] == cap and seen["model"] == agent.MODEL and seen["effort"] == "medium" and seen["price_scale"] == 1.0, version
        seen.clear()
        try:
            run_agent.main("r", "c", version="3.2", model="claude-sonnet-5-5", effort="low", max_usd=0.5)
        except Stop:
            pass
        assert seen["max_usd"] == 0.5 and seen["model"] == "claude-sonnet-5-5" and seen["effort"] == "low" and seen["price_scale"] == 0.5
    finally:
        run_agent.ROOT, agent.run_agent = real_root, real_run
    assert run_agent.EVAL_MAX_USD_32 <= 1.0


def test_agent_judge_replays_office_21_for_32_and_skips_the_llm_judge():
    import judge_agent_runs as jar
    versions, judged = [], []

    class Office:
        def __init__(self, *a, version="2.0", **k):
            versions.append(version)
            self.state = {}
    root = tempfile.mkdtemp()
    os.makedirs(os.path.join(root, "experiments", "r"))
    for name in ("audit.jsonl", "office_transcript.jsonl"):
        open(os.path.join(root, "experiments", "r", name), "w").close()
    real = (jar.ROOT, jar.provider_sim.Office, jar.build_view, jar.ju.run)
    jar.ROOT, jar.provider_sim.Office = root, Office
    try:
        for v in ("3.0", "3.1", "3.2"):
            jar.replay("r", "c", v)
        assert versions == ["2.0", "2.1", "2.1"]
        jar.build_view = lambda *a: "/tmp/view"
        jar.ju.run = lambda *a, **k: judged.append(a) or []
        jar.main("r", "c", "3.2")
        assert judged == []
        jar.main("r", "c", "3.1")
        assert len(judged) == 1
    finally:
        jar.ROOT, jar.provider_sim.Office, jar.build_view, jar.ju.run = real


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
