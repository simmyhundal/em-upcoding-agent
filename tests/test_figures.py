"""The per-version figures and the progression slide must agree with the results file. Run: python tests/test_figures.py"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "docs"))
import make_figures as mf  # noqa: E402


def _text(svg):
    return " ".join(re.findall(r">([^<]+)</text>", open(os.path.join(ROOT, "docs", "images", svg)).read()))


def test_progression_slide_shows_the_numbers_in_the_results_file():
    cells = mf.progression_cells()
    text = _text("progression.svg").replace("  ", " ")
    for v, line in cells.items():
        nums = re.findall(r"\d+ of \d+", line)
        assert nums, v
        for n in nums:
            assert n in text, (v, n)


def test_every_version_has_a_figure_with_eight_steps_and_the_latest_is_the_readme_figure():
    for v in mf.VERSIONS:
        svg = open(os.path.join(ROOT, "docs", "images", f"how_it_works_{v}.svg")).read()
        assert len(re.findall(r'font-size="14.5" font-weight="bold"', svg)) == 8 and v in svg
    assert open(os.path.join(ROOT, "docs", "images", "pipeline.svg")).read() == \
        open(os.path.join(ROOT, "docs", "images", f"how_it_works_{mf.LATEST}.svg")).read()


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
