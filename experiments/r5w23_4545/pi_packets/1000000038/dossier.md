# Payment Integrity dossier: 1000000038

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 238 / 111 |
| Billed mix (99211 to 99215) | 3 / 12 / 90 / 94 / 39 |
| 99215 share | 16.4% |
| Expected 99215 share given patient complexity | 4.0% |
| Screen scores | z vs peers 1.76; risk-adjusted 3.52; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000038: 16 of 19 documented 99215 claims (84%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000038 billed 99215 on 16.4% of 238 claims against an expected 4.0% given patient complexity (risk-adjusted score 3.52; plain z-score vs peers 1.76). 59% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 43 claims. Of 19 documented 99215 claims, 16 (84%) were documented below the billed level, against 48% for the comparison providers. Note checks on 43 returned notes (share showing each sign): problems 23%, late 0%, unsigned 0%, data 5%. No audit trail was received. 2 of 24 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0013864: billed 99215; documented MDM level moderate, 31 minutes. C0013946: billed 99215; documented MDM level moderate, minutes not recorded. C0014034: billed 99215, patient aged 46 with 0 chronic condition(s); documented MDM level moderate, 30 minutes. C0013819: billed 99215, patient aged 55 with 0 chronic condition(s). C0013855: billed 99215, patient aged 54 with 1 chronic condition(s) (hyperlipidemia); documented MDM level high, minutes not recorded. C0013887: billed 99215, patient aged 73 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000038.svg)

## Records-review sample so far

Documentation is on file for 43 claims (18% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 12 | 1 | 8.3% | 4.7% |
| 99214 | 10 | 5 | 50.0% | 4.7% |
| 99215 | 19 | 16 | 84.2% | 48.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (25 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0013864, C0013946, C0014034 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 23% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0013864, C0013946, C0014034.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
