# Payment Integrity dossier: 1000000142

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 359 / 168 |
| Billed mix (99211 to 99215) | 1 / 11 / 83 / 177 / 87 |
| 99215 share | 24.2% |
| Expected 99215 share given patient complexity | 4.3% |
| Screen scores | z vs peers 3.43; risk-adjusted 7.00; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000142: 19 of 22 documented 99215 claims (86%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000142 billed 99215 on 24.2% of 359 claims against an expected 4.3% given patient complexity (risk-adjusted score 7.00; plain z-score vs peers 3.43). 57% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 22 documented 99215 claims, 19 (86%) were documented below the billed level, against 24% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 51%, late 4%, unsigned 0%, data 4%. No audit trail was received. 2 of 34 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0069222: billed 99215; documented MDM level moderate, minutes not recorded. C0069253: billed 99215; documented MDM level moderate, 34 minutes. C0069351: billed 99215, patient aged 54 with 1 chronic condition(s) (atrial fibrillation); documented MDM level moderate, 39 minutes. C0069113: billed 99215, patient aged 56 with 0 chronic condition(s). C0069127: billed 99215, patient aged 68 with 0 chronic condition(s). C0069134: billed 99215, patient aged 35 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000142.svg)

## Records-review sample so far

Documentation is on file for 45 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 1.8% |
| 99214 | 17 | 5 | 29.4% | 5.2% |
| 99215 | 22 | 19 | 86.4% | 24.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (39 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0069222, C0069253, C0069351 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 51% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0069222, C0069253, C0069351.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
