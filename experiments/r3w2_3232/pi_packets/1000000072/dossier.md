# Payment Integrity dossier: 1000000072

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 236 / 115 |
| Billed mix (99211 to 99215) | 4 / 2 / 62 / 116 / 52 |
| 99215 share | 22.0% |
| Expected 99215 share given patient complexity | 3.6% |
| Screen scores | z vs peers 2.30; risk-adjusted 5.12; flagged by eb_ratio |

## Case summary (advisory)

**1000000072: 13 of 19 documented 99215 claims (68%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000072 billed 99215 on 22.0% of 236 claims against an expected 3.6% given patient complexity (risk-adjusted score 5.12; plain z-score vs peers 2.30). 69% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 44 claims. Of 19 documented 99215 claims, 13 (68%) were documented below the billed level, against 29% for the comparison providers. Note checks on 44 returned notes (share showing each sign): problems 34%, late 9%, unsigned 0%, data 7%. No audit trail was received. 4 of 27 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0042480: billed 99215; documented MDM level low, minutes not recorded. C0042526: billed 99215, patient aged 50 with 0 chronic condition(s); documented MDM level moderate, 38 minutes. C0042569: billed 99215, patient aged 51 with 4 chronic condition(s) (type 2 diabetes;hypertension;heart failure;COPD); documented MDM level moderate, minutes not recorded. C0042419: billed 99215, patient aged 43 with 1 chronic condition(s) (COPD). C0042425: billed 99215, patient aged 72 with 0 chronic condition(s). C0042431: billed 99215, patient aged 51 with 1 chronic condition(s) (COPD).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000072.svg)

## Records-review sample so far

Documentation is on file for 44 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 0 | 0.0% | 2.2% |
| 99214 | 15 | 6 | 40.0% | 3.8% |
| 99215 | 19 | 13 | 68.4% | 28.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (30 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0042480, C0042526, C0042569 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 34% address fewer problems than their level implies and 9% were signed late; request the audit trail for C0042480, C0042526, C0042569.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
