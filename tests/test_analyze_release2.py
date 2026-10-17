"""Tests for the release 2 analysis arithmetic (issue 90). Run: python tests/test_analyze_release2.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "eval"))
import analyze_release2 as ar  # noqa: E402


def test_p_values():
    assert ar.p_z(0, 0) == 1.0 and ar.p_exact(0, 0) == 1.0
    assert abs(ar.p_exact(8, 3) - 0.2266) < 1e-3                       # the release 1 figures: 8 workflow-only, 3 agent-only
    assert ar.p_z(8, 3) > ar.p_exact(8, 3) - 0.1                       # the design effect makes the z-test no more liberal than exact here
    assert ar.p_z(20, 2) < ar.ALPHA and ar.p_z(10, 8) > ar.ALPHA


def test_report_is_descriptive_below_the_first_look():
    rows = [{"seed": s, "upcoders": 8, "w_found": 1, "a_found": 2, "w_only": 0, "a_only": 1, "both": 1, "w_honest": 0, "a_honest": 0, "w_asked": 5, "a_asked": 5,
             "w_cost": 0.0, "a_cost": 0.2} for s in (1, 2, 3)]
    t = ar.report(rows)
    assert "descriptive only" in t and "Total" in t


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
