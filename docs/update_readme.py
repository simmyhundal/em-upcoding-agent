"""Refresh the generated parts of the README so they cannot go stale.

  * the scoreboard table (between <!-- scoreboard:start --> and <!-- scoreboard:end -->), computed from the saved outputs
    listed in experiments/runs.json by eval/scoreboard.py;
  * the roadmap (between <!-- roadmap:start --> and <!-- roadmap:end -->), built from this repository's GitHub milestones.
    Each milestone is a live progress badge, so title and open/closed counts update on their own; running this script
    also picks up milestones created later.

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


def build(text, with_roadmap=True):
    text = replace_block(text, "scoreboard", scoreboard.markdown())
    if with_roadmap:
        try:
            text = replace_block(text, "roadmap", roadmap_markdown())
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("note: could not read milestones with gh; roadmap left as is", file=sys.stderr)
    return text


if __name__ == "__main__":
    old = open(README).read()
    new = build(old)
    if "--check" in sys.argv:
        sys.exit(0 if new == old else 1)
    if new != old:
        open(README, "w").write(new)
        print("README updated")
    else:
        print("README already up to date")
