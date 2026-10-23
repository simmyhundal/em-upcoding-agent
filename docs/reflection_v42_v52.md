# The deepest flaws after release 4.2 and 5.2

[Back to the README](../README.md) · [test result](v42_test_result.md) · [process](process.md) · [previous reflection](reflection_v41_v51.md)

**What this page is.** Step 7 of the [release process](process.md): what is weakest about the system as it stands after workflow v4.2 and agent v5.2, written for a reader who was not there. Each flaw is filed as an issue in the milestone "v4.3 and v5.3". It is meant to be uncomfortable.

## 1. The headline gain rests on a signal the generator made clean
Workflow v4.2 and agent v5.2 score about $375,000 and $372,000 over ten test seeds against $17,713 for workflow v4.1, and 94% of that is the [volume screen](concepts/volume-screen.md): count visits per provider per day and look at the days above 30. In the synthetic data the busiest honest day is at most 26 visits and the least busy impossible-days provider's is 33, so a threshold separates them perfectly (319 of 319 on 100 seeds). Real claims have group practices billing under one number, locum coverage, scribes and bad dates; the honest tail will overlap. We have measured how a reviewer uses a clean signal, not how large or how clean the real one is. **What a sceptic says:** "you built the answer into the data and then found it". Filed: [#197](https://github.com/simmyhundal/em-upcoding-agent/issues/197), with larger datasets (about 2,160 providers in one run) beside it.

## 2. The score was built for upcoding, and stretched to fraud
A demand for visits that never happened is in practice a fraud referral, not a demand letter, and it costs more than $276 of staff time (investigators, legal review). Score 4.2 prices it as a demand. The false-flag side was never tested (the lane flagged no honest provider in the 150 seeds it ran on: 40 development, 100 confirm and 10 test), so the abrasion for wrongly pursuing a busy honest practice is untried. The office is also assumed honest about having no record; a real fraud ring may produce a chart. Filed: [#200](https://github.com/simmyhundal/em-upcoding-agent/issues/200), [#201](https://github.com/simmyhundal/em-upcoding-agent/issues/201).

## 3. Level upcoding is still barely reached
Of 478 providers whose true overpayment is at least the cost of pursuing them, workflow v4.2 sent a demand to 38 (8%). The level review recovers the same $2,500 per seed workflow v4.1 did and has been stuck there for two releases; opportunistic habits are unreachable by chart sampling by construction. The lane's size hides this. Filed: [#198](https://github.com/simmyhundal/em-upcoding-agent/issues/198).

## 4. The persistence result depends on a simulated office's response table
Hypothesis H28 (keep following up while nothing usable came back) added $3,036 per seed, better on 9 of 40 seeds, p = 0.0042 against a bar of 0.01. It converts silent offices at the rates in `provider_sim.py`, which were written to be plausible and were never checked against public data on records-request response. The confirm pool agreed (86% of impossible-day providers sent a demand), but it shares the same office. Filed: [#201](https://github.com/simmyhundal/em-upcoding-agent/issues/201).

## 5. The agent and the workflow are not independent here
Agent v5.2 matches workflow v4.2 (−$292 per seed, p = 0.94) because the lane is the same code in both and the model followed the advice. That is parity, not evidence that the agent could find the lane unaided. One run per seed; agent run-to-run noise is still unmeasured ([#187](https://github.com/simmyhundal/em-upcoding-agent/issues/187)).

## 6. The ceiling is not recomputed
The oracle with triage was built before the lane existed. Score over oracle ([#186](https://github.com/simmyhundal/em-upcoding-agent/issues/186)) is not reported for release 4.2 and 5.2; the share of true overpayment available that W4.2 pursued is (27%).

## 7. Most parameters of score 4.2 are assumptions
Copy fee $0, the 15% error gate, 30 visits, 30 claims in the stratum, the 70% criterion in the freeze declaration: assumptions or design choices. The calibration of data 4.2 (habit shares, date range, lab line: [#137](https://github.com/simmyhundal/em-upcoding-agent/issues/137), [#144](https://github.com/simmyhundal/em-upcoding-agent/issues/144)) is not done.

## 8. The seed discipline held, with one soft spot
Five hypotheses were tried on the same 40 development seeds, the freeze was written before the confirm read, and the test pool was read once. Soft spot: data 4.2 had no earlier test seeds, so the confirm pool served as the final development run; and the lane threshold (30) was chosen from five seeds and then checked on 100 development seeds from claims alone, which is development data for it.

## 9. Fraud kinds with no volume signal are unreached
Ghost-member billing and unbundling have no clean claims signal in the data and no arm tool. Filed: [#199](https://github.com/simmyhundal/em-upcoding-agent/issues/199).

## What changed in the process because of this cycle
A run that ended its turn to wait for a background job handed the release back to the owner; [Running without stopping](process.md#running-without-stopping-run-release-paid-or-until-done) is the rule now: a pin list, no waiting turns, no wrap-up until finished. Terminology rules ([Writing for outside readers](process.md#writing-for-outside-readers)) were applied to every page this release added.
