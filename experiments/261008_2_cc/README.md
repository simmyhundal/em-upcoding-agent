# Experiment: cold-context subagent writes 25 case summaries

**What this is:** a separate Claude agent, given no project context, was asked to write the case summary for each of the
25 flagged providers (seed-42 synthetic data) from the evidence packets and the same system prompt `src/case_summary.py`
uses. It is **not** an API run and **not** a scored sample. It was told not to open the answer key; that was on trust.

Files: `packets.jsonl`, `system_prompt.txt`, `schema.json` (inputs); `summaries.jsonl` (outputs);
`summaries_checked.jsonl` (after the citation guardrail).

## Results (checked afterwards)
- **Citations:** 25/25 summaries passed the guardrail; 112/112 cited claims valid.
- **Leaning vs the answer key** (25 flagged: 8 upcoders, 3 hard negatives, 14 normal providers):

| Actual role | upcoding | high-acuity panel | inconclusive |
|---|---|---|---|
| Upcoder (8) | 7 | 0 | 1 |
| Hard negative (3) | 1 | 2 | 0 |
| Normal (14) | 9 | 1 | 4 |

"Upcoding" leanings: 17, of which 7 were real upcoders (41% precision, vs 32% for the flagged list itself).
Nine honest providers were still labeled "upcoding".

## Limits (important)
- By the agent's own report, most rationales follow a template: numbers filled from each packet, a leaning-specific closing
  sentence, and a hand-written line for only 8 providers. 17 summaries share one closing sentence, and rationale length is
  nearly constant. So this tests a templated pass over the packet, not careful per-provider writing, and says little about
  summary quality or how an API run would read.
- The leaning is largely readable from the packet numbers; accuracy here reflects how informative the packet is.
- One run, one seed, small counts. Not the Opus 5.5 API call. No usefulness rubric scoring was done.
