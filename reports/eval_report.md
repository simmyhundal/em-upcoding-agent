# Eval report (top 25 flagged)

| Metric | Plain z-score | Risk-adjusted | Combined list | Target |
|---|---|---|---|---|
| Upcoders found | 7 / 8 | 8 / 8 | 8 / 8 | >= 7 / 8 |
| Hard negatives falsely flagged | 3 / 8 | 3 / 8 | 3 / 8 | lower than plain z-score |
| Normal providers falsely flagged | 15 / 200 | 14 / 200 | 14 / 200 | - |
| Precision (upcoders / flagged) | 28% | 32% | 32% | - |
| Upcoder ranks | 2,3,4,5,7,10,13,35 | 1,2,3,4,6,7,9,10 | 1,3,4,5,6,7,9,19 | - |
| Hard-negative ranks | 1,9,24,27,40,91,103,147 | 5,12,22,27,63,148,173,206 | 2,8,24,30,40,120,140,179 | - |

## LLM summary metrics

### Live API run (261009_1_api): claude-opus-5-5, with documentation evidence
- Templating check: no templating detected (boilerplate share 0%, similarity median 0.05 / p90 0.09)
- Citation accuracy: 100.0% (261/261); 25/25 summaries passed the guardrail. Target: 100%.

| Actual role (summaries scored) | upcoding | high-acuity panel | inconclusive |
|---|---|---|---|
| Upcoder (8) | 8 | 0 | 0 |
| Hard negative (3) | 0 | 3 | 0 |
| Normal (14) | 0 | 9 | 5 |

- "Upcoding" calls: 8; precision 100%, recall 100% (8 of 8 upcoders).
- Honest providers labeled upcoding: 0 of 17.
- Summaries rejected by the guardrail and not scored: 0.
- Summary usefulness (LLM judge, 1-5, eval/rubric.md): mean 3.44 over 25 summaries (scores 1: 0, 2: 0, 3: 15, 4: 9, 5: 1); target >= 4: NOT met. The judge is itself an LLM, so treat this as a rough rubric check.

### Experiment 261008_2_cc: single agent, templated (no documentation)
- Templating check: TEMPLATED - do not score quality on this run (boilerplate share 77%, similarity median 0.30 / p90 1.00)
- Citation accuracy: 100.0% (112/112); 25/25 summaries passed the guardrail. Target: 100%.

| Actual role (summaries scored) | upcoding | high-acuity panel | inconclusive |
|---|---|---|---|
| Upcoder (8) | 7 | 0 | 1 |
| Hard negative (3) | 1 | 2 | 0 |
| Normal (14) | 9 | 1 | 4 |

- "Upcoding" calls: 17; precision 41%, recall 88% (7 of 8 upcoders).
- Honest providers labeled upcoding: 10 of 17.
- Summaries rejected by the guardrail and not scored: 0.

### Experiment 261008_3_cc: one agent per provider (no documentation)
- Templating check: no templating detected (boilerplate share 0%, similarity median 0.04 / p90 0.08)
- Citation accuracy: 100.0% (287/287); 25/25 summaries passed the guardrail. Target: 100%.

| Actual role (summaries scored) | upcoding | high-acuity panel | inconclusive |
|---|---|---|---|
| Upcoder (8) | 8 | 0 | 0 |
| Hard negative (3) | 1 | 0 | 2 |
| Normal (14) | 13 | 0 | 1 |

- "Upcoding" calls: 22; precision 36%, recall 100% (8 of 8 upcoders).
- Honest providers labeled upcoding: 14 of 17.
- Summaries rejected by the guardrail and not scored: 0.

### Experiment 261008_4_cc: one agent per provider, with documentation evidence
- Templating check: no templating detected (boilerplate share 0%, similarity median 0.05 / p90 0.08)
- Citation accuracy: 100.0% (230/230); 25/25 summaries passed the guardrail. Target: 100%.

| Actual role (summaries scored) | upcoding | high-acuity panel | inconclusive |
|---|---|---|---|
| Upcoder (8) | 8 | 0 | 0 |
| Hard negative (3) | 0 | 3 | 0 |
| Normal (14) | 0 | 10 | 4 |

- "Upcoding" calls: 8; precision 100%, recall 100% (8 of 8 upcoders).
- Honest providers labeled upcoding: 0 of 17.
- Summaries rejected by the guardrail and not scored: 0.

## Target check
- Recall >= 7/8: met (combined list)
- Hard-negative false flags lower than plain z-score: NOT met (3 vs 3)
- Live API run (261009_1_api): claude-opus-5-5, with documentation evidence: citation accuracy 100%: met (261/261); summary usefulness >= 4: NOT met (mean 3.44)

## Caveats
- Synthetic data. Billed level depends on patient complexity by construction, so the risk-adjusted detector is helped by how the data was built; results do not transfer directly to real claims.
- One seed, 8 upcoders and 8 hard negatives: small counts, so one provider moves a rate a lot.
- The CMS file hides small cells; the synthetic data is calibrated to it only in the upper tail (see docs/synthetic_data.md).
- A 100% citation accuracy means every cited claim exists and belongs to the provider; it does not mean each cited claim supports the sentence that cites it (see "Guardrail scope" in the README).
- Summary runs listed here come from in-session agents, not the API step, unless labeled otherwise; see each experiment's README for what it is and is not.
