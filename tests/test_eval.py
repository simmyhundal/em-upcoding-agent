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
    md = run_eval.render(res, 10, None, TRUTH)
    assert "pending" in md and "Plain z-score" in md and "Caveats" in md


def _record(pid, leaning, passed=True):
    return {"provider_id": pid, "summary": {"leaning": leaning},
            "citation_check": {"passed": passed, "n_cited": 3, "n_valid": 3 if passed else 2}}


def test_leaning_stats_counts_precision_and_excludes_rejected():
    roles = {p: v["role"] for p, v in TRUTH["providers"].items()}
    up = [p for p, r in roles.items() if r == "upcoder"]
    hn = [p for p, r in roles.items() if r == "hard_negative"]
    nm = [p for p, r in roles.items() if r == "normal"]
    U, H, I = ("pattern_consistent_with_upcoding", "pattern_consistent_with_high_acuity_panel", "inconclusive")
    recs = [_record(up[0], U), _record(up[1], U), _record(up[2], I), _record(hn[0], U), _record(hn[1], H),
            _record(nm[0], U), _record(nm[1], H), _record(nm[2], H, passed=False)]
    L = run_eval.leaning_stats(recs, TRUTH)
    assert L["scored"] == 7 and L["rejected"] == 1                 # the rejected one is not scored
    assert L["upcoding_calls"] == 4 and L["true_upcoders_called"] == 2
    assert abs(L["precision"] - 0.5) < 1e-9 and abs(L["recall"] - 2 / 3) < 1e-9
    assert L["honest_called_upcoding"] == 2 and L["honest_total"] == 4
    assert L["table"]["upcoder"]["inconclusive"] == 1


def test_report_includes_leaning_table_and_multiple_runs():
    res = run_eval.evaluate([{k: str(v) for k, v in r.items()} for r in ROWS], TRUTH, top_n=10)
    roles = {p: v["role"] for p, v in TRUTH["providers"].items()}
    p0 = next(p for p, r in roles.items() if r == "upcoder")
    runs = [("run A", [_record(p0, "pattern_consistent_with_upcoding")]), ("run B", [_record(p0, "inconclusive")])]
    md = run_eval.render(res, 10, runs, TRUTH)
    assert "### run A" in md and "### run B" in md and "Honest providers labeled upcoding" in md


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
