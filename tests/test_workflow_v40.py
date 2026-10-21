"""Workflow v4.0 (issue 131): the frozen options reproduce the loop's stored result for two development seeds, rules 4.0 call from pooled 99214 and 99215 charts and leave rules 2.3's
calls alone, the policy options behave, and the demand floor withdraws a call whose estimate is below the demand cost. Run: python tests/test_workflow_v40.py (needs development seeds; skipped otherwise)"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import summary_rules as sr  # noqa: E402
import workflow_policy_40 as wp40  # noqa: E402


def _packet(rows, **kw):
    return {"provider_id": "P", "n_claims": 300, "share_99215": 0.05, "expected_share_given_patient_complexity": 0.05,
            "documentation_review": {"claims_with_documentation": 30, "by_billed_level": rows}, **kw}


def _one(n, x, peer):
    return _packet([{"billed_cpt": "99214", "documented_claims": n, "documentation_does_not_support_billed_level": x, "unsupported_rate": x / n, "all_provider_unsupported_rate": peer}])


def test_rules_40_pool_99214_and_99215_and_leave_2_3_calls_alone():
    assert sr.rule_leaning_23(_one(10, 3, 0.05))[0] == sr.INCONCLUSIVE                                  # rules 2.3 need 12 pooled charts
    lean, reason = sr.rule_leaning_40(_one(10, 3, 0.05))
    assert lean == sr.UPCODING and "rules 4.0" in reason                                                # 3 of 10 against a 5% peer rate beats chance
    assert sr.rule_leaning_40(_one(10, 1, 0.05))[0] != sr.UPCODING                                      # a low unsupported share is not called
    assert sr.rule_leaning_40(_one(9, 4, 0.05))[0] != sr.UPCODING                                       # fewer than 10 pooled charts
    assert sr.rule_leaning_40(_one(10, 3, 0.4))[0] != sr.UPCODING                                       # does not beat a high peer rate by more than chance
    big = _one(12, 4, 0.1)
    assert sr.rule_leaning_40(big) == sr.rule_leaning_23(big)                                           # what rules 2.3 decide is left as it was


def test_frozen_options_and_defaults():
    assert wp40.FROZEN_V40 == {"screen": "eb_upper_t", "w40": {"ask": "linear", "escalate": "stop", "demand_floor": "cost"}}
    assert wp40.DEFAULTS["ask"] == "policy25" and wp40.DEFAULTS["escalate"] == "policy25" and wp40.DEFAULTS["sample_cpts"] is None and wp40.DEFAULTS["n"] == 30       # all off = policy 2.5
    model = json.load(open(wp40.ASK_MODEL))
    assert len(model["beta"]) == len(model["mu"]) + 1 and model["fit_on_batches"] == [1, 2, 3, 4] and max(model["fit_on_seeds"]) < 5555


def test_the_frozen_workflow_reproduces_two_stored_development_seeds():
    path = os.path.join(ROOT, "experiments", "w_loop", "H8.json")
    if not (os.path.exists(path) and os.path.isdir(os.path.join(ROOT, "data", "synthetic_v2_d4_1515", "view"))):
        print("skipped (no development data)")
        return
    import w_loop as wl
    stored = json.load(open(path))
    fresh = {}
    import shutil
    for seed in (1515, 3000):
        rid = f"wlh8_{seed}"
        shutil.rmtree(os.path.join(ROOT, "experiments", rid), ignore_errors=True)                  # force a real rerun
        _, res = wl._run(("H8", seed))
        fresh[seed] = res
        assert abs(res["score"] - stored[str(seed)]["score"]) < 1e-6 and res["found"] == stored[str(seed)]["found"] and res["rounds"] == stored[str(seed)]["rounds"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
