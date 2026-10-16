# Payment Integrity dossier: 1000000146

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 668 / 331 |
| Billed mix (99211 to 99215) | 5 / 4 / 228 / 368 / 63 |
| 99215 share | 9.4% |
| Expected 99215 share given patient complexity | 1.8% |
| Screen scores | z vs peers 0.68; risk-adjusted 5.82; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000146's 99215 billing runs well above what its patient complexity predicts and is concentrated on patients with few or no chronic conditions, a pattern consistent with upcoding, though the chart review is too thin to confirm it.**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000146 billed 99215 on 9.4% of 668 claims against an expected 1.8% given patient complexity (risk-adjusted score 5.82; plain z-score vs peers 0.68). 57% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 3 documented 99215 claims, 0 (0%) were documented below the billed level, against 5% for the comparison providers. 1 of 18 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The risk-adjusted excess is the main signal, and the plain peer z-score is modest, so the concern comes from billing relative to case mix rather than raw volume. The 99215 share runs about three times the all-provider rate in every complexity stratum, and most 99215s fall on 0–1 condition patients. Sampled low-complexity claims such as C0075079 and C0075177 (R21 rash), C0075071 and C0075332 (J06.9 upper respiratory infection) and C0075081 (Z09 follow-up) carry diagnoses that rarely support high-complexity decision-making. The documentation neither confirms nor refutes this: only 3 documented 99215s came back, and all were supported. One of those, C0075150, is a single-condition depression visit with high decision-making complexity (MDM) and 49 minutes recorded, a reminder that some low-complexity 99215s may be legitimate. A reviewer should first request charts for the sampled low-complexity 99215 claims, prioritizing the symptom-only and Z09 encounters, and check whether the notes support high MDM or time. They should also watch for templated or cloned note language, although the one data-reviewed mismatch is too small to weigh. Examples: C0074719: billed 99214; documented MDM level low, minutes not recorded. C0074690: billed 99215, patient aged 38 with 1 chronic condition(s) (type 2 diabetes). C0074749: billed 99215, patient aged 60 with 1 chronic condition(s) (atrial fibrillation). C0074824: billed 99215, patient aged 48 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000146.svg)

## Records-review sample so far

Documentation is on file for 30 claims (4% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 0 | 0.0% | 1.6% |
| 99214 | 18 | 1 | 5.6% | 3.0% |
| 99215 | 3 | 0 | 0.0% | 4.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (33 claims across 99215).
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
