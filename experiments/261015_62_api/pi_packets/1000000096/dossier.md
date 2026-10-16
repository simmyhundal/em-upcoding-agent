# Payment Integrity dossier: 1000000096

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,551 / 762 |
| Billed mix (99211 to 99215) | 4 / 9 / 431 / 967 / 140 |
| 99215 share | 9.0% |
| Expected 99215 share given patient complexity | 1.7% |
| Screen scores | z vs peers 0.82; risk-adjusted 8.11; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000096's 99215 billing is concentrated on patients with few or no chronic conditions and runs above peer rates at every complexity level, a pattern consistent with upcoding, though the chart review is too thin to confirm it.**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000096 billed 99215 on 9.0% of 1,551 claims against an expected 1.7% given patient complexity (risk-adjusted score 8.11; plain z-score vs peers 0.82). 73% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 3 documented 99215 claims, 0 (0%) were documented below the billed level, against 9% for the comparison providers. 2 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The complexity comparison is the core concern. Most of this provider's 99215s fall on patients with 0–1 chronic conditions, and the sampled low-complexity 99215s (e.g., C0064844, C0065101, C0066128, C0066276) carry routine diagnoses such as UTI, follow-up, abdominal pain and URI, while the 99215 share exceeds the all-provider share in every complexity band, including patients with no conditions. The documentation neither confirms nor clears this: only 3 documented 99215s came back, all supported, which is too few to judge. One of them, C0065595, is a hypertension-plus-URI visit documented at high MDM, which deserves a close read for possible inflated or templated notes. The 2 notes claiming moderate-or-higher data reviewed with no lab or test line on the claim are weak evidence of note-to-service mismatch, not proof. Ambiguity remains because the plain peer z-score is unremarkable and the 99214-heavy mix could reflect a genuinely engaged practice style, so a reviewer should first request charts for a targeted sample of the low-complexity 99215s and check whether the MDM and time documented are specific to the visit or cloned. Examples: C0064844: billed 99215, patient aged 52 with 0 chronic condition(s). C0065061: billed 99215, patient aged 57 with 1 chronic condition(s) (hypertension). C0065099: billed 99215, patient aged 37 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000096.svg)

## Records-review sample so far

Documentation is on file for 30 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 12 | 0 | 0.0% | 4.3% |
| 99214 | 15 | 0 | 0.0% | 3.5% |
| 99215 | 3 | 0 | 0.0% | 9.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (46 claims across 99215).
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
