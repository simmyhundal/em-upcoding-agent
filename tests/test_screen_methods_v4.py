"""Data 4.0 screens (issue 127): payer-visible inputs only, deterministic, wired into flagging, and the chosen screen finds more habits than the frozen one on a development seed.
Run: python tests/test_screen_methods_v4.py   (needs the data 4.0 development seed d4_42; skipped otherwise)"""
import inspect
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
import flagging  # noqa: E402
import screen_methods_v4 as v4  # noqa: E402

VIEW = os.path.join(ROOT, "data", "synthetic_v2_d4_42", "view")
KEY = os.path.join(ROOT, "eval", "answer_key", "ground_truth_v2_d4_42.json")


def test_screens_read_only_the_view_and_never_the_key():
    src = inspect.getsource(v4).split('"""', 2)[2]                    # the code, not the module docstring
    assert "answer_key" not in src and "ground_truth" not in src and "role" not in src and "habit" not in src


def test_methods_are_wired_into_flagging():
    assert set(flagging.V4_METHODS) <= set(flagging.SCREEN_METHODS) and "eb_upper_t" in flagging.V4_METHODS and "eb_ratio_t" in flagging.SCREEN_METHODS


def test_scores_are_deterministic_and_the_chosen_screen_beats_the_frozen_one_on_habits():
    if not (os.path.isdir(VIEW) and os.path.exists(KEY)):
        print("skipped (no data 4.0 development seed)")
        return
    a, b = v4.score_v4(VIEW, only=["eb_upper_t", "eb_ratio_t"]), v4.score_v4(VIEW, only=["eb_upper_t", "eb_ratio_t"])
    assert a == b and len(a["eb_upper_t"]) == 216
    K = json.load(open(KEY))["providers"]
    ups = {p for p, v in K.items() if v["role"] == "upcoder"}
    rows = flagging.flag(VIEW, method="eb_upper_t", top_pct=10)
    rows0 = flagging.flag(VIEW, method="eb_ratio_t", top_pct=10)
    top = {r["provider_id"] for r in rows if r["flagged"]}
    top0 = {r["provider_id"] for r in rows0 if r["flagged"]}
    assert len(top) == 22 and len(top & ups) > len(top0 & ups)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
