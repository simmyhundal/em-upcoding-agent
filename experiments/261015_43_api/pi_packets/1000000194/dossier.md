# Payment Integrity dossier: 1000000194

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 238 / 128 |
| Billed mix (99211 to 99215) | 0 / 2 / 44 / 149 / 43 |
| 99215 share | 18.1% |
| Expected 99215 share given patient complexity | 2.0% |
| Screen scores | z vs peers 2.21; risk-adjusted 5.54; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000194: 5 of 6 documented 99215 claims (83%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000194 billed 99215 on 18.1% of 238 claims against an expected 2.0% given patient complexity (risk-adjusted score 5.54; plain z-score vs peers 2.21). 49% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 6 documented 99215 claims, 5 (83%) were documented below the billed level, against 0% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 23%, late 3%, unsigned 0%, data 3%. No audit trail was received. 2 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0108387: billed 99215, patient aged 50 with 4 chronic condition(s) (type 2 diabetes;hyperlipidemia;hypertension;chronic kidney disease); documented MDM level moderate, 24 minutes. C0108439: billed 99215; documented MDM level moderate, minutes not recorded. C0108462: billed 99215, patient aged 44 with 1 chronic condition(s) (hyperlipidemia); documented MDM level moderate, 34 minutes. C0108344: billed 99215, patient aged 39 with 1 chronic condition(s) (hypertension). C0108390: billed 99215, patient aged 44 with 0 chronic condition(s). C0108401: billed 99215, patient aged 20 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000194.svg)

## Records-review sample so far

Documentation is on file for 30 claims (13% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 1.6% |
| 99214 | 20 | 3 | 15.0% | 3.3% |
| 99215 | 6 | 5 | 83.3% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (27 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0108387, C0108439, C0108462 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 23% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0108387, C0108439, C0108462.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
