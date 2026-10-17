"""Tests for the screen ranking metrics (issue 83). Run: python tests/test_screen_metrics.py"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import screen_metrics as sm  # noqa: E402


def approx(a, b):
    return abs(a - b) < 1e-9


def test_perfect_and_worst_rankings():
    s, y = [0.9, 0.8, 0.3, 0.2, 0.1], [1, 1, 0, 0, 0]
    assert approx(sm.average_precision(s, y), 1.0) and approx(sm.roc_auc(s, y), 1.0)
    assert approx(sm.precision_at_k(s, y, 2), 1.0) and approx(sm.precision_at_k(s, y, 4), 0.5)
    r = [0.1, 0.2, 0.3, 0.8, 0.9]
    assert approx(sm.roc_auc(r, y), 0.0)


def test_average_precision_by_hand():
    # positives at ranks 1 and 3 of 4: AP = (1/2)(1/1) + (1/2)(2/3)
    s, y = [4, 3, 2, 1], [1, 0, 1, 0]
    assert approx(sm.average_precision(s, y), 0.5 + 1 / 3)
    assert approx(sm.roc_auc(s, y), 0.75)


def test_ties_and_random_baseline():
    s, y = [1, 1, 1, 1], [1, 0, 0, 0]
    assert approx(sm.roc_auc(s, y), 0.5)
    assert approx(sm.average_precision(s, y), 0.25)           # one block: precision after the block is the base rate
    assert sm.average_precision([1, 2], [0, 0]) is None and sm.roc_auc([1, 2], [1, 1]) is None


def test_results_file_carries_the_metrics_on_screen_rows():
    import csv
    rows = list(csv.DictReader(open(os.path.join(ROOT, "experiments", "results.csv"))))
    screens = [r for r in rows if r["stage"] == "Screen" and r["run_id"].startswith("261015_")]
    assert screens and all(r["screen_auprc"] and 0 <= float(r["screen_roc_auc"]) <= 1 for r in screens)
    assert all(r["screen_auprc"] == "" for r in rows if r["stage"] != "Screen")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
