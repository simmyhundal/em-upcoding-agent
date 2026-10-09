# Payment Integrity packet (Issue 10)

After an investigator reads a case summary and decides to pursue a provider, Payment Integrity (PI) needs to start recovery work.
`src/pi_packet.py` prepares draft material for the providers whose summaries lean "upcoding" and passed the citation guardrail.
It is a starting point for people, not a finding.

## What each provider gets (`experiments/<run>/pi_packets/<provider>/`, for example `experiments/261009_1_api/pi_packets/`)
- `dossier.md`: provider overview, billed vs expected, the case summary and evidence chart, the records-review sample so far, next steps, limits.
- `record_request_list.csv`: a seeded random sample of the provider's 99215 claims to request records for (patient, date, billed code, diagnoses). Documentation facts are deliberately not included.
- `sampling_plan.md` and `plan.json`: the frame, sample size, seed and formula. Sample size is for a proportion within +/-10% at 90% confidence (assume 50%), with finite-population correction; frames of 30 or fewer claims are reviewed in full. `--codes 99215,99214` samples both codes as separate strata.
- `reviewed_example.csv` and `example_estimate.md`: a SIMULATED review (supported level taken from the synthetic documentation sample; sampled claims without documentation count as records not received).
- `pi_packets/tracker.csv` in the run folder: a status row per provider (not started, records requested, received, reviewed, notice sent, resolved).

## Estimator (`src/pi_estimate.py`)
Per-claim overpayment is allowed(billed) minus allowed(supported) when the supported level is lower, else 0 (underbilling is ignored).
The estimate extrapolates the sample mean to the frame with a finite-population-corrected standard error and a t interval
(90% or 95%). Missing records are excluded by default (the response rate is reported); `--missing unsupported` treats a blank as one level below billed.
Allowed amounts are GA Family Practice averages from the public CMS file (`data/baselines/allowed_amounts_ga_fp.json`); real recoupment uses each claim's allowed amount.

## Does the estimator work? (eval only, uses the answer key)
`python eval/check_pi_estimate.py ...` compares each simulated estimate with the true overpayment on that provider's 99215 frame:

| Provider | True overpayment | Estimate | 90% CI | Covered | Reviewed / sampled |
|---|---|---|---|---|---|
| P0002 | $1,999 | $1,973 | $1,281 to $2,665 | yes | 9 / 28 |
| P0041 | $1,699 | $2,343 | $1,846 to $2,841 | no | 13 / 30 |
| P0064 | $2,099 | $899 | $0 to $1,951 | no | 8 / 36 |
| P0088 | $12,193 | $11,336 | $7,302 to $15,371 | yes | 18 / 56 |
| P0095 | $4,347 | $4,405 | $3,492 to $5,319 | yes | 14 / 41 |
| P0143 | $4,497 | $4,264 | $3,691 to $4,838 | yes | 18 / 40 |
| P0161 | $3,148 | $2,199 | $759 to $3,639 | yes | 7 / 37 |
| P0215 | $26,284 | $27,364 | $17,358 to $37,370 | yes | 16 / 63 |

Intervals covering the true value: 6 of 8

Six of eight 90% intervals covering the truth is consistent with the nominal rate for eight providers, but eight is too few to judge. On the held-out dataset (seed 101, `experiments/261009_2_api/pi_packets/`) all 8 of 8 covered, so 14 of 16 across both runs.
The simulated documentation is off by one level 15% of the time, which adds a small upward bias for honest claims; the review step in a real case replaces it.

## Not in scope, on purpose
Demand letters, payment suspension, referral decisions, provider notice and appeal handling need people and legal review. Nothing here drafts them.
In a real case the supported level for each sampled claim must come from a human review of the records; this tool only does the arithmetic.
