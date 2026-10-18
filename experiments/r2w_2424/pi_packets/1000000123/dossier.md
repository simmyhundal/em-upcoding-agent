# Payment Integrity dossier: 1000000123

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,070 / 525 |
| Billed mix (99211 to 99215) | 0 / 14 / 128 / 543 / 385 |
| 99215 share | 36.0% |
| Expected 99215 share given patient complexity | 4.9% |
| Screen scores | z vs peers 4.82; risk-adjusted 16.56; flagged by eb_ratio |

## Case summary (advisory)

**1000000123: 1 of 19 documented 99215 claims (5%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000123 billed 99215 on 36.0% of 1,070 claims against an expected 4.9% given patient complexity (risk-adjusted score 16.56; plain z-score vs peers 4.82). 39% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 21 claims. Of 19 documented 99215 claims, 1 (5%) were documented below the billed level, against 38% for the comparison providers. Note checks on 21 returned notes (share showing each sign): problems 43%, late 14%, unsigned 0%, data 10%. No audit trail was received. 2 of 17 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0061936: billed 99215; documented MDM level moderate, minutes not recorded. C0060959: billed 99215, patient aged 36 with 0 chronic condition(s). C0061020: billed 99215, patient aged 61 with 0 chronic condition(s). C0061110: billed 99215, patient aged 52 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000123.svg)

## Records-review sample so far

Documentation is on file for 21 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99214 | 2 | 0 | 0.0% | 8.3% |
| 99215 | 19 | 1 | 5.3% | 37.9% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (58 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0061936, C0060959, C0061020 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 43% address fewer problems than their level implies and 14% were signed late; request the audit trail for C0061936, C0060959, C0061020.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
