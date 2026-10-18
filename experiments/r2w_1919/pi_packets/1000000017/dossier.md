# Payment Integrity dossier: 1000000017

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 288 / 137 |
| Billed mix (99211 to 99215) | 3 / 3 / 76 / 139 / 67 |
| 99215 share | 23.3% |
| Expected 99215 share given patient complexity | 3.9% |
| Screen scores | z vs peers 3.15; risk-adjusted 6.92; flagged by eb_ratio |

## Case summary (advisory)

**1000000017: 4 of 7 documented 99215 claims (57%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000017 billed 99215 on 23.3% of 288 claims against an expected 3.9% given patient complexity (risk-adjusted score 6.92; plain z-score vs peers 3.15). 63% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 7 documented 99215 claims, 4 (57%) were documented below the billed level, against 35% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 23%, late 7%, unsigned 0%, data 0%. No audit trail was received. 2 of 14 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0008282: billed 99215; documented MDM level moderate, 33 minutes. C0008372: billed 99215; documented MDM level moderate, 31 minutes. C0008473: billed 99215; documented MDM level moderate, minutes not recorded. C0008227: billed 99215, patient aged 62 with 1 chronic condition(s) (atrial fibrillation). C0008233: billed 99215, patient aged 48 with 0 chronic condition(s). C0008240: billed 99215, patient aged 42 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000017.svg)

## Records-review sample so far

Documentation is on file for 30 claims (10% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 0 | 0.0% | 3.4% |
| 99214 | 14 | 4 | 28.6% | 4.6% |
| 99215 | 7 | 4 | 57.1% | 34.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (34 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0008282, C0008372, C0008473 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 23% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0008282, C0008372, C0008473.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
