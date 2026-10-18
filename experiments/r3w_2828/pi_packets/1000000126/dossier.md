# Payment Integrity dossier: 1000000126

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 629 / 295 |
| Billed mix (99211 to 99215) | 12 / 6 / 175 / 312 / 124 |
| 99215 share | 19.7% |
| Expected 99215 share given patient complexity | 4.7% |
| Screen scores | z vs peers 2.62; risk-adjusted 7.23; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000126: 18 of 23 documented 99215 claims (78%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000126 billed 99215 on 19.7% of 629 claims against an expected 4.7% given patient complexity (risk-adjusted score 7.23; plain z-score vs peers 2.62). 48% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 23 documented 99215 claims, 18 (78%) were documented below the billed level, against 43% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 38%, late 7%, unsigned 0%, data 2%. No audit trail was received. 2 of 26 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0063719: billed 99215; documented MDM level moderate, minutes not recorded. C0064176: billed 99215, patient aged 35 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0064267: billed 99215; documented MDM level moderate, minutes not recorded. C0063729: billed 99215, patient aged 38 with 1 chronic condition(s) (COPD). C0063730: billed 99215, patient aged 46 with 0 chronic condition(s). C0063754: billed 99215, patient aged 30 with 1 chronic condition(s) (heart failure).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000126.svg)

## Records-review sample so far

Documentation is on file for 45 claims (7% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 2.4% |
| 99214 | 17 | 5 | 29.4% | 4.8% |
| 99215 | 23 | 18 | 78.3% | 43.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (45 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0063719, C0064176, C0064267 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 38% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0063719, C0064176, C0064267.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
