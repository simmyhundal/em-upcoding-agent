"""Tests for the Stage 2 learned stop-or-escalate policy (issue 108). Run: python tests/test_rl_escalate.py
Uses the committed dataset experiments/rl_escalate_dataset.json (written by eval/rl_escalate_policy.py)."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "eval"))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import rl_escalate_policy as rl2  # noqa: E402

ROWS = json.load(open(rl2.DATA))


def test_state_is_payer_visible_only_and_matrix_matches():
    assert not {"upcoder", "found", "honest_called", "role", "justified"} & set(rl2.STATE)
    assert rl2.matrix(ROWS[:5]).shape == (5, len(rl2.STATE))


def test_every_provider_is_observed_under_every_branch_and_extra_steps_never_remove_rounds():
    for r in ROWS:
        assert all(b in r for b in rl2.BRANCHES)
        stop = r["STOP"]["rounds"]
        assert all(r[b]["rounds"] >= stop for b in rl2.BRANCHES)
        assert r["BOTH"]["rounds"] >= max(r["TARG"]["rounds"], r["AUD"]["rounds"]) or r["BOTH"]["rounds"] >= stop


def test_cross_validated_predictions_are_probabilities_and_evaluate_counts_the_choice():
    P, honest = rl2.cv_predict(ROWS)
    assert all(np.all((P[b]["found"] >= 0) & (P[b]["found"] <= 1)) for b in rl2.BRANCHES) and np.all((honest >= 0) & (honest <= 1))
    stop = rl2.evaluate(ROWS, ["STOP"] * len(ROWS))
    assert stop["found"] == sum(r["STOP"]["found"] for r in ROWS)
    assert rl2.evaluate(ROWS, ["BOTH"] * len(ROWS))["honest_rounds"] >= stop["honest_rounds"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
