# Payment Integrity dossier: P0161

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 250 / 99 |
| Billed mix (99211 to 99215) | 4 / 1 / 46 / 122 / 77 |
| 99215 share | 30.8% |
| Expected 99215 share given patient complexity | 3.2% |
| Screen scores | z vs peers 3.89; risk-adjusted 9.00; flagged by zscore+riskadj |

## Case summary (advisory)

**P0161 (Family Practice, GA): 99215 share of 30.8% vs 3.2% expected, with 75% of documented 99215s unsupported. The pattern is consistent with upcoding.**

Leaning: pattern consistent with upcoding. Citations checked: 10/10 valid.

P0161 billed 77 of 250 claims (30.8%) as 99215. Patient complexity predicts about 3.2% (z = 3.89 vs peers; risk-adjusted score 9.0). The excess appears at every complexity level, not just among sicker patients. Patients with 0 chronic conditions get 99215 at 27.3% (12/44) vs 2.1% for all providers, and 1-condition patients at 28.9% vs 3.4%. Sampled examples include 99215s for rash (C0073067), UTI (C0073101) and a follow-up visit (C0073162) in patients with no chronic conditions. The records review points the same way. Of 16 documented 99215 claims, 12 (75%) do not support the billed level, vs 24.2% across all providers. Examples documented as moderate MDM at 30–37 minutes include C0073057, C0073105, C0073176 and C0073242. Billed 99214s are also elevated: 11/40 unsupported (27.5%) vs 8.4%, including C0073277, a URI visit in a 0-condition patient documented as low MDM. By contrast, 0/12 documented 99213s were unsupported, so the mismatch concentrates at the higher levels. Some 99215s are well supported, such as C0073230 (4 conditions, high MDM, 42 min) and C0073109 (CKD, high MDM, 45 min). So part of the high-level billing may be legitimate. Only 28% of claims have records and documentation is noisy, but the 99215 gap is large. This is a screening pattern, not a finding of fraud.

## Evidence chart

![99215 share by patient complexity](../../charts/P0161.svg)

## Records-review sample so far

Documentation is on file for 70 claims (28% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 12 | 0 | 0.0% | 7.5% |
| 99214 | 40 | 11 | 27.5% | 8.4% |
| 99215 | 16 | 12 | 75.0% | 24.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (37 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request full records for the remaining undocumented 99215 claims, prioritizing the 0–1 chronic condition visits (e.g., C0073067, C0073101, C0073162, C0073108, C0073165, C0073263) to test whether the 75% unsupported rate holds.
- Have a certified coder re-review the 12 unsupported 99215s and 11 unsupported 99214s for MDM elements and total time, checking whether billing relied on time thresholds not met by documented minutes (30–37 min).
- Check for templated or cloned notes and for after-the-fact time attestations across the provider's high-level visits.
- Review whether a billing service or EHR auto-leveling feature sets this provider's E/M levels, and compare with other clinicians in the same practice.
- Confirm diagnosis coding completeness in case undercoded comorbidities understate patient complexity, though current diagnosis codes (R21, N39.0, Z09) suggest simple problems.
- Estimate the financial impact by extrapolating the unsupported rate to all 99215 and 99214 claims, with appropriate statistical sampling before any recovery action.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
