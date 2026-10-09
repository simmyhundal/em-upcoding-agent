"""Tests for the flagging modes. Run: python tests/test_flagging.py"""
import os
import sys
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "eval"))
import flagging  # noqa: E402
import generate_synthetic as g  # noqa: E402
import threshold_sweep as ts  # noqa: E402

D = tempfile.mkdtemp()
g.build(D, os.path.join(tempfile.mkdtemp(), "gt.json"), seed=17, n_normal=60, n_upcoders=4, n_hard_neg=4)


def flagged(rows):
    return {r["provider_id"] for r in rows if r["flagged"]}


def test_default_mode_flags_exactly_top_n():
    rows = flagging.flag(D, top_n=12)
    assert len(flagged(rows)) == 12 and [r["rank"] for r in rows] == list(range(1, len(rows) + 1))
    assert all(r["suspicion"] == r["z_adj"] for r in rows)


def test_threshold_mode_flags_everyone_at_or_above_and_nobody_below():
    rows = flagging.flag(D, min_suspicion=4.0)
    for r in rows:
        assert r["flagged"] == (r["suspicion"] >= 4.0)
    assert [r["suspicion"] for r in rows] == sorted((r["suspicion"] for r in rows), reverse=True)   # ordered by suspicion
    assert all(r["flagged_by"].startswith("suspicion>=") for r in rows if r["flagged"])


def test_higher_threshold_is_a_subset_and_count_is_monotone():
    lo, hi = flagged(flagging.flag(D, min_suspicion=3.0)), flagged(flagging.flag(D, min_suspicion=6.0))
    assert hi <= lo and len(hi) <= len(lo)


def test_cap_keeps_the_highest_and_volume_floor_excludes_small_practices():
    rows = flagging.flag(D, min_suspicion=0.0, max_flagged=5)
    top = [r for r in rows if r["flagged"]]
    assert len(top) == 5 and all(r["suspicion"] >= max(x["suspicion"] for x in rows if not x["flagged"]) for r in top)
    floor = sorted(r["n_claims"] for r in rows)[len(rows) // 2]
    big = flagging.flag(D, min_suspicion=0.0, min_claims=floor)
    assert all(r["n_claims"] >= floor for r in big if r["flagged"]) and len(flagged(big)) < len(rows)


def test_sweep_counts_match_a_direct_count():
    truth = {"providers": {"A": {"role": "upcoder"}, "B": {"role": "normal"}, "C": {"role": "hard_negative"}}}
    rows = [{"provider_id": "A", "z_adj": "9"}, {"provider_id": "B", "z_adj": "4"}, {"provider_id": "C", "z_adj": "6"}]
    res = {r["threshold"]: r for r in ts.sweep(rows, truth, (3, 5, 8))}
    assert (res[3]["flagged"], res[3]["upcoder"], res[3]["normal"]) == (3, 1, 1)
    assert (res[5]["flagged"], res[5]["hard_negative"], res[5]["precision"]) == (2, 1, 0.5)
    assert res[8]["flagged"] == 1 and res[8]["precision"] == 1.0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
