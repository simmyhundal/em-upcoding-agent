# Payment Integrity dossier: 1000000038

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 116 |
| Billed mix (99211 to 99215) | 0 / 1 / 54 / 133 / 54 |
| 99215 share | 22.3% |
| Expected 99215 share given patient complexity | 4.2% |
| Screen scores | z vs peers 2.83; risk-adjusted 5.45; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000038: 5 of 7 documented 99215 claims (71%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000038 billed 99215 on 22.3% of 242 claims against an expected 4.2% given patient complexity (risk-adjusted score 5.45; plain z-score vs peers 2.83). 43% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 7 documented 99215 claims, 5 (71%) were documented below the billed level, against 0% for the comparison providers. 1 of 16 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0025510: billed 99215, patient aged 28 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0025523: billed 99215, patient aged 24 with 1 chronic condition(s) (obesity); documented MDM level moderate, 34 minutes. C0025589: billed 99215, patient aged 57 with 1 chronic condition(s) (type 2 diabetes); documented MDM level moderate, 38 minutes. C0025459: billed 99215, patient aged 70 with 1 chronic condition(s) (obesity). C0025492: billed 99215, patient aged 78 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000038.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 0 | 0.0% | 1.2% |
| 99214 | 13 | 3 | 23.1% | 3.1% |
| 99215 | 7 | 5 | 71.4% | 0.0% |

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
