"""Tests for the scoreboard thresholds and README freshness. Run: python tests/test_scoreboard.py"""
import os
import sys

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "eval"))
sys.path.insert(0, os.path.join(ROOT, "docs"))
import scoreboard as sb  # noqa: E402


def test_threshold_logic_and_edge_cases():
    assert sb.judge((7, 8), 3, "upcoders") and not sb.judge((6, 8), 3, "upcoders")
    assert sb.judge((2, 8), 3, "hard") and not sb.judge((3, 8), 3, "hard")          # must be lower, not equal
    assert sb.judge((0, 8), 0, "hard")                                              # zero always passes
    assert sb.judge(0.8, None, "prec") and not sb.judge(0.79, None, "prec")
    assert sb.judge(1.0, None, "cite") and not sb.judge(0.99, None, "cite")
    assert sb.judge(4.0, None, "useful") and not sb.judge(3.99, None, "useful")
    assert sb.judge(False, None, "templ") and not sb.judge(True, None, "templ")
    assert sb.judge(None, 3, "upcoders") is None                                    # not scored: excluded


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
