# Payment Integrity dossier: 1000000104

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,083 / 528 |
| Billed mix (99211 to 99215) | 9 / 11 / 456 / 516 / 91 |
| 99215 share | 8.4% |
| Expected 99215 share given patient complexity | 2.0% |
| Screen scores | z vs peers 0.69; risk-adjusted 7.27; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000104's 99215 billing is concentrated on low-complexity patients and runs above peer rates at every complexity level, a pattern consistent with upcoding, though the chart evidence is too thin to confirm it.**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000104 billed 99215 on 8.4% of 1,083 claims against an expected 2.0% given patient complexity (risk-adjusted score 7.27; plain z-score vs peers 0.69). 67% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 18 claims. Of 3 documented 99215 claims, 1 (33%) were documented below the billed level, against 0% for the comparison providers. 2 of 10 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The claims data point toward upcoding rather than a sicker panel. The excess over the risk-adjusted expectation persists in every complexity stratum, roughly double the all-provider share even for patients with no chronic conditions. Most 99215s fall on 0-1 condition patients with routine diagnoses such as UTI, follow-up, abdominal pain or rash (e.g., C0056901, C0057250, C0058000), while the high-complexity 99215s (e.g., C0057200, C0057624) look appropriate. The documentation cannot settle the question: only 3 documented 99215s came back. One was unsupported (C0056935, moderate MDM). The two supported ones (C0057470, C0057654) are themselves 0-condition UTI and follow-up visits documented as high MDM, which is plausible but worth scrutiny for inflated or templated notes. The modest peer z-score and the few data-reviewed notes lacking a lab line are weak signals on their own. A reviewer should first request a larger targeted sample of charts for low-complexity 99215 claims, starting with the sampled claims above, and compare MDM elements and time against the visit's actual content. Examples: C0056935: billed 99215, patient aged 36 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0056890: billed 99215, patient aged 65 with 0 chronic condition(s). C0056901: billed 99215, patient aged 41 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000104.svg)

## Records-review sample so far

Documentation is on file for 18 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 4.7% |
| 99214 | 9 | 0 | 0.0% | 3.7% |
| 99215 | 3 | 1 | 33.3% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (40 claims across 99215).
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
