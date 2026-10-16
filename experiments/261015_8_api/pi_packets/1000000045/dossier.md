# Payment Integrity dossier: 1000000045

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 579 / 305 |
| Billed mix (99211 to 99215) | 10 / 7 / 144 / 318 / 100 |
| 99215 share | 17.3% |
| Expected 99215 share given patient complexity | 4.1% |
| Screen scores | z vs peers 2.43; risk-adjusted 6.35; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000045: 15 of 20 documented 99215 claims (75%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000045 billed 99215 on 17.3% of 579 claims against an expected 4.1% given patient complexity (risk-adjusted score 6.35; plain z-score vs peers 2.43). 24% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 43 claims. Of 20 documented 99215 claims, 15 (75%) were documented below the billed level, against 7% for the comparison providers. Note checks on 43 returned notes (share showing each sign): problems 7%, late 2%, unsigned 0%, data 0%. No audit trail was received. 0 of 30 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0017129: billed 99215; documented MDM level moderate, 31 minutes. C0017324: billed 99215; documented MDM level moderate, 35 minutes. C0017417: billed 99215; documented MDM level moderate, 32 minutes. C0017053: billed 99215, patient aged 54 with 1 chronic condition(s) (hypothyroidism). C0017064: billed 99215, patient aged 39 with 1 chronic condition(s) (obesity). C0017080: billed 99215, patient aged 36 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000045.svg)

## Records-review sample so far

Documentation is on file for 43 claims (7% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 1 | 16.7% | 3.8% |
| 99214 | 17 | 3 | 17.6% | 2.2% |
| 99215 | 20 | 15 | 75.0% | 6.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (41 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0017129, C0017324, C0017417 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 7% address fewer problems than their level implies and 2% were signed late; request the audit trail for C0017129, C0017324, C0017417.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
