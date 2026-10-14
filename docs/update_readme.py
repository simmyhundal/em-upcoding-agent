"""Refresh the generated parts of the README so they cannot go stale.

  * the README's TL;DR sentence and headline table (between the tldr and scoreboard markers), rendered from experiments/results.csv (the source of truth,
    written from the saved outputs listed in experiments/runs.json by `python eval/scoreboard.py --write`);
  * docs/results.md (every run) and docs/roadmap.md (built from this repository's GitHub milestones as live progress badges; running this script
    also picks up milestones created later).

GitHub cannot run code when a README is viewed, so the scoreboard and the milestone list refresh when this script runs
(`python docs/update_readme.py`). tests/test_scoreboard.py fails if the committed scoreboard no longer matches the data.

Usage:
    python docs/update_readme.py [--check]    # --check exits non-zero if the README would change
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import scoreboard  # noqa: E402

README = os.path.join(ROOT, "README.md")


def replace_block(text, name, body):
    pat = re.compile(rf"(<!-- {name}:start -->).*?(<!-- {name}:end -->)", re.S)
    if not pat.search(text):
        raise SystemExit(f"markers for {name} not found in README")
    return pat.sub(lambda m: m.group(1) + "\n" + body + "\n" + m.group(2), text)


def milestones():
    repo = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
                          capture_output=True, text=True, cwd=ROOT, check=True).stdout.strip()
    raw = subprocess.run(["gh", "api", f"repos/{repo}/milestones?state=all&per_page=100"],
                         capture_output=True, text=True, cwd=ROOT, check=True).stdout
    return repo, sorted(json.loads(raw), key=lambda m: m["number"])


def roadmap_markdown():
    repo, ms = milestones()
    lines = [f"Live from this repository's [milestones](https://github.com/{repo}/milestones); each badge shows the milestone's current title and closed/total issues.", ""]
    for m in ms:
        first = re.split(r"(?<=[.!?])\s", (m.get("description") or "").strip())[0]
        lines.append(f"- ![{m['title']}](https://img.shields.io/github/milestones/progress/{repo}/{m['number']}) {first}")
    return "\n".join(lines)


RESULTS_DOC = os.path.join(ROOT, "docs", "results.md")


def results_doc():
    return ("# Results\n\n[Back to the README](../README.md)\n\nRendered from `experiments/results.csv` by `python docs/update_readme.py`. "
            "Columns are explained in [results_table.md](results_table.md).\n\n## Every run, key numbers\n\n" + scoreboard.markdown_compact().replace("(docs/results.md)", "(results.md)").replace("(docs/results_table.md)", "(results_table.md)")
            + "\n\n## Every run, all columns\n\n" + scoreboard.markdown_from_csv() + "\n")


def build(text, with_roadmap=True):
    text = replace_block(text, "tldr", scoreboard.headline_sentence())
    text = replace_block(text, "scoreboard", scoreboard.headline_table())
    return text


ROADMAP_DOC = os.path.join(ROOT, "docs", "roadmap.md")


def roadmap_doc():
    old = open(ROADMAP_DOC).read() if os.path.exists(ROADMAP_DOC) else "# Roadmap\n\n[Back to the README](../README.md)\n\n<!-- roadmap:start -->\n<!-- roadmap:end -->\n"
    try:
        return replace_block(old, "roadmap", roadmap_markdown())
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("note: could not read milestones with gh; roadmap left as is", file=sys.stderr)
        return old


if __name__ == "__main__":
    old = open(README).read()
    new = build(old)
    doc_old = open(RESULTS_DOC).read() if os.path.exists(RESULTS_DOC) else ""
    if "--check" in sys.argv:
        sys.exit(0 if new == old and results_doc() == doc_old else 1)
    if results_doc() != doc_old:
        open(RESULTS_DOC, "w").write(results_doc())
        print("docs/results.md updated")
    rm_old = open(ROADMAP_DOC).read() if os.path.exists(ROADMAP_DOC) else ""
    rm_new = roadmap_doc()
    if rm_new != rm_old and "--check" not in sys.argv:
        open(ROADMAP_DOC, "w").write(rm_new)
        print("docs/roadmap.md updated")
    if new != old:
        open(README, "w").write(new)
        print("README updated")
    else:
        print("README already up to date")
