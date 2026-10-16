# Payment Integrity dossier: 1000000072

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 244 / 122 |
| Billed mix (99211 to 99215) | 4 / 3 / 54 / 128 / 55 |
| 99215 share | 22.5% |
| Expected 99215 share given patient complexity | 3.5% |
| Screen scores | z vs peers 2.93; risk-adjusted 5.76; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000072: 7 of 9 documented 99215 claims (78%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000072 billed 99215 on 22.5% of 244 claims against an expected 3.5% given patient complexity (risk-adjusted score 5.76; plain z-score vs peers 2.93). 35% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 9 documented 99215 claims, 7 (78%) were documented below the billed level, against 0% for the comparison providers. 2 of 18 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0031979: billed 99215, patient aged 50 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0032002: billed 99215; documented MDM level moderate, minutes not recorded. C0032102: billed 99215; documented MDM level moderate, minutes not recorded. C0031910: billed 99215, patient aged 32 with 1 chronic condition(s) (hyperlipidemia). C0031925: billed 99215, patient aged 79 with 1 chronic condition(s) (hypothyroidism). C0031931: billed 99215, patient aged 70 with 1 chronic condition(s) (type 2 diabetes).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000072.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 4.7% |
| 99214 | 14 | 5 | 35.7% | 2.4% |
| 99215 | 9 | 7 | 77.8% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (31 claims across 99215).
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
