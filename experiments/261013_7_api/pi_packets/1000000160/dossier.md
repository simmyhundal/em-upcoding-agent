# Payment Integrity dossier: 1000000160

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 237 / 122 |
| Billed mix (99211 to 99215) | 1 / 3 / 50 / 134 / 49 |
| 99215 share | 20.7% |
| Expected 99215 share given patient complexity | 3.7% |
| Screen scores | z vs peers 3.06; risk-adjusted 6.63; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000160: 4 of 12 documented 99214 and 99215 claims (33%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000160 billed 99215 on 20.7% of 237 claims against an expected 3.7% given patient complexity (risk-adjusted score 6.63; plain z-score vs peers 3.06). 39% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 15 claims. Of 3 documented 99215 claims, 2 (67%) were documented below the billed level, against 0% for the comparison providers. 1 of 10 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0081766: billed 99215; documented MDM level moderate, minutes not recorded. C0081802: billed 99215, patient aged 51 with 0 chronic condition(s); documented MDM level moderate, 38 minutes. C0081673: billed 99215, patient aged 45 with 1 chronic condition(s) (hypertension). C0081678: billed 99215, patient aged 52 with 1 chronic condition(s) (asthma). C0081694: billed 99215, patient aged 63 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000160.svg)

## Records-review sample so far

Documentation is on file for 15 claims (6% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 1 | 0 | 0.0% | 4.7% |
| 99214 | 9 | 2 | 22.2% | 3.7% |
| 99215 | 3 | 2 | 66.7% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
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
