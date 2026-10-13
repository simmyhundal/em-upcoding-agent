# Catching billing upcoding with AI-assisted review

**A proof of concept that finds doctors who may be billing for more complex visits than they delivered, explains why in plain language with evidence a reviewer can check, and prepares the follow-up for the team that recovers money. It tells those doctors apart from honest ones who simply treat sicker patients.**

Everything here runs on **synthetic (invented) data** shaped like real Medicare billing. No real patients, doctors or claims are used.

## What problem does this solve?
When you see a doctor for an ordinary office visit, the doctor bills your insurer using one of five codes (99211 to 99215). Higher codes mean a longer, more complex visit and **pay more**. **Upcoding** is billing a higher code than the visit justified. It costs health insurers and Medicare money, and teams called *payment integrity* or *special investigations* look for it.

The hard part: a doctor who bills the top code often is **not necessarily cheating**. They may just see sicker patients. A useful tool has to tell those two cases apart, and it has to show its evidence, because a wrong accusation is costly.

## What does this project do?
![Statistics screens upcoders then AI suggests and explains. Humans review generated cases. Eight steps: billing data, statistical screen, AI review, AI filter, citation check, case pages, recovery packets, people review.](docs/images/pipeline.svg)

1. **Billing data.** A fake (synthetic) population of 216 family doctors in Georgia, about 100,000 visits, shaped to match public Medicare statistics. Eight doctors are planted upcoders, eight are honest but treat unusually sick patients, and the rest are typical. Because the answer is known, the tools can be graded.
2. **Statistical screen.** Statistics flag doctors who bill the top visit code unusually often, adjusted for how sick their patients are. The most unusual go on: the top 25, or everyone above a chosen suspicion level. It is a wide net: it catches the upcoders but also many honest doctors.
3. **AI review.** An AI reads each flagged doctor's billing pattern and the records sample, and writes a short explanation that **cites the exact visits** it relies on.
4. **AI filter.** In the same call, the AI suggests whether each flagged doctor looks like upcoding, like a sicker patient base, or unclear. **This is the second filter: the doctors it calls upcoding are the suspected upcoders, and only they move on.** On this synthetic data it kept all 8 planted upcoders and set aside all 17 honest doctors; see [Limitations](#limitations-of-this-version) for why that is optimistic.
5. **Citation check.** Plain code rejects any summary that cites a visit that does not exist or belongs to a different doctor.
6. **Case pages.** One page per flagged doctor: the summary, its cited visits, and a chart comparing the doctor to peers.
7. **Recovery packets.** For the suspected upcoders only: draft material for the team that recovers money, namely which records to request, a reproducible sampling plan, and a way to estimate the overpayment with a confidence range.
8. **People review.** SIU reviewers read the cases, payment integrity requests records, and people make every real decision. Nothing happens to a doctor without a person checking the records.

In short: statistics cast a wide net, the AI is the second filter that decides who the suspected upcoders are, and people decide what happens next. The AI's call is advice, not a verdict, and its accuracy here rests on a records sample that a payer would not normally have at this point (see [Limitations](#limitations-of-this-version)).

## How the filtering works
![Funnel: 216 doctors, 25 flagged by statistics, then 8 that look like upcoding, 12 that look like sicker patients and 5 that are unclear; the 8 get recovery packets](docs/images/funnel.svg)

The screen only says "unusual", and many honest doctors are unusual, so the AI acts as a second filter and sorts the flagged group. On this synthetic data the 8 that moved on were exactly the 8 planted upcoders; a real team would not have that answer key, which is why a person reviews the records before anything happens.

## A worked example
Two doctors the screen flagged, drawn on the same axes. Each box shows how *other* doctors bill the top code at each patient-sickness level (0, 1, 2 ... chronic conditions); the orange dot with a bar is this doctor, with a 95% confidence range.

<table>
<tr>
<td width="50%"><img src="experiments/261009_1_api/charts/P0215.svg" alt="Chart for provider P0215: billing of the top visit code sits well above peers at every patient-sickness level"></td>
<td width="50%"><img src="experiments/261009_1_api/charts/P0014.svg" alt="Chart for provider P0014: billing is high but tracks a much sicker patient panel"></td>
</tr>
<tr>
<td><b>P0215 (a planted upcoder).</b> Bills the top code far more than peers at every level, even for patients with no chronic conditions: 18% of those visits against 2.1% for all doctors. The AI's summary and the records sample point the same way.</td>
<td><b>P0014 (honest, sicker patients).</b> Also flagged, but two thirds of its visits are on patients with five or more chronic conditions, and at several lower levels it bills close to its peers. The summary reads this as a heavy panel, not a billing pattern.</td>
</tr>
</table>

This is what a reviewer sees for one case (summary, key numbers, cited visits and chart):

![Example case page for provider P0215 with three key numbers, the AI's shortened explanation, cited claims and the evidence chart](docs/images/case_card.svg)

## Does it work?
**These first results are from version 1 of the data** (`v1.0`, one random seed, small counts, so read them as directional). The version 2 results, which are closer to what a payer holds and are the current baseline, are in [Version 2](#version-2-inputs-closer-to-what-a-payer-holds-milestone-5) below and in the Eval table.

![Bar chart: of 17 honest doctors in the flagged list, 17 are accused by the screen alone, 14 after AI summaries without records evidence, and 0 after AI summaries with records evidence; all 8 real upcoders are caught in each case](docs/images/results.svg)

- The screen (statistics only) puts **8 of 8 planted upcoders** in the top 25, along with 17 honest doctors, so the screen alone cannot tell them apart.
- AI summaries that only see billing patterns still wrongly accuse **14 of the 17** honest doctors. From billing data alone, an honest high biller and an upcoder can look the same.
- Adding a sample of **records-review evidence** (what the medical record says the visit supported) brings that to **0 of 17**, with the AI saying "inconclusive" when too few records exist (this records evidence is the unrealistic part; see [Limitations](#limitations-of-this-version)). **This last result is a ceiling, not a forecast:** the records evidence is generated from the same hidden truth that defines an upcoded visit, so it makes the problem easier by construction.
- In the latest run every cited visit was real: **230 of 230** citations passed the check. The check confirms the visits exist and belong to the doctor, not that each one supports the sentence citing it.
- **The real pipeline run:** the project's own API step (Claude Opus 5.5) wrote the 25 summaries with the records evidence and got the same result: all 8 real upcoders called upcoding, 0 of 17 honest doctors, 3 of 3 sicker-panel doctors read as a heavy panel, and **261 of 261** citations real. The first two AI bars above came from agents in a chat session.
- **A held-out check:** I froze the code, generated a brand-new dataset and ran the whole pipeline once, with no tuning. The headline held: all 8 real upcoders called upcoding, 0 of 17 honest doctors accused, 278 of 278 citations real. It is still the same data generator and the same kind of records evidence, so it is a check on tuning, not on real-world difficulty (details in `experiments/261009_2_api/`).
- **Quality is not yet at the bar I set.** An independent AI grader (a different model, using a written 1-to-5 rubric) averaged **3.4 out of 5** on how useful the summaries are, against a target of 4. The usual complaints were small numeric slips, a cited visit that does not quite fit the sentence citing it, and headlines that lean a little too hard. The grader is itself an AI and makes mistakes, so this is a rough check, not a verdict.

**Level billed versus level the chart supports** (v2 data, shown as if every chart were reviewed; version 1 used a records-review sample):

![Three grids of expected level versus billed level for upcoders, normal doctors and high-acuity panels](docs/images/expected_billed.svg)

Upcoders with honest notes bill above what their charts support on about 21% of visits, and the other groups on none. **Upcoders who clone their notes look clean**: their charts were inflated to match the bill, so the red cells vanish. The grid is built from how the data was generated, so it shows the mechanism, not proof the method works on real charts.

## How are office-visit levels really chosen?
In practice nobody grades a visit when it is billed. The doctor picks the level, the claim is paid, and any checking happens later.

![How an office-visit level is chosen and checked](docs/images/em_levels.svg)

Since 2021 the level (99212 to 99215) comes from **either** the medical decision making in the visit (two of three elements: problems, data, risk) **or** the doctor's total time that day. Later, contractors and auditors re-score a sample of notes against the same rules. Most errors found this way are notes that do not support the level billed, not proven fraud, and borderline calls (99214 versus 99215) are where reviewers disagree most. Thresholds change over time, so check the current CPT and CMS guidance before relying on the numbers above. This project uses a much simpler stand-in for step 1; see the limitations below.

## The agent (Milestone 6)
The frozen workflow (`v2.0`) fixes the order of steps in code. Milestone 6 built the other design to compare against it: an **agent** that gets tools and decides what to do: which screen to run and where to put the cutoff, which providers to look at, whether to ask a provider's office for charts, what to do about an incomplete response, and when to stop. Code only supplies tools and enforces limits (tool calls, dollars, records requests) and logs every call. Tools, limits and what the agent can see: [docs/agent_tools.md](docs/agent_tools.md); the simulated provider office it negotiates with: [docs/provider_sim.md](docs/provider_sim.md).

**Head-to-head on two reserved seeds (202 and 303; never looked at before this test), 8 upcoders each, same simulated office for every arm.** Totals over the two seeds (16 upcoders, 416 honest doctors):

| Arm | Upcoders found (of 16) | Honest doctors accused | Honest doctors sent records requests | Request rounds (all / on honest) | Cost per seed |
|---|---|---|---|---|---|
| Workflow, screen at suspicion 5, fixed office policy | 6 | 0 | 17 | 41 / 23 | $0.19 to $0.35 |
| Workflow, screen at top 25, fixed office policy | 6 | 0 | 35 | 71 / 49 | $0.40 to $0.43 |
| Agent with the screen tool (3 runs per seed) | 4 in every run | 0 | 8 to 9 | 23 to 26 / 11 to 13 | $0.27 to $0.39 |
| Agent without the screen tool | 4 | 0 | 12 | 28 / 16 | $0.30 to $0.36 |
| Workflow as frozen in v2.0, single-draw records (not a fair baseline) | 3 | 3 | 17 | 30 / 17 | $0.25 to $0.35 |

Workflow costs include the usefulness judge; agent costs do not (about $0.05 more per run).

- **No arm is good enough.** The best found 4 of 8 on one seed; the false negative threshold is 1 of 8. Every arm is limited by what it can reach, not by false accusations.
- **The agent did not find more upcoders than the workflow.** It found 4 of 16 to the workflow's 6 of 16 (a gap of two doctors). Repeating the agent three times per seed gave the same 2 of 8 every time, so the run-to-run noise is small here and the gap is more likely a real difference in reach, but 16 upcoders is still few. It also asked far fewer honest practices for records (9 against 17 or 35) and used fewer request rounds. Both agents screened with the combined rank at the top 25 (with at least 100 claims) and never tried a suspicion cutoff, then narrowed to 12 or 13 providers before asking for charts. So on this evidence the agent's contribution is **restraint, not reach**.
- **The screen mattered little for the agent's reach, more for its burden.** Without the screen tool the agent found the same 2 of 8 on each seed and asked more honest practices on one seed (8 against 4). One seed is not a pattern.
- **Nothing here shows the agent beating a fixed policy.** One run per arm per seed, 16 upcoders in all, a simulated office, and cloned notes that defeat chart-based checks. **The agent's summaries are less useful by the judge's rubric:** 2.6 to 3.0 with the screen tool and 2.3 without, against 3.3 to 3.6 for the workflow's (target 4); the agent writes a shorter interpretation and more of its numbers fail the number check (about 65% to 85% of its summaries pass against 92% to 100%).
- The rows, with dollars at stake and request rounds, are in the Eval table below; the protocol (arms, seeds, rules) is [issue 50](https://github.com/simmyhundal/em-upcoding-agent/issues/50).

## Limitations of this version
- **The inputs are unrealistic: the AI sees records a payer would not have yet.** A payer normally screens on claims data alone. Medical records (the equivalent of this project's `documentation.csv`) reach a payer only after it requests them from the fee-for-service primary care physician, and that request usually comes after a provider is already suspected. Here, a records sample is handed to the AI *before* it decides. It stands in for a first records request, but the order of events is not how it works in practice.
- **Why that matters.** The AI's filtering power comes largely from that sample. With it the AI accused 0 of 17 honest doctors; without it (the chat-session runs) it accused 14 of 17. So read the results as what the AI can do once records are in hand, not as detection from claims alone. Put another way, in this version the AI turns a records sample into a cited, checkable case file, and it is also the filter that decides which flagged doctors move on, but its accuracy rests on that sample.
- **Status.** [Milestone 5](https://github.com/simmyhundal/em-upcoding-agent/milestone/5) rebuilt the inputs the way a payer would receive them and models records requests as a later step (see Version 2 below). The AI results above are still from version 1; the AI has not been re-run on version 2 yet.
- **The documentation signal is cleaner than real records.** In this data the documented level is a noisy copy of the hidden truth, and the documented minutes are filled in to match it exactly, so time never disagrees with the decision-making level. Real records are messier: upcoding practices may also inflate the documentation, and time and decision making are recorded independently. Version 2 addresses this (separate MDM elements, independent time, cloned notes); it is not yet used for the AI results.
- **Other limits.** Synthetic data from one generator; two seeds; the usefulness score comes from an AI grader and is below its target; the citation check confirms cited visits exist, not that each one supports its sentence.

## Version 2: inputs closer to what a payer holds (Milestone 5)
Version 1 handed the screen tidy tables and the AI a ready-made records sample. Version 2 (data under `src/generate_v2.py`, schemas in [docs/v2_schemas.md](docs/v2_schemas.md)) changes that:
- **Plan-shaped tables:** members with coverage spans, a provider directory, claim headers and lines, remittance with denials, replacement and void claims, and a fee schedule. Conditions and risk are **derived from diagnosis codes on claims**, across every provider a member saw, never stored on the member.
- **Records are requested, not given.** After the screen flags a provider the plan requests a limited sample of charts; some never arrive, some arrive late, and coders disagree about borderline levels. A small control sample of unflagged providers stands in for prior reviews as the peer baseline.
- **Realistic documentation:** the three MDM elements (problems, data, risk) and recorded minutes are separate; the documented level is the second-highest element or the level the time supports, whichever is higher. Some upcoders **clone their notes** so charts match the bill (a tunable share).
- **Base rate is a setting**, so low rates can be tested. Recovery estimates are priced from each sampled claim's allowed and paid amounts.

What the code-only runs show (no AI yet; rows are in the Eval table above, thresholds for the rules were frozen after looking at seed 42):
- **The screen is weaker on v2.** At suspicion 5 it misses 2 of 8 upcoders on seed 42 and 4 of 8 on the held-out seed 101 (version 1 missed none), because risk derived from claims is noisier than a stored condition count. The top 25 still reaches all 8 on seed 42, with 17 honest doctors flagged beside them.
- **Precision collapses as upcoding gets rarer.** Of the doctors the screen flags at suspicion 5, 46% are upcoders at a 3.7% base rate, 43% at 2%, 15% at 1% and 9% at 0.5%. A realistic base rate makes the second filter matter much more.
- **A simple rule on the charts works until notes are cloned.** Flagging doctors whose charts support a lower level than billed finds every upcoder the screen sent when nobody clones notes, flags no honest doctor, and finds **none** when every upcoder clones. A rule that checks note claims against the claim itself (a "moderate data reviewed" note with no lab or test line on the claim) is a weak backstop: it accused honest doctors in several runs.
- **Cheaper AI step.** Code now writes the numeric facts, the cited claims and the next steps, and a few plain rules decide the clear-cut cases outright (documented 99215 claims mostly unsupported, or mostly supported with a share close to expected). On the saved packets those rules decided about 16% of cases, 36% on version 1 and about 15% on version 2, and made no wrong call in 25 decisions; the rest still go to the model. The model reads a compact evidence card (about half the input tokens of the old pretty-printed packet) and calls run through the half-price Batch API with a response cache, so repeats cost nothing. A version 2 AI run cost about $0.25 including the judge, against about $2 before (four runs plus one judge re-run: about $1.04). A number checker (no model) verifies every figure in a summary against the card.
- **The AI on v2 data (four runs, about $0.25 each).** The model writes only the cases the rules cannot decide (11 of 13, 8 of 9, 9 of 13 and 9 of 9 providers). Citations stay at 100%; usefulness is 3.4 to 3.7 against a target of 4; the number checker matched every figure in 43 of 44 summaries. Against the screen and the simple chart rule (see the Eval table):
  - **Nobody clones notes:** the chart rule finds 6 of 8 upcoders and the AI finds 4 of 8. The simple rule is better, and neither accuses an honest doctor.
  - **Half clone:** the AI and the rule each find 2 on seed 42 (no honest doctor accused); on the held-out seed the AI finds 2 and the rule 1, but the AI accuses one honest doctor (precision 67%).
  - **Every upcoder clones:** the chart rule finds none and the AI finds 3 of 8, with one honest doctor accused (precision 75%). This is the only setting where the AI clearly adds something, by reading the claims against the notes.
  - **At lower base rates the AI step breaks down.** With 600 doctors (seed 7), the AI found 0 of 3 upcoders at a 0.5% rate and accused 5 of the 20 honest doctors the screen sent (precision 0%); at 1% it found 2 of 6 and accused 3 of 17 (precision 40%); at 2% it found 4 of 12 and accused 1 of 13 (precision 80%). The thinner the real signal, the more the model reads patterns into honest doctors. This is the clearest reason not to trust the 3.7% results as a forecast. Cost for these three runs: $1.33.
  - **Hybrid (chart rule first, model only where the rules are silent), computed from the stored outputs:** it finds at least as many upcoders as the AI step in every run and more in two (6 vs 4 of 8 when nobody clones; 5 vs 4 of 12 at 2%), but it does not remove the model's false accusations (1 honest doctor in the all-clone run and the held-out run, 5 of 20 at 0.5%). The "Hybrid" rows in the Eval table; a live version where the model also sees the chart-rule result is still to run.
  - **The biggest loss is upstream:** the screen at suspicion 5 sends only 4 to 6 of the 8 upcoders on for review, and no later step can recover the rest.
  - **Read with care:** 8 upcoders per run, so one doctor moves a rate by 12.5 points; thresholds for the rules were set on seed 42; the cloned-notes mechanism is an assumption.
- **Asking for more charts barely helps** ([sample-size sweep](docs/sample_size_sweep.md)): requesting 10, 20, 30, 60 or 100 charts per flagged provider, the AI called 0, 2, 2, 2 and 3 of the 8 upcoders on seed 42 with no honest doctor accused, and the chart rule found 1 to 2. The limit is upstream: the screen sent only 6 of the 8, and 4 of those clone their notes.
- Caveats: same generator family, small counts, and the cloned-notes mechanism and its prevalence are assumptions.

## Built responsibly
- **Synthetic data only.** No real patients, doctors or claims, and no real provider is ever flagged.
- **The AI advises; people decide.** Statistics choose who is reviewed. The AI sorts the flagged cases (upcoding, sicker patients, or unclear) as advice to a reviewer, and nothing happens to anyone without a person checking the records.
- **A guardrail on the AI.** Invented evidence is rejected automatically.
- **Honest reporting.** The reports state what is easier by construction, what is simulated, and where the data is thin.
- **Nothing here accuses anyone.** The recovery packet is draft material for human, compliance and legal review. It does not write demand letters or make findings.

## What this project demonstrates
- Framing an open-ended problem (fraud versus legitimate complexity) as something measurable.
- Designing and calibrating synthetic data against public Medicare statistics so a method can be graded against a known answer.
- Evaluation design and candid reporting: baselines, a ground-truth answer key kept apart from the tools, results tables with caveats, and a log of what went wrong (see the experiment READMEs).
- Putting an LLM in a pipeline with guardrails and tests, rather than trusting its output.
- Building for the downstream user: charts a reviewer can read, and a packet the recovery team can act on.
- Test-driven delivery: 7 test files, and work tracked as GitHub issues grouped into milestones.

## Glossary
| Term | Meaning |
|---|---|
| E/M visit | An ordinary office visit (evaluation and management) that a doctor bills by complexity |
| CPT 99211 to 99215 | Five billing codes for established-patient office visits; a higher number means a more complex, higher-paying visit; 99215 is the top |
| Upcoding | Billing a higher visit code than the visit justified |
| Medical decision-making (MDM) | The doctor's documented reasoning that supports a visit's level |
| Medicare | US government health insurance; its public billing statistics shape the synthetic data |
| Payment integrity | The team that checks claims were paid correctly and recovers overpayments |
| SIU | Special Investigations Unit: reviewers who look into suspected billing abuse |
| Synthetic data | Invented data with realistic statistical shape, so no real person is involved |
| Z-score | How far a number sits from the average, in units of typical variation |
| Confidence interval | A range that likely contains the true value |
| Guardrail | An automatic check that blocks bad output |
| LLM | "Large language model": the kind of AI that writes the case summaries |
| Hard negative | An honest provider who looks suspicious at first glance |

## Explore the repo
- **Case pages (the review queue):** [experiments/261009_1_api/cases/index.md](experiments/261009_1_api/cases/index.md), with charts in [experiments/261009_1_api/charts/](experiments/261009_1_api/charts/)
- **Eval report:** [reports/eval_report.md](reports/eval_report.md)
- **Recovery packets (simulated review):** [experiments/261009_1_api/pi_packets/](experiments/261009_1_api/pi_packets/), explained in [docs/payment_integrity.md](docs/payment_integrity.md). Each run keeps its own charts, case pages and packets in its folder, so a later run never overwrites them.
- **Data design and calibration notes:** [docs/synthetic_data.md](docs/synthetic_data.md)
- **Experiments and what they do and do not show:** [experiments/README.md](experiments/README.md)
- **Open and closed work:** the GitHub issues and milestones for this repository
- **For AI agents working on this repo:** [CLAUDE.md](CLAUDE.md)

To rebuild the figures above: `python docs/make_figures.py`.

---

## For technical readers

### The bet
Statistics find outliers, but a raw outlier is not an upcoder: some providers legitimately see sicker patients. Two jobs, two tools:
- **The statistical screen selects.** It uses the numeric signal, billed level versus what patient complexity predicts, to choose who gets a close look.
- **The LLM then reads and sorts.** For each selected provider it reads structured evidence (patient complexity, sample visits, and a records-review sample giving each sampled visit's documented level and minutes) and writes a cited summary with an advisory leaning (upcoding, high-acuity panel, or inconclusive). That leaning is what separates real upcoders from honest doctors with sicker patients, and it decides which cases move on to the recovery packet. It does not set the flag, and it is not a verdict: people review the records.

In the live runs most of the separation came from the records-review evidence, not from the billing numbers alone. "Path A", an LLM judging from free-text clinical notes, is parked (see Roadmap); today's evidence is structured, not free text.

### Approach
1. **Baselines** - realistic E/M level mix for Family Practice in GA, from CMS's public *Medicare Physician & Other Practitioners - by Provider and Service* file (aggregated, no PHI).
2. **Synthetic data** - ~200 normal providers, 8 planted upcoders, 8 hard negatives (high 99215 share explained by sicker panels), with synthetic patients and claim lines, calibrated to the CMS distribution.
3. **Detectors** (the main metric is each provider's 99215 share):
   - *Baseline 1*: plain z-score of 99215 share against peers.
   - *Baseline 2*: risk-adjusted observed-versus-expected, using patient complexity (visit-weighted chronic-condition count).
4. **Flagging** - choose who goes to review: by default the top N (25), or every provider at or above a chosen suspicion level (`python src/flagging.py ... --min-suspicion 5`, with optional `--max-flagged` and `--min-claims`). A threshold flags fewer, better-targeted providers and cuts the number of AI calls; see `docs/threshold_sweep.md` for what each cutoff would flag.
5. **Case summaries (LLM)** - for each flagged provider, summarise the claims and patient complexity as `{decision_rationale, cited_claim_ids[]}`. The LLM does not set the flag (the screen does); it advises, and its advice gates the recovery packet.
6. **Guardrail** - rejects any summary citing claim IDs that don't exist for that provider.

### Eval
Every run is graded against the same thresholds. How each is computed is in `eval/`; per-run detail tables are in `reports/eval_report.md`.

| Eval | Threshold |
|---|---|
| False negative rate | at most 12.5% of the real upcoders missed (1 of 8) |
| False positive rate | at most 12.5% of the honest doctors a step examines are wrongly accused. For the screen that is all honest doctors in the data; for the AI step it is the honest doctors the screen sent to it. "Honest" means every non-upcoder, ordinary doctors and sicker-panel doctors alike |
| Precision of "upcoding" calls | at least 80% are real upcoders (*proposed*; the end-to-end check on how trustworthy an accusation is, which the screen's false positive rate does not capture) |
| Citations valid | 100% |
| Case Summary Usefulness (1-5) | average of at least 4 (scored by an LLM judge) |

Note that in the synthetic data, billed level depends on patient complexity by construction, so the risk-adjusted baseline is helped by how the data was built. Report that plainly.

### Status
Done: synthetic data generator (with a records-review documentation sample), both baselines, flagging, case-summary step (run live on the API), citation guardrail, evidence charts and case pages, Payment Integrity packet, eval harness (detectors, LLM leanings, deterministic number check, LLM-judge usefulness), a held-out run.

**What is the suspicion score?** It is the risk-adjusted score from the statistical screen. For every doctor, the screen predicts how often they should bill the top visit code (99215) given how many chronic conditions their patients have, then compares that with what they billed: (billed - expected) / the statistical noise you would expect by chance. That raw score is then rescaled by the typical spread across all doctors, because honest doctors legitimately differ too. A score of 0 is the middle of the pack; in the seed-42 data a score of 5 is about where the top 5% of doctors begin, and the highest score is above 22. It is computed from claims and patient condition counts only, never from the records sample.

The **Tuning** column says how the list was chosen: the top 25 outliers, or everyone at or above a suspicion level. On AI rows it also names the screen that fed the AI.

Each run has a **Screen** row (the statistical screen's flagged doctors count as accused) and, when AI summaries were written, an **AI** row (what the AI called upcoding, out of the doctors the screen sent it). **Records evidence** says whether the AI was shown the records-review sample. 🟩 means the threshold was met, 🟥 means it was missed, and a dash means not scored or not applicable and is left out of the total.

<!-- scoreboard:start -->
| Run | Seed | Seed status | Source | Agents | Code version | Data version | Upcoders in data | Upcoder clone level | Screen / AI | Tuning | Records evidence | False negative rate | False positive rate | Precision of upcoding calls | Citations valid | Case Summary Usefulness (1-5) | Evals passed | Evals scored | Honest doctors sent records requests | Request rounds (honest / total) | Dollars overpaid to upcoders | Dollars at stake in upcoders called |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Threshold** | | | | | | | | | | | | at most 12.5% | at most 12.5% | at least 80% (proposed) | 100% | at least 4 | | | | | | |
| screen_v1_s42 | 42 | development | code | – | v1.0 | v1 | 3.7% (8 of 216) | n/a | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟩 0.0%<br>(0 / 8) | 🟩 1.4%<br>(3 / 208) | 🟥 73% | – | – | **2** | 3 | – | – | $59,578 | $59,578 (100%) |
| 261008_2_cc | 42 | development | cc | – | v1.0 | v1 | 3.7% (8 of 216) | n/a | Screen | Top 25 upcoding outliers | No | 🟩 0.0%<br>(0 / 8) | 🟩 8.2%<br>(17 / 208) | 🟥 32% | – | – | **2** | 3 | – | – | $59,578 | $59,578 (100%) |
| 261008_2_cc | 42 | development | cc | 1 | v1.0 | v1 | 3.7% (8 of 216) | n/a | AI | AI calls upcoding (screen: top 25 upcoding outliers) | No | 🟩 12.5%<br>(1 / 8) | 🟥 58.8%<br>(10 / 17) | 🟥 41% | 🟩 100% | – | **2** | 4 | – | – | $59,578 | $53,906 (90%) |
| 261008_3_cc | 42 | development | cc | – | v1.0 | v1 | 3.7% (8 of 216) | n/a | Screen | Top 25 upcoding outliers | No | 🟩 0.0%<br>(0 / 8) | 🟩 8.2%<br>(17 / 208) | 🟥 32% | – | – | **2** | 3 | – | – | $59,578 | $59,578 (100%) |
| 261008_3_cc | 42 | development | cc | 25 | v1.0 | v1 | 3.7% (8 of 216) | n/a | AI | AI calls upcoding (screen: top 25 upcoding outliers) | No | 🟩 0.0%<br>(0 / 8) | 🟥 82.4%<br>(14 / 17) | 🟥 36% | 🟩 100% | – | **2** | 4 | – | – | $59,578 | $59,578 (100%) |
| 261008_4_cc | 42 | development | cc | – | v1.0 | v1 | 3.7% (8 of 216) | n/a | Screen | Top 25 upcoding outliers | No | 🟩 0.0%<br>(0 / 8) | 🟩 8.2%<br>(17 / 208) | 🟥 32% | – | – | **2** | 3 | – | – | $59,578 | $59,578 (100%) |
| 261008_4_cc | 42 | development | cc | 25 | v1.0 | v1 | 3.7% (8 of 216) | n/a | AI | AI calls upcoding (screen: top 25 upcoding outliers) | Yes | 🟩 0.0%<br>(0 / 8) | 🟩 0.0%<br>(0 / 17) | 🟩 100% | 🟩 100% | – | **4** | 4 | – | – | $59,578 | $59,578 (100%) |
| 261009_1_api | 42 | development | api | – | v1.0 | v1 | 3.7% (8 of 216) | n/a | Screen | Top 25 upcoding outliers | No | 🟩 0.0%<br>(0 / 8) | 🟩 8.2%<br>(17 / 208) | 🟥 32% | – | – | **2** | 3 | – | – | $59,578 | $59,578 (100%) |
| 261009_1_api | 42 | development | api | 25 | v1.0 | v1 | 3.7% (8 of 216) | n/a | AI | AI calls upcoding (screen: top 25 upcoding outliers) | Yes | 🟩 0.0%<br>(0 / 8) | 🟩 0.0%<br>(0 / 17) | 🟩 100% | 🟩 100% | 🟥 3.44 | **4** | 5 | – | – | $59,578 | $59,578 (100%) |
| screen_v1_s101 | 101 | held-out | code | – | v1.0 | v1 | 3.7% (8 of 216) | n/a | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟩 0.0%<br>(0 / 8) | 🟩 0.5%<br>(1 / 208) | 🟩 89% | – | – | **3** | 3 | – | – | $54,523 | $54,523 (100%) |
| 261009_2_api | 101 | held-out | api | – | v1.0 | v1 | 3.7% (8 of 216) | n/a | Screen | Top 25 upcoding outliers | No | 🟩 0.0%<br>(0 / 8) | 🟩 8.2%<br>(17 / 208) | 🟥 32% | – | – | **2** | 3 | – | – | $54,523 | $54,523 (100%) |
| 261009_2_api | 101 | held-out | api | 25 | v1.0 | v1 | 3.7% (8 of 216) | n/a | AI | AI calls upcoding (screen: top 25 upcoding outliers) | Yes | 🟩 0.0%<br>(0 / 8) | 🟩 0.0%<br>(0 / 17) | 🟩 100% | 🟩 100% | 🟥 3.24 | **4** | 5 | – | – | $54,523 | $54,523 (100%) |
| 261012_8_api | 42 | development | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟥 25.0%<br>(2 / 8) | 🟩 3.4%<br>(7 / 208) | 🟥 46% | – | – | **1** | 3 | – | – | $44,856 | $41,216 (92%) |
| 261012_8_api | 42 | development | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Rules | Documented level below billed in over 15% of returned charts | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 7) | 🟩 100% | – | – | **2** | 3 | 7 | 7 / 13 | $44,856 | $23,887 (53%) |
| 261012_8_api | 42 | development | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Rules | Note claims moderate+ data but claim has no lab or test line, over 12% of returned charts | Yes | 🟥 62.5%<br>(5 / 8) | 🟥 14.3%<br>(1 / 7) | 🟥 75% | – | – | **0** | 3 | 7 | 7 / 13 | $44,856 | $14,951 (33%) |
| 261012_8_api | 42 | development | api | 11 | v2.0 | v2 | 3.7% (8 of 216) | 50% | AI | AI calls upcoding (screen: z-score of risk-adjusted coding >= 5) | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 7) | 🟩 100% | 🟩 100% | 🟥 3.54 | **3** | 5 | 7 | 7 / 13 | $44,856 | $23,887 (53%) |
| 261012_8_api | 42 | development | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Hybrid | Chart rule first, then summary rules and model | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 7) | 🟩 100% | – | – | **2** | 3 | 7 | 7 / 13 | $44,856 | $23,887 (53%) |
| 261012_9_api | 101 | held-out | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟥 50.0%<br>(4 / 8) | 🟩 2.4%<br>(5 / 208) | 🟥 44% | – | – | **1** | 3 | – | – | $14,448 | $8,774 (61%) |
| 261012_9_api | 101 | held-out | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Rules | Documented level below billed in over 15% of returned charts | Yes | 🟥 87.5%<br>(7 / 8) | 🟩 0.0%<br>(0 / 5) | 🟩 100% | – | – | **2** | 3 | 5 | 5 / 9 | $14,448 | $1,815 (13%) |
| 261012_9_api | 101 | held-out | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Rules | Note claims moderate+ data but claim has no lab or test line, over 12% of returned charts | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 5) | 🟩 100% | – | – | **2** | 3 | 5 | 5 / 9 | $14,448 | $5,088 (35%) |
| 261012_9_api | 101 | held-out | api | 8 | v2.0 | v2 | 3.7% (8 of 216) | 50% | AI | AI calls upcoding (screen: z-score of risk-adjusted coding >= 5) | Yes | 🟥 75.0%<br>(6 / 8) | 🟥 20.0%<br>(1 / 5) | 🟥 67% | 🟩 100% | 🟥 3.44 | **1** | 5 | 5 | 5 / 9 | $14,448 | $3,686 (26%) |
| 261012_9_api | 101 | held-out | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Hybrid | Chart rule first, then summary rules and model | Yes | 🟥 75.0%<br>(6 / 8) | 🟥 20.0%<br>(1 / 5) | 🟥 67% | – | – | **0** | 3 | 5 | 5 / 9 | $14,448 | $3,686 (26%) |
| 261012_12_api | 7 | held-out | api | – | v2.0 | v2 | 0.5% (3 of 600) | 50% | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟥 33.3%<br>(1 / 3) | 🟩 3.4%<br>(20 / 597) | 🟥 9% | – | – | **1** | 3 | – | – | $18,862 | $16,014 (85%) |
| 261012_12_api | 7 | held-out | api | – | v2.0 | v2 | 0.5% (3 of 600) | 50% | Rules | Documented level below billed in over 15% of returned charts | Yes | 🟥 100.0%<br>(3 / 3) | 🟩 0.0%<br>(0 / 20) | – | – | – | **1** | 2 | 20 | 20 / 22 | $18,862 | $0 (0%) |
| 261012_12_api | 7 | held-out | api | – | v2.0 | v2 | 0.5% (3 of 600) | 50% | Rules | Note claims moderate+ data but claim has no lab or test line, over 12% of returned charts | Yes | 🟥 100.0%<br>(3 / 3) | 🟥 15.0%<br>(3 / 20) | 🟥 0% | – | – | **0** | 3 | 20 | 20 / 22 | $18,862 | $0 (0%) |
| 261012_12_api | 7 | held-out | api | 21 | v2.0 | v2 | 0.5% (3 of 600) | 50% | AI | AI calls upcoding (screen: z-score of risk-adjusted coding >= 5) | Yes | 🟥 100.0%<br>(3 / 3) | 🟥 25.0%<br>(5 / 20) | 🟥 0% | 🟩 100% | 🟥 3.45 | **1** | 5 | 20 | 20 / 22 | $18,862 | $0 (0%) |
| 261012_12_api | 7 | held-out | api | – | v2.0 | v2 | 0.5% (3 of 600) | 50% | Hybrid | Chart rule first, then summary rules and model | Yes | 🟥 100.0%<br>(3 / 3) | 🟥 25.0%<br>(5 / 20) | 🟥 0% | – | – | **0** | 3 | 20 | 20 / 22 | $18,862 | $0 (0%) |
| 261012_13_api | 7 | held-out | api | – | v2.0 | v2 | 1.0% (6 of 600) | 50% | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟥 50.0%<br>(3 / 6) | 🟩 2.9%<br>(17 / 594) | 🟥 15% | – | – | **1** | 3 | – | – | $21,794 | $7,511 (34%) |
| 261012_13_api | 7 | held-out | api | – | v2.0 | v2 | 1.0% (6 of 600) | 50% | Rules | Documented level below billed in over 15% of returned charts | Yes | 🟥 100.0%<br>(6 / 6) | 🟩 0.0%<br>(0 / 17) | – | – | – | **1** | 2 | 17 | 17 / 20 | $21,794 | $0 (0%) |
| 261012_13_api | 7 | held-out | api | – | v2.0 | v2 | 1.0% (6 of 600) | 50% | Rules | Note claims moderate+ data but claim has no lab or test line, over 12% of returned charts | Yes | 🟥 50.0%<br>(3 / 6) | 🟩 5.9%<br>(1 / 17) | 🟥 75% | – | – | **1** | 3 | 17 | 17 / 20 | $21,794 | $7,511 (34%) |
| 261012_13_api | 7 | held-out | api | 19 | v2.0 | v2 | 1.0% (6 of 600) | 50% | AI | AI calls upcoding (screen: z-score of risk-adjusted coding >= 5) | Yes | 🟥 66.7%<br>(4 / 6) | 🟥 17.6%<br>(3 / 17) | 🟥 40% | 🟩 100% | 🟥 3.25 | **1** | 5 | 17 | 17 / 20 | $21,794 | $4,288 (20%) |
| 261012_13_api | 7 | held-out | api | – | v2.0 | v2 | 1.0% (6 of 600) | 50% | Hybrid | Chart rule first, then summary rules and model | Yes | 🟥 66.7%<br>(4 / 6) | 🟥 17.6%<br>(3 / 17) | 🟥 40% | – | – | **0** | 3 | 17 | 17 / 20 | $21,794 | $4,288 (20%) |
| 261012_14_api | 7 | held-out | api | – | v2.0 | v2 | 2.0% (12 of 600) | 50% | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟥 16.7%<br>(2 / 12) | 🟩 2.2%<br>(13 / 588) | 🟥 43% | – | – | **1** | 3 | – | – | $106,811 | $103,532 (97%) |
| 261012_14_api | 7 | held-out | api | – | v2.0 | v2 | 2.0% (12 of 600) | 50% | Rules | Documented level below billed in over 15% of returned charts | Yes | 🟥 75.0%<br>(9 / 12) | 🟩 0.0%<br>(0 / 13) | 🟩 100% | – | – | **2** | 3 | 13 | 13 / 23 | $106,811 | $35,718 (33%) |
| 261012_14_api | 7 | held-out | api | – | v2.0 | v2 | 2.0% (12 of 600) | 50% | Rules | Note claims moderate+ data but claim has no lab or test line, over 12% of returned charts | Yes | 🟥 66.7%<br>(8 / 12) | 🟩 7.7%<br>(1 / 13) | 🟩 80% | – | – | **2** | 3 | 13 | 13 / 23 | $106,811 | $29,548 (28%) |
| 261012_14_api | 7 | held-out | api | 21 | v2.0 | v2 | 2.0% (12 of 600) | 50% | AI | AI calls upcoding (screen: z-score of risk-adjusted coding >= 5) | Yes | 🟥 66.7%<br>(8 / 12) | 🟩 7.7%<br>(1 / 13) | 🟩 80% | 🟩 100% | 🟥 3.57 | **3** | 5 | 13 | 13 / 23 | $106,811 | $39,332 (37%) |
| 261012_14_api | 7 | held-out | api | – | v2.0 | v2 | 2.0% (12 of 600) | 50% | Hybrid | Chart rule first, then summary rules and model | Yes | 🟥 58.3%<br>(7 / 12) | 🟩 7.7%<br>(1 / 13) | 🟩 83% | – | – | **2** | 3 | 13 | 13 / 23 | $106,811 | $57,654 (54%) |
| 261012_10_api | 42 | development | api | – | v2.0 | v2 | 3.7% (8 of 216) | 0% | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟥 25.0%<br>(2 / 8) | 🟩 3.4%<br>(7 / 208) | 🟥 46% | – | – | **1** | 3 | – | – | $28,803 | $24,174 (84%) |
| 261012_10_api | 42 | development | api | – | v2.0 | v2 | 3.7% (8 of 216) | 0% | Rules | Documented level below billed in over 15% of returned charts | Yes | 🟥 25.0%<br>(2 / 8) | 🟩 0.0%<br>(0 / 7) | 🟩 100% | – | – | **2** | 3 | 7 | 7 / 13 | $28,803 | $24,174 (84%) |
| 261012_10_api | 42 | development | api | – | v2.0 | v2 | 3.7% (8 of 216) | 0% | Rules | Note claims moderate+ data but claim has no lab or test line, over 12% of returned charts | Yes | 🟥 100.0%<br>(8 / 8) | 🟥 28.6%<br>(2 / 7) | 🟥 0% | – | – | **0** | 3 | 7 | 7 / 13 | $28,803 | $0 (0%) |
| 261012_10_api | 42 | development | api | 9 | v2.0 | v2 | 3.7% (8 of 216) | 0% | AI | AI calls upcoding (screen: z-score of risk-adjusted coding >= 5) | Yes | 🟥 50.0%<br>(4 / 8) | 🟩 0.0%<br>(0 / 7) | 🟩 100% | 🟩 100% | 🟥 3.54 | **3** | 5 | 7 | 7 / 13 | $28,803 | $18,250 (63%) |
| 261012_10_api | 42 | development | api | – | v2.0 | v2 | 3.7% (8 of 216) | 0% | Hybrid | Chart rule first, then summary rules and model | Yes | 🟥 25.0%<br>(2 / 8) | 🟩 0.0%<br>(0 / 7) | 🟩 100% | – | – | **2** | 3 | 7 | 7 / 13 | $28,803 | $24,174 (84%) |
| 261012_11_api | 42 | development | api | – | v2.0 | v2 | 3.7% (8 of 216) | 100% | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟥 50.0%<br>(4 / 8) | 🟩 2.4%<br>(5 / 208) | 🟥 44% | – | – | **1** | 3 | – | – | $23,638 | $16,039 (68%) |
| 261012_11_api | 42 | development | api | – | v2.0 | v2 | 3.7% (8 of 216) | 100% | Rules | Documented level below billed in over 15% of returned charts | Yes | 🟥 100.0%<br>(8 / 8) | 🟩 0.0%<br>(0 / 5) | – | – | – | **1** | 2 | 5 | 5 / 9 | $23,638 | $0 (0%) |
| 261012_11_api | 42 | development | api | – | v2.0 | v2 | 3.7% (8 of 216) | 100% | Rules | Note claims moderate+ data but claim has no lab or test line, over 12% of returned charts | Yes | 🟥 87.5%<br>(7 / 8) | 🟥 20.0%<br>(1 / 5) | 🟥 50% | – | – | **0** | 3 | 5 | 5 / 9 | $23,638 | $6,228 (26%) |
| 261012_11_api | 42 | development | api | 9 | v2.0 | v2 | 3.7% (8 of 216) | 100% | AI | AI calls upcoding (screen: z-score of risk-adjusted coding >= 5) | Yes | 🟥 62.5%<br>(5 / 8) | 🟥 20.0%<br>(1 / 5) | 🟥 75% | 🟩 100% | 🟥 3.67 | **1** | 5 | 5 | 5 / 9 | $23,638 | $14,125 (60%) |
| 261012_11_api | 42 | development | api | – | v2.0 | v2 | 3.7% (8 of 216) | 100% | Hybrid | Chart rule first, then summary rules and model | Yes | 🟥 62.5%<br>(5 / 8) | 🟥 20.0%<br>(1 / 5) | 🟥 75% | – | – | **0** | 3 | 5 | 5 / 9 | $23,638 | $14,125 (60%) |
| 261013_3_api | 42 | development | api | 1 | agent-dev | v2 | 3.7% (8 of 216) | 50% | Agent | Agent chose: combined rank, top 25; records for 10 providers | Yes | 🟥 62.5%<br>(5 / 8) | 🟩 0.0%<br>(0 / 4) | 🟩 100% | 🟩 100% | – | **3** | 4 | 3 | 4 / 14 | $44,856 | $25,887 (58%) |
| 261013_6_api | 202 | reserved | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟥 25.0%<br>(2 / 8) | 🟩 2.9%<br>(6 / 208) | 🟥 50% | – | – | **1** | 3 | – | – | $48,602 | $45,073 (93%) |
| 261013_6_api | 202 | reserved | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Rules | Documented level below billed in over 15% of returned charts | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 6) | 🟩 100% | – | – | **2** | 3 | 6 | 6 / 12 | $48,602 | $10,492 (22%) |
| 261013_6_api | 202 | reserved | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Rules | Note claims moderate+ data but claim has no lab or test line, over 12% of returned charts | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 6) | 🟩 100% | – | – | **2** | 3 | 6 | 6 / 12 | $48,602 | $28,823 (59%) |
| 261013_6_api | 202 | reserved | api | 12 | v2.0 | v2 | 3.7% (8 of 216) | 50% | AI | AI calls upcoding (screen: z-score of risk-adjusted coding >= 5) | Yes | 🟥 87.5%<br>(7 / 8) | 🟩 0.0%<br>(0 / 6) | 🟩 100% | 🟩 100% | 🟥 3.08 | **3** | 5 | 6 | 6 / 12 | $48,602 | $23,957 (49%) |
| 261013_6_api | 202 | reserved | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Hybrid | Chart rule first, then summary rules and model | Yes | 🟥 62.5%<br>(5 / 8) | 🟩 0.0%<br>(0 / 6) | 🟩 100% | – | – | **2** | 3 | 6 | 6 / 12 | $48,602 | $34,449 (71%) |
| 261013_7_api | 303 | reserved | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟩 12.5%<br>(1 / 8) | 🟩 5.3%<br>(11 / 208) | 🟥 39% | – | – | **2** | 3 | – | – | $43,296 | $41,714 (96%) |
| 261013_7_api | 303 | reserved | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Rules | Documented level below billed in over 15% of returned charts | Yes | 🟥 62.5%<br>(5 / 8) | 🟩 9.1%<br>(1 / 11) | 🟥 75% | – | – | **1** | 3 | 11 | 11 / 18 | $43,296 | $6,905 (16%) |
| 261013_7_api | 303 | reserved | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Rules | Note claims moderate+ data but claim has no lab or test line, over 12% of returned charts | Yes | 🟥 62.5%<br>(5 / 8) | 🟥 18.2%<br>(2 / 11) | 🟥 60% | – | – | **0** | 3 | 11 | 11 / 18 | $43,296 | $20,156 (47%) |
| 261013_7_api | 303 | reserved | api | 16 | v2.0 | v2 | 3.7% (8 of 216) | 50% | AI | AI calls upcoding (screen: z-score of risk-adjusted coding >= 5) | Yes | 🟥 75.0%<br>(6 / 8) | 🟥 27.3%<br>(3 / 11) | 🟥 40% | 🟩 100% | 🟥 3.44 | **1** | 5 | 11 | 11 / 18 | $43,296 | $3,949 (9%) |
| 261013_7_api | 303 | reserved | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Hybrid | Chart rule first, then summary rules and model | Yes | 🟥 62.5%<br>(5 / 8) | 🟥 36.4%<br>(4 / 11) | 🟥 43% | – | – | **0** | 3 | 11 | 11 / 18 | $43,296 | $6,905 (16%) |
| 261013_12_api | 202 | reserved | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟥 25.0%<br>(2 / 8) | 🟩 2.9%<br>(6 / 208) | 🟥 50% | – | – | **1** | 3 | – | – | $48,602 | $45,073 (93%) |
| 261013_12_api | 202 | reserved | api | 7 | v2.0 | v2 | 3.7% (8 of 216) | 50% | AI | AI calls upcoding (screen: z-score of risk-adjusted coding >= 5) | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 6) | 🟩 100% | 🟩 100% | 🟥 3.50 | **3** | 5 | 6 | 9 / 17 | $48,602 | $8,782 (18%) |
| 261013_13_api | 303 | reserved | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Screen | Z-score of risk-adjusted coding >= 5 | No | 🟩 12.5%<br>(1 / 8) | 🟩 5.3%<br>(11 / 208) | 🟥 39% | – | – | **2** | 3 | – | – | $43,296 | $41,714 (96%) |
| 261013_13_api | 303 | reserved | api | 15 | v2.0 | v2 | 3.7% (8 of 216) | 50% | AI | AI calls upcoding (screen: z-score of risk-adjusted coding >= 5) | Yes | 🟥 50.0%<br>(4 / 8) | 🟩 0.0%<br>(0 / 11) | 🟩 100% | 🟩 100% | 🟥 3.39 | **3** | 5 | 11 | 14 / 24 | $43,296 | $21,389 (49%) |
| 261013_14_api | 202 | reserved | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Screen | Top 25 upcoding outliers | No | 🟩 12.5%<br>(1 / 8) | 🟩 8.7%<br>(18 / 208) | 🟥 28% | – | – | **2** | 3 | – | – | $48,602 | $47,599 (98%) |
| 261013_14_api | 202 | reserved | api | 16 | v2.0 | v2 | 3.7% (8 of 216) | 50% | AI | AI calls upcoding (screen: top 25 upcoding outliers) | Yes | 🟥 62.5%<br>(5 / 8) | 🟩 0.0%<br>(0 / 18) | 🟩 100% | 🟩 100% | 🟥 3.36 | **3** | 5 | 18 | 27 / 37 | $48,602 | $32,740 (67%) |
| 261013_15_api | 303 | reserved | api | – | v2.0 | v2 | 3.7% (8 of 216) | 50% | Screen | Top 25 upcoding outliers | No | 🟩 0.0%<br>(0 / 8) | 🟩 8.2%<br>(17 / 208) | 🟥 32% | – | – | **2** | 3 | – | – | $43,296 | $43,296 (100%) |
| 261013_15_api | 303 | reserved | api | 19 | v2.0 | v2 | 3.7% (8 of 216) | 50% | AI | AI calls upcoding (screen: top 25 upcoding outliers) | Yes | 🟥 62.5%<br>(5 / 8) | 🟩 0.0%<br>(0 / 17) | 🟩 100% | 🟩 100% | 🟥 3.56 | **3** | 5 | 17 | 22 / 34 | $43,296 | $6,905 (16%) |
| 261013_8_api | 202 | reserved | api | 1 | v3.0 | v2 | 3.7% (8 of 216) | 50% | Agent | Agent with the screen tool | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 7) | 🟩 100% | 🟩 100% | 🟥 2.83 | **3** | 5 | 4 | 6 / 12 | $48,602 | $8,782 (18%) |
| 261013_9_api | 303 | reserved | api | 1 | v3.0 | v2 | 3.7% (8 of 216) | 50% | Agent | Agent with the screen tool | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 6) | 🟩 100% | 🟩 100% | 🟥 2.92 | **3** | 5 | 5 | 7 / 14 | $43,296 | $4,803 (11%) |
| 261013_10_api | 202 | reserved | api | 1 | v3.0 | v2 | 3.7% (8 of 216) | 50% | Agent | Agent without the screen tool | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 10) | 🟩 100% | 🟩 100% | 🟥 2.29 | **3** | 5 | 8 | 11 / 16 | $48,602 | $8,782 (18%) |
| 261013_11_api | 303 | reserved | api | 1 | v3.0 | v2 | 3.7% (8 of 216) | 50% | Agent | Agent without the screen tool | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 12) | 🟩 100% | 🟩 100% | 🟥 2.33 | **3** | 5 | 4 | 5 / 12 | $43,296 | $3,949 (9%) |
| 261013_16_api | 202 | reserved | api | 1 | v3.0 | v2 | 3.7% (8 of 216) | 50% | Agent | Agent with the screen tool | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 7) | 🟩 100% | 🟩 100% | 🟥 2.91 | **3** | 5 | 5 | 7 / 12 | $48,602 | $8,782 (18%) |
| 261013_17_api | 202 | reserved | api | 1 | v3.0 | v2 | 3.7% (8 of 216) | 50% | Agent | Agent with the screen tool | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 6) | 🟩 100% | 🟩 100% | 🟥 3.00 | **3** | 5 | 6 | 9 / 15 | $48,602 | $8,782 (18%) |
| 261013_18_api | 303 | reserved | api | 1 | v3.0 | v2 | 3.7% (8 of 216) | 50% | Agent | Agent with the screen tool | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 6) | 🟩 100% | 🟩 100% | 🟥 2.83 | **3** | 5 | 3 | 4 / 11 | $43,296 | $4,803 (11%) |
| 261013_19_api | 303 | reserved | api | 1 | v3.0 | v2 | 3.7% (8 of 216) | 50% | Agent | Agent with the screen tool | Yes | 🟥 75.0%<br>(6 / 8) | 🟩 0.0%<br>(0 / 7) | 🟩 100% | 🟩 100% | 🟥 2.57 | **3** | 5 | 3 | 4 / 11 | $43,296 | $4,803 (11%) |

Columns: **Seed status**: development = the seed used to build and tune the workflow, held-out = generated or scored after those settings were frozen, reserved = held back and never looked at until the Milestone 6 evaluation. **Source**: api = the project's own pipeline calling the API, cc = mimicked with Claude Code agents, code = no model. **Evals scored**: how many of the evals applied to that row (a screen row has 3; an AI row has 4, or 5 when the usefulness judge ran), so compare passes only between rows with the same count; the templating check was removed, which lowered AI rows' count by one. **Agents**: separate model calls or chat agents that wrote summaries (code-written ones do not count). **Upcoders in data**: the share of providers that are real upcoders (the prevalence; "baseline" is used only for a comparison arm). **Honest doctors sent records requests** and **Request rounds**: the burden on practices (a round is the first request or one follow-up). **Dollars overpaid to upcoders**: what upcoders were paid above what the justified levels would have paid (answer key). **Dollars at stake in upcoders called**: the same dollars for only the upcoders that stage called, an upper bound on what recovery could reach. **Upcoder clone level**: the share of upcoders whose notes are cloned to match the bill. Source of truth: `experiments/results.csv`.

- **v1**: Version 1 synthetic data: provider, patient and claim tables with a stored chronic-condition count, plus a records-review sample (documentation.csv, about 30% of claims) handed to the AI up front.
- **v2**: Version 2 synthetic data: plan-shaped tables (members, providers, claim headers and lines, remittance with denials, replacements and voids); conditions derived from claims; charts only by records request (limited, late or missing responses, coder disagreement); separate MDM elements and minutes; some upcoders clone their notes.
<!-- scoreboard:end -->

This table is generated from the saved outputs (`python docs/update_readme.py`). Usefulness is scored by an LLM judge (`eval/judge_usefulness.py`, a different model from the writer), so it is a rough rubric check. Run outputs are in `experiments/`; the naming is explained in `experiments/README.md`.

### Roadmap
<!-- roadmap:start -->
Live from this repository's [milestones](https://github.com/simmyhundal/em-upcoding-agent/milestones); each badge shows the milestone's current title and closed/total issues.

- ![PoC (Path B): statistics select, AI explains and advises](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/1) Statistics choose who gets a close look; an AI reads each flagged provider's evidence, writes a cited summary and gives an advisory leaning (upcoding, high-acuity panel, inconclusive); code checks the citations; people decide.
- ![Path A (parked): LLM judges from clinical notes](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/2) An LLM judges from synthetic free-text clinical notes instead of structured evidence.
- ![M3: Enhancements to Path B](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/3) Follow-on features once the Path B PoC (Milestone 1) is evaluated: evidence visuals for reviewers and a downstream artifact for the Payment Integrity team.
- ![M4: Reduce API cost](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/4) Cut the cost per run (about $2.14 for the first full run: $1.49 Claude Opus 5.5 writer, $0.65 Claude Sonnet 5.5 judge) without losing quality.
- ![M5: Realistic plan inputs (v2 data model)](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/5) A new version of the tool whose inputs look like what a health plan actually holds, in the shapes plans store them, instead of the simplified CSVs used so far.
- ![M6: Autonomous investigator agent](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/6) Turn the workflow (code fixes the order, one LLM step) into an agent that chooses which tools to use to find upcoders.
- ![Backlog (v2.1)](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/7) Work deferred past the v2.0 freeze.
- ![M7: Recovery and downstream actions](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/8) Simulate what happens after a provider is finally flagged (recovery sampling, deficient responses, extrapolated overpayment, notices) so results cover recovery and other downstream uses, not only advising which providers to look at.
- ![Housekeeping: docs, visuals and releases](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/9) Keep the README, visuals and GitHub releases current and consistent with each tagged version.
<!-- roadmap:end -->

### Repo layout
```
data/baselines/   CMS-derived specialty distributions (small, no provider-level rows)
data/synthetic/   generated providers, patients, claims (regenerated from a seed)
src/              baseline builder, data generator, detectors, summary step
eval/             eval harness and rubric
reports/          results and failure-mode write-ups
```

### Baseline data caveats
`data/baselines/em_specialty_baselines.json` is built by `src/build_baselines.py` from the CMS file above. Read these before relying on it:
- **Small-cell suppression distorts the mix.** CMS hides provider-code rows with 10 or fewer beneficiaries, so low-volume codes drop out. Shares of higher codes are biased, and many providers show zero 99215 only because it is hidden. Treat the shares as biased, not as true billing mix.
- **Not a national sample.** The committed baseline covers all individual providers in five states (OH, NC, WA, GA, MI), not a random national draw. The GA Family Practice pull is the calibration target for the synthetic data.
- **Data year is unverified.** The JSON records `UNVERIFIED` until the release year is confirmed on data.cms.gov.
- **Office-visit codes only.** Established-patient 99211-99215; new-patient codes (99202-99205) are excluded.
- **Privacy.** NPIs are used only to group rows, then replaced by a discarded salted hash. Only aggregate distributions are saved; no provider-level rows.

### Evidence charts and case pages
`python src/evidence_chart.py data/synthetic reports/flagged.csv reports/charts` draws one SVG per flagged provider: boxes show how
the other providers' 99215 share varies at each patient-complexity level, and the provider is a point with a 95% Wilson interval
(thin levels are hollow and dashed). `python src/case_report.py CHECKED_SUMMARIES CHARTS_DIR OUT_DIR` builds a markdown page per
provider that combines the summary, its cited claims and the chart; see `experiments/261008_4_cc/cases/` for an example.

### Payment Integrity packet
`src/pi_packet.py` turns an "upcoding" case into draft material for the Payment Integrity team: a dossier, a reproducible sample of
claims to request records for, a sampling plan, and an overpayment estimator that extrapolates a reviewed sample with a confidence
interval. It does not draft letters or make findings. See `docs/payment_integrity.md`; worked examples (simulated review) are in
`reports/pi_packets/`.

### Guardrail scope
`src/guardrail.py` checks that every cited claim ID exists and belongs to the provider being summarized, and rejects summaries
with no citations. It does **not** check that a cited claim supports the sentence that cites it. For example, a summary could
call a visit "high-acuity" while citing a claim on a patient with no chronic conditions, and still pass. So 100% citation
accuracy means "no invented or misattributed claims", not "every statement is supported". Reviewers should treat the cited
claims as pointers to check. A lightweight support check (verifying numeric attributes a rationale states about cited claims)
has not been built.

### Ground rules
- Synthetic data only. No real claims, no PHI.
- Never flag real, named providers, even from public data.
- Synthetic claims are cleaner than real ones, and patient complexity is a simplified proxy for documentation. Results don't transfer directly to production.
