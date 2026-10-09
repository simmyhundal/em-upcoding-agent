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

**P0088 (Family Practice, GA): elevated 99215 billing across every complexity tier, with 77% of documented 99215 claims unsupported, a pattern consistent with upcoding**

Leaning: pattern consistent with upcoding. Citations checked: 13/13 valid.

P0088 billed 99215 on 26.5% of 1,169 claims, against an expected 5.7% given patient complexity (z=3.23 vs peers; risk-adjusted score 11.3). The excess is not confined to sicker patients. The provider's 99215 share is roughly 4-5x the all-provider rate for patients with 0-2 chronic conditions (9.3% vs 2.1%, 15.8% vs 3.4%, 24.7% vs 5.6%). It narrows only in the 5+ tier (42.5% vs 29.8%). The sampled low-complexity 99215 claims include single routine or symptom codes, such as Z09 follow-up (C0044545), R10.9 alone (C0044789, C0044898), M54.50 alone (C0044781, C0045451) and E78.5 alone (C0044783, C0045332). Documentation is reasonably deep (105 documented 99215 claims). Of these, 81 (77.1%) do not support the billed level, versus 24.2% across all providers. Examples include C0044626 and C0044716, which document moderate MDM and about 31-32 minutes. The 99214 unsupported rate is also elevated (23.4% vs 8.4%), while 99213 is near peer rates (8.5% vs 7.5%). Some 99215s are well supported (e.g., C0045134, C0045303: high MDM, 40+ minutes), and some high-complexity patients plausibly warrant 99215 (e.g., C0045426, C0045587). Overall the pattern is more consistent with upcoding than with a sicker panel. This is not a finding of fraud, and the records cover only about 30% of claims.

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

- Pull full records for the sampled low-complexity 99215 claims (e.g., C0044545, C0044789, C0044898, C0045451) and verify MDM elements and total time.
- Expand documentation review on 99214 claims given the 23.4% unsupported rate, to gauge whether level inflation extends beyond 99215.
- Check whether time-based coding is being claimed for 99215 visits documented at about 30 minutes and moderate MDM.
- Compare problem-list conditions against claim diagnosis codes for high-complexity patients (e.g., C0044667 lists only I10) to confirm complexity is actually addressed at the visit.
- Review the provider's coding education and EHR templates or default level settings, and consider an extrapolated statistical sample audit.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
