"""Tests for the deterministic judge (v2.1). Run: python tests/test_judge_rules.py"""
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "eval"))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import judge_rules as jr  # noqa: E402
import summary_rules as sr  # noqa: E402
from test_summary_rules import packet  # noqa: E402


def rec(summary, passed=True):
    return {"citation_check": {"passed": passed}, "summary": summary}


def good(pk, leaning):
    return sr.assemble(pk, leaning)


def test_code_written_summary_is_deterministic_and_boilerplate_next_steps_are_flagged_generic():
    pk = packet(bad=6)
    a, b = jr.score_summary(rec(good(pk, sr.UPCODING)), pk), jr.score_summary(rec(good(pk, sr.UPCODING)), pk)
    assert a == b and a["score"] == 4 and a["problems"] == ["no next step is specific (none names a claim, a count or a figure)"]
    s = good(pk, sr.UPCODING)
    s["next_steps"] = ["Request the full charts for C0000010 and C0000012 and have a coder re-score them."]
    assert jr.score_summary(rec(s), pk)["score"] == 5


def test_headline_figures_missing_from_the_body_and_understated_signals_lose_points():
    pk = packet(bad=1, share=0.3, exp=0.05)                      # 6 times expected
    s = good(pk, sr.INCONCLUSIVE)
    s["next_steps"] = ["Request charts for C0000010 and C0000012."]
    s["headline"] = "Only a modest elevation: 77.7% of visits"
    s["rationale"] = s["rationale"] + " The elevation is mild."
    r = jr.score_summary(rec(s), pk)
    assert any("understates" in p for p in r["problems"]) and any("headline figures" in p for p in r["problems"])


def test_guardrail_failure_scores_one():
    pk = packet(bad=6)
    assert jr.score_summary(rec(good(pk, sr.UPCODING), passed=False), pk)["score"] == 1


def test_unsupported_leaning_and_contradictions_lose_points():
    pk = packet(docs_total=3, n99215=3, bad=0, share=0.30, exp=0.05)           # 6x expected, almost no documents
    s = good(pk, sr.HIGH_ACUITY)
    r = jr.score_summary(rec(s), pk)
    text = " ".join(r["problems"])
    assert "not supported" in text and "fewer than 5 documented claims" in text and r["score"] <= 3
    s2 = good(pk, sr.INCONCLUSIVE)
    assert jr.score_summary(rec(s2), pk)["score"] >= 4


def test_invented_numbers_and_accusatory_words_lose_points():
    pk = packet(bad=6)
    s = good(pk, sr.UPCODING)
    s["rationale"] += " This proves fraud of 4321 dollars."
    r = jr.score_summary(rec(s), pk)
    assert any("accusatory" in p for p in r["problems"]) and r["unverified_numbers"] == ["4321"] and r["score"] == 3


def test_no_request_but_next_step_requests_records_is_flagged():
    pk = packet(docs_total=0, n99215=0, bad=0)
    s = good(pk, sr.INCONCLUSIVE)
    s["rationale"] += " Not prioritized for records."
    s["next_steps"] = ["Request records for a larger sample of this provider's 99214 and 99215 claims."]
    assert any("no records were prioritized" in p for p in jr.score_summary(rec(s), pk)["problems"])


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
