"""Tests for the candidate screen methods (issue 88). Run: python tests/test_screen_methods.py"""
import os
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for sub in ("src", "eval"):
    sys.path.insert(0, os.path.join(ROOT, sub))
import baseline_riskadj as ra  # noqa: E402
import generate_synthetic as g1  # noqa: E402
import screen_methods as sm  # noqa: E402

_CACHE = {}


def small_dataset():
    if "d" not in _CACHE:
        tmp = tempfile.mkdtemp()
        out, key = os.path.join(tmp, "d"), os.path.join(tmp, "key", "k.json")
        g1.build(out, key, seed=5, n_normal=50, n_upcoders=5, n_hard_neg=5)
        import json
        _CACHE["d"] = (out, json.load(open(key)))
    return _CACHE["d"]


def test_every_method_scores_every_provider_and_riskadj_matches_the_frozen_screen():
    out, _ = small_dataset()
    S = sm.score_all(out)
    pids = set(S["zscore"])
    assert len(pids) == 60
    for m in sm.METHODS:
        assert set(S[m]) == pids, m
    rows, _, _ = ra.rank(out, 25)
    assert max(abs(r["z_adj"] - S["riskadj"][r["provider_id"]]) for r in rows) < 1e-3     # same score, rounding aside


def test_eb_ratio_shrinks_toward_one_and_more_for_small_panels():
    sc = {"big": {"n_99215": 300, "expected": 100.0, "z_raw": 0.0}, "small": {"n_99215": 3, "expected": 1.0, "z_raw": 0.0}}
    for i in range(30):
        sc[f"h{i}"] = {"n_99215": 10 + (i % 3) - 1, "expected": 10.0, "z_raw": 0.0}
    eb = sm.eb_scores(sc)
    assert 1 < eb["eb_ratio"]["small"] < 3 and 1 < eb["eb_ratio"]["big"] < 3        # both pulled in from the raw ratio of 3
    assert eb["eb_ratio"]["small"] < eb["eb_ratio"]["big"]                           # the small panel is pulled in further


def test_gamma_tail_close_to_exact():
    # exact values (scipy.stats.gamma.sf): Gamma(5, rate 1) > 5 is 0.44049; Gamma(20, rate 2) > 15 is 0.021873
    assert abs(sm._gamma_tail(5, 1, 5) - 0.44049) < 0.005
    assert abs(sm._gamma_tail(20, 2, 15) - 0.021873) < 0.002


def test_eb_ratio_finds_planted_upcoders_on_a_small_dataset():
    out, truth = small_dataset()
    S = sm.score_all(out)
    top = sorted(S["eb_ratio"], key=lambda p: -S["eb_ratio"][p])[:10]
    assert sum(truth["providers"][p]["role"] == "upcoder" for p in top) >= 4


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
