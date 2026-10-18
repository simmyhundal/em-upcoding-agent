# Payment Integrity dossier: 1000000071

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 243 / 120 |
| Billed mix (99211 to 99215) | 4 / 4 / 68 / 122 / 45 |
| 99215 share | 18.5% |
| Expected 99215 share given patient complexity | 7.0% |
| Screen scores | z vs peers 2.06; risk-adjusted 2.54; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000071: 5 of 7 documented 99215 claims (71%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000071 billed 99215 on 18.5% of 243 claims against an expected 7.0% given patient complexity (risk-adjusted score 2.54; plain z-score vs peers 2.06). 20% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 7 documented 99215 claims, 5 (71%) were documented below the billed level, against 21% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 10%, late 0%, unsigned 0%, data 0%. No audit trail was received. 0 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0032617: billed 99215, patient aged 77 with 5 chronic condition(s) (hypothyroidism;type 2 diabetes;obesity;hypertension;heart failure); documented MDM level moderate, minutes not recorded. C0032634: billed 99215, patient aged 26 with 4 chronic condition(s) (type 2 diabetes;hyperlipidemia;hypertension;osteoarthritis); documented MDM level moderate, minutes not recorded. C0032670: billed 99215, patient aged 28 with 1 chronic condition(s) (COPD); documented MDM level moderate, 24 minutes. C0032656: billed 99215, patient aged 21 with 1 chronic condition(s) (obesity). C0032664: billed 99215, patient aged 49 with 0 chronic condition(s). C0032669: billed 99215, patient aged 20 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000071.svg)

## Records-review sample so far

Documentation is on file for 29 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 2.6% |
| 99214 | 16 | 1 | 6.2% | 6.4% |
| 99215 | 7 | 5 | 71.4% | 20.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (28 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0032617, C0032634, C0032670 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 10% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0032617, C0032634, C0032670.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
