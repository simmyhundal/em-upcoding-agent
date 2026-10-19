# Results and evaluation

[Back to the README](../README.md)

Every run, with all columns, is in [results.md](results.md); the source of truth is `experiments/results.csv` ([columns](results_table.md)). The version 1 results are archived in [archive-version-1.md](archive-version-1.md).

## Multi-seed evaluation of v2.1 and v3.1 (issue 61)
All four versions (workflow v2.0 and v2.1, agent v3.0 and v3.1) on **ten fresh seeds** (404 to 1313, 80 planted upcoders) plus one fresh seed at 0.5%, 1% and 2% upcoders, with the protocol and decision rules [posted on the issue](https://github.com/simmyhundal/em-upcoding-agent/issues/61) before any run. Full tables: [eval61.md](eval61.md).

| Arm | Upcoders found (of 80) | Honest providers accused | Cloned-notes upcoders found (of 40) | Requests and follow-ups to honest providers |
|---|---|---|---|---|
| Workflow v2.0 (frozen) | 19 | 3 | 3 | 80 |
| Workflow v2.1 | 32 | 0 | 10 | 203 |
| Agent v3.0 (frozen) | 18 | 0 | 1 | 68 |
| Agent v3.1 | 27 | 0 | 8 | 101 |

- **Both upgrades helped** (paired per seed, 95% bootstrap interval): workflow v2.1 over v2.0 by +1.3 upcoders per seed (+0.6 to +2.0) with 3 fewer false accusations; agent v3.1 over v3.0 by +0.9 (+0.1 to +1.8).
- **Workflow and agent are not reliably different:** v3.1 minus v2.1 is -0.5 per seed (-1.2 to +0.2). By the rule fixed in advance for release 1, the workflow was kept as the lead design at that point; from release 3 on, both designs are developed side by side. The Milestone 6 gap (v3.0 behind v2.0) did not replicate on ten seeds (-0.1, -0.7 to +0.5).
- **The note checks are where the gain came from:** cloned-notes upcoders found rose from 3 to 10 (workflow) and 1 to 8 (agent). The clone signals are planted by the data 2.1 generator, so real notes would be harder.
- **The cost is burden:** workflow v2.1's second requests and audit-trail requests more than double the follow-ups sent to honest providers (203 against 80); agent v3.1 sends half as many as workflow v2.1.
- **Low base rates** (one seed each, descriptive): v2.1 and v3.1 accused one honest provider between them across the three rates (workflow v2.1 at 1%), against five for v2.0.
- Still no version meets the 12.5% miss-rate threshold. Evaluation spend: about $19 (plus about $0.30 for one crashed run, issue 85).

## Agent versus workflow: the first comparison on two seeds
The frozen workflow (`v2.0`) fixes the order of steps in code. Milestone 6 built the other design to compare against it: an **agent** that gets tools and decides what to do: which screen to run and where to put the cutoff, which providers to look at, whether to ask a provider's office for charts, what to do about an incomplete response, and when to stop. Code only supplies tools and enforces limits (tool calls, dollars, records requests) and logs every call. Tools, limits and what the agent can see: [docs/agent_tools.md](agent_tools.md); the simulated provider office it negotiates with: [docs/provider_sim.md](provider_sim.md).

**Head-to-head on two reserved seeds (202 and 303; never looked at before this test), 8 upcoders each, same simulated office for every version.** Totals over the two seeds (16 upcoders, 416 honest providers):

| Arm | Upcoders found (of 16) | Honest providers accused | Honest providers sent records requests | Request rounds (all / on honest) | Cost per seed |
|---|---|---|---|---|---|
| Workflow, screen at suspicion 5, fixed office policy | 6 | 0 | 17 | 41 / 23 | $0.19 to $0.35 |
| Workflow, screen at top 25, fixed office policy | 6 | 0 | 35 | 71 / 49 | $0.40 to $0.43 |
| Agent with the screen tool (3 runs per seed) | 4 in every run | 0 | 8 to 9 | 23 to 26 / 11 to 13 | $0.27 to $0.39 |
| Agent without the screen tool | 4 | 0 | 12 | 28 / 16 | $0.30 to $0.36 |
| Workflow as frozen in v2.0, single-draw records (not a fair baseline) | 3 | 3 | 17 | 30 / 17 | $0.25 to $0.35 |

Workflow costs include the usefulness judge; agent costs do not (about $0.05 more per run).

- **No version is good enough.** The best found 4 of 8 on one seed; the false negative threshold is 1 of 8. Every version is limited by what it can reach, not by false accusations.
- **The agent did not find more upcoders than the workflow.** It found 4 of 16 to the workflow's 6 of 16 (a gap of two providers). Repeating the agent three times per seed gave the same 2 of 8 every time, so the run-to-run noise is small here and the gap is more likely a real difference in reach, but 16 upcoders is still few. It also asked far fewer honest providers for records (9 against 17 or 35) and used fewer request rounds. Both agents screened with the combined rank at the top 25 (with at least 100 claims) and never tried a suspicion cutoff, then narrowed to 12 or 13 providers before asking for charts. So on this evidence the agent's contribution is **restraint, not reach**.
- **The screen mattered little for the agent's reach, more for its burden.** Without the screen tool the agent found the same 2 of 8 on each seed and asked more honest providers on one seed (8 against 4). One seed is not a pattern.
- **Nothing here shows the agent beating a fixed policy.** One run per version per seed, 16 upcoders in all, a simulated office, and cloned notes that defeat chart-based checks. **The agent's summaries are less useful by the judge's rubric:** 2.6 to 3.0 with the screen tool and 2.3 without, against 3.3 to 3.6 for the workflow's (target 4); the agent writes a shorter interpretation and more of its numbers fail the number check (about 65% to 85% of its summaries pass against 92% to 100%).
- The rows, with dollars at stake and request rounds, are in the Eval table below; the protocol (versions, seeds, rules) is [issue 50](https://github.com/simmyhundal/em-upcoding-agent/issues/50).


## Releases 2 and 3: harder data (2.2), and what the fresh seeds showed

Data 2.2 adds honest coding noise (about 8% of honest visits miscoded, half upward), group billing, and an upcoder defined as billing above the honest baseline by a margin (set from payer provider; [data_v2_2.md](data_v2_2.md)). Every number below is on generated data with generated notes, so cloned-notes signs are probably easier than real ones.

- **Release 2 (workflow v2.2, agent v3.2, ten seeds, [release2_results.md](release2_results.md)).** The workflow found 21 of 78 upcoders and the agent 12. The pre-registered looks were at 22 and 44 seeds; the ten-seed result was an **unplanned look** and no significance claim is valid for it, whatever its p-value (exact McNemar 0.012; with the design effect for seed clusters 0.027). It was reported as suggestive, and the cheaper decision to stop at ten seeds was Simmy's.
- **Release 3 (workflow v2.3, agent v3.3, ten fresh seeds, pre-registered on issue 99, [release3_results.md](release3_results.md)).** Workflow v2.3 found 37 of 79, agent v3.3 34, workflow v2.2 24. Workflow against agent: **no significant gap** (p = 0.59). Workflow v2.3 against v2.2: 21 upcoders found only by v2.3 against 8 (p = 0.049 against the pre-registered 0.025, so not significant by the rule; exact McNemar 0.024). The wider list behind v2.3 asks 150 honest providers for records against 64 for v2.2 (the agent 79).
- **Where the misses are** ([release2_misses.md](release2_misses.md), [dev_release3.md](dev_release3.md)): the screen's top 5% held only 44 of 78 upcoders; cloned-notes upcoders were the largest hole (workflow v2.2 called 4 of 23 screened ones; rules 2.3 raise that to about 17 on the development seeds, in sample).

## Thresholds
Every run is graded against the same thresholds. How each is computed is in `eval/`; per-run detail tables are in `reports/eval_report.md`.

| Eval | Threshold |
|---|---|
| False negative rate | at most 12.5% of the real upcoders missed (1 of 8) |
| False positive rate | at most 12.5% of the honest providers a step examines are wrongly accused. For the screen that is all honest providers in the data; for the AI step it is the honest providers the screen sent to it. "Honest" means every non-upcoder, ordinary providers and sicker-panel providers alike |
| Precision of "upcoding" calls | at least 80% are real upcoders (*proposed*; the end-to-end check on how trustworthy an accusation is, which the screen's false positive rate does not capture) |
| Citations valid | 100% |
| Case Summary Usefulness (1-5) | average of at least 4 (scored by an LLM judge in release 1; from release 2, by the free rule judges j3.2 and j3.3, which no person has checked) |

Note that in the synthetic data, billed level depends on patient complexity by construction, so the risk-adjusted baseline is helped by how the data was built. Report that plainly.


## Releases 4 and 5: learned policies, scored in net dollars

From release 5 the primary score is **net dollars** (the RL score; formula and prices in the [README](../README.md), code in `eval/dollar_reward.py`), with upcoders found, honest providers accused and rounds sent shown beside it. Release 4 was scored in points (+1 per upcoder found, -1 per honest provider accused, -0.05 per extra round to an honest provider).

- **Release 4 (workflow v2.4, agent v3.4, ten fresh seeds, [release4_results.md](release4_results.md), [release4_agent_results.md](release4_agent_results.md)).** The default workflow variant (GL: ratio gate plus a learned stop-or-escalate rule) found 49 of 80 upcoders against 46 for workflow v2.3, accused 2 honest providers against 6, and sent about 11 fewer rounds per seed to honest providers; the gap on upcoders found was not significant. Agent v3.4 found 40 of 80 and never called its advisor tool.
- **Release 5 (workflow v2.5, agent v3.5, ten fresh seeds, pre-registered on issue 109, [release5_results.md](release5_results.md)).** Net dollars per seed: agent v3.5 $32,159, workflow v2.5 $31,888, v2.4 $29,569, v2.3 $24,086. Agent against workflow: a paired gap of $270 per seed (range -$29,015 to +$17,537), not a confirmed difference. Recall was flat at 46 to 47%: the dollars came from lower costs and fewer false accusations, not more upcoders found. Wrap-up and hypotheses: [release5_wrapup.md](release5_wrapup.md).
- **Caveats.** Dollars use the optimistic recovery model (a sampled 99215 whose note shows any cloning sign is denied in full), providers have about 240 claims a year in the simulation, and $2,000 per honest provider accused is an assumption: dollars rank versions, they do not forecast recovery ([limitations](limitations.md)).

## Where things stand
Through release 5 (workflow v2.5 and agent v3.5, tagged): a synthetic data generator with harder data (2.2), the screens (`eb_ratio_t` is current), a simulated provider office with records requests, a workflow that obeys learned ask-or-skip and stop-or-escalate formulas, an agent that gets the same formulas as advice, citation and number checks, a deterministic rule judge for summaries, and fresh-seed evaluations scored in net dollars. Release 6 hypotheses: [#116](https://github.com/simmyhundal/em-upcoding-agent/issues/116) (agent summary text), [#117](https://github.com/simmyhundal/em-upcoding-agent/issues/117) (how many dollars sit in the missed upcoders, and silent providers), [#118](https://github.com/simmyhundal/em-upcoding-agent/issues/118) (whether the agent should obey the stop advice). Recovery (M7) is still open.

**What is the suspicion score?** It is the risk-adjusted score from the statistical screen. For every provider, the screen predicts how often they should bill the top visit code (99215) given how many chronic conditions their patients have, then compares that with what they billed: (billed - expected) / the statistical noise you would expect by chance. That raw score is then rescaled by the typical spread across all providers, because honest providers legitimately differ too. A score of 0 is the middle of the pack; in the seed-42 data a score of 5 is about where the top 5% of providers begin, and the highest score is above 22. It is computed from claims and patient condition counts only, never from the records sample.

The **Tuning** column says how the list was chosen: the top 25 outliers, or everyone at or above a suspicion level. On AI rows it also names the screen that fed the AI.

Each run has a **Screen** row (the statistical screen's flagged providers count as accused) and, when AI summaries were written, an **AI** row (what the AI called upcoding, out of the providers the screen sent it). **Records evidence** says whether the AI was shown the records-review sample. 🟩 means the threshold was met, 🟥 means it was missed, and a dash means not scored or not applicable and is left out of the total.




