"""Terminology: every concept page exists and is in the glossary, and the pages meant for outside readers use the plain term, linked, with the old project term only inside code spans or the glossary. Run: python tests/test_concepts.py"""
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CONCEPTS = {
    "workflow-and-agent": "workflow", "shortlist": "shortlist", "request-recommendation": "request recommendation", "triage": "triage",
    "chart-review": "chart review", "demand-check": "demand check", "conservative-estimate": "conservative", "borderline-case": "borderline",
    "break-even-rule": "break-even rule", "hard-rule": "hard rule", "no-more-requests": "no-more-requests",
    "volume-screen": "volume screen", "records-not-provided": "records not provided", "stratified-sample": "stratified sample",
}
OLD_SLUGS = ["workflow-and-agent", "shortlist", "request-recommendation", "triage", "chart-review", "demand-check", "conservative-estimate", "borderline-case", "break-even-rule", "hard-rule", "no-more-requests"]
OLD = ["near-miss", "demand floor", "narrow binding rule", "ask-or-skip", "stop-after-first-sample", "(?<!short)listed provider"]
OUTSIDE_PAGES = {"docs/agent_v51.md": OLD_SLUGS,
                 "docs/score_42.md": ["records-not-provided", "stratified-sample"],
                 "docs/w42_freeze.md": ["volume-screen", "stratified-sample", "records-not-provided", "conservative-estimate", "break-even-rule"]}


def strip_code(t):
    return re.sub(r"`[^`]*`", "", t)


def main():
    gl = open(os.path.join(ROOT, "docs", "glossary.md")).read()
    for slug in CONCEPTS:
        path = os.path.join(ROOT, "docs", "concepts", slug + ".md")
        assert os.path.exists(path), slug
        text = open(path).read()
        for h in ("## What it means", "## Why it exists", "## Example", "## Where to find it"):
            assert h in text, (slug, h)
        assert f"concepts/{slug}.md" in gl, f"{slug} missing from the glossary"
        assert slug + ".md" in open(os.path.join(ROOT, "docs", "concepts", "README.md")).read()
    for page, need in OUTSIDE_PAGES.items():
        text = open(os.path.join(ROOT, page)).read()
        plain = strip_code(re.sub(r"\]\([^)]*\)", "]", text)).lower()
        for old in OLD:
            assert not re.search(old, plain), f"{page}: old term {old!r} outside code"
        for slug in need:
            assert f"concepts/{slug}.md" in text, f"{page} does not link concepts/{slug}.md"
    print("ok test_concepts")


if __name__ == "__main__":
    main()
