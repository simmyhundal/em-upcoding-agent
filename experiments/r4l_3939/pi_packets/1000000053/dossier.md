# Payment Integrity dossier: 1000000053

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,294 / 619 |
| Billed mix (99211 to 99215) | 20 / 19 / 347 / 660 / 248 |
| 99215 share | 19.2% |
| Expected 99215 share given patient complexity | 5.9% |
| Screen scores | z vs peers 2.09; risk-adjusted 7.21; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000053: 1 of 19 documented 99214 and 99215 claims (5%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000053 billed 99215 on 19.2% of 1,294 claims against an expected 5.9% given patient complexity (risk-adjusted score 7.21; plain z-score vs peers 2.09). 27% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 5 documented 99215 claims, 1 (20%) were documented below the billed level, against 40% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 27%, late 17%, unsigned 0%, data 17%, bulk created 17%, paste heavy 23%. 6 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0028394: billed 99215, patient aged 34 with 1 chronic condition(s) (hypertension); documented MDM level moderate, minutes not recorded. C0027695: billed 99215, patient aged 43 with 0 chronic condition(s). C0027697: billed 99215, patient aged 37 with 0 chronic condition(s). C0027786: billed 99215, patient aged 90 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000053.svg)

## Records-review sample so far

Documentation is on file for 30 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 0 | 0.0% | 2.9% |
| 99214 | 14 | 0 | 0.0% | 4.6% |
| 99215 | 5 | 1 | 20.0% | 40.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (54 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0028394, C0027695, C0027697 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 27% address fewer problems than their level implies and 17% were signed late; request the audit trail for C0028394, C0027695, C0027697.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
