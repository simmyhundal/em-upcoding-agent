# Payment Integrity dossier: 1000000039

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 325 / 173 |
| Billed mix (99211 to 99215) | 3 / 11 / 72 / 167 / 72 |
| 99215 share | 22.2% |
| Expected 99215 share given patient complexity | 5.4% |
| Screen scores | z vs peers 2.35; risk-adjusted 5.14; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000039: 5 of 7 documented 99215 claims (71%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000039 billed 99215 on 22.2% of 325 claims against an expected 5.4% given patient complexity (risk-adjusted score 5.14; plain z-score vs peers 2.35). 51% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 7 documented 99215 claims, 5 (71%) were documented below the billed level, against 21% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 23%, late 0%, unsigned 0%, data 3%. No audit trail was received. 2 of 17 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0018813: billed 99215, patient aged 49 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0019070: billed 99215, patient aged 25 with 0 chronic condition(s); documented MDM level moderate, 31 minutes. C0019091: billed 99215; documented MDM level moderate, minutes not recorded. C0018816: billed 99215, patient aged 74 with 1 chronic condition(s) (atrial fibrillation). C0018872: billed 99215, patient aged 85 with 1 chronic condition(s) (type 2 diabetes).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000039.svg)

## Records-review sample so far

Documentation is on file for 30 claims (9% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 1 | 25.0% | 2.2% |
| 99214 | 17 | 3 | 17.6% | 8.9% |
| 99215 | 7 | 5 | 71.4% | 20.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (36 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0018813, C0019070, C0019091 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 23% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0018813, C0019070, C0019091.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
