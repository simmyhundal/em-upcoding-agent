"""Sanity tests for the two baselines. Run: python tests/test_baselines.py"""
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import baseline_riskadj as ra  # noqa: E402
import baseline_zscore as bz  # noqa: E402
import generate_synthetic as g  # noqa: E402

D = tempfile.mkdtemp()
g.build(D, seed=7, n_normal=30, n_upcoders=3, n_hard_neg=3)


def test_zscore_ranks_every_provider_once():
    rows, _, _ = bz.rank(D, top_n=5)
    assert len(rows) == 36 and len({r["provider_id"] for r in rows}) == 36
    assert [r["rank"] for r in rows] == list(range(1, 37))
    assert sum(r["flagged"] for r in rows) == 5


def test_riskadj_expected_matches_observed_overall():
    prov, cat, y = ra.load(D)
    beta = ra.fit_logistic(ra.design(cat), y)
    p = 1 / (1 + np.exp(-ra.design(cat) @ beta))
    assert abs(p.sum() - y.sum()) < 1e-3 * len(y)   # a fitted logistic reproduces the total


def test_riskadj_ranks_every_provider_once():
    rows, _, _ = ra.rank(D, top_n=5)
    assert len(rows) == 36 and sum(r["flagged"] for r in rows) == 5


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
