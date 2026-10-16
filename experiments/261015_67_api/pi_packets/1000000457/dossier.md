# Payment Integrity dossier: 1000000457

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 240 / 115 |
| Billed mix (99211 to 99215) | 1 / 1 / 45 / 120 / 73 |
| 99215 share | 30.4% |
| Expected 99215 share given patient complexity | 2.1% |
| Screen scores | z vs peers 4.83; risk-adjusted 12.03; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000457 bills 99215 heavily on patients with few or no chronic conditions, often for routine diagnoses; the handful of returned charts support the billed level but are too few to settle the question.**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000457 billed 99215 on 30.4% of 240 claims against an expected 2.1% given patient complexity (risk-adjusted score 12.03; plain z-score vs peers 4.83). 71% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 24 claims. Of 6 documented 99215 claims, 0 (0%) were documented below the billed level, against 9% for the comparison providers. 4 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The core concern is the mismatch between billed level and patient complexity: most of this provider's 99215s fall on 0–1 condition patients, and the sampled low-complexity 99215s are largely routine presentations such as upper respiratory infection (C0250530, C0250548), low back pain (C0250576, C0250588) and UTI (C0250574), which is not the profile of a legitimately sicker panel. The records review cuts the other way, since none of the documented 99215s fell below the billed level, but six charts is too thin a base to offset the complexity pattern. Some supported notes also raise their own question: C0250594, a URI visit on a patient with no chronic conditions, was documented at high MDM. Together with the moderate-or-higher data-reviewed notes that have no lab or test line, this is weak evidence that documentation may be templated or inflated to match the code, not proof. A reviewer should first request and read the full notes for the low-complexity 99215 claims, starting with the URI, back-pain and UTI visits, to check whether the MDM narrative and any time statements reflect the actual encounter. They should also expand the records sample beyond the current small share. Examples: C0250557: billed 99213; documented MDM level straightforward, minutes not recorded. C0250529: billed 99215, patient aged 42 with 1 chronic condition(s) (hypothyroidism). C0250530: billed 99215, patient aged 48 with 0 chronic condition(s). C0250535: billed 99215, patient aged 72 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000457.svg)

## Records-review sample so far

Documentation is on file for 24 claims (10% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 1 | 20.0% | 3.0% |
| 99214 | 13 | 0 | 0.0% | 3.3% |
| 99215 | 6 | 0 | 0.0% | 8.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (36 claims across 99215).
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
