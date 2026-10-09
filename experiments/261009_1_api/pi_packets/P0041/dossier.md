# Payment Integrity dossier: P0041

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 250 / 100 |
| Billed mix (99211 to 99215) | 1 / 3 / 48 / 146 / 52 |
| 99215 share | 20.8% |
| Expected 99215 share given patient complexity | 2.5% |
| Screen scores | z vs peers 2.35; risk-adjusted 6.73; flagged by zscore+riskadj |

## Case summary (advisory)

**P0041 (Family Practice, GA): 99215 share of 20.8% vs 2.5% expected for this panel's complexity, concentrated on low-complexity patients, with 11 of 16 documented 99215s unsupported. The pattern is consistent with upcoding.**

Leaning: pattern consistent with upcoding. Citations checked: 11/11 valid.

Panel complexity does not explain the 99215 rate. P0041 billed 52 of 250 claims as 99215 (20.8%), while the expected share given patient complexity is 2.5%. Most visits are on patients with 0-1 chronic conditions (177 of 250), and 36 of the 99215s fall there: 16.3% vs 2.1% all-provider for 0 conditions, and 24.7% vs 3.4% for 1 condition. The sampled low-complexity 99215s carry routine diagnoses such as Z09, R21, M54.50, N39.0 and R10.9 (e.g., C0020325, C0020335, C0020364, C0020384). Only a few 99215s involve truly complex patients (e.g., C0020426 and C0020473 for a 96-year-old with 6 conditions). The records review points the same way. Among the 16 documented 99215s, 11 were unsupported (68.8% vs 24.2% all-provider). Examples include C0020348, C0020410 and C0020438, each documented as moderate MDM at about 36-37 minutes, and C0020436, documented as low MDM at 28 minutes. Among the 41 documented 99214s, 6 were unsupported (14.6% vs 8.4%). Some 99215s are supported, such as C0020443, a 0-condition UTI visit documented as high MDM at 46 minutes, and documentation is noisy. Still, 16 documented 99215s is a modest but meaningful sample, and the gap from peers is large. Only 28% of claims have records, so this is not a determination of fraud.

## Evidence chart

![99215 share by patient complexity](../../charts/P0041.svg)

## Records-review sample so far

Documentation is on file for 70 claims (28% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 12 | 0 | 0.0% | 7.5% |
| 99214 | 41 | 6 | 14.6% | 8.4% |
| 99215 | 16 | 11 | 68.8% | 24.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (30 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Expand the records review to the remaining undocumented 99215 claims, prioritizing 0-1 condition patients with routine diagnoses (e.g., C0020339, C0020404, C0020497, C0020515).
- Check whether documented time or MDM elements, such as data reviewed, prescription drug management or comorbidity risk, could justify 99215 on low-complexity visits like C0020443.
- Review the 99214 claims flagged unsupported (e.g., C0020338, C0020369, C0020379, C0020459) to assess whether level inflation extends beyond 99215.
- Check for templated or cloned notes and copy-forward time entries in the 99215 documentation, given the recurring 36-37 minute pattern.
- Consider provider education or an extrapolated audit sample, depending on the findings of the expanded review.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
