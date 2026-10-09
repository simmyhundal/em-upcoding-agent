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

**Family Practice provider P0161: 30.8% 99215 share (vs 3.2% expected) concentrated on low-complexity patients, with 75% of documented 99215 claims unsupported**

Leaning: pattern consistent with upcoding. Citations checked: 13/13 valid.

P0161 billed 99215 on 30.8% of 250 claims against an expected 3.2% given patient complexity (z = 3.89, risk-adjusted score 9.0). The elevation is not explained by acuity: 99215 share is 27.3% for patients with 0 chronic conditions and 28.9% with 1 condition (vs 2.1% and 3.4% for all providers), and sampled low-complexity 99215 claims include routine-appearing presentations such as rash (C0073067, C0073103), UTI (C0073101, C0073108), abdominal pain (C0073075), and follow-up (C0073162). The records review points the same way: 12 of 16 documented 99215 claims (75%) did not support the billed level, roughly three times the 24.2% all-provider rate, with examples documenting only moderate MDM at 30-37 minutes (C0073057, C0073105, C0073176, C0073242). 99214 also shows 27.5% unsupported (11 of 40) vs 8.4%, for example C0073277 on a 0-condition patient with low MDM. Some 99215s are supported by high-MDM documentation (C0073109, C0073230), and the documented 99215 sample is small (16 claims), so this is a pattern consistent with upcoding rather than a finding of fraud.

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

- Pull full medical records for the remaining 61 undocumented 99215 claims, prioritizing 0-1 condition patients (e.g., C0073067, C0073101, C0073075, C0073162), and score MDM/time against 2021 E/M guidelines.
- Expand documentation review of 99214 claims given the 27.5% unsupported rate, to assess whether level inflation is systematic across levels.
- Check whether documented minutes on 99215 claims meet the 40-minute time threshold and whether time statements are templated or cloned.
- Review the 4 supported 99215 examples to confirm high MDM is genuine and not boilerplate.
- Compare the provider's diagnosis coding and problem lists to claims history to verify chronic condition counts are not understated or overstated.
- Consider a statistically valid random sample for extrapolation before any overpayment determination.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
