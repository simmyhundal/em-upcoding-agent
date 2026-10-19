# Payment Integrity dossier: 1000000076

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 240 / 119 |
| Billed mix (99211 to 99215) | 1 / 6 / 73 / 116 / 44 |
| 99215 share | 18.3% |
| Expected 99215 share given patient complexity | 5.8% |
| Screen scores | z vs peers 1.85; risk-adjusted 2.90; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000076: 2 of 22 documented 99215 claims (9%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000076 billed 99215 on 18.3% of 240 claims against an expected 5.8% given patient complexity (risk-adjusted score 2.90; plain z-score vs peers 1.85). 34% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 22 documented 99215 claims, 2 (9%) were documented below the billed level, against 58% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 29%, late 27%, unsigned 0%, data 20%. No audit trail was received. 12 of 39 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0032732: billed 99215; documented MDM level moderate, minutes not recorded. C0032733: billed 99215, patient aged 72 with 4 chronic condition(s) (hypothyroidism;depression;hypertension;heart failure); documented MDM level moderate, minutes not recorded. C0032607: billed 99215, patient aged 49 with 1 chronic condition(s) (atrial fibrillation). C0032617: billed 99215, patient aged 49 with 1 chronic condition(s) (atrial fibrillation). C0032625: billed 99215, patient aged 60 with 1 chronic condition(s) (asthma).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000076.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 3.1% |
| 99214 | 16 | 0 | 0.0% | 6.2% |
| 99215 | 22 | 2 | 9.1% | 57.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (27 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0032732, C0032733, C0032607 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 29% address fewer problems than their level implies and 27% were signed late; request the audit trail for C0032732, C0032733, C0032607.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
