# Payment Integrity dossier: 1000000064

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 236 / 122 |
| Billed mix (99211 to 99215) | 4 / 0 / 67 / 125 / 40 |
| 99215 share | 16.9% |
| Expected 99215 share given patient complexity | 2.9% |
| Screen scores | z vs peers 2.29; risk-adjusted 5.91; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000064 bills 99215 well above its risk-adjusted expectation, with nearly half of those claims on patients with few or no chronic conditions, but the records returned are too thin to confirm or refute the billing pattern.**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000064 billed 99215 on 16.9% of 236 claims against an expected 2.9% given patient complexity (risk-adjusted score 5.91; plain z-score vs peers 2.29). 48% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 21 claims. Of 1 documented 99215 claims, 0 (0%) were documented below the billed level, against 0% for the comparison providers. 1 of 9 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The excess 99215 share holds after risk adjustment and appears in every complexity stratum, including patients with zero or one condition. The sampled low-complexity 99215 claims carry simple diagnoses such as upper respiratory infection (C0031862, C0031885), rash (C0031824), low back pain (C0031936) and follow-up codes (C0031929, C0031931), which is the more concerning part of the pattern than a sicker panel would explain. The documentation cannot settle this: only one 99215 claim has records, and it is C0031775, a four-condition patient whose note supports high MDM, so it says nothing about the low-complexity claims. The lower levels look largely supported, with one 99214 documented below billed (C0031854) and one moderate-plus data-reviewed note lacking a lab line, which is weak evidence at most. A reviewer should first request charts for the low-complexity 99215 claims listed above and check whether their MDM and time support level 5, and watch for cloned or templated notes. Examples: C0031854: billed 99214; documented MDM level low, minutes not recorded. C0031708: billed 99215, patient aged 41 with 1 chronic condition(s) (atrial fibrillation). C0031709: billed 99215, patient aged 51 with 0 chronic condition(s). C0031728: billed 99215, patient aged 18 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000064.svg)

## Records-review sample so far

Documentation is on file for 21 claims (9% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 0 | 0.0% | 2.2% |
| 99214 | 11 | 1 | 9.1% | 3.4% |
| 99215 | 1 | 0 | 0.0% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (26 claims across 99215).
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
