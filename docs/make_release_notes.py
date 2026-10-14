"""Write release-note drafts for each tagged version (docs/releases/vX.Y.md) from the figures, results file and versioning doc.

A GitHub release for a tag is published by hand after the user approves it (the repository is public): paste the matching file as the
release notes. The figure links point at the main branch so they work for tags that predate the figures.

Usage:
    python docs/make_release_notes.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "docs"))
import make_figures as mf  # noqa: E402

RAW = "https://raw.githubusercontent.com/simmyhundal/em-upcoding-agent/main/docs/images"
INTRO = {"v1.0": "The first workflow: statistics screen, an AI writes and filters, code checks citations, people review. Held-out freeze of the version-1 data.",
         "v2.0": "The workflow on plan-shaped data: charts come only by request, code writes the facts and settles clear cases, a model handles the rest.",
         "v3.0": "The agent design: a model chooses its own tools and steps within caps, against a simulated provider office. The v2.0 workflow stays frozen as the comparison."}
LIMITS = {"v1.0": ["Synthetic data from one generator; two seeds.", "The AI is handed a records sample before it decides, which a payer would not have.",
                   "Usefulness 3.4 against a target of 4."],
          "v2.0": ["Synthetic data from one generator; 8 upcoders per run.", "Cloned notes defeat the chart rules and the model.",
                   "At 0.5% to 1% upcoders the AI step accuses many honest doctors.", "v2 schemas not yet reviewed by someone who works with 837/834/835 data."],
          "v3.0": ["Found fewer upcoders than the workflow on the reserved seeds (4 of 16 against 6), with fewer honest practices asked.",
                   "Agent summaries score 2.3 to 3.0 on usefulness (target 4).", "Not yet tested below a 3.7% upcoder rate.",
                   "Recovery (extrapolated dollars, post-flag rounds) is not simulated yet."]}


def main():
    cells = mf.progression_cells()
    os.makedirs(os.path.join(ROOT, "docs", "releases"), exist_ok=True)
    for v, (title, steps) in mf.VERSIONS.items():
        lines = [f"# {v}", "", INTRO[v], "", f"![{title}]({RAW}/how_it_works_{v}.svg)", "", "## How it works"]
        lines += [f"{i}. **{t}.** {body}" for i, (t, body, _) in enumerate(steps, 1)]
        lines += ["", "## Headline result", cells[v], "", "Numbers are not comparable across versions (different data and inputs). Full table: "
                  "[docs/results.md](https://github.com/simmyhundal/em-upcoding-agent/blob/main/docs/results.md).", "", "## Known limits"]
        lines += [f"- {x}" for x in LIMITS[v]]
        lines += ["", "More: [docs/versioning.md](https://github.com/simmyhundal/em-upcoding-agent/blob/main/docs/versioning.md)", ""]
        open(os.path.join(ROOT, "docs", "releases", f"{v}.md"), "w").write("\n".join(lines))
        print("wrote", v)


if __name__ == "__main__":
    main()
