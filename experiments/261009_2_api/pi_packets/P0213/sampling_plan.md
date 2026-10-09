# Sampling plan for P0213

| Billed code | Claims in frame | Claims to review | Method |
|---|---|---|---|
| 99215 | 57 | 32 | random sample |

- Seed `pi-v1:P0213` (the sample is reproducible).
- Size rule: proportion within +/-10% at 90% confidence, assuming 50% (the conservative case), with finite-population correction; frames of 30 or fewer are reviewed in full.

## After the records come back
1. A reviewer fills `supported_cpt` for each requested claim in a copy of `record_request_list.csv` (blank = records not received / not reviewed).
2. Run `python src/pi_estimate.py plan.json reviewed.csv ALLOWED_JSON` to extrapolate an overpayment estimate with a confidence interval.
- Allowed amounts used (GA Family Practice average, CMS public file): 99211 $21.18, 99212 $51.50, 99213 $84.02, 99214 $120.21, 99215 $170.18. Real recoupment uses each claim's actual allowed amount.
- Per-claim overpayment = allowed(billed) - allowed(supported) when the supported level is lower; underbilling is ignored.
- The estimate is only as good as the review. Missing records, a non-random sample or a wrong frame change the answer.
