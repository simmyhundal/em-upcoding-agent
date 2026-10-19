# Payment Integrity dossier: 1000000204

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 417 / 212 |
| Billed mix (99211 to 99215) | 2 / 4 / 115 / 196 / 100 |
| 99215 share | 24.0% |
| Expected 99215 share given patient complexity | 5.7% |
| Screen scores | z vs peers 3.67; risk-adjusted 6.26; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000204: 8 of 20 documented 99214 and 99215 claims (40%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000204 billed 99215 on 24.0% of 417 claims against an expected 5.7% given patient complexity (risk-adjusted score 6.26; plain z-score vs peers 3.67). 23% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 4 documented 99215 claims, 4 (100%) were documented below the billed level, against 50% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 17%, late 7%, unsigned 0%, data 7%. No audit trail was received. 3 of 15 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0116209: billed 99215; documented MDM level moderate, 32 minutes. C0116320: billed 99215, patient aged 35 with 1 chronic condition(s) (hypertension); documented MDM level moderate, 32 minutes. C0116422: billed 99215; documented MDM level moderate, 36 minutes. C0116131: billed 99215, patient aged 52 with 1 chronic condition(s) (hyperlipidemia). C0116160: billed 99215, patient aged 47 with 1 chronic condition(s) (hypertension). C0116165: billed 99215, patient aged 67 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000204.svg)

## Records-review sample so far

Documentation is on file for 29 claims (7% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 0 | 0.0% | 3.7% |
| 99214 | 16 | 4 | 25.0% | 5.9% |
| 99215 | 4 | 4 | 100.0% | 50.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (41 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0116209, C0116320, C0116422 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 17% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0116209, C0116320, C0116422.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
