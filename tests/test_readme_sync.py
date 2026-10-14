"""The README stays short, its figures exist and match the code, and every relative link in the README and docs resolves. Run: python tests/test_readme_sync.py"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "docs"))
import make_figures as mf  # noqa: E402


def test_readme_is_short_and_shows_the_agent_figure_and_progression_slide():
    text = open(os.path.join(ROOT, "README.md")).read()
    assert len(text) < 6000, "the README should stay about a tenth of its old length"
    for img in ("docs/images/agent.svg", "docs/images/progression.svg"):
        assert img in text and os.path.exists(os.path.join(ROOT, img))
    assert "Evaluation and Management" in text and "TL;DR" in text and "(Milestone" not in text


def test_agent_figure_lists_the_actions_in_the_code():
    svg = open(os.path.join(ROOT, "docs", "images", "agent.svg")).read()
    titles = re.findall(r'font-size="14.5" font-weight="bold" fill="[^"]+">([^<]+)</text>', svg)
    assert titles == [a[0] for a in mf.AGENT_ACTIONS] and len(titles) == 8
    assert "pipeline.svg" not in open(os.path.join(ROOT, "README.md")).read()


def test_no_section_title_in_the_docs_names_a_milestone():
    for name in os.listdir(os.path.join(ROOT, "docs")):
        if name.endswith(".md"):
            for line in open(os.path.join(ROOT, "docs", name)):
                if line.startswith("#"):
                    assert "(Milestone" not in line and "Milestone " not in line.split("(")[0], (name, line)


def test_every_relative_link_resolves():
    pages = [os.path.join(ROOT, "README.md")] + [os.path.join(ROOT, "docs", n) for n in os.listdir(os.path.join(ROOT, "docs")) if n.endswith(".md")]
    for page in pages:
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", open(page).read()) + re.findall(r'src="([^"]+)"', open(page).read()):
            if target.startswith(("http", "mailto:")):
                continue
            path = os.path.normpath(os.path.join(os.path.dirname(page), target))
            assert os.path.exists(path), f"{os.path.relpath(page, ROOT)} links to {target}, which does not exist"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
