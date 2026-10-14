"""Tests for the v2.1 workflow policy, the v3.1 agent tools and the note-based rule. Run: python tests/test_v31.py"""
import csv
import os
import sys
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "eval"))
import agent_tools as at  # noqa: E402
import derive  # noqa: E402
import generate_v2 as g  # noqa: E402
import provider_sim as ps  # noqa: E402
import summary_rules as sr  # noqa: E402
import workflow_policy_v21 as wp  # noqa: E402
from test_summary_rules import packet  # noqa: E402

D = tempfile.mkdtemp()
g.build(D, os.path.join(tempfile.mkdtemp(), "k.json"), seed=21, n_providers=40, n_upcoders=5, n_hard_neg=3, data_version="2.1", clone_signal_strength=1.0)
VIEW = os.path.join(D, "view")
derive.build_view(D, VIEW)
CLAIMS = {}
for r in csv.DictReader(open(os.path.join(VIEW, "claims.csv"))):
    CLAIMS.setdefault(r["provider_id"], []).append(r)
BIG = sorted(CLAIMS, key=lambda p: -len(CLAIMS[p]))[:6]


def test_v31_has_the_new_tools_and_v30_does_not():
    e31, e30 = at.Environment(D, VIEW, version="3.1"), at.Environment(D, VIEW)
    n31, n30 = {t["name"] for t in e31.tool_schemas()}, {t["name"] for t in e30.tool_schemas()}
    assert {"note_checks", "request_audit_trail"} <= n31 and not ({"note_checks", "request_audit_trail"} & n30)
    assert "error" in e30.call("note_checks", {"provider_id": BIG[0]})


def test_v31_second_request_note_checks_and_estimate_use_only_random_charts():
    e = at.Environment(D, VIEW, version="3.1", records_budget=10)
    pid = BIG[0]
    e.office._st(pid)["behavior"] = "cooperative"
    r1 = e.request_records(pid, {"kind": "random", "n": 30})
    assert "error" not in r1 and e.note_checks(pid)["notes"] > 0 or r1["usable_total"] == 0
    r2 = e.request_records(pid, {"kind": "targeted", "cpt": "99215", "n": 10})
    assert "error" not in r2 and r2["sample_kinds"] == ["random", "targeted"]
    est = e.estimate_overpayment(pid)
    assert est["valid_for_extrapolation"] and est["sampled_claims"] == len(e.office.random_claim_ids(pid))
    nc = e.note_checks(pid)
    assert set(nc["rates"]) == {"problems", "data", "unsigned", "late", "time_repeat", "duplicate", "bulk_created", "paste_heavy"}
    aud = e.request_audit_trail(pid, sorted(e.office.state[pid]["usable"])[:5])
    assert aud.get("status") in ("audit_trail_provided", "refused")
    assert "documentation" in e.provider_profile(pid)


def test_v21_workflow_policy_runs_random_then_targeted_then_audit_and_closes():
    o = ps.Office(D, VIEW, seed=1, version="2.1")
    for p in BIG:
        o._st(p)["behavior"] = "cooperative"
    wp.run_policy_v21(o, BIG, CLAIMS)
    assert all(o.state[p]["closed"] for p in BIG)
    kinds = [q["kind"] for p in BIG for q in o.state[p]["requests"]]
    assert kinds.count("random") == len(BIG)
    assert all(q["kind"] == "random" for p in BIG for q in o.state[p]["requests"][:1])          # random always first


def test_inflated_notes_rule_needs_two_signals_and_enough_notes():
    base = packet(docs_total=30, n99215=10, bad=0, share=0.3, exp=0.05)           # clean documentation, high share
    def with_signals(problems, late, notes=20, audit=False, bulk=0.0):
        pk = packet(docs_total=30, n99215=10, bad=0, share=0.3, exp=0.05)
        pk["documentation_review"]["note_signals"] = {"notes": notes, "audit_trail_received": audit,
                                                      "rates": {"problems": problems, "late": late, "unsigned": 0, "data": 0, "time_repeat": 0.1,
                                                                "duplicate": 0.1, "bulk_created": bulk, "paste_heavy": 0.0}, "examples": {}}
        return pk
    assert sr.rule_leaning(with_signals(0.45, 0.2))[0] == sr.UPCODING
    assert sr.rule_leaning(with_signals(0.45, 0.02))[0] != sr.UPCODING                  # one signal alone is not enough
    assert sr.rule_leaning(with_signals(0.45, 0.02, audit=True, bulk=0.2))[0] == sr.UPCODING
    assert sr.rule_leaning(with_signals(0.45, 0.2, notes=4))[0] != sr.UPCODING          # too few notes for a pattern
    assert sr.rule_leaning(base)[0] != sr.UPCODING


def test_v31_screen_columns_priority_candidates_and_budget_status():
    e = at.Environment(D, VIEW, version="3.1")
    r = e.screen_providers(method="priority", top_n=10)
    assert r["table"]["cols"][-4:] == ["ratio_to_expected", "excess_99215", "low_complexity_share", "excess_usd"] and len(r["table"]["rows"]) == 10
    assert e.screen_candidates == {row[0] for row in r["table"]["rows"] if row[7] >= at.CANDIDATE_RATIO}
    assert "Records budget: 0 of 15" in e.budget_status()
    assert "error" in at.Environment(D, VIEW).screen_providers(method="priority", top_n=5)             # not in v3.0


def test_v31_submit_needs_dispositions_and_refuses_unsupported_findings():
    import summary_lint
    e = at.Environment(D, VIEW, version="3.1")
    e.screen_providers(method="riskadj", top_n=10)
    cands = sorted(e.screen_candidates)
    assert cands
    miss = e.submit_findings([])
    assert "error" in miss and set(miss["missing"]) == set(cands)
    aside = [{"provider_id": c, "reason": "claims signal only; budget kept for stronger cases"} for c in cands]
    bad = e.submit_findings([{"provider_id": cands[0], "leaning": sr.HIGH_ACUITY, "headline": "h", "interpretation": "Looks like a sicker panel."}], aside[1:])
    assert "problems" in bad and any("not supported" in m for m in bad["problems"][cands[0]])                # high acuity with no charts at 3x expected
    ok = e.submit_findings([{"provider_id": cands[0], "leaning": sr.INCONCLUSIVE, "headline": "h", "interpretation": "No charts yet."}], aside[1:])
    assert ok.get("accepted") == 1 and e.set_aside and cands[0] in e.findings
    steps = e.findings[cands[0]]["next_steps"]
    assert any("request a random sample" in x.lower() for x in steps) and not summary_lint.contradictions(e.findings[cands[0]], e._packet(cands[0]))


def test_v31_estimate_is_marked_unreliable_with_few_charts_in_its_stratum():
    e = at.Environment(D, VIEW, version="3.1", records_budget=10)
    pid = BIG[1]
    e.office._st(pid)["behavior"] = "cooperative"
    e.request_records(pid, {"kind": "random", "n": 20})
    est = e.estimate_overpayment(pid)
    assert est["valid_for_extrapolation"] and "reliable" in est and "stratum_reviewed" in est
    if not est["reliable"]:
        assert est["ci_low"] is None and "Not reliable" in est["note"]
    import summary_lint
    s = {"headline": "h", "rationale": "The estimate is $5,000 (valid for extrapolation).", "next_steps": [], "leaning": sr.INCONCLUSIVE}
    assert summary_lint.unreliable_estimate_quoted(s, 'estimate_overpayment output: {"reliable": false}')
    assert not summary_lint.unreliable_estimate_quoted(s, 'estimate_overpayment output: {"reliable": true}')


def test_version_21_next_steps_never_contradict_the_facts_and_repair_keeps_only_supported_leanings():
    import summary_lint
    for kw in (dict(docs_total=0, n99215=0, bad=0), dict(docs_total=3, n99215=3, bad=1), dict(docs_total=30, n99215=10, bad=1, share=0.1), dict(bad=6)):
        pk = packet(**kw)
        for lean in (sr.UPCODING, sr.HIGH_ACUITY, sr.INCONCLUSIVE):
            s = sr.assemble(pk, lean, version="2.1")
            assert not summary_lint.contradictions(s, pk), (kw, lean)
            assert any(c.isdigit() or "C0" in c for c in " ".join(s["next_steps"]))                     # names a count or a claim
    pk = packet(docs_total=3, n99215=3, bad=0, share=0.30, exp=0.05)
    bad = sr.assemble(pk, sr.HIGH_ACUITY, "h", "A sicker panel.")
    fixed = summary_lint.repair(bad, pk)
    assert fixed["leaning"] == sr.INCONCLUSIVE and "A sicker panel." not in fixed["rationale"]
    pk2 = packet(bad=6)
    assert summary_lint.repair(sr.assemble(pk2, sr.UPCODING, "h", "Contradicts: no records requested."), pk2)["leaning"] == sr.UPCODING


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
