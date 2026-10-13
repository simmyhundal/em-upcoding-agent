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
| Screen scores | z vs peers 3.06; risk-adjusted 6.63; flagged by zscore+riskadj |

## Case summary (advisory)

**1000000160: 3 of 7 documented 99215 claims (43%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000160 billed 99215 on 20.7% of 237 claims against an expected 3.7% given patient complexity (risk-adjusted score 6.63; plain z-score vs peers 3.06). 39% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 7 documented 99215 claims, 3 (43%) were documented below the billed level, against 0% for the comparison providers. 5 of 21 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0081678: billed 99215, patient aged 52 with 1 chronic condition(s) (asthma); documented MDM level moderate, 32 minutes. C0081799: billed 99215, patient aged 55 with 4 chronic condition(s) (hypothyroidism;type 2 diabetes;depression;asthma); documented MDM level moderate, minutes not recorded. C0081822: billed 99215; documented MDM level moderate, 34 minutes. C0081673: billed 99215, patient aged 45 with 1 chronic condition(s) (hypertension); documented MDM level high, minutes not recorded. C0081694: billed 99215, patient aged 63 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000160.svg)

## Records-review sample so far

Documentation is on file for 30 claims (13% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 4.7% |
| 99214 | 17 | 1 | 5.9% | 3.7% |
| 99215 | 7 | 3 | 42.9% | 0.0% |

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
