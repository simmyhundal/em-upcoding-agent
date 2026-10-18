"""Tests for the deterministic summary parts and the number check. Run: python tests/test_summary_rules.py"""
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "eval"))
import numcheck  # noqa: E402
import summary_rules as sr  # noqa: E402


def packet(docs_total=30, n99215=10, bad=6, peer=0.08, share=0.2, exp=0.05, extra=None):
    d = {"claims_with_documentation": docs_total, "share_of_claims_documented": 0.1,
         "by_billed_level": ([{"billed_cpt": "99215", "documented_claims": n99215, "documentation_does_not_support_billed_level": bad,
                               "unsupported_rate": bad / n99215 if n99215 else 0, "all_provider_unsupported_rate": peer}] if n99215 else []),
         "examples_documentation_below_billed_level": [{"claim_id": "C0000010", "billed_cpt": "99215", "documented_mdm_level": "low",
                                                       "documented_minutes": 15}],
         "examples_99215_documentation_supports": [{"claim_id": "C0000011", "billed_cpt": "99215", "documented_mdm_level": "high",
                                                    "documented_minutes": 45}]}
    d.update(extra or {})
    card = {"claim_id": "C0000012", "cpt": "99215", "date": "2024-02-01", "patient_id": "P0001-N0001", "age": 40,
            "chronic_conditions": 1, "conditions": "hypertension", "diagnosis_codes": "I10"}
    return {"provider_id": "P0001", "n_claims": 400, "n_patients": 150, "billed_mix": {"99213": 100, "99214": 200, "99215": 80, "99211": 5, "99212": 15},
            "share_99215": share, "expected_share_given_patient_complexity": exp, "z_vs_peers": 3.1, "risk_adjusted_score": 6.2,
            "99215_share_by_patient_complexity": [{"chronic_conditions": "0", "visits": 100, "n_99215": 30, "provider_99215_share": 0.3,
                                                   "all_provider_99215_share": 0.02},
                                                  {"chronic_conditions": "3", "visits": 100, "n_99215": 10, "provider_99215_share": 0.1,
                                                   "all_provider_99215_share": 0.06}],
            sr.LOW_KEY: [card], sr.HIGH_KEY: [], sr.COMPARE_KEY: [], "documentation_review": d}


def test_rules_22_cap_the_peer_rate_so_noisy_peers_do_not_blind_the_chart_rule():
    # data 2.2: honest coding errors lift the peer unsupported rate on 99215 charts to 54%; the frozen rule can then never lean upcoding
    noisy = packet(bad=6, n99215=9, peer=0.536, share=0.3)
    assert sr.rule_leaning(noisy)[0] is None                                          # frozen: 67% is not 3 times 54%, and "supports billing" is true up to 80%
    lean, reason = sr.rule_leaning_22(noisy)
    assert lean == sr.UPCODING and "capped at 15%" in reason
    assert sr.rule_leaning_22(packet(bad=2, n99215=9, peer=0.536, share=0.3))[0] == sr.INCONCLUSIVE   # 22%: not upcoding, rules leave it inconclusive
    assert sr.rule_leaning_22(packet(bad=1, n99215=9, peer=0.536, share=0.1))[0] == sr.HIGH_ACUITY       # clean charts, share within 3x expected
    # below the cap (every release 1 run) rules 2.2 decide exactly as before, apart from the inconclusive-by-rule cases
    for kw in ({"bad": 6}, {"bad": 1, "share": 0.1}, {"bad": 3}, {"n99215": 0}):
        a, b = sr.rule_leaning(packet(**kw)), sr.rule_leaning_22(packet(**kw))
        assert b[0] == a[0] or (a[0] is None and b[0] == sr.INCONCLUSIVE)
    pk = packet(bad=6, n99215=9, peer=0.536, share=0.3)
    sr.rule_leaning_22(pk)
    assert pk["documentation_review"]["by_billed_level"][0]["all_provider_unsupported_rate"] == 0.536       # the packet is not modified


def test_rules_23_lean_upcoding_on_late_signatures_when_the_share_is_far_above_expected():
    sig = lambda late, notes=30: {"note_signals": {"notes": notes, "audit_trail_received": False, "rates": {"late": late, "problems": 0.2}}}
    base = dict(bad=1, share=0.3)                                                  # documentation supports billing, share 15x expected: rules 2.2 say inconclusive
    assert sr.rule_leaning_22(packet(**base))[0] == sr.INCONCLUSIVE
    assert sr.rule_leaning_23(packet(**base))[0] == sr.INCONCLUSIVE                # no note signals: unchanged
    lean, reason = sr.rule_leaning_23(packet(extra=sig(0.2), **base))
    assert lean == sr.UPCODING and "rules 2.3" in reason
    assert sr.rule_leaning_23(packet(extra=sig(0.05), **base))[0] == sr.INCONCLUSIVE        # few late signatures
    assert sr.rule_leaning_23(packet(extra=sig(0.2, notes=5), **base))[0] == sr.INCONCLUSIVE  # too few notes to read rates from
    assert sr.rule_leaning_23(packet(bad=1, share=0.1, extra=sig(0.2)))[0] == sr.HIGH_ACUITY  # a decided call is never overridden
    assert sr.rule_leaning_23(packet(bad=6, extra=sig(0.0)))[0] == sr.UPCODING
    # the ask-the-model case (notes claim data review the claims do not show) is also decided when the late signal is there
    ask = {"documented_data_reviewed_moderate_or_higher": 10, "of_those_with_no_lab_or_test_line_on_the_claim": 6}
    assert sr.rule_leaning_23(packet(extra={**ask, **sig(0.2)}, **base))[0] == sr.UPCODING
    assert sr.rule_leaning_23(packet(extra=ask, **base))[0] is None


def test_rule_leaning_cases():
    assert sr.rule_leaning(packet(bad=6))[0] == sr.UPCODING                          # 60% unsupported, peer 8%
    assert sr.rule_leaning(packet(bad=1, share=0.1))[0] == sr.HIGH_ACUITY            # 10% unsupported, share within 3x expected
    assert sr.rule_leaning(packet(bad=1, share=0.3))[0] is None                      # documentation fine but share far above expected
    assert sr.rule_leaning(packet(bad=3))[0] is None                                 # 30%: between the cutoffs
    assert sr.rule_leaning(packet(docs_total=3, n99215=3, bad=2))[0] == sr.INCONCLUSIVE
    assert sr.rule_leaning(packet(n99215=0))[0] is None                              # no documented 99215 and thin pool
    assert sr.rule_leaning(packet(extra={"documented_data_reviewed_moderate_or_higher": 10,
                                         "of_those_with_no_lab_or_test_line_on_the_claim": 6}, bad=6))[0] is None   # data claims unsupported


def test_assemble_is_deterministic_and_cites_only_packet_claims():
    p = packet(bad=6)
    a, b = sr.assemble(p, sr.UPCODING), sr.assemble(p, sr.UPCODING)
    assert a == b and set(a) == {"headline", "leaning", "rationale", "cited_claim_ids", "next_steps"}
    assert set(a["cited_claim_ids"]) <= {"C0000010", "C0000012", "C0000011"} and a["cited_claim_ids"]
    assert "20.0%" in a["rationale"] and "60%" in a["rationale"] and "C0000010" in a["rationale"]
    m = sr.assemble(p, sr.INCONCLUSIVE, "Headline", "Model words here.")
    assert "Model words here." in m["rationale"] and m["headline"] == "Headline"


def test_numcheck_accepts_card_numbers_and_flags_invented_ones():
    p = packet(bad=6)
    good = sr.assemble(p, sr.UPCODING)
    assert numcheck.verify(good, p)["unverified"] == []
    bad = dict(good, rationale=good["rationale"] + " The provider overbilled by 4321 claims and 77.7% of visits.")
    assert set(numcheck.verify(bad, p)["unverified"]) == {"4321", "77.7"}


def test_numcheck_ignores_plural_cpt_codes_and_ten_digit_provider_ids():
    p = packet(bad=6)
    good = sr.assemble(p, sr.UPCODING)
    ok = dict(good, rationale=good["rationale"] + " Provider 1000000043 has many 99215s and some 99214s.")
    assert numcheck.verify(ok, p)["unverified"] == []


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
