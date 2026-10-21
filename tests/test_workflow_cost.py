"""Tests for the workflow v2.2 cost changes (issue 91): rules 2.2 and running without the LLM judge. Run: python tests/test_workflow_cost.py"""
import inspect
import os
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import summary_rules as sr  # noqa: E402


def test_rules_22_reasons_are_rule_leaning_reasons():
    src = inspect.getsource(sr.rule_leaning) + inspect.getsource(sr._pooled)
    for reason in sr.RULES_22_INCONCLUSIVE:
        assert f'"{reason}"' in src, reason          # a renamed reason would silently stop rules 2.2 from applying


def test_rules_22_only_fills_listed_gaps():
    real = sr.rule_leaning
    try:
        for lean, reason in [(None, sr.RULES_22_INCONCLUSIVE[0]), (None, "notes claim data reviewed that the claims do not show"),
                             (sr.UPCODING, "x"), (sr.HIGH_ACUITY, "y"), (sr.INCONCLUSIVE, "z")]:
            sr.rule_leaning = lambda p, lean=lean, reason=reason: (lean, reason)
            got = sr.rule_leaning_22({})
            if lean is None and reason in sr.RULES_22_INCONCLUSIVE:
                assert got[0] == sr.INCONCLUSIVE and got[1].startswith(reason)
            else:
                assert got == (lean, reason)       # decided cases, and the case that still goes to the model, are untouched
    finally:
        sr.rule_leaning = real


def _fake_run_dirs():
    import make_v2_ai_runs as ai
    root = tempfile.mkdtemp()
    src = os.path.join(root, "experiments", "c")
    os.makedirs(src)
    os.makedirs(os.path.join(root, "data", "synthetic_v2_c", "view"))
    for name in ("flagged.csv", "flagged_threshold.csv", "documentation.csv", "records_requests.csv"):
        open(os.path.join(src, name), "w").write("provider_id,flagged\n")
    calls = []
    ai.ROOT, ai.sh = root, lambda *a: calls.append(a)
    return ai, root, calls


def test_ai_run_without_llm_judge():
    ai, root, calls = _fake_run_dirs()
    ai.run("r22", "c", "note", v21=True, v22=True, llm_judge=False)
    scripts = [c[0] for c in calls]
    assert "eval/judge_usefulness.py" not in scripts
    writer = next(c for c in calls if c[0] == "src/case_summary.py")
    assert "--v22" in writer and "--v21" not in writer
    assert "no LLM usefulness judge" in open(os.path.join(root, "experiments", "r22", "README.md")).read()


def test_ai_run_default_keeps_llm_judge():
    ai, root, calls = _fake_run_dirs()
    ai.run("r21", "c", "note", v21=True)
    assert "eval/judge_usefulness.py" in [c[0] for c in calls]
    assert "--v21" in next(c for c in calls if c[0] == "src/case_summary.py")


def test_office_workflow_flags_by_version():
    import make_v2_office_workflow_runs as ow
    seen = {}

    class Office:
        def write_transcript(self, path):
            pass
    real_bv, real_run = ow.build_view, ow.ai.run
    try:
        ow.build_view = lambda rid, src, screen, version="2.0": ("/tmp/view_x", Office(), "/tmp/flagged_x.csv")
        ow.ai.run = lambda *a, **k: seen.update({"k": k})
        for v in ("2.0", "2.1", "2.2", "2.3", "2.4", "2.5", "4.0"):
            seen.clear()
            ow.run("r", "c", "threshold", "n", version=v)
            k = next(iter(seen.values()))
            assert k["v22"] == (v in ("2.2", "2.3", "2.4", "2.5", "4.0")) and k["llm_judge"] == (v not in ("2.2", "2.3", "2.4", "2.5", "4.0")) and k["v21"] == (v != "2.0")
            assert k["v23"] == (v in ("2.3", "2.4", "2.5", "4.0"))
            assert k["no_model"] == (v in ("2.5", "4.0")) and k["rules40"] == (v == "4.0")       # workflow 2.5 onward calls no API at all
    finally:
        ow.build_view, ow.ai.run = real_bv, real_run


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
