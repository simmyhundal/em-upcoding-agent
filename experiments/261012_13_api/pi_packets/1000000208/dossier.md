# Payment Integrity dossier: 1000000208

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 450 / 217 |
| Billed mix (99211 to 99215) | 3 / 4 / 131 / 242 / 70 |
| 99215 share | 15.6% |
| Expected 99215 share given patient complexity | 2.1% |
| Screen scores | z vs peers 2.14; risk-adjusted 7.24; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000208's 99215 billing is concentrated on low-complexity patients with routine diagnoses, a pattern consistent with upcoding, though the chart review is too thin to confirm it.**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000208 billed 99215 on 15.6% of 450 claims against an expected 2.1% given patient complexity (risk-adjusted score 7.24; plain z-score vs peers 2.14). 66% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 17 claims. Of 2 documented 99215 claims, 1 (50%) were documented below the billed level, against 14% for the comparison providers. 4 of 11 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The strongest signal is the mismatch between billed level and patient complexity. The elevated 99215 share holds in every complexity stratum, and most sampled low-complexity 99215 claims carry simple diagnoses such as urinary tract infection (N39.0) or abdominal pain (R10.9), for example C0104222, C0104248 and C0104610, rather than the multi-condition profiles seen in C0104511. Documentation cannot yet confirm or refute this: only two 99215 charts came back, one supported and one below the billed level (C0104368). The supported one, C0104637, is an upper respiratory infection on a patient with no chronic conditions documented at high MDM, which deserves a close look for inflated or templated notes. The share of moderate-or-higher data-reviewed notes with no lab or test line on the claim is weak supporting evidence that some notes may not reflect what happened. A reviewer should first request charts for the sampled low-complexity 99215 claims, starting with the N39.0 and R10.9 visits, and check whether the MDM and time documentation genuinely supports level 5. Examples: C0104368: billed 99215; documented MDM level moderate, minutes not recorded. C0104222: billed 99215, patient aged 42 with 0 chronic condition(s). C0104248: billed 99215, patient aged 33 with 0 chronic condition(s). C0104273: billed 99215, patient aged 30 with 1 chronic condition(s) (type 2 diabetes).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000208.svg)

## Records-review sample so far

Documentation is on file for 17 claims (4% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 1 | 20.0% | 5.0% |
| 99214 | 10 | 0 | 0.0% | 3.0% |
| 99215 | 2 | 1 | 50.0% | 14.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (35 claims across 99215).
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
