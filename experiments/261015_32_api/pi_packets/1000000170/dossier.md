# Payment Integrity dossier: 1000000170

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 240 / 124 |
| Billed mix (99211 to 99215) | 3 / 0 / 49 / 122 / 66 |
| 99215 share | 27.5% |
| Expected 99215 share given patient complexity | 4.8% |
| Screen scores | z vs peers 3.76; risk-adjusted 5.74; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000170: 7 of 9 documented 99215 claims (78%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000170 billed 99215 on 27.5% of 240 claims against an expected 4.8% given patient complexity (risk-adjusted score 5.74; plain z-score vs peers 3.76). 24% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 9 documented 99215 claims, 7 (78%) were documented below the billed level, against 14% for the comparison providers. 5 of 21 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0086162: billed 99215; documented MDM level moderate, 23 minutes. C0086180: billed 99215, patient aged 50 with 1 chronic condition(s) (depression); documented MDM level moderate, 39 minutes. C0086251: billed 99215; documented MDM level moderate, minutes not recorded. C0086163: billed 99215, patient aged 62 with 1 chronic condition(s) (hyperlipidemia). C0086166: billed 99215, patient aged 39 with 0 chronic condition(s). C0086174: billed 99215, patient aged 70 with 1 chronic condition(s) (osteoarthritis).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000170.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 3.9% |
| 99214 | 14 | 1 | 7.1% | 2.5% |
| 99215 | 9 | 7 | 77.8% | 14.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (34 claims across 99215).
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
