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

**P0143 (Family Practice, GA): 28% 99215 share on a mostly low-complexity panel, and 30 of 35 documented 99215 claims are unsupported. The pattern is consistent with upcoding.**

Leaning: pattern consistent with upcoding. Citations checked: 10/10 valid.

P0143 billed 96 of 343 claims (28.0%) as 99215. The expected share given patient complexity is about 2.1% (z vs peers 3.45, risk-adjusted score 12.0). The panel is not sicker than average: 263 of 343 visits are for patients with 0-1 chronic conditions, and only 6 visits are for patients with 4+ conditions. On patients with no chronic conditions, the provider's 99215 share is 25%, against 2.1% for all providers. Sampled 99215 claims on low-complexity patients include routine-looking diagnoses: upper respiratory infection (J06.9; C0066276, C0066590), low back pain (M54.50; C0066395, C0066604), rash (R21; C0066483) and UTI (N39.0; C0066558). Documentation strengthens the concern. Of 35 documented 99215 claims, 30 (85.7%) were not supported by the documented level, against 24.2% for all providers. Examples include C0066376 and C0066431, both documented as moderate MDM at 32-34 minutes. The 99214 unsupported rate is also elevated (20.4% vs 8.4%; e.g., C0066383, documented as low MDM at 20 minutes). A few 99215 claims are supported, such as C0066612 (high MDM, 41 minutes) for a heart-failure patient. Limitations: documentation covers only 29% of claims, the claim lists are samples, and documentation is noisy. Even so, the gap is large. This is a pattern for review, not a finding of fraud.

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

- Request full medical records for all 96 billed 99215 claims, and a sample of 99214 claims, and have a certified coder audit MDM elements and time against 2021+ E/M guidelines.
- Check whether 99215 claims billed on time (40+ minutes) have contemporaneous time attestations; documented minutes in the unsupported examples were 32-38.
- Look for templated or cloned notes across the low-complexity 99215 visits, such as repeated URI, back pain and rash encounters.
- Review the 99214 claims with low documented MDM (e.g., C0066369, C0066371, C0066434) to see whether level inflation is systematic across levels.
- Compare against the provider's prior-year billing mix to see whether the 99215 share changed abruptly, and check for any coding education or prior audit history.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
