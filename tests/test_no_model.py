"""Workflow v2.5 is deterministic and API-free: with no_model=True the writer never calls the model, and rule-silent providers come out inconclusive.
Run: python tests/test_no_model.py   (needs the gitignored data of development seed 1515; skipped otherwise)"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import case_summary as cs  # noqa: E402


def test_no_model_never_calls_and_is_deterministic():
    view = os.path.join(ROOT, "data", "synthetic_v2_r2_1515", "view")
    flagged = os.path.join(ROOT, "experiments", "r2_1515", "flagged_eb_ratio_t_10.csv")
    if not (os.path.isdir(view) and os.path.exists(flagged)):
        print("skipped (no development data)")
        return

    def boom(system, user):
        raise AssertionError("the model must not be called")
    out1 = cs.run(view, flagged, "/tmp/nm1.jsonl", llm=boom, rules="2.3", version="2.1", lint=True, no_model=True)
    out2 = cs.run(view, flagged, "/tmp/nm2.jsonl", llm=boom, rules="2.3", version="2.1", lint=True, no_model=True)
    assert all(r["source"] == "rules" for r in out1) and [r["summary"] for r in out1] == [r["summary"] for r in out2]
    silent = [r for r in out1 if r["rule_leaning"] == "inconclusive" and "no model is used" in (r["rule_reason"] or "")]
    assert all(r["summary"]["leaning"] == "inconclusive" for r in silent)


if __name__ == "__main__":
    test_no_model_never_calls_and_is_deterministic()
    print("ok")
