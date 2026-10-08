# Synthetic data: how it is built and how well it matches CMS

Scope: Family Practice, Georgia. Everything is synthetic. Regenerate with
`python src/generate_synthetic.py data/synthetic --seed 42` (identical output for the same seed).

## Files
| File | Who sees it | Contents |
|---|---|---|
| `providers.csv` | detectors, agent | provider id, specialty, state, claim and patient counts |
| `patients.csv` | detectors, agent | age, chronic-condition count, condition list |
| `claims.csv` | detectors, agent | one row per visit: claim id, provider, patient, date, billed CPT, diagnoses |
| `ground_truth.json` | eval only (gitignored) | provider roles and the justified CPT for every claim |

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
