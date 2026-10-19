# Payment Integrity dossier: 1000000114

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,406 / 1,149 |
| Billed mix (99211 to 99215) | 15 / 24 / 598 / 1,210 / 559 |
| 99215 share | 23.2% |
| Expected 99215 share given patient complexity | 4.2% |
| Screen scores | z vs peers 2.47; risk-adjusted 19.46; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000114: 7 of 7 documented 99215 claims (100%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000114 billed 99215 on 23.2% of 2,406 claims against an expected 4.2% given patient complexity (risk-adjusted score 19.46; plain z-score vs peers 2.47). 77% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 7 documented 99215 claims, 7 (100%) were documented below the billed level, against 22% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 30%, late 7%, unsigned 0%, data 0%. No audit trail was received. 2 of 14 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0052736: billed 99215; documented MDM level moderate, 31 minutes. C0053082: billed 99215; documented MDM level moderate, minutes not recorded. C0054044: billed 99215; documented MDM level moderate, minutes not recorded. C0051982: billed 99215, patient aged 18 with 0 chronic condition(s). C0051989: billed 99215, patient aged 38 with 0 chronic condition(s). C0052030: billed 99215, patient aged 40 with 1 chronic condition(s) (depression).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000114.svg)

## Records-review sample so far

Documentation is on file for 30 claims (1% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 0 | 0.0% | 4.1% |
| 99214 | 13 | 6 | 46.2% | 7.3% |
| 99215 | 7 | 7 | 100.0% | 22.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (61 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0052736, C0053082, C0054044 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 30% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0052736, C0053082, C0054044.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
