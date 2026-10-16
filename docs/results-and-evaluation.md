# Results and evaluation

[Back to the README](../README.md)

Every run, with all columns, is in [results.md](results.md); the source of truth is `experiments/results.csv` ([columns](results_table.md)). The version 1 results are archived in [archive-version-1.md](archive-version-1.md).

## Multi-seed evaluation of v2.1 and v3.1 (issue 61)
All four arms (workflow v2.0 and v2.1, agent v3.0 and v3.1) on **ten fresh seeds** (404 to 1313, 80 planted upcoders) plus one fresh seed at 0.5%, 1% and 2% upcoders, with the protocol and decision rules [posted on the issue](https://github.com/simmyhundal/em-upcoding-agent/issues/61) before any run. Full tables: [eval61.md](eval61.md).

| Arm | Upcoders found (of 80) | Honest doctors accused | Cloned-notes upcoders found (of 40) | Requests and follow-ups to honest practices |
|---|---|---|---|---|
| Workflow v2.0 (frozen) | 19 | 3 | 3 | 80 |
| Workflow v2.1 | 32 | 0 | 10 | 203 |
| Agent v3.0 (frozen) | 18 | 0 | 1 | 68 |
| Agent v3.1 | 27 | 0 | 8 | 101 |

- **Both upgrades helped** (paired per seed, 95% bootstrap interval): workflow v2.1 over v2.0 by +1.3 upcoders per seed (+0.6 to +2.0) with 3 fewer false accusations; agent v3.1 over v3.0 by +0.9 (+0.1 to +1.8).
- **Workflow and agent are not reliably different:** v3.1 minus v2.1 is -0.5 per seed (-1.2 to +0.2). By the rule fixed in advance, the workflow stays the main line; the agent stays in development. The Milestone 6 gap (v3.0 behind v2.0) did not replicate on ten seeds (-0.1, -0.7 to +0.5).
- **The note checks are where the gain came from:** cloned-notes upcoders found rose from 3 to 10 (workflow) and 1 to 8 (agent). The clone signals are planted by the data 2.1 generator, so real notes would be harder.
- **The cost is burden:** workflow v2.1's second requests and audit-trail requests more than double the follow-ups sent to honest practices (203 against 80); agent v3.1 sends half as many as workflow v2.1.
- **Low base rates** (one seed each, descriptive): v2.1 and v3.1 accused one honest doctor between them across the three rates (workflow v2.1 at 1%), against five for v2.0.
- Still no arm meets the 12.5% miss-rate threshold. Evaluation spend: about $19 (plus about $0.30 for one crashed run, issue 85).

## Agent versus workflow: the first comparison on two seeds
The frozen workflow (`v2.0`) fixes the order of steps in code. Milestone 6 built the other design to compare against it: an **agent** that gets tools and decides what to do: which screen to run and where to put the cutoff, which providers to look at, whether to ask a provider's office for charts, what to do about an incomplete response, and when to stop. Code only supplies tools and enforces limits (tool calls, dollars, records requests) and logs every call. Tools, limits and what the agent can see: [docs/agent_tools.md](agent_tools.md); the simulated provider office it negotiates with: [docs/provider_sim.md](provider_sim.md).

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


## Thresholds
Every run is graded against the same thresholds. How each is computed is in `eval/`; per-run detail tables are in `reports/eval_report.md`.

| Eval | Threshold |
|---|---|
| False negative rate | at most 12.5% of the real upcoders missed (1 of 8) |
| False positive rate | at most 12.5% of the honest doctors a step examines are wrongly accused. For the screen that is all honest doctors in the data; for the AI step it is the honest doctors the screen sent to it. "Honest" means every non-upcoder, ordinary doctors and sicker-panel doctors alike |
| Precision of "upcoding" calls | at least 80% are real upcoders (*proposed*; the end-to-end check on how trustworthy an accusation is, which the screen's false positive rate does not capture) |
| Citations valid | 100% |
| Case Summary Usefulness (1-5) | average of at least 4 (scored by an LLM judge) |

Note that in the synthetic data, billed level depends on patient complexity by construction, so the risk-adjusted baseline is helped by how the data was built. Report that plainly.


## Where things stand
Done through v3.0: synthetic data (version 1, and plan-shaped version 2 with records requests), both screens, flagging, the summary step (facts, citations and clear cases written by code, a model for the rest, through the Batch API with a cache), citation and number checks, evidence charts and case pages, the Payment Integrity packet, a simulated provider office, the investigator agent with caps, audit log and no access to the answer key, an evaluation harness with a results table, and held-out and reserved-seed evaluations. Next: the parallel workflow (v2.1) and agent (v3.1) builds, then recovery (M7).

**What is the suspicion score?** It is the risk-adjusted score from the statistical screen. For every doctor, the screen predicts how often they should bill the top visit code (99215) given how many chronic conditions their patients have, then compares that with what they billed: (billed - expected) / the statistical noise you would expect by chance. That raw score is then rescaled by the typical spread across all doctors, because honest doctors legitimately differ too. A score of 0 is the middle of the pack; in the seed-42 data a score of 5 is about where the top 5% of doctors begin, and the highest score is above 22. It is computed from claims and patient condition counts only, never from the records sample.

The **Tuning** column says how the list was chosen: the top 25 outliers, or everyone at or above a suspicion level. On AI rows it also names the screen that fed the AI.

Each run has a **Screen** row (the statistical screen's flagged doctors count as accused) and, when AI summaries were written, an **AI** row (what the AI called upcoding, out of the doctors the screen sent it). **Records evidence** says whether the AI was shown the records-review sample. 🟩 means the threshold was met, 🟥 means it was missed, and a dash means not scored or not applicable and is left out of the total.




