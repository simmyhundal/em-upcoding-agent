# Experiment: one fresh agent per provider writes 25 case summaries (rerun)

**What this is:** the closest in-session stand-in for the real step (25 independent LLM calls). Each of the 25 flagged
providers (seed-42 synthetic data) got its own fresh agent with no project context. The agent read one file containing the
system prompt, that provider's evidence packet and the output schema, and wrote one JSON summary. It is **not** an API run
and **not** a scored sample. Packets use the fixed, stratified sampler (Issue 11).

Differences from a true API call: the model is "an Opus-class agent", not `claude-opus-5-5` with schema-constrained output and a
fixed effort setting; the prompt was read from a file (not sent inline); the agents had tools available and were told not to use
them beyond reading and writing their files (each used 3-4 tool calls, consistent with that, but it is not audited). Because of a
concurrency limit, 20 ran first and the last 5 afterwards.

Files: `prompts/` (inputs), `out/` (raw agent outputs), `summaries.jsonl`, `summaries_checked.jsonl` (after the citation guardrail).

## Results (checked afterwards against the answer key)
- **Citations:** 25/25 summaries passed the guardrail; 287/287 cited claims valid.
- **Leaning vs role** (25 flagged: 8 upcoders, 3 hard negatives, 14 normal providers):

| Actual role | upcoding | high-acuity panel | inconclusive |
|---|---|---|---|
| Upcoder (8) | 8 | 0 | 0 |
| Hard negative (3) | 1 | 0 | 2 |
| Normal (14) | 13 | 0 | 1 |

"Upcoding" leanings: 22, of which 8 were real upcoders (36% precision; the flagged list itself is 32%).

## Compared with the first (single-agent) run
| | First run | This rerun |
|---|---|---|
| Upcoders labeled upcoding | 7 / 8 | 8 / 8 |
| Honest flagged providers (hard negative + normal) labeled upcoding | 10 / 17 | 14 / 17 |
| Median rationale length | 477 characters | 1,283 characters |
| Distinct closing sentences | 3 | 25 |
| Citations valid | 112 / 112 | 287 / 287 |

## What this shows
- The writing is now real, per-provider work: specific numbers from the packet, cited claims, cautious wording, concrete next steps, and honest statements of what is missing (no clinical documentation).
- Accuracy did not improve. The agents mostly agree with the statistical flag: 22 of 25 labeled "upcoding". They recall every upcoder but also label 13 of 14 honest flagged providers as upcoding.
- A likely reason (an inference, not tested): in the synthetic data, some honest providers code 99215 more often for reasons the claims do not show, so their packets look the same as an upcoder's (for example P0114, an honest provider whose summary reads as a clear upcoding pattern). With only claim-level features, those cases cannot be told apart. That is the case for richer evidence (Path A, clinical notes), and for treating the leaning as advisory.

## Limits
One run, one seed, 8/3/14 cases. Not scored on the usefulness rubric. See also `experiments/cold_agent_25/` (first run, templated).
