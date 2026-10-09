"""Tests for the eval harness. Run: python tests/test_eval.py"""
import csv
import json
import os
import sys
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "eval"))
import flagging  # noqa: E402
import generate_synthetic as g  # noqa: E402
import run_eval  # noqa: E402

D = tempfile.mkdtemp()
KEY = os.path.join(tempfile.mkdtemp(), "ground_truth.json")
g.build(D, KEY, seed=5, n_normal=40, n_upcoders=3, n_hard_neg=3)
TRUTH = json.load(open(KEY))
ROWS = flagging.flag(D, top_n=10)


def test_counts_are_consistent():
    res = run_eval.evaluate([{k: str(v) for k, v in r.items()} for r in ROWS], TRUTH, top_n=10)
    for r in res.values():
        assert r["upcoders_total"] == 3 and r["hard_neg_total"] == 3 and r["normal_total"] == 40
        assert r["upcoders_found"] + r["hard_neg_flagged"] + r["normal_flagged"] == 10
        assert len(r["upcoder_ranks"]) == 3


def test_report_renders_with_pending_llm_metrics():
    res = run_eval.evaluate([{k: str(v) for k, v in r.items()} for r in ROWS], TRUTH, top_n=10)
    md = run_eval.render(res, 10, None)
    assert "pending" in md and "Plain z-score" in md and "Caveats" in md


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
