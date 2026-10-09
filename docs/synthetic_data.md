# Synthetic data: how it is built and how well it matches CMS

Scope: Family Practice, Georgia. Everything is synthetic. Regenerate with
`python src/generate_synthetic.py data/synthetic --seed 42` (answer key goes to `eval/answer_key/ground_truth.json`, outside the data folder) (identical output for the same seed).

## Files
| File | Who sees it | Contents |
|---|---|---|
| `providers.csv` | detectors, agent | provider id, specialty, state, claim and patient counts |
| `patients.csv` | detectors, agent | age, chronic-condition count, condition list |
| `claims.csv` | detectors, agent | one row per visit: claim id, provider, patient, date, billed CPT, diagnoses |
| `documentation.csv` | agent | records-review sample for about 30% of claims: documented MDM level and minutes |
| `eval/answer_key/ground_truth.json` | eval only (gitignored; outside `data/`) | provider roles and the justified CPT for every claim |

## Model
- Each patient has a chronic-condition count (complexity).
- Each visit has a *justified* level (99211-99215) from an ordered logit on patient complexity, a provider panel effect, and a provider-level shift on the 99215 threshold only (a heavier upper tail).
- Normal providers bill the justified level. Hard negatives are honest but have panels about twice as sick. Upcoders bill justified+1 on 15-40% of visits (capped at 99215).
- Provider volume is lognormal (median 283, from the CMS GA Family Practice file).

## Calibration (fitted by random search; not a tight fit)
Target: GA Family Practice, individual providers with at least 50 E/M services (1,572 providers).

| | CMS GA (observed) | Synthetic (all 216 providers) |
|---|---|---|
| 99215 share, mean | 0.031 | 0.055 |
| 90th percentile | 0.099 | 0.139 |
| 95th percentile | 0.181 | 0.194 |
| 75th percentile | 0.016 | 0.067 |
| Visit mix 99211 / 99212 / 99213 / 99214 / 99215 (normal providers, fitted run) | 0.007 / 0.010 / 0.287 / 0.665 / 0.031 | 0.012 / 0.012 / 0.362 / 0.570 / 0.044 |

Known mismatches:
- **Low end.** CMS hides rows with 10 or fewer beneficiaries, so 74% of real providers show zero 99215. Synthetic providers rarely show exactly zero, so the lower percentiles are not matched on purpose. Mean and 75th percentile are therefore higher than observed.
- **Mix.** Synthetic 99213 is a bit high and 99214 a bit low versus observed.
- The all-provider synthetic figures include the planted upcoders and hard negatives, which push the tail up.

## Difficulty (first check, seed 42)
A plain z-score on 99215 share puts 7 of 8 upcoders, 3 of 8 hard negatives and 15 of 200 normal providers in the top 25. The upcoders may be too easy to find. If the eval shows that, lower the upcoder upgrade rate (`UPCODER_FRACTION`).

## Tests
`python tests/test_generate_synthetic.py` checks determinism, role counts, that the agent-visible files do not leak ground truth, and that only upcoders bill above the justified level.

## Baseline 2 result (risk-adjusted, seed 42)
Top 25 flagged: 8 of 8 upcoders, 3 of 8 hard negatives, 14 of 200 normal providers. Upcoder ranks 1-10 (plain z-score: 2-35). Hard negatives still rank 5, 12 and 22.

Why risk adjustment does not clear the hard negatives: it only uses the chronic-condition count. In the generator, providers also differ in a legitimate way that complexity does not explain (a coding-style effect and a separate provider-level propensity for 99215). Those providers look like outliers even after adjusting for patient complexity. That is a property of how the data was built, not a bug in the baseline.

## Documentation sample (Issue 16)
`documentation.csv` simulates a records review of a random ~30% of claims. The documented level equals the visit's justified
level, off by one in 15% of cases; minutes are drawn from a typical band for that level. It uses its own random stream, so
`claims.csv` is identical with or without it. On the seed-42 data, documented 99215 claims show documentation below the billed
level 69% of the time for upcoders and 8% for everyone else (counts: 468 upcoder, 1,318 other documented 99215s).

Caveat: documentation is generated from the same hidden level that defines an upcoded visit, so this makes the problem
easier by construction. It measures how well the summarizer uses records-review evidence, not how well it would do on real claims.
Providers with few documented claims (many honest ones have fewer than 10) give noisy rates, which the summarizer has to weigh.
