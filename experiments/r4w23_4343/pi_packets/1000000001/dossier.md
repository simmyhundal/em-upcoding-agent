# Payment Integrity dossier: 1000000001

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 121 |
| Billed mix (99211 to 99215) | 2 / 4 / 51 / 126 / 58 |
| 99215 share | 24.1% |
| Expected 99215 share given patient complexity | 4.7% |
| Screen scores | z vs peers 3.15; risk-adjusted 5.92; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000001: 17 of 20 documented 99215 claims (85%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000001 billed 99215 on 24.1% of 241 claims against an expected 4.7% given patient complexity (risk-adjusted score 5.92; plain z-score vs peers 3.15). 57% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 43 claims. Of 20 documented 99215 claims, 17 (85%) were documented below the billed level, against 22% for the comparison providers. Note checks on 43 returned notes (share showing each sign): problems 26%, late 9%, unsigned 0%, data 7%. No audit trail was received. 3 of 28 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0000029: billed 99215; documented MDM level moderate, minutes not recorded. C0000100: billed 99215; documented MDM level moderate, 20 minutes. C0000178: billed 99215; documented MDM level moderate, minutes not recorded. C0000020: billed 99215, patient aged 52 with 1 chronic condition(s) (hypertension); documented MDM level high, 49 minutes. C0000045: billed 99215, patient aged 58 with 1 chronic condition(s) (hyperlipidemia). C0000058: billed 99215, patient aged 18 with 1 chronic condition(s) (asthma).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000001.svg)

## Records-review sample so far

Documentation is on file for 43 claims (18% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 4.1% |
| 99214 | 19 | 4 | 21.1% | 5.0% |
| 99215 | 20 | 17 | 85.0% | 21.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (32 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0000029, C0000100, C0000178 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 26% address fewer problems than their level implies and 9% were signed late; request the audit trail for C0000029, C0000100, C0000178.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
