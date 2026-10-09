# Eval report (top 25 flagged)

| Metric | Plain z-score | Risk-adjusted | Combined list | Target |
|---|---|---|---|---|
| Upcoders found | 8 / 8 | 8 / 8 | 8 / 8 | false negative rate <= 12.5% (at least 7 of 8) |
| Hard negatives falsely flagged | 2 / 8 | 1 / 8 | 1 / 8 | - |
| Normal providers falsely flagged | 15 / 200 | 16 / 200 | 16 / 200 | false positive rate <= 12.5% over all honest doctors |
| Precision (upcoders / flagged) | 32% | 32% | 32% | - |
| Upcoder ranks | 1,7,8,9,10,11,15,16 | 1,2,3,4,5,6,7,8 | 1,2,4,6,7,8,9,10 | - |
| Hard-negative ranks | 3,18,28,53,74,111,189,202 | 9,40,58,78,136,181,188,201 | 3,29,52,63,122,127,186,201 | - |

## LLM summary metrics

### Held-out API run (261009_2_api, seed 101): claude-opus-5-5, with documentation evidence
- Templating check: no templating detected (boilerplate share 0%, similarity median 0.04 / p90 0.07)
- Citation accuracy: 100.0% (278/278); 25/25 summaries passed the guardrail. Target: 100%.

| Actual role (summaries scored) | upcoding | high-acuity panel | inconclusive |
|---|---|---|---|
| Upcoder (8) | 8 | 0 | 0 |
| Hard negative (1) | 0 | 1 | 0 |
| Normal (16) | 0 | 13 | 3 |

- "Upcoding" calls: 8; precision 100%, recall 100% (8 of 8 upcoders).
- Honest providers labeled upcoding: 0 of 17.
- Summaries rejected by the guardrail and not scored: 0.
- Summary usefulness (LLM judge, 1-5, eval/rubric.md): mean 3.24 over 25 summaries (scores 1: 0, 2: 3, 3: 13, 4: 9, 5: 0); target >= 4: NOT met. The judge is itself an LLM, so treat this as a rough rubric check.

## Target check
- False negative rate <= 12.5% (screen, combined list): met (0 of 8 upcoders missed, 0.0%)
- False positive rate <= 12.5% (screen, combined list): met (17 of 208 honest doctors flagged, 8.2%)
- Held-out API run (261009_2_api, seed 101): claude-opus-5-5, with documentation evidence: citation accuracy 100%: met (278/278); summary usefulness >= 4: NOT met (mean 3.24)

## Caveats
- Synthetic data. Billed level depends on patient complexity by construction, so the risk-adjusted detector is helped by how the data was built; results do not transfer directly to real claims.
- One seed, 8 upcoders and 8 hard negatives: small counts, so one provider moves a rate a lot.
- The CMS file hides small cells; the synthetic data is calibrated to it only in the upper tail (see docs/synthetic_data.md).
- A 100% citation accuracy means every cited claim exists and belongs to the provider; it does not mean each cited claim supports the sentence that cites it (see "Guardrail scope" in the README).
- Summary runs listed here come from in-session agents, not the API step, unless labeled otherwise; see each experiment's README for what it is and is not.
