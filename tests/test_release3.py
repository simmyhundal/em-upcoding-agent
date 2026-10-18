"""Tests for workflow v2.3 (issue 99): the eb_ratio_t screen and the two-tier records policy. Run: python tests/test_release3.py
Rules 2.3 are tested in tests/test_summary_rules.py."""
import os
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
sys.path.insert(0, os.path.join(ROOT, "tests"))
import agent  # noqa: E402
import agent_tools as at  # noqa: E402
import derive  # noqa: E402
import flagging  # noqa: E402
import generate_v2 as g  # noqa: E402
import screen_methods as sm  # noqa: E402
import summary_lint  # noqa: E402
import summary_rules as sr  # noqa: E402
import workflow_policy_23 as wp23  # noqa: E402

D = tempfile.mkdtemp()
KEY = os.path.join(tempfile.mkdtemp(), "k.json")
g.build(D, KEY, seed=41, n_providers=60, n_upcoders=5, n_hard_neg=4, data_version="2.2")
VIEW = os.path.join(D, "view")
derive.build_view(D, VIEW)


def test_eb_ratio_t_is_a_separate_score_and_the_release_2_scores_are_unchanged():
    t = sm.score_t(VIEW)
    core = sm.score_core(VIEW)
    assert set(t) == set(core["eb_ratio"]) and t != core["eb_ratio"]
    assert set(core) == {"riskadj", "priority", "eb_ratio", "_expected"}              # score_core still returns exactly what v2.2 and v3.2 used
    rows = flagging.flag(VIEW, method="eb_ratio_t", top_pct=10)
    top = [r["provider_id"] for r in sorted(rows, key=lambda r: r["rank"])][:6]
    assert top == sorted(t, key=lambda p: (-t[p], p))[:6] and sum(r["flagged"] for r in rows) == 6 and rows[0]["screen_method"] == "eb_ratio_t"


class FakeOffice:
    """Records what the policy asks for; every provider returns 12 charts with a given late-signature rate."""
    max_rounds = 5

    def __init__(self, late, n_top=2):
        self.late, self.n_top, self.log, self.state = late, n_top, [], {}

    def send_request(self, pid, sample, deadline=30):
        self.log.append((pid, sample["kind"]))
        usable = {}
        for i in range(12):
            usable[f"{pid}-{i}"] = {"claim_id": f"{pid}-{i}", "note_id": f"N{i}", "late": "1" if i < round(12 * self.late) else "0"}
        self.state[pid] = {"round": len([x for x in self.log if x[0] == pid]), "usable": usable}
        return {"ok": True}

    def follow_up(self, pid, codes, deadline=30):
        return {"ok": True}

    def request_audit_trail(self, pid, ids):
        self.log.append((pid, "audit"))

    def close_request(self, pid, note):
        pass


def test_policy_23_light_tier_asks_once_unless_the_notes_show_cloning():
    claims = {p: [{"claim_id": f"{p}-{i}", "cpt": "99214" if i < 12 else "99215"} for i in range(40)] for p in ("a", "b", "c", "d")}   # 12 usable charts, none 99215; 28 billed 99215
    orig = wp23.cloning_signs
    wp23.cloning_signs = lambda rows, by_id: len(rows) >= 8 and sum(r["late"] == "1" for r in rows) / len(rows) >= 0.12
    try:
        quiet = FakeOffice(late=0.0)
        wp23.run_policy_23(quiet, ["a", "b", "c", "d"], claims, tier1_n=2)
        assert [x for x in quiet.log if x[0] in ("c", "d")] == [("c", "random"), ("d", "random")]            # light tier: one request, nothing more
        assert ("a", "targeted") in quiet.log and ("b", "targeted") in quiet.log and not any(x[1] == "audit" for x in quiet.log)   # tier 1: full policy
        loud = FakeOffice(late=0.5)
        wp23.run_policy_23(loud, ["a", "b", "c", "d"], claims, tier1_n=2)
        assert ("c", "targeted") in loud.log and ("c", "audit") in loud.log                                    # cloning signs escalate the light tier
        assert ("a", "audit") in loud.log
    finally:
        wp23.cloning_signs = orig


def test_agent_v33_screen_prompt_and_rules():
    e32, e33 = at.Environment(D, VIEW, version="3.2"), at.Environment(D, VIEW, version="3.3")
    t = sm.score_t(VIEW)
    out = e33.screen_providers(method="eb_ratio_t", top_pct=10)
    k = flagging.top_n_from_pct(len(e33.rows), 10)
    assert out["selected"] == k and [r[0] for r in out["table"]["rows"]][:k] == sorted(t, key=lambda p: (-t[p], p))[:k]
    assert "error" in e32.screen_providers(method="eb_ratio_t")                            # 3.2 is unchanged
    enum = lambda e: [x for x in e.tool_schemas() if x["name"] == "screen_providers"][0]["input_schema"]["properties"]["method"]["enum"]
    assert "eb_ratio_t" in enum(e33) and "eb_ratio_t" not in enum(e32)
    assert e33.v31 and e33.v32 and e33.v33 and not e32.v33 and e33.scores32["eb_ratio"] == e32.scores32["eb_ratio"]          # 3.3 keeps every 3.2 tool and score
    assert "Version 3.3" in agent.SYSTEM_33 and agent.SYSTEM_33.startswith(agent.SYSTEM_32) and "Version 3.3" not in agent.SYSTEM_32


def test_lint_accepts_a_rules_23_upcoding_call_only_in_v33():
    import test_summary_rules as ts
    sig = {"note_signals": {"notes": 30, "audit_trail_received": False, "rates": {"late": 0.2, "problems": 0.2}}}
    pk = ts.packet(bad=1, share=0.3, extra=sig)                                              # documentation supports billing, share 15x expected, 20% late
    assert sr.rule_leaning_23(pk)[0] == sr.UPCODING and sr.rule_leaning_22(pk)[0] == sr.INCONCLUSIVE
    assert summary_lint.leaning_supported(sr.UPCODING, pk, rules23=True) and not summary_lint.leaning_supported(sr.UPCODING, pk)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
