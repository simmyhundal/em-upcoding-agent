# Payment Integrity dossier: 1000000088

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 115 |
| Billed mix (99211 to 99215) | 1 / 0 / 38 / 92 / 110 |
| 99215 share | 45.6% |
| Expected 99215 share given patient complexity | 8.2% |
| Screen scores | z vs peers 6.37; risk-adjusted 7.02; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000088: 11 of 26 documented 99215 claims (42%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000088 billed 99215 on 45.6% of 241 claims against an expected 8.2% given patient complexity (risk-adjusted score 7.02; plain z-score vs peers 6.37). 13% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 59 claims. Of 26 documented 99215 claims, 11 (42%) were documented below the billed level, against 12% for the comparison providers. 3 of 35 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0049856: billed 99215; documented MDM level moderate, minutes not recorded. C0049891: billed 99215; documented MDM level moderate, 38 minutes. C0049895: billed 99215, patient aged 58 with 4 chronic condition(s) (depression;hypertension;COPD;asthma); documented MDM level moderate, 37 minutes. C0049818: billed 99215, patient aged 53 with 1 chronic condition(s) (heart failure). C0049846: billed 99215, patient aged 67 with 1 chronic condition(s) (type 2 diabetes). C0049854: billed 99215, patient aged 60 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000088.svg)

## Records-review sample so far

Documentation is on file for 59 claims (24% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 0 | 0.0% | 4.4% |
| 99214 | 23 | 7 | 30.4% | 3.4% |
| 99215 | 26 | 11 | 42.3% | 12.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (43 claims across 99215).
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
