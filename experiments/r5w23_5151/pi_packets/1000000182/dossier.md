# Payment Integrity dossier: 1000000182

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 289 / 138 |
| Billed mix (99211 to 99215) | 7 / 8 / 131 / 97 / 46 |
| 99215 share | 15.9% |
| Expected 99215 share given patient complexity | 5.1% |
| Screen scores | z vs peers 2.04; risk-adjusted 3.77; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000182: 0 of 19 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000182 billed 99215 on 15.9% of 289 claims against an expected 5.1% given patient complexity (risk-adjusted score 3.77; plain z-score vs peers 2.04). 43% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 0 (0%) were documented below the billed level, against 30% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 31%, late 27%, unsigned 0%, data 13%, bulk created 4%, paste heavy 7%. 6 of 23 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0104380: billed 99213; documented MDM level straightforward, minutes not recorded. C0104090: billed 99215, patient aged 55 with 1 chronic condition(s) (osteoarthritis); documented MDM level high, minutes not recorded. C0104103: billed 99215, patient aged 30 with 0 chronic condition(s). C0104111: billed 99215, patient aged 27 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000182.svg)

## Records-review sample so far

Documentation is on file for 45 claims (16% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 19 | 1 | 5.3% | 4.7% |
| 99214 | 3 | 0 | 0.0% | 4.4% |
| 99215 | 19 | 0 | 0.0% | 30.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (28 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0104380, C0104090, C0104103 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 31% address fewer problems than their level implies and 27% were signed late; request the audit trail for C0104380, C0104090, C0104103.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
