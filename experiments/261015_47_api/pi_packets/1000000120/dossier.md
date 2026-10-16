# Payment Integrity dossier: 1000000120

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 236 / 118 |
| Billed mix (99211 to 99215) | 2 / 1 / 53 / 116 / 64 |
| 99215 share | 27.1% |
| Expected 99215 share given patient complexity | 2.4% |
| Screen scores | z vs peers 4.25; risk-adjusted 8.80; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000120: 8 of 11 documented 99215 claims (73%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000120 billed 99215 on 27.1% of 236 claims against an expected 2.4% given patient complexity (risk-adjusted score 8.80; plain z-score vs peers 4.25). 61% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 11 documented 99215 claims, 8 (73%) were documented below the billed level, against 8% for the comparison providers. 2 of 18 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0054193: billed 99215; documented MDM level moderate, 37 minutes. C0054211: billed 99215, patient aged 30 with 1 chronic condition(s) (heart failure); documented MDM level moderate, 33 minutes. C0054263: billed 99215, patient aged 42 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0054136: billed 99215, patient aged 44 with 1 chronic condition(s) (heart failure). C0054141: billed 99215, patient aged 62 with 0 chronic condition(s). C0054144: billed 99215, patient aged 37 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000120.svg)

## Records-review sample so far

Documentation is on file for 30 claims (13% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 2.8% |
| 99214 | 15 | 1 | 6.7% | 1.7% |
| 99215 | 11 | 8 | 72.7% | 7.7% |

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
