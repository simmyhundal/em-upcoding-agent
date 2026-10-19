# Payment Integrity dossier: 1000000126

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 240 / 114 |
| Billed mix (99211 to 99215) | 1 / 7 / 54 / 116 / 62 |
| 99215 share | 25.8% |
| Expected 99215 share given patient complexity | 4.4% |
| Screen scores | z vs peers 2.93; risk-adjusted 6.26; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000126: 0 of 22 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000126 billed 99215 on 25.8% of 240 claims against an expected 4.4% given patient complexity (risk-adjusted score 6.26; plain z-score vs peers 2.93). 66% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 44 claims. Of 22 documented 99215 claims, 0 (0%) were documented below the billed level, against 21% for the comparison providers. Note checks on 44 returned notes (share showing each sign): problems 55%, late 23%, unsigned 0%, data 16%. No audit trail was received. 8 of 33 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0064918: billed 99215, patient aged 59 with 0 chronic condition(s). C0064940: billed 99215, patient aged 21 with 0 chronic condition(s); documented MDM level high, minutes not recorded. C0064947: billed 99215, patient aged 36 with 1 chronic condition(s) (chronic kidney disease); documented MDM level high, minutes not recorded.

## Evidence chart

![99215 share by patient complexity](../../charts/1000000126.svg)

## Records-review sample so far

Documentation is on file for 44 claims (18% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 2.2% |
| 99214 | 15 | 0 | 0.0% | 8.9% |
| 99215 | 22 | 0 | 0.0% | 20.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (33 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0064918, C0064940, C0064947 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 55% address fewer problems than their level implies and 23% were signed late; request the audit trail for C0064918, C0064940, C0064947.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
