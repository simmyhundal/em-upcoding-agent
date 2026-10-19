# Payment Integrity dossier: 1000000056

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 813 / 396 |
| Billed mix (99211 to 99215) | 9 / 8 / 124 / 390 / 282 |
| 99215 share | 34.7% |
| Expected 99215 share given patient complexity | 8.6% |
| Screen scores | z vs peers 4.82; risk-adjusted 9.55; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000056: 18 of 23 documented 99215 claims (78%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000056 billed 99215 on 34.7% of 813 claims against an expected 8.6% given patient complexity (risk-adjusted score 9.55; plain z-score vs peers 4.82). 10% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 44 claims. Of 23 documented 99215 claims, 18 (78%) were documented below the billed level, against 40% for the comparison providers. Note checks on 44 returned notes (share showing each sign): problems 4%, late 2%, unsigned 0%, data 2%. No audit trail was received. 3 of 36 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0030556: billed 99215; documented MDM level moderate, 37 minutes. C0030558: billed 99215; documented MDM level moderate, minutes not recorded. C0030731: billed 99215; documented MDM level moderate, 31 minutes. C0030357: billed 99215, patient aged 53 with 1 chronic condition(s) (COPD). C0030362: billed 99215, patient aged 64 with 1 chronic condition(s) (hypertension). C0030419: billed 99215, patient aged 61 with 1 chronic condition(s) (hypothyroidism).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000056.svg)

## Records-review sample so far

Documentation is on file for 44 claims (5% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 1 | 20.0% | 2.9% |
| 99214 | 16 | 2 | 12.5% | 4.6% |
| 99215 | 23 | 18 | 78.3% | 40.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (55 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0030556, C0030558, C0030731 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 4% address fewer problems than their level implies and 2% were signed late; request the audit trail for C0030556, C0030558, C0030731.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
