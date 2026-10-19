# Payment Integrity dossier: 1000000128

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 952 / 494 |
| Billed mix (99211 to 99215) | 12 / 30 / 303 / 462 / 145 |
| 99215 share | 15.2% |
| Expected 99215 share given patient complexity | 4.7% |
| Screen scores | z vs peers 1.54; risk-adjusted 5.63; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000128: 0 of 22 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000128 billed 99215 on 15.2% of 952 claims against an expected 4.7% given patient complexity (risk-adjusted score 5.63; plain z-score vs peers 1.54). 53% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 22 documented 99215 claims, 0 (0%) were documented below the billed level, against 48% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 36%, late 16%, unsigned 0%, data 16%. No audit trail was received. 8 of 39 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0055236: billed 99214; documented MDM level low, minutes not recorded. C0054364: billed 99215, patient aged 54 with 0 chronic condition(s); documented MDM level high, 49 minutes. C0054478: billed 99215, patient aged 55 with 0 chronic condition(s). C0054494: billed 99215, patient aged 52 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000128.svg)

## Records-review sample so far

Documentation is on file for 45 claims (5% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 0 | 0.0% | 4.7% |
| 99214 | 13 | 1 | 7.7% | 4.7% |
| 99215 | 22 | 0 | 0.0% | 48.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (47 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0055236, C0054364, C0054478 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 36% address fewer problems than their level implies and 16% were signed late; request the audit trail for C0055236, C0054364, C0054478.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
