# Payment Integrity dossier: 1000000589

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 837 / 421 |
| Billed mix (99211 to 99215) | 10 / 6 / 206 / 456 / 159 |
| 99215 share | 19.0% |
| Expected 99215 share given patient complexity | 2.1% |
| Screen scores | z vs peers 2.73; risk-adjusted 12.51; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000589: 6 of 13 documented 99214 and 99215 claims (46%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000589 billed 99215 on 19.0% of 837 claims against an expected 2.1% given patient complexity (risk-adjusted score 12.51; plain z-score vs peers 2.73). 58% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 19 claims. Of 5 documented 99215 claims, 3 (60%) were documented below the billed level, against 9% for the comparison providers. 0 of 12 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0326362: billed 99215; documented MDM level moderate, minutes not recorded. C0326409: billed 99215; documented MDM level moderate, minutes not recorded. C0326941: billed 99215; documented MDM level moderate, 35 minutes. C0326287: billed 99215, patient aged 51 with 1 chronic condition(s) (asthma). C0326325: billed 99215, patient aged 38 with 0 chronic condition(s). C0326346: billed 99215, patient aged 44 with 1 chronic condition(s) (depression).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000589.svg)

## Records-review sample so far

Documentation is on file for 19 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 4.3% |
| 99214 | 8 | 3 | 37.5% | 3.5% |
| 99215 | 5 | 3 | 60.0% | 9.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (48 claims across 99215).
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
