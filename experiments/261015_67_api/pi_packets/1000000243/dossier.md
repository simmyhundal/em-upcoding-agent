# Payment Integrity dossier: 1000000243

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 114 |
| Billed mix (99211 to 99215) | 0 / 0 / 58 / 116 / 67 |
| 99215 share | 27.8% |
| Expected 99215 share given patient complexity | 2.6% |
| Screen scores | z vs peers 4.34; risk-adjusted 9.64; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000243: 6 of 6 documented 99215 claims (100%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000243 billed 99215 on 27.8% of 241 claims against an expected 2.6% given patient complexity (risk-adjusted score 9.64; plain z-score vs peers 4.34). 45% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 6 documented 99215 claims, 6 (100%) were documented below the billed level, against 9% for the comparison providers. 2 of 14 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0136916: billed 99215; documented MDM level moderate, 39 minutes. C0136980: billed 99215, patient aged 30 with 0 chronic condition(s); documented MDM level moderate, 39 minutes. C0137047: billed 99215; documented MDM level moderate, minutes not recorded. C0136889: billed 99215, patient aged 45 with 0 chronic condition(s). C0136895: billed 99215, patient aged 19 with 0 chronic condition(s). C0136919: billed 99215, patient aged 44 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000243.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 3.0% |
| 99214 | 17 | 6 | 35.3% | 3.3% |
| 99215 | 6 | 6 | 100.0% | 8.7% |

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
