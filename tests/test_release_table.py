"""The README's release 2 and 3 table is rendered from experiments/release23_table.json and the progression slide agrees with it. Run: python tests/test_release_table.py"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "eval"))
sys.path.insert(0, os.path.join(ROOT, "docs"))
import make_figures as mf  # noqa: E402
import release_table as rt  # noqa: E402


def test_readme_block_is_the_rendered_json():
    text = open(os.path.join(ROOT, "README.md")).read()
    block = re.search(r"<!-- release23:start -->\n(.*?)\n<!-- release23:end -->", text, re.S).group(1)
    assert block == rt.markdown()


def test_rows_are_consistent_and_cover_the_arms():
    rows = rt.rows()
    assert [(r["arm"], r["seeds"]) for r in rows[len(rt.R1):]] == [(a, w) for a, w, *_ in rt.ROWS] and len(rows) == len(rt.R1) + len(rt.ROWS)
    for r in rows:
        assert 0 <= r["found"] <= r["upcoders"] and r["accused"] >= 0 and r["asked"] <= r["requests"]


def test_progression_slide_shows_the_release_5_numbers():
    svg = " ".join(re.findall(r">([^<]+)</text>", open(os.path.join(ROOT, "docs", "images", "progression.svg")).read())).replace("  ", " ")
    for line in rt.headline_cells().values():
        for n in re.findall(r"\d+ of \d+", line):
            assert n in svg, n


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
