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

**1000000143: 5 of 7 documented 99215 claims (71%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000143 billed 99215 on 30.8% of 2,372 claims against an expected 4.3% given patient complexity (risk-adjusted score 21.24; plain z-score vs peers 4.01). 32% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 20 claims. Of 7 documented 99215 claims, 5 (71%) were documented below the billed level, against 15% for the comparison providers. 2 of 15 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0076627: billed 99215; documented MDM level moderate, minutes not recorded. C0076995: billed 99215; documented MDM level low, minutes not recorded. C0077120: billed 99215, patient aged 32 with 1 chronic condition(s) (hyperlipidemia); documented MDM level moderate, minutes not recorded. C0076565: billed 99215, patient aged 55 with 1 chronic condition(s) (hyperlipidemia). C0076824: billed 99215, patient aged 59 with 1 chronic condition(s) (type 2 diabetes). C0076832: billed 99215, patient aged 22 with 1 chronic condition(s) (atrial fibrillation).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000143.svg)

## Records-review sample so far

Documentation is on file for 20 claims (1% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 4.4% |
| 99214 | 9 | 0 | 0.0% | 5.0% |
| 99215 | 7 | 5 | 71.4% | 14.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (62 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full records for the cited claims and have a certified coder re-score each against current E/M documentation rules (medical decision making or total time).
- If the re-scoring confirms the pattern, use the sampling plan in the recovery packet to review a statistical sample of this provider's 99215 claims.
- Check whether notes for the cited claims look copied forward, and whether documented minutes repeat from visit to visit.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
