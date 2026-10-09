# Payment Integrity dossier: P0195

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 250 / 96 |
| Billed mix (99211 to 99215) | 0 / 2 / 38 / 120 / 90 |
| 99215 share | 36.0% |
| Expected 99215 share given patient complexity | 2.6% |
| Screen scores | z vs peers 4.77; risk-adjusted 12.66; flagged by zscore+riskadj |

## Case summary (advisory)

**P0195 (Family Practice, GA): 36% 99215 share vs ~2.6% expected; 26 of 30 documented 99215 claims (86.7%) unsupported, pattern consistent with upcoding**

Leaning: pattern consistent with upcoding. Citations checked: 17/17 valid.

P0195 billed 90 of 250 claims (36%) as 99215. The expected share given patient complexity is about 2.6%, and the screen scores are z=4.77 and risk-adjusted 12.66. The elevation is not driven by sicker patients. The 99215 share is 31.3% on patients with 0 chronic conditions and 31.6% on patients with 1, against 2.6% and 3.3% for all providers. In the sample, 99215s were billed for single-issue diagnoses such as UTI (N39.0; C0084079, C0084081, C0084083), low back pain (M54.50; C0084038, C0084139, C0084192), URI (J06.9; C0084196) and follow-up visits (Z09; C0084109, C0084168). The documentation review is reasonably sized at 92 claims (36.8% of claims). Of the 30 documented 99215s, 26 were unsupported (86.7%), versus 26.9% for all providers. 99214 claims were also unsupported at 28.6% versus 8%. Examples include C0083998, billed 99215 for a single-condition CKD patient with documented low MDM and 27 minutes, and C0084090 and C0084116, both documented as moderate MDM. A minority of 99215s were supported with documented high MDM, including C0084154 and C0084190. This fits the expected noise and does not offset the overall pattern. This is a pattern consistent with upcoding, not a finding of fraud.

## Evidence chart

![99215 share by patient complexity](../../charts/P0195.svg)

## Records-review sample so far

Documentation is on file for 92 claims (37% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 11 | 0 | 0.0% | 7.1% |
| 99214 | 49 | 14 | 28.6% | 8.0% |
| 99215 | 30 | 26 | 86.7% | 26.9% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (39 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Pull full records for the remaining 60 undocumented 99215 claims, prioritizing those on patients with 0-1 chronic conditions.
- Have a certified coder independently re-level the 26 unsupported 99215 and 14 unsupported 99214 documented claims to confirm the MDM and time findings.
- Check whether 99215s were billed on time (40+ minutes) and whether the documented minutes and time attestations are credible.
- Look for templated or cloned note language across low-complexity 99215 visits (e.g., UTI, back pain, Z09 follow-ups).
- Estimate the overpayment from the documented-sample unsupported rates by level, and consider a statistically valid extrapolation sample.
- Consider provider education or a prepayment review, and refer for further investigation if the coder review confirms the findings.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
