# Payment Integrity dossier: 1000000073

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,496 / 724 |
| Billed mix (99211 to 99215) | 17 / 13 / 418 / 769 / 279 |
| 99215 share | 18.6% |
| Expected 99215 share given patient complexity | 3.2% |
| Screen scores | z vs peers 2.70; risk-adjusted 13.41; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000073: 11 of 13 documented 99215 claims (85%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000073 billed 99215 on 18.6% of 1,496 claims against an expected 3.2% given patient complexity (risk-adjusted score 13.41; plain z-score vs peers 2.70). 35% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 28 claims. Of 13 documented 99215 claims, 11 (85%) were documented below the billed level, against 7% for the comparison providers. Note checks on 28 returned notes (share showing each sign): problems 18%, late 4%, unsigned 0%, data 0%. No audit trail was received. 2 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0029780: billed 99215; documented MDM level moderate, 36 minutes. C0029878: billed 99215; documented MDM level moderate, 33 minutes. C0030157: billed 99215; documented MDM level moderate, 35 minutes. C0029584: billed 99215, patient aged 41 with 0 chronic condition(s). C0029690: billed 99215, patient aged 28 with 1 chronic condition(s) (hypertension). C0029747: billed 99215, patient aged 65 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000073.svg)

## Records-review sample so far

Documentation is on file for 28 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 3 | 0 | 0.0% | 3.8% |
| 99214 | 12 | 0 | 0.0% | 2.2% |
| 99215 | 13 | 11 | 84.6% | 6.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (55 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0029780, C0029878, C0030157 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 18% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0029780, C0029878, C0030157.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
