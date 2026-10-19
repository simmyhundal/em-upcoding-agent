"""Tests for the Stage 1 learned ask-or-skip policy (issue 108). Run: python tests/test_rl_ask.py"""
import os
import sys

import numpy as np

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "eval"))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import rl_ask_policy as rl  # noqa: E402


def rows(n=200, seed=0):
    rng = np.random.default_rng(seed)
    out = []
    for i in range(n):
        up = rng.random() < 0.3
        ratio = float(np.exp(rng.normal(1.3 if up else 0.7, 0.4)))
        out.append({"seed": i % 10, "set": "r2", "pid": str(i), "rank": 1 + i % 22, "ratio": ratio, "excess": 30 * (ratio - 1), "claims": 200 + i, "screen_score": ratio,
                    "z_adj": ratio * 2, "upcoder": bool(up), "found": bool(up and rng.random() < 0.8), "honest_called": False, "rounds": 1})
    return out


def test_features_are_payer_visible_only():
    assert not {"upcoder", "found", "honest_called", "role", "justified"} & set(rl.FEATURES)
    assert rl.matrix(rows(5)).shape == (5, len(rl.FEATURES))


def test_cross_validated_scores_use_only_other_seeds_and_rank_upcoders_higher():
    r = rows()
    pf, ph, phc = rl.cv_scores(r)
    up = np.array([x["upcoder"] for x in r])
    assert pf[up].mean() > pf[~up].mean() and ph[~up].mean() > ph[up].mean()
    assert np.all((pf >= 0) & (pf <= 1))


def test_totals_count_only_asked_providers():
    r = rows(20)
    t_all, t_none = rl.totals(r, [True] * 20), rl.totals(r, [False] * 20)
    assert t_none == {"found": 0, "honest_asked": 0, "honest_called": 0, "asked": 0} and t_all["asked"] == 20
    assert t_all["honest_asked"] == sum(not x["upcoder"] for x in r)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
