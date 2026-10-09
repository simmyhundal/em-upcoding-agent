# Payment Integrity dossier: P0064

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 250 / 99 |
| Billed mix (99211 to 99215) | 0 / 1 / 44 / 133 / 72 |
| 99215 share | 28.8% |
| Expected 99215 share given patient complexity | 3.5% |
| Screen scores | z vs peers 3.58; risk-adjusted 7.96; flagged by zscore+riskadj |

## Case summary (advisory)

**P0064 (Family Practice, GA): 99215 share of 28.8% vs ~3.5% expected for panel complexity, with 55% of documented 99215s unsupported; pattern consistent with upcoding**

Leaning: pattern consistent with upcoding. Citations checked: 12/12 valid.

P0064 billed 72 of 250 claims (28.8%) as 99215, against an expected share of about 3.5% given patient complexity (z vs peers 3.58, risk-adjusted score 7.96). The elevation appears in every complexity stratum with more than one visit, not only among sicker patients. On patients with 0 chronic conditions the 99215 share is 15.2% vs 2.1% for all providers, and with 1 condition it is 19.2% vs 3.4%. The sampled low-complexity 99215s include visits for rash (R21; C0028417, C0028627), back pain (C0028513), and single stable conditions such as hyperlipidemia (C0028397, C0028538) and obesity (C0028456). Documentation is reasonably sized (82 claims, 20 of them 99215) and points the same way. 11 of 20 documented 99215s (55%) do not support the billed level, vs 24.2% for all providers. 99214 claims also run high at 23.3% vs 8.4%. Examples C0028395 and C0028459 are 99215s on 0-condition patients with only moderate MDM and 33-34 minutes documented. Some 99215s are well supported, with high MDM and 42-51 minutes (C0028470, C0028575), and the 4-condition patients (e.g., C0028495, C0028583) are plausibly complex. This is a sampled, noisy review, so the pattern is consistent with upcoding but is not proof of it.

## Evidence chart

![99215 share by patient complexity](../../charts/P0064.svg)

## Records-review sample so far

Documentation is on file for 82 claims (33% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 19 | 1 | 5.3% | 7.5% |
| 99214 | 43 | 10 | 23.3% | 8.4% |
| 99215 | 20 | 11 | 55.0% | 24.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (36 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Expand the records request to the remaining undocumented 99215 claims, prioritizing those on 0-1 condition patients (e.g., C0028417, C0028627, C0028531, C0028577).
- Have a certified coder re-audit the 11 unsupported 99215s and 10 unsupported 99214s to confirm the MDM/time scoring.
- Check whether time-based billing (prolonged counseling, care coordination) is documented on low-complexity 99215s such as repeat visits for patient P0064-N0038 and P0064-N0061.
- Review the 99214 pattern separately, since its unsupported rate (23.3%) is also well above peers.
- Compare against peer Family Practice providers in GA and check for templated or cloned notes across visits.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
