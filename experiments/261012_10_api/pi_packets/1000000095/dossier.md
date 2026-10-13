# Payment Integrity dossier: 1000000095

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 945 / 452 |
| Billed mix (99211 to 99215) | 10 / 4 / 189 / 572 / 170 |
| 99215 share | 18.0% |
| Expected 99215 share given patient complexity | 2.5% |
| Screen scores | z vs peers 2.01; risk-adjusted 9.99; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000095: 2 of 4 documented 99215 claims (50%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000095 billed 99215 on 18.0% of 945 claims against an expected 2.5% given patient complexity (risk-adjusted score 9.99; plain z-score vs peers 2.01). 56% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 20 claims. Of 4 documented 99215 claims, 2 (50%) were documented below the billed level, against 14% for the comparison providers. 1 of 12 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0058794: billed 99215; documented MDM level moderate, 34 minutes. C0059199: billed 99215; documented MDM level moderate, 35 minutes. C0058463: billed 99215, patient aged 60 with 0 chronic condition(s). C0058464: billed 99215, patient aged 39 with 0 chronic condition(s). C0058472: billed 99215, patient aged 18 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000095.svg)

## Records-review sample so far

Documentation is on file for 20 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 2.8% |
| 99214 | 11 | 3 | 27.3% | 1.7% |
| 99215 | 4 | 2 | 50.0% | 13.6% |

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
