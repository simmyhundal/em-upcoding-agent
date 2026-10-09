# Payment Integrity dossier: P0215

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,500 / 985 |
| Billed mix (99211 to 99215) | 14 / 9 / 386 / 1,274 / 817 |
| 99215 share | 32.7% |
| Expected 99215 share given patient complexity | 5.2% |
| Screen scores | z vs peers 4.18; risk-adjusted 22.69; flagged by zscore+riskadj |

## Case summary (advisory)

**P0215 (Family Practice, GA): 99215 share of 32.7% vs 5.2% expected, elevated in every complexity stratum, with 59.8% of documented 99215s unsupported; pattern consistent with upcoding**

Leaning: pattern consistent with upcoding. Citations checked: 13/13 valid.

P0215 billed 817 of 2,500 claims as 99215 (32.7%), against 5.2% expected given patient complexity (z vs peers 4.18, risk-adjusted score 22.7). The excess is not explained by a sicker panel. The 99215 share is far above all-provider rates even for patients with 0 chronic conditions (18.0% vs 2.1%) and 1 condition (25.4% vs 3.4%). Sampled 99215s on low-complexity patients include visits coded only for rash (R21: C0098128, C0098191, C0098499), upper respiratory infection (J06.9: C0098773, C0099737, C0099825) and UTI (N39.0: C0098522). The documentation review is reasonably sized at 234 documented 99215 claims. Of these, 59.8% did not support the billed level, versus 24.2% for all providers (e.g., C0098676 and C0098775 documented moderate MDM at about 30 minutes). Documented 99214s were also unsupported at 19.0% vs 8.4%. Some 99215s are well supported, such as C0098276 and C0098923 (high MDM, 42–47 minutes), and the 4+ condition sample (e.g., C0098431, C0099387) is plausibly complex. Taken together, the pattern is consistent with systematic upcoding rather than a high-acuity panel. This is not a finding of fraud. Records cover only 29.5% of claims, and the claim lists are random samples.

## Evidence chart

![99215 share by patient complexity](../../charts/P0215.svg)

## Records-review sample so far

Documentation is on file for 737 claims (30% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 119 | 10 | 8.4% | 7.5% |
| 99214 | 379 | 72 | 19.0% | 8.4% |
| 99215 | 234 | 140 | 59.8% | 24.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (63 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request full medical records for the sampled low-complexity 99215 claims, especially the R21, J06.9 and N39.0 visits, and check whether MDM or total time meets 99215 criteria.
- Check whether the unsupported 99215s cluster among 0–1 condition patients versus 4+ condition patients, to separate upcoding from a complex subpanel.
- Extend the review to 99214s, given the 19.0% unsupported rate (about 2.3x peers).
- Look for templated or cloned notes, and for time documentation that is inconsistent with MDM, across the unsupported claims.
- Consider a statistically valid probe sample of 99215 claims for extrapolation and possible provider education or prepayment review.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
