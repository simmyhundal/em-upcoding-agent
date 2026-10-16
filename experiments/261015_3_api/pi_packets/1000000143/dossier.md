# Payment Integrity dossier: 1000000143

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,372 / 1,155 |
| Billed mix (99211 to 99215) | 5 / 3 / 185 / 1,449 / 730 |
| 99215 share | 30.8% |
| Expected 99215 share given patient complexity | 4.3% |
| Screen scores | z vs peers 4.01; risk-adjusted 21.24; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000143: 7 of 10 documented 99215 claims (70%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000143 billed 99215 on 30.8% of 2,372 claims against an expected 4.3% given patient complexity (risk-adjusted score 21.24; plain z-score vs peers 4.01). 32% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 10 documented 99215 claims, 7 (70%) were documented below the billed level, against 15% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 13%, late 0%, unsigned 0%, data 3%. No audit trail was received. 3 of 24 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0077174: billed 99215; documented MDM level moderate, 32 minutes. C0077337: billed 99215; documented MDM level moderate, 36 minutes. C0077551: billed 99215; documented MDM level moderate, minutes not recorded. C0076565: billed 99215, patient aged 55 with 1 chronic condition(s) (hyperlipidemia). C0076824: billed 99215, patient aged 59 with 1 chronic condition(s) (type 2 diabetes). C0076832: billed 99215, patient aged 22 with 1 chronic condition(s) (atrial fibrillation).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000143.svg)

## Records-review sample so far

Documentation is on file for 30 claims (1% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 1 | 0 | 0.0% | 4.4% |
| 99214 | 19 | 2 | 10.5% | 5.0% |
| 99215 | 10 | 7 | 70.0% | 14.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (62 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0077174, C0077337, C0077551 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 13% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0077174, C0077337, C0077551.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
