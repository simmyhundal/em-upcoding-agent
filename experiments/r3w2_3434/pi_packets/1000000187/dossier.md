# Payment Integrity dossier: 1000000187

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 240 / 114 |
| Billed mix (99211 to 99215) | 2 / 8 / 67 / 106 / 57 |
| 99215 share | 23.8% |
| Expected 99215 share given patient complexity | 7.8% |
| Screen scores | z vs peers 2.32; risk-adjusted 3.12; flagged by eb_ratio |

## Case summary (advisory)

**1000000187: 7 of 9 documented 99215 claims (78%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000187 billed 99215 on 23.8% of 240 claims against an expected 7.8% given patient complexity (risk-adjusted score 3.12; plain z-score vs peers 2.32). 21% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 9 documented 99215 claims, 7 (78%) were documented below the billed level, against 32% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 14%, late 3%, unsigned 0%, data 3%. No audit trail was received. 1 of 16 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0079320: billed 99215; documented MDM level moderate, 20 minutes. C0079321: billed 99215, patient aged 66 with 4 chronic condition(s) (type 2 diabetes;hyperlipidemia;depression;chronic kidney disease); documented MDM level moderate, 24 minutes. C0079412: billed 99215; documented MDM level moderate, 33 minutes. C0079255: billed 99215, patient aged 28 with 1 chronic condition(s) (atrial fibrillation). C0079271: billed 99215, patient aged 47 with 1 chronic condition(s) (hypertension). C0079295: billed 99215, patient aged 50 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000187.svg)

## Records-review sample so far

Documentation is on file for 29 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 2 | 20.0% | 4.6% |
| 99214 | 9 | 5 | 55.6% | 0.8% |
| 99215 | 9 | 7 | 77.8% | 32.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (32 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0079320, C0079321, C0079412 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 14% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0079320, C0079321, C0079412.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
