# Payment Integrity dossier: 1000000176

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 471 / 238 |
| Billed mix (99211 to 99215) | 2 / 4 / 99 / 235 / 131 |
| 99215 share | 27.8% |
| Expected 99215 share given patient complexity | 4.6% |
| Screen scores | z vs peers 3.05; risk-adjusted 9.77; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000176: 0 of 7 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000176 billed 99215 on 27.8% of 471 claims against an expected 4.6% given patient complexity (risk-adjusted score 9.77; plain z-score vs peers 3.05). 51% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 7 documented 99215 claims, 0 (0%) were documented below the billed level, against 29% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 37%, late 17%, unsigned 0%, data 23%, bulk created 13%, paste heavy 17%. 7 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0078858: billed 99214; documented MDM level low, minutes not recorded. C0078570: billed 99215, patient aged 46 with 0 chronic condition(s). C0078592: billed 99215, patient aged 56 with 1 chronic condition(s) (COPD). C0078601: billed 99215, patient aged 70 with 1 chronic condition(s) (depression).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000176.svg)

## Records-review sample so far

Documentation is on file for 30 claims (6% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 4.6% |
| 99214 | 16 | 1 | 6.2% | 4.1% |
| 99215 | 7 | 0 | 0.0% | 28.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (45 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0078858, C0078570, C0078592 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 37% address fewer problems than their level implies and 17% were signed late; request the audit trail for C0078858, C0078570, C0078592.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
