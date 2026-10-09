# Payment Integrity dossier: P0088

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,169 / 451 |
| Billed mix (99211 to 99215) | 8 / 8 / 229 / 614 / 310 |
| 99215 share | 26.5% |
| Expected 99215 share given patient complexity | 5.7% |
| Screen scores | z vs peers 3.23; risk-adjusted 11.30; flagged by zscore+riskadj |

## Case summary (advisory)

**P0088 (Family Practice, GA): 99215 billing well above complexity-adjusted expectation, and 77% of documented 99215 claims are unsupported**

Leaning: pattern consistent with upcoding. Citations checked: 9/9 valid.

P0088 billed 99215 on 26.5% of 1,169 claims, against an expected 5.7% given patient complexity (z = 3.23 vs peers, risk-adjusted score 11.3). The excess shows up in every complexity stratum. It is largest in relative terms on low-complexity patients: 9.3% vs 2.1% all-provider for 0 conditions, and 15.8% vs 3.4% for 1 condition. Sampled 99215 claims on low-complexity patients include single-condition or symptom-only visits, such as C0044545 (Z09 follow-up only), C0044781 (back pain only) and C0045414 (hypertension only, age 20). The documentation review is substantial (355 claims, 105 of them billed 99215), and 81 of those 105 (77.1%) had documentation below the billed level, against a 24.2% all-provider rate. Examples include C0044626 and C0044716, both documented at moderate MDM and about 31-32 minutes. 99214 is also elevated (23.4% unsupported vs 8.4%), while 99213 is near the norm (8.5% vs 7.5%). Some 99215s on multimorbid patients look plausible (C0045426, C0045587), and some are well documented (C0045134, C0045303). However, the overall pattern is consistent with upcoding to 99215, and to a lesser extent 99214, rather than with a sicker panel. This is not a finding of fraud. Records cover about 30% of claims, and the claim lists are random samples.

## Evidence chart

![99215 share by patient complexity](../../charts/P0088.svg)

## Records-review sample so far

Documentation is on file for 355 claims (30% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 71 | 6 | 8.5% | 7.5% |
| 99214 | 175 | 41 | 23.4% | 8.4% |
| 99215 | 105 | 81 | 77.1% | 24.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (56 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Pull full records for the sampled low-complexity 99215 claims (e.g., C0044545, C0044781, C0045414) and check whether MDM or total time supports level 5.
- Expand the documentation review across 99215 and 99214 claims to confirm the unsupported rates and estimate the dollar impact.
- Compare time-based billing claims against documented minutes, since unsupported examples show about 31-32 minutes on 99215 claims.
- Check whether a template, EHR default or coding vendor is driving level selection, and interview the provider and billing staff.
- Consider prepayment review or a statistically valid extrapolation sample if the expanded review confirms the pattern.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
