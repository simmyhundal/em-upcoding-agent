"""The README's step list must match the pipeline slide, step for step. Run: python tests/test_readme_sync.py"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def test_readme_steps_match_the_slide():
    readme = open(os.path.join(ROOT, "README.md")).read()
    section = readme[readme.index("## What does this project do?"):readme.index("## How the filtering works")]
    steps = re.findall(r"^(\d+)\. \*\*(.+?)\.?\*\*", section, flags=re.M)
    svg = open(os.path.join(ROOT, "docs", "images", "pipeline.svg")).read()
    slide = re.findall(r'font-size="14.5" font-weight="bold" fill="[^"]+">([^<]+)</text>', svg)
    assert [t for _, t in steps] == slide, (steps, slide)
    assert [n for n, _ in steps] == [str(i) for i in range(1, len(slide) + 1)]
    assert section.index("pipeline.svg") < section.index("1. **")          # the image sits under the header, above the steps


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
