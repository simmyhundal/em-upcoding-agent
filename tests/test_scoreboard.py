"""Tests for the scoreboard thresholds and README freshness. Run: python tests/test_scoreboard.py"""
import os
import sys

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "eval"))
sys.path.insert(0, os.path.join(ROOT, "docs"))
import scoreboard as sb  # noqa: E402


def test_threshold_logic_and_edge_cases():
    assert sb.judge((1, 8), "fn") and not sb.judge((2, 8), "fn")                    # 12.5% is the limit, inclusive
    assert sb.judge((26, 208), "fp") and not sb.judge((27, 208), "fp")             # 26/208 = 12.5% exactly
    assert sb.judge((0, 8), "fn") and sb.judge((0, 208), "fp")
    assert sb.judge(0.8, "prec") and not sb.judge(0.79, "prec")
    assert sb.judge(1.0, "cite") and not sb.judge(0.99, "cite")
    assert sb.judge(4.0, "useful") and not sb.judge(3.99, "useful")
    assert sb.judge(False, "templ") and not sb.judge(True, "templ")
    assert sb.judge(None, "fn") is None                                            # not scored: excluded


def test_total_ignores_unscored_evals():
    assert sb.total([True, False, None, True, None]) == "2 / 3"
    assert sb.total([None, None]) == "0 / 0"


def test_readme_scoreboard_is_current():
    needed = [os.path.join(ROOT, "eval", "answer_key", "ground_truth.json"),
              os.path.join(ROOT, "eval", "answer_key", "ground_truth_s101.json")]
    if not all(os.path.exists(p) for p in needed):
        print("skipped: answer keys are gitignored; regenerate them first")
        return
    text = open(os.path.join(ROOT, "README.md")).read()
    start = text.index("<!-- scoreboard:start -->") + len("<!-- scoreboard:start -->")
    end = text.index("<!-- scoreboard:end -->")
    assert text[start:end].strip() == sb.markdown().strip(), "README scoreboard is stale: run python docs/update_readme.py"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
