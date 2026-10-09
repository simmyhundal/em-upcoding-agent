# Payment Integrity dossier: P0143

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 343 / 132 |
| Billed mix (99211 to 99215) | 0 / 5 / 46 / 196 / 96 |
| 99215 share | 28.0% |
| Expected 99215 share given patient complexity | 2.1% |
| Screen scores | z vs peers 3.45; risk-adjusted 12.02; flagged by zscore+riskadj |

## Case summary (advisory)

**P0143 (Family Practice, GA): 99215 billed on 28% of claims, mostly on low-complexity patients, and the records reviewed do not support 99215 on 86% of those claims. This pattern is consistent with upcoding.**

Leaning: pattern consistent with upcoding. Citations checked: 8/8 valid.

P0143 billed 99215 on 96 of 343 claims (28.0%). Given this panel's patient complexity, the expected share is 2.1% (z = 3.45 vs peers; risk-adjusted score 12.0). The panel is mostly low-complexity: 263 of 343 visits are for patients with 0 or 1 chronic conditions. Yet 99215 was billed on 25.0% of 0-condition visits (all providers: 2.1%) and 23.4% of 1-condition visits (all providers: 3.4%). Sampled examples include 99215 claims for routine single-problem diagnoses such as J06.9 (C0066276), M54.50 (C0066431), N39.0 (C0066376) and Z09 (C0066566). The records review is strong enough to judge: 35 billed 99215 claims were documented, and in 30 of them (85.7%) the documentation did not support the billed level, against an all-provider rate of 24.2%. Records for C0066376, C0066431, C0066306 and C0066504 show moderate MDM at 32 to 38 minutes. 99214 claims are also unsupported at an elevated rate (20.4% vs 8.4%). Some 99215s are supported (for example C0066612 and C0066425, both high MDM). Taken together, this pattern is consistent with systematic upcoding, not a sicker panel. This is not a finding of fraud. Only 29% of claims have records, and the claim lists are random samples.

## Evidence chart

![99215 share by patient complexity](../../charts/P0143.svg)

## Records-review sample so far

Documentation is on file for 100 claims (29% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 0 | 0.0% | 7.5% |
| 99214 | 54 | 11 | 20.4% | 8.4% |
| 99215 | 35 | 30 | 85.7% | 24.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (40 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Pull the full records for the 30 documented 99215 claims that were not supported, and confirm the MDM and time findings with a certified coder.
- Expand records review to the undocumented 99215 claims, starting with 0- and 1-condition patients billed for routine diagnoses (J06.9, M54.50, N39.0, R21, Z09).
- Review the 11 unsupported 99214 claims (e.g. C0066383) to see whether upcoding also reaches level 4.
- Check whether billed time on 99215 claims meets the 40-minute threshold, or whether the claims rely on MDM that was not documented.
- Look for templated or cloned notes and any recent change in billing software or coding staff.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
