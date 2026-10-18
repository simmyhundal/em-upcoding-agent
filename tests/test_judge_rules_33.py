"""Tests for the release 3 rule judge j3.3 (issue 99). Run: python tests/test_judge_rules_33.py"""
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "eval"))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import judge_rules_32 as j32  # noqa: E402
import judge_rules_33 as j33  # noqa: E402
import summary_rules as sr  # noqa: E402
from test_judge_rules_32 import FACTS, rec  # noqa: E402
from test_summary_rules import packet  # noqa: E402

SIG = {"note_signals": {"notes": 30, "audit_trail_received": False, "rates": {"late": 0.2, "problems": 0.2}}}


def test_j32_is_unchanged_and_j33_leaves_other_tiers_alone():
    assert j32.VERSION == "j3.2" and j33.VERSION == "j3.3"
    for pk in (packet(bad=6), packet(bad=1, share=0.1), packet(bad=2), packet(docs_total=3, n99215=3, bad=2)):
        sm = sr.assemble(pk, sr.UPCODING)
        a, b = j32.score_summary(rec(sm), pk, "", FACTS), j33.score_summary(rec(sm), pk, "", FACTS)
        assert {k: v for k, v in a.items() if k != "checklist"} == {k: v for k, v in b.items() if k != "checklist"} or a["evidence_tier"] == b["evidence_tier"]
        assert a["score"] == b["score"] and a["deductions"] == b["deductions"]
    assert j32.VERSION == "j3.2" and j32.evidence_tier is not j33.evidence_tier             # the patch is undone after every call


def test_cloning_signs_make_an_upcoding_call_supported():
    pk = packet(bad=1, share=0.3, extra=SIG)                  # charts support billing, share 15x expected, 20% late
    assert j32.evidence_tier(pk) == "charts_support_billing" and j33.evidence_tier(pk) == "cloning_signs"
    sm = sr.assemble(pk, sr.UPCODING)
    old, new = j32.score_summary(rec(sm), pk, "", FACTS), j33.score_summary(rec(sm), pk, "", FACTS)
    assert "overstated" in old["deductions"] and "overstated" not in new["deductions"] and new["score"] >= old["score"]
    assert new["evidence_tier"] == "cloning_signs"


def test_the_basis_must_be_stated_and_other_leanings_are_checked():
    pk = packet(bad=1, share=0.3, extra=SIG)
    sm = dict(sr.assemble(pk, sr.UPCODING), headline="Provider bills 99215 far above expectation.", rationale="The share is 15 times the expected share. Review the charts.")
    assert "basis_not_stated" in j33.score_summary(rec(sm), pk, "", FACTS)["deductions"]
    ok = dict(sm, rationale=sm["rationale"] + " 20% of 30 returned notes were signed late, which is consistent with notes written to match the bill.")
    assert "basis_not_stated" not in j33.score_summary(rec(ok), pk, "", FACTS)["deductions"]
    assert "understated_leaning" in j33.score_summary(rec(sr.assemble(pk, sr.INCONCLUSIVE)), pk, "", FACTS)["deductions"]
    assert j33.score_summary(rec(sr.assemble(pk, sr.HIGH_ACUITY)), pk, "", FACTS)["deductions"].get("overstated") == 1.5
    quiet = packet(bad=1, share=0.3, extra={"note_signals": {"notes": 30, "audit_trail_received": False, "rates": {"late": 0.02, "problems": 0.2}}})
    assert j33.evidence_tier(quiet) == "charts_support_billing"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
