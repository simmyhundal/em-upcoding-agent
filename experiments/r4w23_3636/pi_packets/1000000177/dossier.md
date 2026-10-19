# Payment Integrity dossier: 1000000177

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,371 / 696 |
| Billed mix (99211 to 99215) | 7 / 21 / 270 / 840 / 233 |
| 99215 share | 17.0% |
| Expected 99215 share given patient complexity | 6.4% |
| Screen scores | z vs peers 1.41; risk-adjusted 5.70; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000177: 6 of 18 documented 99214 and 99215 claims (33%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000177 billed 99215 on 17.0% of 1,371 claims against an expected 6.4% given patient complexity (risk-adjusted score 5.70; plain z-score vs peers 1.41). 32% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 27 claims. Of 5 documented 99215 claims, 4 (80%) were documented below the billed level, against 27% for the comparison providers. Note checks on 27 returned notes (share showing each sign): problems 22%, late 7%, unsigned 0%, data 4%. No audit trail was received. 2 of 16 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0096836: billed 99215; documented MDM level moderate, minutes not recorded. C0097373: billed 99215; documented MDM level moderate, 33 minutes. C0097628: billed 99215; documented MDM level moderate, minutes not recorded. C0096543: billed 99215, patient aged 31 with 0 chronic condition(s). C0096576: billed 99215, patient aged 61 with 1 chronic condition(s) (atrial fibrillation). C0096602: billed 99215, patient aged 40 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000177.svg)

## Records-review sample so far

Documentation is on file for 27 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 0 | 0.0% | 0.0% |
| 99214 | 13 | 2 | 15.4% | 5.3% |
| 99215 | 5 | 4 | 80.0% | 26.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (53 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0096836, C0097373, C0097628 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 22% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0096836, C0097373, C0097628.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
