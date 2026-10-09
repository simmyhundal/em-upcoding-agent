# Experiment: one fresh agent per provider, with documentation evidence (20 of 25 completed)

**What this is:** the same setup as `experiments/cold_agent_25_rerun/` (one fresh, context-free agent per flagged provider,
reading one prompt file and writing one JSON summary), but the evidence packets now include the documentation review from
Issue 16 and the prompt explains how to read it. Not an API run; not a scored sample. Same caveats about differences from a true
API call as in the rerun README.

**Incomplete:** 20 of 25 providers finished. The last five agents (P0209, P0035, P0134, P0109, P0086) failed with an API
rate-limit error (session usage limit) and produced nothing. P0109 is a hard negative; the other four are normal providers.
Results below cover the 20 that finished and should not be read as the full 25.

## Results (20 providers, checked afterwards against the answer key)
- **Citations:** 20/20 passed the guardrail; 191/191 cited claims valid.

| Actual role | upcoding | high-acuity panel | inconclusive |
|---|---|---|---|
| Upcoder (8) | 8 | 0 | 0 |
| Hard negative (2) | 0 | 2 | 0 |
| Normal (10) | 0 | 8 | 2 |

"Upcoding" leanings: 8, all real upcoders (100% precision). No honest provider was labeled upcoding.

## Same 20 providers, previous run (no documentation)
Upcoders 8/8 labeled upcoding, but 11 of 12 honest providers were also labeled upcoding or left inconclusive (10 normal + 1 hard
negative labeled upcoding). "Upcoding" leanings: 19, of which 8 were real upcoders (42% precision).

## What this shows, and what it does not
- Given records-review evidence, the agents used it well: they read the unsupported rate against the all-provider rate, weighed
  small documented samples (the two "inconclusive" calls have only 3 and 4 documented 99215s), and recommended expanding the
  documentation sample where it was thin.
- **This is easier by construction.** The documentation is generated from the same hidden level that defines an upcoded visit
  (documented level = justified level, off by one 15% of the time). The result shows that a summarizer can use records-review
  evidence, not that it would perform like this on real claims or on real documentation.
- 20 providers, 8/2/10 per role, one run. Not scored on the usefulness rubric.
- The five missing providers include the only third hard negative; rerun them after the usage limit resets before quoting a 25-provider figure.
