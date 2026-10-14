# Version 1 (archived)

[Back to the README](../README.md)

Material from the first version of the system: a fixed workflow handed a records sample up front. Kept for the record; the current results are in [results-and-evaluation.md](results-and-evaluation.md).

## How the filtering works (a version 1 example)
![Funnel: 216 doctors, 25 flagged by statistics, then 8 that look like upcoding, 12 that look like sicker patients and 5 that are unclear; the 8 get recovery packets](images/funnel.svg)

The screen only says "unusual", and many honest doctors are unusual, so the AI acts as a second filter and sorts the flagged group. On this synthetic data the 8 that moved on were exactly the 8 planted upcoders; a real team would not have that answer key, which is why a person reviews the records before anything happens.


## A worked example (version 1)
Two doctors the screen flagged, drawn on the same axes. Each box shows how *other* doctors bill the top code at each patient-sickness level (0, 1, 2 ... chronic conditions); the orange dot with a bar is this doctor, with a 95% confidence range.

<table>
<tr>
<td width="50%"><img src="../experiments/261009_1_api/charts/P0215.svg" alt="Chart for provider P0215: billing of the top visit code sits well above peers at every patient-sickness level"></td>
<td width="50%"><img src="../experiments/261009_1_api/charts/P0014.svg" alt="Chart for provider P0014: billing is high but tracks a much sicker patient panel"></td>
</tr>
<tr>
<td><b>P0215 (a planted upcoder).</b> Bills the top code far more than peers at every level, even for patients with no chronic conditions: 18% of those visits against 2.1% for all doctors. The AI's summary and the records sample point the same way.</td>
<td><b>P0014 (honest, sicker patients).</b> Also flagged, but two thirds of its visits are on patients with five or more chronic conditions, and at several lower levels it bills close to its peers. The summary reads this as a heavy panel, not a billing pattern.</td>
</tr>
</table>

This is what a reviewer sees for one case (summary, key numbers, cited visits and chart):

![Example case page for provider P0215 with three key numbers, the AI's shortened explanation, cited claims and the evidence chart](images/case_card.svg)


## Does it work?
**These first results are from version 1 of the data** (`v1.0`, one random seed, small counts, so read them as directional). The version 2 results, which are closer to what a payer holds and are the current baseline, are in [Version 2](version-2.md) and in [results-and-evaluation.md](results-and-evaluation.md).

![Bar chart: of 17 honest doctors in the flagged list, 17 are accused by the screen alone, 14 after AI summaries without records evidence, and 0 after AI summaries with records evidence; all 8 real upcoders are caught in each case](images/results.svg)

- The screen (statistics only) puts **8 of 8 planted upcoders** in the top 25, along with 17 honest doctors, so the screen alone cannot tell them apart.
- AI summaries that only see billing patterns still wrongly accuse **14 of the 17** honest doctors. From billing data alone, an honest high biller and an upcoder can look the same.
- Adding a sample of **records-review evidence** (what the medical record says the visit supported) brings that to **0 of 17**, with the AI saying "inconclusive" when too few records exist (this records evidence is the unrealistic part; see [Limitations](limitations.md)). **This last result is a ceiling, not a forecast:** the records evidence is generated from the same hidden truth that defines an upcoded visit, so it makes the problem easier by construction.
- In the latest run every cited visit was real: **230 of 230** citations passed the check. The check confirms the visits exist and belong to the doctor, not that each one supports the sentence citing it.
- **The real pipeline run:** the project's own API step (Claude Opus 5.5) wrote the 25 summaries with the records evidence and got the same result: all 8 real upcoders called upcoding, 0 of 17 honest doctors, 3 of 3 sicker-panel doctors read as a heavy panel, and **261 of 261** citations real. The first two AI bars above came from agents in a chat session.
- **A held-out check:** I froze the code, generated a brand-new dataset and ran the whole pipeline once, with no tuning. The headline held: all 8 real upcoders called upcoding, 0 of 17 honest doctors accused, 278 of 278 citations real. It is still the same data generator and the same kind of records evidence, so it is a check on tuning, not on real-world difficulty (details in `experiments/261009_2_api/`).
- **Quality is not yet at the bar I set.** An independent AI grader (a different model, using a written 1-to-5 rubric) averaged **3.4 out of 5** on how useful the summaries are, against a target of 4. The usual complaints were small numeric slips, a cited visit that does not quite fit the sentence citing it, and headlines that lean a little too hard. The grader is itself an AI and makes mistakes, so this is a rough check, not a verdict.

**Level billed versus level the chart supports** (v2 data, shown as if every chart were reviewed; version 1 used a records-review sample):

![Three grids of expected level versus billed level for upcoders, normal doctors and high-acuity panels](images/expected_billed.svg)

Upcoders with honest notes bill above what their charts support on about 21% of visits, and the other groups on none. **Upcoders who clone their notes look clean**: their charts were inflated to match the bill, so the red cells vanish. The grid is built from how the data was generated, so it shows the mechanism, not proof the method works on real charts.

