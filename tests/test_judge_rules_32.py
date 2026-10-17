"""Tests for the release 2 rule judge j3.2 (issue 93). Run: python tests/test_judge_rules_32.py"""
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "eval"))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import judge_rules as j23  # noqa: E402
import judge_rules_32 as j32  # noqa: E402
import summary_rules as sr  # noqa: E402
from test_summary_rules import packet  # noqa: E402

FACTS = {"C0000012": {"cpt": "99215", "age": "40", "chronic": "1"},
         "C0000010": {"cpt": "99215", "age": "55", "chronic": "0", "mdm": "low", "minutes": "15"},
         "C0000011": {"cpt": "99215", "age": "70", "chronic": "4", "mdm": "high", "minutes": "45"}}


def rec(summary, passed=True):
    return {"citation_check": {"passed": passed}, "summary": summary}


def score(summary, pk, evidence="", dq=None):
    return j32.score_summary(rec(summary), pk, evidence, FACTS, dq)


def test_versions_are_separate():
    assert j23.VERSION == "j2.3" and j32.VERSION == "j3.2"


def test_evidence_tiers_use_the_judges_own_thresholds():
    assert j32.evidence_tier(packet(bad=6)) == "charts_show_upcoding"          # 60% below billed, peer 8%
    assert j32.evidence_tier(packet(bad=1)) == "charts_support_billing"        # 10% below billed on 10 documented 99215
    assert j32.evidence_tier(packet(docs_total=3, n99215=3, bad=2)) == "no_charts"
    assert j32.evidence_tier(packet(bad=2)) == "mixed"                         # 20%: neither


def test_leaning_must_fit_the_evidence():
    strong, weak = packet(bad=6), packet(bad=1, share=0.1)
    up = sr.assemble(weak, sr.UPCODING)
    assert "overstated" in score(up, weak)["deductions"]                       # upcoding although the charts support billing
    inc = sr.assemble(strong, sr.INCONCLUSIVE)
    assert "understated_leaning" in score(inc, strong)["deductions"]
    ha = sr.assemble(strong, sr.HIGH_ACUITY)
    assert score(ha, strong)["deductions"].get("overstated") == 1.5
    ok = sr.assemble(strong, sr.UPCODING)
    assert not {"overstated", "weak_basis", "understated_leaning"} & set(score(ok, strong)["deductions"])
    sure = dict(ok, leaning=sr.INCONCLUSIVE, rationale=ok["rationale"] + " The notes clearly confirm it.")
    assert "certainty" not in score(sure, strong)["deductions"]                # strong charts: certainty allowed
    assert "certainty" in score(dict(sure), packet(bad=2))["deductions"]


def test_citation_support_checks_stated_facts_against_the_rows():
    pk = packet(bad=6)
    s = sr.assemble(pk, sr.UPCODING)
    n, bad = j32.citation_support(s, FACTS)
    assert n > 0 and bad == []
    wrong = dict(s, rationale=s["rationale"].replace("aged 40", "aged 51"))
    n2, bad2 = j32.citation_support(wrong, FACTS)
    assert len(bad2) == 1 and "age 51" in bad2[0]
    assert "citation_support" in score(wrong, pk)["deductions"]


def test_dollars_need_a_reliable_random_estimate():
    pk = packet(bad=6)
    s = sr.assemble(pk, sr.UPCODING)
    s["rationale"] += " The extrapolated overpayment is $12,400."
    assert "dollars" in score(s, pk)["deductions"]
    good = 'estimate_overpayment output: {"valid_for_extrapolation": true, "point_estimate": 12400, "reliable": true}'
    assert "dollars" not in score(s, pk, good)["deductions"]
    unreliable = 'estimate_overpayment output: {"valid_for_extrapolation": true, "point_estimate": 12400, "reliable": false}'
    assert "dollars" in score(s, pk, unreliable)["deductions"]


def test_checklist_items_and_the_data_caveat():
    pk = packet(bad=6)
    s = sr.assemble(pk, sr.UPCODING)
    cl = score(s, pk)["checklist"]
    assert cl["observed_vs_expected"] and cl["chart_state"] and cl["citations_valid"] and cl["data_caveat"] is None
    assert score(s, pk, dq=True)["checklist"]["data_caveat"] is False
    with_caveat = dict(s, rationale=s["rationale"] + " Data caveat (low confidence): diagnosis codes look capped.")
    assert score(with_caveat, pk, dq=True)["checklist"]["data_caveat"] is True
    no_exp = dict(s, rationale=s["rationale"].replace("against an expected 5.0% given patient complexity", ""))
    assert score(no_exp, pk)["checklist"]["observed_vs_expected"] is False
    told = dict(s, rationale=s["rationale"] + " That is 4.0 times the expected share.")
    assert score(told, pk)["checklist"]["excess_stated"] is True


def test_next_steps_must_fit_the_leaning():
    pk = packet(bad=6)
    s = sr.assemble(pk, sr.UPCODING)
    s["next_steps"] = ["Close the case for C0000010 and C0000012; nothing further."]
    out = score(s, pk)
    assert "steps_do_not_fit" in out["deductions"] and out["checklist"]["next_step_fits_leaning"] is False


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
