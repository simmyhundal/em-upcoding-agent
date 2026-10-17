"""Tests for how the release 2 screens (eb_ratio, priority), defect profiles and holds are wired into the workflow and agent. Run: python tests/test_release2_wiring.py"""
import csv
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
import agent_tools as at  # noqa: E402
import data_quality as dq  # noqa: E402
import derive  # noqa: E402
import flagging  # noqa: E402
import generate_v2 as g  # noqa: E402
import screen_methods as sm  # noqa: E402

D = tempfile.mkdtemp()
KEY = os.path.join(tempfile.mkdtemp(), "k.json")
g.build(D, KEY, seed=41, n_providers=60, n_upcoders=5, n_hard_neg=4, data_version="2.2")
VIEW = os.path.join(D, "view")
derive.build_view(D, VIEW)


def test_flagging_methods_rank_by_their_own_score_and_the_default_is_unchanged():
    S = sm.score_core(VIEW)
    for m in ("eb_ratio", "priority"):
        rows = flagging.flag(VIEW, 10, method=m)
        top = [r["provider_id"] for r in sorted(rows, key=lambda r: r["rank"])][:10]
        assert top == sorted(S[m], key=lambda p: (-S[m][p], p))[:10] and sum(r["flagged"] for r in rows) == 10
        assert all(r["screen_method"] == m for r in rows)
    base, explicit = flagging.flag(VIEW, 10), flagging.flag(VIEW, 10, method="riskadj")
    assert base == explicit and "screen_method" not in base[0]
    try:
        flagging.flag(VIEW, 10, min_suspicion=5, method="eb_ratio")
    except ValueError:
        return
    raise AssertionError("a suspicion threshold must be refused for the new scores")


def test_flagging_cli_writes_the_method_columns():
    out = os.path.join(tempfile.mkdtemp(), "f.csv")
    subprocess.run([sys.executable, os.path.join(ROOT, "src", "flagging.py"), VIEW, out, "--method", "eb_ratio"], check=True, capture_output=True)
    rows = list(csv.DictReader(open(out)))
    assert rows[0]["screen_method"] == "eb_ratio" and sum(r["flagged"] == "True" for r in rows) == 25


def test_agent_screen_tool_offers_the_new_scores_only_in_v32():
    e31, e32 = at.Environment(D, VIEW, version="3.1"), at.Environment(D, VIEW, version="3.2")
    assert "error" in e31.screen_providers(method="eb_ratio")
    S = sm.score_core(VIEW)
    for m in ("eb_ratio", "priority"):
        out = e32.screen_providers(method=m, top_n=8)
        assert [r[0] for r in out["table"]["rows"]] == sorted(S[m], key=lambda p: (-S[m][p], p))[:8]
    enum = [t for t in e32.tool_schemas() if t["name"] == "screen_providers"][0]["input_schema"]["properties"]["method"]["enum"]
    assert "eb_ratio" in enum and "eb_ratio" not in [t for t in e31.tool_schemas() if t["name"] == "screen_providers"][0]["input_schema"]["properties"]["method"]["enum"]


def test_v31_screen_output_is_unchanged_by_the_wiring():
    e31 = at.Environment(D, VIEW, version="3.1")
    out = e31.screen_providers(method="priority", top_n=5)
    assert out["table"]["cols"][:7] == ["provider", "claims", "share_99215", "expected_share", "z", "z_adj", "rank_combined"] and len(out["table"]["rows"]) == 5


def test_apply_holds_adds_the_caveat_and_downgrades_unsupported_upcoding():
    report = {"per_provider": {"A": [{"flag": "dx_truncation", "detail": "40% of claims in capped months"}]}}
    recs = [{"provider_id": "A", "summary": {"leaning": "pattern_consistent_with_upcoding", "headline": "h", "rationale": "r"}},
            {"provider_id": "B", "summary": {"leaning": "pattern_consistent_with_upcoding", "headline": "h", "rationale": "r"}}]
    out, held = dq.apply_holds(recs, report, {"A": 3})
    assert held == ["A"] and out[0]["summary"]["leaning"] == "inconclusive" and "Data caveat" in out[0]["summary"]["rationale"] and out[1] == recs[1]
    out2, held2 = dq.apply_holds(recs, report, {"A": 12})
    assert held2 == [] and out2[0]["summary"]["leaning"] == "pattern_consistent_with_upcoding" and "Data caveat" in out2[0]["summary"]["rationale"]
    assert recs[0]["summary"]["rationale"] == "r"                                   # the input is not modified


def test_defect_profiles_expand_and_explicit_options_override():
    def build(**kw):
        d = tempfile.mkdtemp()
        k = os.path.join(tempfile.mkdtemp(), "k.json")
        g.build(d, k, seed=42, n_providers=40, n_upcoders=3, n_hard_neg=3, data_version="2.2", **kw)
        return json.load(open(k))
    a = build(defect_profile="moderate")["defects"]
    assert a["dx_truncation"]["cap"] == 4 and a["dx_truncation"]["months"] == [10, 11, 12] and a["duplicates"]["count"] >= 0 and "orphans" in a
    b = build(defect_profile="moderate", dx_cap=2)["defects"]
    assert b["dx_truncation"]["cap"] == 2
    assert build()["defects"].keys() == {"control_totals"}
    for bad in ({"defect_profile": "nope"},):
        try:
            build(**bad)
        except ValueError:
            continue
        raise AssertionError("unknown profile accepted")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
