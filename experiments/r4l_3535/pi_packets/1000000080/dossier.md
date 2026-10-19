# Payment Integrity dossier: 1000000080

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 251 / 115 |
| Billed mix (99211 to 99215) | 8 / 7 / 72 / 133 / 31 |
| 99215 share | 12.4% |
| Expected 99215 share given patient complexity | 5.4% |
| Screen scores | z vs peers 0.75; risk-adjusted 1.71; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000080: 0 of 20 documented 99214 and 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000080 billed 99215 on 12.4% of 251 claims against an expected 5.4% given patient complexity (risk-adjusted score 1.71; plain z-score vs peers 0.75). 48% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 5 documented 99215 claims, 0 (0%) were documented below the billed level, against 24% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 37%, late 20%, unsigned 0%, data 20%, bulk created 7%, paste heavy 10%. 8 of 21 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0042988: billed 99215, patient aged 74 with 1 chronic condition(s) (type 2 diabetes). C0043006: billed 99215, patient aged 33 with 1 chronic condition(s) (COPD). C0043007: billed 99215, patient aged 42 with 1 chronic condition(s) (heart failure).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000080.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 0 | 0.0% | 2.7% |
| 99214 | 15 | 0 | 0.0% | 7.1% |
| 99215 | 5 | 0 | 0.0% | 23.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (22 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0042988, C0043006, C0043007 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 37% address fewer problems than their level implies and 20% were signed late; request the audit trail for C0042988, C0043006, C0043007.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
