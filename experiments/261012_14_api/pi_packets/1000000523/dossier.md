# Payment Integrity dossier: 1000000523

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 369 / 176 |
| Billed mix (99211 to 99215) | 6 / 2 / 93 / 179 / 89 |
| 99215 share | 24.1% |
| Expected 99215 share given patient complexity | 2.2% |
| Screen scores | z vs peers 3.63; risk-adjusted 10.32; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000523 bills 99215 at roughly ten times the expected rate, mostly on patients with few or no chronic conditions; the small set of returned charts supports the billed level but is too thin to clear the pattern.**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000523 billed 99215 on 24.1% of 369 claims against an expected 2.2% given patient complexity (risk-adjusted score 10.32; plain z-score vs peers 3.63). 65% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 17 claims. Of 8 documented 99215 claims, 0 (0%) were documented below the billed level, against 0% for the comparison providers. 5 of 15 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The elevated 99215 share holds across every complexity stratum, including visits with zero chronic conditions. Sampled 99215 claims there carry simple diagnoses such as abdominal pain (C0277180, C0277333), upper respiratory infection (C0277233, C0277420), UTI (C0277232) and follow-up codes (C0277258), which is the concern rather than a sicker panel. The returned charts point the other way, since all 8 documented 99215 claims were supported. But records came back for under 5% of claims, which is too thin to offset the claim-level pattern. Some notes may also be inflated: C0277491, a single-condition hypertension and follow-up visit, is documented as high MDM at 50 minutes. A third of the notes claiming moderate-or-higher data review have no lab or test line on the claim, which is weak evidence that notes may be templated rather than reflecting what happened. A reviewer should first request a larger chart sample focused on 0–1 condition 99215 visits. Those notes should be checked for cloned or templated language, and the documented data review and time compared against orders, results and scheduling records. Examples: C0277180: billed 99215, patient aged 45 with 0 chronic condition(s). C0277184: billed 99215, patient aged 48 with 0 chronic condition(s). C0277186: billed 99215, patient aged 61 with 1 chronic condition(s) (osteoarthritis).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000523.svg)

## Records-review sample so far

Documentation is on file for 17 claims (5% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 2 | 0 | 0.0% | 3.1% |
| 99214 | 7 | 0 | 0.0% | 4.8% |
| 99215 | 8 | 0 | 0.0% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (39 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full records for the cited claims and have a certified coder re-score each against current E/M documentation rules (medical decision making or total time).
- If the re-scoring confirms the pattern, use the sampling plan in the recovery packet to review a statistical sample of this provider's 99215 claims.
- Check whether notes for the cited claims look copied forward, and whether documented minutes repeat from visit to visit.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
