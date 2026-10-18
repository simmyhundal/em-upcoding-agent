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


BLOB = "https://github.com/simmyhundal/em-upcoding-agent/blob"


def _row(arm, seeds):
    import release_table
    x = {(r["arm"], r["seeds"]): r for r in release_table.rows()}[(arm, seeds)]
    prec = 100 * x["found"] / (x["found"] + x["accused"]) if x["found"] + x["accused"] else 0
    return x, f"**{x['found']} of {x['upcoders']} upcoders found ({100 * x['found'] / x['upcoders']:.0f}% recall), {x['accused']} honest accused ({prec:.0f}% precision)**, {x['asked']} honest practices asked for charts"


def newer_notes():
    """Notes for releases 2 and 3 (data 2.2): v2.2, v3.2, v2.3, v3.3. Headline numbers are read from experiments/release23_table.json."""
    sys.path.insert(0, os.path.join(ROOT, "eval"))
    w2r2, a2 = _row("Workflow v2.2", "release 2 seeds")[1], _row("Agent v3.2", "release 2 seeds")[1]
    w2r3, w3, a3 = _row("Workflow v2.2", "release 3 seeds")[1], _row("Workflow v2.3", "release 3 seeds")[1], _row("Agent v3.3", "release 3 seeds")[1]
    flow = {"workflow": f"{RAW}/how_it_works_v2.0.svg", "agent": f"{RAW}/how_it_works_v3.0.svg"}
    return {
        "v2.2": ("The workflow on harder data (data 2.2): honest doctors miscode too, practices bill through groups, and the extract can have defects. Evaluated with agent v3.2 on ten seeds.",
                 "workflow", ["**Data 2.2.** Honest coding noise (about 8% of honest visits miscoded, half upward), group billing, level-changing corrections, optional diagnosis truncation and injected data defects; an upcoder is a provider whose true rate is above the honest 95th percentile and at least 6 points above the honest mean ([data_v2_2.md]({b}/v2.2/docs/data_v2_2.md)).",
                              "**Screen.** `eb_ratio` (empirical-Bayes shrinkage of the ratio to expected), top 5% of the panel.",
                              "**Rules 2.2.** A peer-rate cap for noisy honest peers, and the cases the model always answered inconclusive are decided by rule: about $0.01 a seed, no LLM judge.",
                              "**Data-quality pre-flight** on the delivered extract, with a hold on findings affected by a data problem; deterministic rule judge j3.2."],
                 f"Ten seeds (1515 to 2424): {w2r2}. Agent v3.2 on the same seeds found fewer. The comparison was an **unplanned ten-seed look** (the pre-registered looks were at 22 and 44 seeds), so it carries no significance claim: 10 upcoders found only by the workflow against 1 only by the agent (exact McNemar p = 0.012; with a design effect for seeds as clusters p = 0.027).",
                 ["Misses most upcoders: the top-5% list held only 44 of 78 upcoders, and cloned-notes upcoders were the largest hole (4 of 23 screened ones found).",
                  "Seeds 1515 to 2424 became development data afterwards.", "Notes are generated, so cloned-notes signs are probably easier than real ones."]),
        "v3.2": ("The agent on harder data (data 2.2), with the data-quality tools and the new screens. Evaluated with workflow v2.2 on ten seeds.", "agent",
                 ["**Data-quality tools** `data_quality` and `flag_data_issue`; findings affected by a data problem need chart evidence.", "**Screens** `eb_ratio` and `priority` with a percentile cutoff (`top_pct`).",
                  "**Cost controls.** $1 cap per run, Opus 5.5 at low effort (about $0.19 a seed), no LLM judge."],
                 f"Ten seeds (1515 to 2424): {a2}. Not significantly different from workflow v2.2 by the pre-registered plan (the ten-seed look was unplanned; see v2.2).",
                 ["Found fewer upcoders than the workflow on these seeds.", "Low effort and one model; a different setting might behave differently.", "Same data limits as v2.2."]),
        "v2.3": ("The workflow with cloned-notes detection and a wider list, on the same data 2.2. Evaluated once on ten fresh seeds with a pre-registered rule (issue 99).", "workflow",
                 ["**Rules 2.3.** Late-signature or audit-trail signs of cloned notes lean upcoding when the 99215 share is more than 3 times expected, even though the charts support the bill; a chart-based call must also beat the real peer rate by more than chance.",
                  "**Screen `eb_ratio_t`:** eb_ratio with the lab or test line on the claim as a covariate.", "**Wider list, two tiers:** top 10%; the first 5% get the full policy, the rest one request unless the notes show cloning.",
                  "Judge j3.3 for these summaries ([judge_release3.md]({b}/v2.3/docs/judge_release3.md))."],
                 f"Ten fresh seeds (2525 to 3434): {w3}, against {w2r3} for v2.2. Workflow v2.3 against v2.2: 21 upcoders found only by v2.3, 8 only by v2.2; p = 0.049 against the pre-registered 0.025, so **not significant by the rule** (exact McNemar 0.024 beside it).",
                 ["The wider list asks 150 honest practices for charts against 64 for v2.2 (agent v3.3: 79).", "On the development seeds it found 38 of 78 (in sample); 37 of 79 held out.", "Most remaining misses are upcoders the screen never lists."]),
        "v3.3": ("The agent mirroring workflow v2.3, on data 2.2. Evaluated once on ten fresh seeds with a pre-registered rule (issue 99).", "agent",
                 ["**Rules 2.3 in `hybrid_review` and the lint**, the `eb_ratio_t` screen, a prompt that explains cloned notes and the chart test, records budget 22.",
                  "Same $1 cap and Opus 5.5 low effort (about $0.23 a seed)."],
                 f"Ten fresh seeds (2525 to 3434): {a3}. Workflow v2.3 against agent v3.3: 12 upcoders found only by the workflow, 9 only by the agent; p = 0.59, **no significant gap**.",
                 ["Found nearly as many upcoders as v2.3 with about half the honest requests; its reading of charts matches the rules, so the gap is in which providers it asks.",
                  "Ten seeds, one data version, generated notes, low effort."]),
    }


def main():
    for v, (intro, kind, changes, headline, limits) in newer_notes().items():
        lines = [f"# {v}", "", intro, "", f"![The flow this version builds on]({RAW}/how_it_works_{'v2.0' if kind == 'workflow' else 'v3.0'}.svg)", "", "## What changed"]
        lines += [f"{i}. {c.replace('{b}', BLOB)}" for i, c in enumerate(changes, 1)]
        lines += ["", "## Headline result", headline, "", f"Full tables: [docs/release{'2' if v.endswith('.2') else '3'}_results.md]({BLOB}/{v}/docs/release{'2' if v.endswith('.2') else '3'}_results.md) and [docs/eval61.md]({BLOB}/{v}/docs/eval61.md).",
                  "", "## Known limits"] + [f"- {x}" for x in limits] + ["", f"More: [docs/versioning.md]({BLOB}/{v}/docs/versioning.md)", ""]
        open(os.path.join(ROOT, "docs", "releases", f"{v}.md"), "w").write("\n".join(lines))
        print("wrote", v)
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
