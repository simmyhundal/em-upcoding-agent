# Payment Integrity dossier: 1000000151

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,394 / 1,201 |
| Billed mix (99211 to 99215) | 13 / 6 / 550 / 1,337 / 488 |
| 99215 share | 20.4% |
| Expected 99215 share given patient complexity | 2.7% |
| Screen scores | z vs peers 2.80; risk-adjusted 19.78; flagged by zscore+riskadj |

## Case summary (advisory)

**Provider 1000000151 bills 99215 far above its risk-adjusted expectation across every complexity stratum, including many visits for patients with no or one chronic condition, while documentation is too thin to confirm or refute the billed levels.**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000151 billed 99215 on 20.4% of 2,394 claims against an expected 2.7% given patient complexity (risk-adjusted score 19.78; plain z-score vs peers 2.80). 45% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 4 documented 99215 claims, 0 (0%) were documented below the billed level, against 11% for the comparison providers. 6 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The claims data point toward upcoding rather than a sicker panel. The 99215 share is several times the all-provider share at every complexity level, and the gap is widest among patients with 0 or 1 conditions. The sampled low-complexity 99215 claims carry simple diagnoses such as UTI (C0077210, C0078057), upper respiratory infection (C0077478, C0078076) and follow-up Z09 visits (C0076525, C0078053), which rarely call for high-complexity decision making. The records review cuts the other way but is weak: only 4 documented 99215 claims came back, all supported (for example C0076582 and C0077186). That is too few to judge, and the unsupported rate cannot be separated from the comparison rate on that sample. There is also a mild signal of possibly templated notes, since some notes claiming moderate-or-higher data reviewed have no lab or test line on the claim; this is weak evidence and does not prove inflation. A reviewer should first request charts targeted at the low-complexity 99215 claims listed above and check whether the MDM and time actually support level 5. Those charts should also be checked for cloned or templated language. Examples: C0076320: billed 99215, patient aged 38 with 1 chronic condition(s) (type 2 diabetes). C0076525: billed 99215, patient aged 48 with 0 chronic condition(s). C0076564: billed 99215, patient aged 31 with 1 chronic condition(s) (type 2 diabetes).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000151.svg)

## Records-review sample so far

Documentation is on file for 30 claims (1% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 2.3% |
| 99214 | 20 | 0 | 0.0% | 3.6% |
| 99215 | 4 | 0 | 0.0% | 11.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (60 claims across 99215).
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
