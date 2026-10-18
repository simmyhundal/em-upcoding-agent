"""Tests for the exported learned policy (issue 108): the runtime features equal the ones it was trained on, and running it reproduces what the training table predicts.
Run: python tests/test_policy_24.py   (needs the gitignored data of development seed 1515; skipped otherwise)"""
import json
import math
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import escalation_policy as ep  # noqa: E402

POL = ep.load()


def test_policy_file_is_complete_and_payer_visible():
    assert POL["features"] == ep.STATE and len(POL["mu"]) == len(ep.STATE) == len(POL["sd"])
    assert not {"upcoder", "found", "honest_called", "role", "justified"} & set(POL["features"])
    assert set(POL["branches"]) == set(ep.BRANCHES) and POL["lambda"] == 0.05 and len(POL["honest"]) == len(ep.STATE) + 1
    for b in ep.BRANCHES:
        assert all(len(POL["branches"][b][k]) == len(ep.STATE) + 1 for k in ("found", "hc", "extra"))


def test_choose_is_deterministic_and_responds_to_the_state():
    quiet = [1, 1.0, 0, 0, 0.0, 0, 0.0, 0.0, 0.0, 1.0, 4]            # silent office, four rounds already
    loud = [3, 1.6, 30, 12, 0.1, 30, 0.3, 0.3, 0.1, 0.0, 1]            # charts back, many late signatures
    assert ep.choose(POL, quiet) == ep.choose(POL, quiet) and ep.choose(POL, quiet) == "STOP"
    assert ep.choose(POL, loud) in ep.BRANCHES


def test_runtime_features_equal_training_features_and_the_run_matches_the_training_table():
    if not os.path.isdir(os.path.join(ROOT, "data", "synthetic_v2_r2_1515")):
        print("skipped (no development data)")
        return
    import rl_escalate_policy as r2
    import make_v2_office_workflow_runs as mw
    rows = {r["pid"]: r for r in json.load(open(r2.DATA)) if r["seed"] == 1515}
    view, office, flagged_file = mw.build_view("p24test_1515", "r2_1515", "eb_ratio_t_10", version="2.4", tier1_n=11, policy24={"learned": True})
    assert len(office.policy_log) == 22
    for pid, (x, branch) in office.policy_log.items():
        train = list(r2.matrix([rows[pid]])[0])
        assert all(abs(a - b) < 1e-6 for a, b in zip(x, train)), (pid, x, train)
        assert branch == ep.choose(POL, train)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
