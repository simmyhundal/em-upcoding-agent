# Payment Integrity dossier: P0095

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,015 / 394 |
| Billed mix (99211 to 99215) | 17 / 19 / 406 / 476 / 97 |
| 99215 share | 9.6% |
| Expected 99215 share given patient complexity | 2.3% |
| Screen scores | z vs peers 0.62; risk-adjusted 5.51; flagged by riskadj |

## Case summary (advisory)

**P0095 (Family Practice, GA): 99215 billing is concentrated on low-complexity patients, and 25 of 27 documented 99215 claims are not supported, a pattern consistent with upcoding**

Leaning: pattern consistent with upcoding. Citations checked: 10/10 valid.

P0095 billed 99215 on 9.6% of 1,015 claims. Given this panel's patient complexity, about 2.3% would be expected (risk-adjusted score 5.51). The raw z vs peers is modest (0.62), so it is the risk adjustment that drives the flag. The excess is on simpler patients. The 99215 share is 6.8% vs 2.1% for all providers on patients with 0 chronic conditions and 11.3% vs 3.4% on patients with 1. On patients with 4+ conditions it is at or below the all-provider rate. Sampled 99215 claims on low-complexity patients include routine diagnoses such as upper respiratory infection (C0048602, C0048948, C0048998) and low back pain (C0048381). Documentation, available for 30% of claims, points the same way. 25 of 27 documented 99215 claims (92.6%) do not support the billed level, against an all-provider rate of 24.2%. Examples are C0048719 and C0049258, each billed 99215 with moderate MDM and about 35 minutes documented. 99214 is also elevated at 22.1% unsupported vs 8.4%, e.g. C0048956 and C0049119 with low MDM documented. A few 99215 claims are supported (C0048506, C0049159), but they are the exception. Only 27 99215 claims have records, and the claim lists are samples, so the full extent is not established. This is a pattern consistent with upcoding, not a finding of fraud.

## Evidence chart

![99215 share by patient complexity](../../charts/P0095.svg)

## Records-review sample so far

Documentation is on file for 303 claims (30% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 132 | 13 | 9.8% | 7.5% |
| 99214 | 131 | 29 | 22.1% | 8.4% |
| 99215 | 27 | 25 | 92.6% | 24.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (41 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request full medical records for a larger random sample of 99215 and 99214 claims, focused on patients with 0-1 chronic conditions, to confirm the unsupported rate.
- Have a certified coder re-score MDM and time on the 25 unsupported 99215 claims to estimate the overpayment from billing 99215 instead of 99214 or 99213.
- Check whether the unsupported claims cluster by date, rendering clinician, or billing staff, and whether templates or EHR auto-coding inflate the level.
- Review the provider's time-based billing practices, since documented minutes on the sampled unsupported 99215 claims (about 35-36) fall below the 99215 time threshold.
- Consider provider education or prepayment review for 99215/99214, depending on how the expanded sample comes out.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
