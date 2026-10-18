# Payment Integrity dossier: 1000000199

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 329 / 159 |
| Billed mix (99211 to 99215) | 0 / 4 / 61 / 168 / 96 |
| 99215 share | 29.2% |
| Expected 99215 share given patient complexity | 8.1% |
| Screen scores | z vs peers 3.68; risk-adjusted 4.82; flagged by eb_ratio |

## Case summary (advisory)

**1000000199: 5 of 8 documented 99215 claims (62%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000199 billed 99215 on 29.2% of 329 claims against an expected 8.1% given patient complexity (risk-adjusted score 4.82; plain z-score vs peers 3.68). 12% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 8 documented 99215 claims, 5 (62%) were documented below the billed level, against 38% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 13%, late 0%, unsigned 0%, data 3%. No audit trail was received. 1 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0102089: billed 99215, patient aged 69 with 1 chronic condition(s) (chronic kidney disease); documented MDM level moderate, minutes not recorded. C0102120: billed 99215; documented MDM level moderate, minutes not recorded. C0102159: billed 99215, patient aged 66 with 1 chronic condition(s) (osteoarthritis); documented MDM level moderate, 29 minutes. C0102009: billed 99215, patient aged 67 with 0 chronic condition(s). C0102036: billed 99215, patient aged 40 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000199.svg)

## Records-review sample so far

Documentation is on file for 30 claims (9% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 3.4% |
| 99214 | 17 | 0 | 0.0% | 8.3% |
| 99215 | 8 | 5 | 62.5% | 37.9% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (40 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0102089, C0102120, C0102159 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 13% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0102089, C0102120, C0102159.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
