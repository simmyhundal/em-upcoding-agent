# Payment Integrity dossier: 1000000067

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 490 / 246 |
| Billed mix (99211 to 99215) | 3 / 1 / 132 / 275 / 79 |
| 99215 share | 16.1% |
| Expected 99215 share given patient complexity | 2.3% |
| Screen scores | z vs peers 2.03; risk-adjusted 7.53; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000067: 5 of 20 documented 99214 and 99215 claims (25%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000067 billed 99215 on 16.1% of 490 claims against an expected 2.3% given patient complexity (risk-adjusted score 7.53; plain z-score vs peers 2.03). 59% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 4 documented 99215 claims, 3 (75%) were documented below the billed level, against 14% for the comparison providers. 1 of 16 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0035079: billed 99215; documented MDM level moderate, 37 minutes. C0035267: billed 99215; documented MDM level moderate, minutes not recorded. C0035419: billed 99215, patient aged 55 with 0 chronic condition(s); documented MDM level moderate, 30 minutes. C0035056: billed 99215, patient aged 41 with 1 chronic condition(s) (hypertension). C0035074: billed 99215, patient aged 30 with 1 chronic condition(s) (hypothyroidism). C0035083: billed 99215, patient aged 65 with 1 chronic condition(s) (chronic kidney disease).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000067.svg)

## Records-review sample so far

Documentation is on file for 30 claims (6% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 0 | 0.0% | 2.7% |
| 99214 | 16 | 2 | 12.5% | 4.2% |
| 99215 | 4 | 3 | 75.0% | 14.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (37 claims across 99215).
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
