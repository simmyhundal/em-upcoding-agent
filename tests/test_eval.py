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
import template_check  # noqa: E402

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


def test_template_check_flags_templated_and_passes_varied_text():
    templated = [f"Provider P{i:04d} billed {10 + i} of {100 + i} claims as 99215. The pattern is consistent with upcoding. "
                 f"No clinical documentation is in the packet, so this cannot be confirmed." for i in range(8)]
    varied = ["The first provider shows an elevated share concentrated among healthy patients with minor complaints.",
              "Documentation for most reviewed visits supports the billed level, which points to a complex panel.",
              "Thin evidence here: only a handful of documented visits exist, and the rate is within normal range.",
              "Billing rises with complexity in a way peers also show; the gap sits in the sickest band only.",
              "Several simple acute diagnoses carry the top code, and nothing in the notes supports that level.",
              "A modest excess at every level, with no single stratum driving it, and no strong documentation signal."]
    assert template_check.check(templated)["flagged"]
    assert not template_check.check(varied)["flagged"]
    assert "skipped" in template_check.check(varied[:3])["note"]


def test_shared_caveat_sentence_alone_does_not_flag():
    # Real, varied rationales from the committed experiment, each with one identical caveat sentence added.
    path = os.path.join(HERE, "..", "experiments", "cold_agent_25_docs", "summaries.jsonl")
    real = [json.loads(line)["summary"]["rationale"] for line in open(path)][:12]
    res = template_check.check([r + " No clinical documentation is in the packet." for r in real])
    assert not res["flagged"] and res["boilerplate_sentences"] >= 1


def test_usefulness_line_reports_mean_distribution_and_target():
    rows = [{"score": 4}, {"score": 5}, {"score": 3}, {"score": 4}]
    line = run_eval.usefulness_line(rows)
    assert "mean 4.00" in line and "target >= 4: met" in line and "3: 1" in line
    assert "NOT met" in run_eval.usefulness_line([{"score": 3}, {"score": 4}])


def test_report_shows_usefulness_for_a_labeled_run():
    res = run_eval.evaluate([{k: str(v) for k, v in r.items()} for r in ROWS], TRUTH, top_n=10)
    roles = {p: v["role"] for p, v in TRUTH["providers"].items()}
    p0 = next(p for p, r in roles.items() if r == "upcoder")
    runs = [("run A", [_record(p0, "pattern_consistent_with_upcoding")])]
    md = run_eval.render(res, 10, runs, TRUTH, {"run A": [{"score": 3}, {"score": 4}]})
    assert "mean 3.50" in md and "usefulness (1-5, see eval/rubric.md): pending" not in md


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
