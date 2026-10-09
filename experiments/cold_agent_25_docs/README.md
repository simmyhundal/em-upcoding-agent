# Experiment: one fresh agent per provider, with documentation evidence (25 of 25)

**What this is:** the same setup as `experiments/cold_agent_25_rerun/` (one fresh, context-free agent per flagged provider,
reading one prompt file and writing one JSON summary), but the evidence packets now include the documentation review from
Issue 16 and the prompt explains how to read it. Not an API run; not a scored sample. Same caveats about differences from a true
API call as in the rerun README.

**Run history:** the first attempt completed 20 of 25; the last five (P0209, P0035, P0134, P0109, P0086) failed on an API
rate-limit error and were rerun after the limit reset with the same prompts. The results below cover all 25.

## Results (25 providers, checked afterwards against the answer key)
- **Citations:** 25/25 passed the guardrail; 230/230 cited claims valid.

| Actual role | upcoding | high-acuity panel | inconclusive |
|---|---|---|---|
| Upcoder (8) | 8 | 0 | 0 |
| Hard negative (3) | 0 | 3 | 0 |
| Normal (14) | 0 | 10 | 4 |

"Upcoding" leanings: 8, all real upcoders (100% precision). No honest provider was labeled upcoding.

## Previous run on the same 25 providers (no documentation)
`experiments/cold_agent_25_rerun/`: 8/8 upcoders labeled upcoding, but 14 of 17 honest providers were also labeled upcoding
(13 of 14 normal, 1 of 3 hard negatives). 22 "upcoding" leanings, 8 real upcoders (36% precision).

## What this shows, and what it does not
- Given records-review evidence, the agents used it well: they read the unsupported rate against the all-provider rate, weighed
  small documented samples (the "inconclusive" calls have only 3 or 4 documented 99215s), and recommended expanding the
  documentation sample where it was thin.
- **This is easier by construction.** The documentation is generated from the same hidden level that defines an upcoded visit
  (documented level = justified level, off by one 15% of the time). The result shows that a summarizer can use records-review
  evidence, not that it would perform like this on real claims or on real documentation.
- 25 providers (8 / 3 / 14 per role), one run, one seed. Not scored on the usefulness rubric.
- Four normal providers were left "inconclusive" because few of their 99215 claims have documentation (3 to 4 documented); the right call, but it means documentation coverage limits how many cases can be settled.
