# Payment Integrity dossier: 1000000002

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 118 |
| Billed mix (99211 to 99215) | 2 / 2 / 58 / 138 / 42 |
| 99215 share | 17.4% |
| Expected 99215 share given patient complexity | 2.2% |
| Screen scores | z vs peers 1.91; risk-adjusted 5.21; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000002: 3 of 4 documented 99215 claims (75%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000002 billed 99215 on 17.4% of 242 claims against an expected 2.2% given patient complexity (risk-adjusted score 5.21; plain z-score vs peers 1.91). 60% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 17 claims. Of 4 documented 99215 claims, 3 (75%) were documented below the billed level, against 14% for the comparison providers. 0 of 6 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0000417: billed 99215; documented MDM level moderate, minutes not recorded. C0000484: billed 99215, patient aged 71 with 1 chronic condition(s) (depression); documented MDM level moderate, 33 minutes. C0000608: billed 99215; documented MDM level moderate, 35 minutes. C0000401: billed 99215, patient aged 57 with 1 chronic condition(s) (depression). C0000409: billed 99215, patient aged 80 with 1 chronic condition(s) (atrial fibrillation). C0000440: billed 99215, patient aged 71 with 1 chronic condition(s) (depression).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000002.svg)

## Records-review sample so far

Documentation is on file for 17 claims (7% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 1 | 25.0% | 2.8% |
| 99214 | 8 | 5 | 62.5% | 1.7% |
| 99215 | 4 | 3 | 75.0% | 13.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (27 claims across 99215).
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
