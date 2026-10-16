# Payment Integrity dossier: 1000000463

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 306 / 147 |
| Billed mix (99211 to 99215) | 1 / 7 / 111 / 144 / 43 |
| 99215 share | 14.1% |
| Expected 99215 share given patient complexity | 1.9% |
| Screen scores | z vs peers 1.79; risk-adjusted 5.68; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000463 bills 99215 well above risk-adjusted expectation, mostly on patients with few or no chronic conditions; the available records support the billed level but are too few to settle the question.**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000463 billed 99215 on 14.1% of 306 claims against an expected 1.9% given patient complexity (risk-adjusted score 5.68; plain z-score vs peers 1.79). 65% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 4 documented 99215 claims, 0 (0%) were documented below the billed level, against 9% for the comparison providers. 4 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The claims pattern does not look like a sicker panel. The excess 99215 billing is concentrated on patients with 0 or 1 conditions, and the sampled examples include routine diagnoses such as follow-up exams (C0260904, C0261155), rash (C0261123) and upper respiratory infection (C0261150), which is consistent with upcoding rather than case mix. The records review is the main ambiguity: all four documented 99215 claims were supported, but four claims are too few to judge. Two of them are low-complexity visits documented at high MDM: C0261068, a 0-condition follow-up, and C0261175, hypertension with abdominal pain. The four moderate-or-higher data-reviewed notes with no lab or test line on the claim are weak evidence that some notes may be cloned or inflated, not proof. A reviewer should first request charts for more of the low-complexity 99215 claims and check whether the high-MDM notes for visits like C0261068 contain visit-specific findings or templated language. Examples: C0260871: billed 99215, patient aged 67 with 1 chronic condition(s) (asthma). C0260889: billed 99215, patient aged 61 with 1 chronic condition(s) (obesity). C0260890: billed 99215, patient aged 54 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000463.svg)

## Records-review sample so far

Documentation is on file for 30 claims (10% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 0 | 0.0% | 4.3% |
| 99214 | 16 | 0 | 0.0% | 3.5% |
| 99215 | 4 | 0 | 0.0% | 9.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (27 claims across 99215).
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
