# Payment Integrity dossier: 1000000159

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,401 / 1,179 |
| Billed mix (99211 to 99215) | 34 / 22 / 837 / 1,156 / 352 |
| 99215 share | 14.7% |
| Expected 99215 share given patient complexity | 2.2% |
| Screen scores | z vs peers 1.85; risk-adjusted 14.88; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000159: 4 of 4 documented 99215 claims (100%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000159 billed 99215 on 14.7% of 2,401 claims against an expected 2.2% given patient complexity (risk-adjusted score 14.88; plain z-score vs peers 1.85). 62% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 21 claims. Of 4 documented 99215 claims, 4 (100%) were documented below the billed level, against 0% for the comparison providers. 0 of 11 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0077537: billed 99215; documented MDM level moderate, minutes not recorded. C0077615: billed 99215; documented MDM level moderate, minutes not recorded. C0078072: billed 99215; documented MDM level moderate, 32 minutes. C0076733: billed 99215, patient aged 44 with 1 chronic condition(s) (asthma). C0076753: billed 99215, patient aged 38 with 1 chronic condition(s) (type 2 diabetes). C0076793: billed 99215, patient aged 49 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000159.svg)

## Records-review sample so far

Documentation is on file for 21 claims (1% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 0 | 0.0% | 3.1% |
| 99214 | 9 | 1 | 11.1% | 4.8% |
| 99215 | 4 | 4 | 100.0% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (57 claims across 99215).
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
