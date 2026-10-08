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
- Citation accuracy: pending (needs the live summary run). Target: 100%.
- Summary usefulness (1-5, see eval/rubric.md): pending. Target: average >= 4.

## Target check
- Recall >= 7/8: met (combined list)
- Hard-negative false flags lower than plain z-score: NOT met (3 vs 3)

## Caveats
- Synthetic data. Billed level depends on patient complexity by construction, so the risk-adjusted detector is helped by how the data was built; results do not transfer directly to real claims.
- One seed, 8 upcoders and 8 hard negatives: small counts, so one provider moves a rate a lot.
- The CMS file hides small cells; the synthetic data is calibrated to it only in the upper tail (see docs/synthetic_data.md).
