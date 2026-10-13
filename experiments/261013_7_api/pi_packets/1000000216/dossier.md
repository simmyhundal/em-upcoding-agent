# Payment Integrity dossier: 1000000216

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 783 / 393 |
| Billed mix (99211 to 99215) | 8 / 5 / 268 / 406 / 96 |
| 99215 share | 12.3% |
| Expected 99215 share given patient complexity | 2.5% |
| Screen scores | z vs peers 1.44; risk-adjusted 8.17; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000216's 99215 billing runs well above what patient complexity predicts and is concentrated on low-complexity patients, but no 99215 charts were returned to test it.**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000216 billed 99215 on 12.3% of 783 claims against an expected 2.5% given patient complexity (risk-adjusted score 8.17; plain z-score vs peers 1.44). 53% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 21 claims. No documented 99215 claims came back. 1 of 14 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The claims pattern leans toward upcoding. Over half of the 99215s fall on patients with zero or one chronic condition. The sampled low-complexity 99215s include visits coded only to follow-up (Z09), back pain (M54.50), abdominal pain (R10.9) or upper respiratory infection (J06.9), for example C0108539, C0108444, C0108449 and C0108682. The 99215 share is also elevated in every complexity band, not just among the sickest patients, which argues against a simply sicker panel. Even so, the high-complexity sample (such as C0108280 and C0108850) shows that some 99215s are plausibly justified. The modest peer z-score and the documentation leave the question open: no 99215 charts came back, and the 21 documented lower-level claims, including the single below-billed 99213 (C0108639), are too thin to judge either way. A reviewer should first request records specifically for the low-complexity 99215 claims listed in the packet and check whether the documented MDM and time support level 5. The note for the one moderate-or-higher data-reviewed claim that has no lab or test line also deserves a look for cloned or inflated content. Examples: C0108639: billed 99213; documented MDM level straightforward, minutes not recorded. C0108353: billed 99215, patient aged 54 with 1 chronic condition(s) (hypertension). C0108373: billed 99215, patient aged 32 with 1 chronic condition(s) (asthma). C0108385: billed 99215, patient aged 40 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000216.svg)

## Records-review sample so far

Documentation is on file for 21 claims (3% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 1 | 14.3% | 4.7% |
| 99214 | 14 | 0 | 0.0% | 3.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (40 claims across 99215).
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
