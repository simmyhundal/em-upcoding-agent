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


def releases_4_5_notes():
    """Notes for releases 4 and 5 (data 2.2): v2.4, v3.4, v2.5, v3.5. Numbers are read from experiments/release23_table.json and experiments/release5_results.json."""
    import json
    sys.path.insert(0, os.path.join(ROOT, "eval"))
    import release_table
    t = {(r["arm"], r["seeds"]): r for r in release_table.rows()}
    r5 = json.load(open(os.path.join(ROOT, "experiments", "release5_results.json")))
    n5 = len(r5["W2.3"]["per_seed"])
    net5 = {k: sum(v["per_seed"]) / n5 for k, v in r5.items()}

    def line(arm, seeds):
        x = t[(arm, seeds)]
        prec = 100 * x["found"] / (x["found"] + x["accused"])
        return f"**{x['found']} of {x['upcoders']} upcoders found ({100 * x['found'] / x['upcoders']:.0f}% recall), {x['accused']} honest accused ({prec:.0f}% precision), ${x['net_per_seed']:,} net per seed**"
    w4, a4, w5, a5 = line("Workflow v2.4", "release 4 seeds"), line("Agent v3.4", "release 4 seeds"), line("Workflow v2.5", "release 5 seeds"), line("Agent v3.5", "release 5 seeds")
    return {
        "v2.4": ("The workflow with a learned rule for when to stop asking and a ratio gate on the second tier, on data 2.2. Evaluated once on ten fresh seeds with a pre-registered rule (issue 108).", "workflow",
                 ["**Learned stop-or-escalate.** After a provider's first sample (30 random charts and a follow-up), a fitted formula picks stop, a targeted request, the audit trail, or both (`src/policy_24.json`, fitted offline on 20 development seeds).",
                  "**Ratio gate.** Beyond the first 5% of the list, a provider is asked only when its 99215 share is at least 2.5 times expected.",
                  "**Default.** The variant with both (GL) was chosen by a rule fixed in advance; the variants with one of them (G, L) are kept for comparison."],
                 f"Ten fresh seeds (3535 to 4444): {w4}. Against workflow v2.3 on the same seeds (46 of 80 found, 6 honest accused, $26,399 net per seed), GL sent about 11 fewer rounds per seed to honest providers; the difference in upcoders found was not significant (docs/release4_results.md). Release 4 was scored in points at the time; the dollar score was applied afterwards.",
                 ["Still misses 39% of the upcoders; no version meets the 12.5% miss-rate target.", "The learned rule was fitted on development seeds and tested on ten fresh ones; the model still writes summaries where the rules are silent (not API-free until v2.5).",
                  "Ten seeds, one data version, generated notes."]),
        "v3.4": ("The agent with a read-only advisor tool and an enforced rule check, on data 2.2. Evaluated once on the release 4 fresh seeds (issue 108).", "agent",
                 ["**Advisor tool `advise_next_step`.** Says ask or skip before a request and, after the first sample, what the workflow's learned rule would do next. Advice only.",
                  "**Rules enforced.** `submit_findings` refuses until `hybrid_review` has run on every provider whose records arrived."],
                 f"Ten fresh seeds (3535 to 4444): {a4}. Against workflow v2.4 (49 of 80 found), it found fewer upcoders and sent far fewer rounds to honest providers (108 against 282). **It never called the advisor tool** in ten runs (docs/release4_agent_results.md, docs/release4_misses.md).",
                 ["The advice was not used, so v3.4 does not test whether the learned rule helps an agent.", "Agent cost about $0.25 a run (Opus 5.5, low effort); ten seeds."]),
        "v2.5": ("The workflow with ask-or-skip and stop-or-escalate both learned on net dollars, deterministic and API-free, on data 2.2. Evaluated once on ten fresh seeds with a pre-registered rule (issue 109).", "workflow",
                 ["**Net dollars are the score.** The overpayment a records sample supports (90% lower bound, cloned notes denied in full) minus $90 per round, $43.84 per round to an honest provider, $158 per provider reviewed and $2,000 per honest provider accused (`eval/dollar_reward.py`).",
                  "**Learned ask-or-skip and stop-or-escalate** fitted on that score over 30 development seeds (`src/policy_25.json`).",
                  "**No API calls.** Where the rules are silent the summary is code-written and inconclusive; on the ten test seeds the results are identical with and without the model."],
                 f"Ten fresh seeds (4545 to 5454): {w5}. On the same seeds workflow v2.4 earned ${net5['GL']:,.0f} and v2.3 ${net5['W2.3']:,.0f}. Recall did not move: the gain is lower cost and fewer false accusations (docs/release5_results.md).",
                 ["Recall stays under half; dollars rank versions at simulated scale and rest on the optimistic recovery model and an assumed $2,000 per false accusation.", "The policy was fitted on 30 development seeds; ten test seeds with about eight upcoders each."]),
        "v3.5": ("The agent with the learned advice inside its tool results, on data 2.2. Evaluated once on the release 5 fresh seeds (issue 109).", "agent",
                 ["**Advice inside tool results** (`request_records`, `follow_up_records`, `request_audit_trail`, and an `ask_advice` column in the screen), from the same policy file as workflow v2.5; use of the advice is logged.",
                  "**A narrow binding rule.** An upcoding call by the rules that the chart rule also supports cannot be overridden without a stated reason naming a fact the rules cannot see.",
                  "**Practice status every turn:** charts back, documented 99215 claims, rounds sent and their dollar cost."],
                 f"Ten fresh seeds (4545 to 5454): {a5}, against {w5.split('**')[1]} for workflow v2.5; a paired gap of $270 per seed (range -$29,015 to +$17,537), **not a confirmed difference**. The agent followed the advice on 79% of 155 actions and overrode a binding call twice, correctly both times. Ten runs cost $2.74.",
                 ["The agent's summaries score lower on the free rule judge (4.54 against 4.89 for the workflow): its own headlines quote figures the rationale does not state, and it repeats sentences. A wording issue, not weaker evidence; fixing it is issue 116.", "Recall under half; same caveats as v2.5."]),
    }


def main():
    for v, (intro, kind, changes, headline, limits) in releases_4_5_notes().items():
        n = "4" if v.endswith(".4") else "5"
        lines = [f"# {v}", "", intro, "", f"![The flow this version builds on]({RAW}/{'workflow.svg' if kind == 'workflow' else 'agent.svg'})", "", "## What changed"]
        lines += [f"{i}. {c}" for i, c in enumerate(changes, 1)]
        lines += ["", "## Headline result", headline, "", f"Full tables: [docs/release{n}_results.md]({BLOB}/{v}/docs/release{n}_results.md) and [docs/release5_dollar_baseline.md]({BLOB}/{v}/docs/release5_dollar_baseline.md).",
                  "", "## Known limits"] + [f"- {x}" for x in limits] + ["", f"More: [docs/versioning.md]({BLOB}/{v}/docs/versioning.md)", ""]
        open(os.path.join(ROOT, "docs", "releases", f"{v}.md"), "w").write("\n".join(lines))
        print("wrote", v)
    if "--only-new" in sys.argv:
        return
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
