# Human spot check of the usefulness judges

[Back to the README](../README.md)

**Status: not done yet (needs Simmy).** Issues [#93](https://github.com/simmyhundal/em-upcoding-agent/issues/93) and [#19](https://github.com/simmyhundal/em-upcoding-agent/issues/19).

Neither usefulness judge has been checked against a person: the LLM judge (j1) and the rule judge (j2.3, now j3.2) agree only weakly with each other. Release 2 uses the rule judge j3.2 alone, so this check is what says whether it measures what a reviewer needs.

## What to do (about 45 minutes)
1. Open `docs/human_spot_check.csv` (25 stored summaries from the release 1 runs: 9 model-written and 8 rule-written by workflow v2.1, 8 by agent v3.1, in random order). The `evidence` column gives what a reviewer would have: claims, observed and expected 99215 share, charts returned and what they showed.
2. For each row, read the headline, rationale and next steps as an SIU reviewer deciding what to do with this provider.
3. Fill in `your_score_1_to_5`: 5 = I could act on this as written; 4 = usable with a small fix; 3 = I would need to check the evidence myself; 2 = misleading or missing something I need; 1 = wrong or unusable.
4. Fill in the five checklist columns with `y` or `n`: the leaning is explained in words; observed and expected 99215 share are both stated; the size of the excess is stated (ratio or extra claims); the chart evidence is described (how many and what they showed, or that none came back); a next step is specific and fits the leaning.
5. Use `notes` for anything a reviewer needs that no column covers.
6. Do not look at the judges' scores first. The sheet does not show them, and it never shows who is a planted upcoder.

Then run `python eval/spot_check_93.py`. It writes `docs/human_spot_check_results.md`: agreement of j3.2 with you (Spearman, exact, within one, per checklist item) and, as a side note, of the LLM judge.

## What happens with the result
j3.2's deductions are adjusted only on this evidence, and any change ships as a new judge version, so scores already recorded keep their meaning. If agreement is poor, the release 2 results should say that usefulness is unvalidated and report the checklist items, not the 1-to-5 score.
