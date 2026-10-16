# Payment Integrity dossier: 1000000485

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 125 |
| Billed mix (99211 to 99215) | 2 / 1 / 21 / 108 / 109 |
| 99215 share | 45.2% |
| Expected 99215 share given patient complexity | 8.1% |
| Screen scores | z vs peers 7.59; risk-adjusted 8.36; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000485: 7 of 17 documented 99215 claims (41%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000485 billed 99215 on 45.2% of 241 claims against an expected 8.1% given patient complexity (risk-adjusted score 8.36; plain z-score vs peers 7.59). 6% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 21 claims. Of 17 documented 99215 claims, 7 (41%) were documented below the billed level, against 9% for the comparison providers. Note checks on 21 returned notes (share showing each sign): problems 0%, late 0%, unsigned 0%, data 5%. No audit trail was received. 1 of 18 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0260969: billed 99215; documented MDM level moderate, 35 minutes. C0260983: billed 99215; documented MDM level moderate, 32 minutes. C0260995: billed 99215; documented MDM level moderate, 31 minutes. C0260952: billed 99215, patient aged 64 with 1 chronic condition(s) (type 2 diabetes). C0260966: billed 99215, patient aged 50 with 0 chronic condition(s). C0260986: billed 99215, patient aged 64 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000485.svg)

## Records-review sample so far

Documentation is on file for 21 claims (9% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 1 | 0 | 0.0% | 3.0% |
| 99214 | 3 | 0 | 0.0% | 3.3% |
| 99215 | 17 | 7 | 41.2% | 8.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (42 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0260969, C0260983, C0260995 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 0% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0260969, C0260983, C0260995.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
