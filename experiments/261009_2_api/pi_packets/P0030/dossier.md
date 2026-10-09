# Payment Integrity dossier: P0030

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,293 / 903 |
| Billed mix (99211 to 99215) | 14 / 20 / 683 / 1,214 / 362 |
| 99215 share | 15.8% |
| Expected 99215 share given patient complexity | 1.9% |
| Screen scores | z vs peers 1.64; risk-adjusted 18.32; flagged by zscore+riskadj |

## Case summary (advisory)

**P0030 (Family Practice, GA): 99215 share of 15.8% vs 1.95% expected for its patient mix, with 78% of documented 99215 claims unsupported by the records**

Leaning: pattern consistent with upcoding. Citations checked: 11/11 valid.

P0030 billed 99215 on 15.8% of 2,293 claims. The expected share given its patients' complexity is 1.95%. Most visits are on low-complexity patients: 913 visits with 0 chronic conditions and 922 with 1. On those visits the 99215 share is 13.1% and 15.8%, against 2.6% and 3.3% for all providers. Sampled examples include 99215s for a 0-condition patient with upper respiratory infection (C0014756, C0013547), rash (C0013428, C0013990), back pain (C0014662) and follow-up visits (C0013852, C0014826). The records review is substantial: 115 documented 99215 claims. Of these, 90 (78.3%) were not supported by the documentation, versus 26.9% for all providers. Examples include C0013063 (low MDM, 26 min) and C0013300 (moderate MDM, 38 min). 99214 is also elevated, at 25.9% unsupported vs 8.0% for all providers (e.g., C0013925, straightforward MDM, 14 min). Some 99215s do appear legitimate, such as C0013554, a 4-condition patient with high MDM and 42 min. Taken together, the pattern is consistent with upcoding rather than a sicker panel. This is not a fraud finding, and the claim lists are random samples.

## Evidence chart

![99215 share by patient complexity](../../charts/P0030.svg)

## Records-review sample so far

Documentation is on file for 692 claims (30% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 191 | 16 | 8.4% | 7.1% |
| 99214 | 378 | 98 | 25.9% | 8.0% |
| 99215 | 115 | 90 | 78.3% | 26.9% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (58 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Pull full medical records for the sampled low-complexity 99215 claims (e.g., C0014756, C0013428, C0013852) and score MDM and time independently.
- Have a certified coder re-review a fresh random sample of documented 99215 and 99214 claims to confirm the 78% and 26% unsupported rates.
- Check whether the documentation uses templated or cloned notes, or time attestations that don't match the visit content.
- Review payment trends over 2024 and compare against prior years to see when the shift toward 99214 and 99215 began.
- Consider provider education or a prepayment review for 99215, and estimate the overpayment from the unsupported rates if confirmed.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
