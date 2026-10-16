# Payment Integrity dossier: 1000000114

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 690 / 330 |
| Billed mix (99211 to 99215) | 6 / 4 / 159 / 346 / 175 |
| 99215 share | 25.4% |
| Expected 99215 share given patient complexity | 2.6% |
| Screen scores | z vs peers 3.45; risk-adjusted 16.75; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000114: 5 of 8 documented 99215 claims (62%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000114 billed 99215 on 25.4% of 690 claims against an expected 2.6% given patient complexity (risk-adjusted score 16.75; plain z-score vs peers 3.45). 58% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 8 documented 99215 claims, 5 (62%) were documented below the billed level, against 17% for the comparison providers. 1 of 17 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0057808: billed 99215, patient aged 46 with 4 chronic condition(s) (type 2 diabetes;obesity;hypertension;asthma); documented MDM level moderate, 35 minutes. C0057937: billed 99215; documented MDM level moderate, minutes not recorded. C0057965: billed 99215, patient aged 53 with 1 chronic condition(s) (asthma); documented MDM level moderate, 30 minutes. C0057714: billed 99215, patient aged 26 with 0 chronic condition(s). C0057722: billed 99215, patient aged 39 with 1 chronic condition(s) (hyperlipidemia). C0057734: billed 99215, patient aged 36 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000114.svg)

## Records-review sample so far

Documentation is on file for 30 claims (4% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 6.2% |
| 99214 | 18 | 5 | 27.8% | 2.6% |
| 99215 | 8 | 5 | 62.5% | 17.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (49 claims across 99215).
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
