# Payment Integrity dossier: 1000000074

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 238 / 112 |
| Billed mix (99211 to 99215) | 0 / 1 / 38 / 150 / 49 |
| 99215 share | 20.6% |
| Expected 99215 share given patient complexity | 5.0% |
| Screen scores | z vs peers 3.04; risk-adjusted 5.30; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000074: 6 of 23 documented 99214 and 99215 claims (26%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000074 billed 99215 on 20.6% of 238 claims against an expected 5.0% given patient complexity (risk-adjusted score 5.30; plain z-score vs peers 3.04). 20% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 4 documented 99215 claims, 3 (75%) were documented below the billed level, against 0% for the comparison providers. 2 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0043082: billed 99215; documented MDM level moderate, 36 minutes. C0043089: billed 99215, patient aged 49 with 1 chronic condition(s) (hypertension); documented MDM level moderate, 31 minutes. C0043228: billed 99215, patient aged 48 with 1 chronic condition(s) (hyperlipidemia); documented MDM level moderate, 37 minutes. C0043032: billed 99215, patient aged 21 with 1 chronic condition(s) (atrial fibrillation). C0043040: billed 99215, patient aged 18 with 1 chronic condition(s) (heart failure). C0043043: billed 99215, patient aged 46 with 1 chronic condition(s) (asthma); documented MDM level high, 52 minutes.

## Evidence chart

![99215 share by patient complexity](../../charts/1000000074.svg)

## Records-review sample so far

Documentation is on file for 30 claims (13% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 4.7% |
| 99214 | 19 | 3 | 15.8% | 3.7% |
| 99215 | 4 | 3 | 75.0% | 0.0% |

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
