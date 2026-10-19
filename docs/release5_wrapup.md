# Release 5 wrap-up: dollars as the score, workflow v2.5 and agent v3.5 (issue 109)

[Back to the README](../README.md)

Release 5 (branch `release5-dev`, milestone "v2.5 and v3.5") made **net dollars the primary score from the start** and built a learned policy and an agent version against it. Results, one look at ten fresh seeds: [release5_results.md](release5_results.md).

## What was built

- **Dollar reward** (`eval/dollar_reward.py`): value is the 90% lower bound of what an arm could recover from the upcoders it calls, under recovery option 2 (a sampled 99215 whose note shows any cloning sign is denied in full; others by level difference), less sourced costs ($90 per round, $43.84 per round to an honest practice, $158 per practice reviewed) and an assumed $2,000 per honest doctor called. Every earlier release is scored the same way in [release5_dollar_baseline.md](release5_dollar_baseline.md).
- **Workflow v2.5** (`src/policy_25.py`, `src/policy_25.json`, `eval/workflow_policy_25.py`): ask-or-skip and stop-or-escalate both fitted on dollars over 30 development seeds ([release5_train.md](release5_train.md)). It is **deterministic and calls no API** (`case_summary.run(no_model=True)`: where the rules are silent the summary is code-written and inconclusive; test `tests/test_no_model.py`).
- **Agent v3.5** (`Environment(version="3.5")`, `SYSTEM_35`): the same policy as advice inside tool results and an `ask_advice` screen column (#111); an upcoding call by the rules that the chart rule also supports is binding unless `override_reason` names a claim, data flag or note sign (#112, narrowed by Simmy); a per-practice status and the rounds sent, with their dollar cost, every turn (#113). Use of the advice is logged in `advice_log.json`.

## Result in one table (net dollars per seed, ten fresh seeds, 79 upcoders)

| Arm | Net per seed | Found | Honest called |
|---|---|---|---|
| A3.5 | $32,159 | 36 | 1 |
| W2.5 | $31,888 | 37 | 3 |
| GL | $29,569 | 36 | 2 |
| W2.3 | $24,086 | 37 | 5 |

A3.5 and W2.5 are indistinguishable (paired gap $270 per seed, range -$29k to +$18k). Both beat GL and W2.3 on average by cutting costs and false calls; **recall did not move (46 to 47%)**. Free replay of the binding rule on the stored A3.4 runs: [release5_binding_replay.md](release5_binding_replay.md). In the fresh test the agent overrode a binding call twice and was right both times (both were honest doctors).

## Why A3.5's summaries score lower on the rule judge (4.54 against 4.89 for W2.5)

The checklist passes for nearly every agent summary; the lost points are two **writing defects in the agent's own text**, not weaker evidence: `headline_not_in_body` (the headline quotes a figure the code-written rationale never states: 41% of A3.5 summaries and 68% of its upcoding calls, against 26% and 44% for A3.4 and 1% for W2.5) and `repeated` (an interpretation sentence repeats the rationale: 35% and 65%, against 21% and 47% for A3.4). The workflow's summaries are fully code-written, so it has neither. A3.5 is worse than A3.4 on both, plausibly because the status and advice text put more figures in front of the agent. The judge is the project's own rule judge and no person has checked it, so this is a presentation finding about wording, not evidence of worse calls.

## Honest limits

Ten seeds of about eight upcoders; option 2 is the optimistic recovery model (one late signature flags a note, honest doctors sign late about 4%); the $2,000 false-call charge is an assumption (A3.5 and W2.5 swap places with it: W2.5 is $129 per seed ahead at $0, A3.5 is $270 ahead at $2,000 and $1,871 ahead at $10,000, all inside the seed-to-seed spread); the policy was fitted on 30 development seeds only. The release 5 fresh seeds (4545 to 5454) are now development data. Release 5's workflow arms in the fresh test did use the model for a handful of rule-silent providers (36 runs, about $0.67 over releases 3 to 5, for example `r4g_4141`: two Batch API calls to Opus 5.5, $0.032); only one of those summaries was an upcoding call, so W2.5's and GL's dollars would not change under the API-free writer, and W2.3's would lose at most that call.

## Hypotheses for release 6 (free ones first)

1. **Code-written headline and rationale for the agent.** Make `headline_not_in_body` and `repeated` hard lint failures in `submit_findings`, or let code write the headline from the agent's leaning. Expect the rule-judge mean to return to about 4.9 with no change in calls. Test: free replay of stored A3.5 summaries through the lint.
2. **Recall is flat at 46 to 47%; the misses are first samples that come back silent or clean.** Test second targeted requests or retries for silent offices (#103, #68) as new learned actions, scored in dollars, on a larger development pool.
3. **Refit on a larger pool (about 100 new development seeds).** Thirty seeds is a small fit for two linear models; check calibration and stability, then one pre-registered fresh test of all arms together.
4. **Make the agent obey a "stop" recommendation.** When advised TARG the agent stopped about half the time it departed from the advice (32 departures in 155 actions); test whether binding STOP (save rounds) or TARG (add evidence) pays on the development pool.
5. **Sweep the false-call charge and the recovery trigger.** The ranking is driven by the $2,000 assumption and by option 2's one-late-signature trigger; show where the order of arms flips, and fit the policy at more than one price.
6. **Run the older workflow arms API-free** so the whole comparison is deterministic (`ow.run(..., no_model=True)`).

## Decisions for Simmy

- Confirm W2.5 as the release 5 workflow default and A3.5 (full) as the release 5 agent.
- Whether to merge #110 (release 4) first; release 5 branches from it.
- Whether to tag v2.4/v3.4 and v2.5/v3.5, and add README rows (nothing is tagged or released).
- Which hypothesis opens release 6.
