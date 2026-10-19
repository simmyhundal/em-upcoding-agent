# Payment Integrity dossier: 1000000032

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 240 / 117 |
| Billed mix (99211 to 99215) | 1 / 5 / 48 / 138 / 48 |
| 99215 share | 20.0% |
| Expected 99215 share given patient complexity | 4.8% |
| Screen scores | z vs peers 2.96; risk-adjusted 4.42; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000032: 7 of 20 documented 99214 and 99215 claims (35%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000032 billed 99215 on 20.0% of 240 claims against an expected 4.8% given patient complexity (risk-adjusted score 4.42; plain z-score vs peers 2.96). 40% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 21 claims. Of 4 documented 99215 claims, 2 (50%) were documented below the billed level, against 47% for the comparison providers. Note checks on 21 returned notes (share showing each sign): problems 29%, late 5%, unsigned 0%, data 0%. No audit trail was received. 0 of 17 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0015805: billed 99215, patient aged 44 with 0 chronic condition(s); documented MDM level moderate, 32 minutes. C0015854: billed 99215, patient aged 58 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0015729: billed 99215, patient aged 37 with 0 chronic condition(s). C0015746: billed 99215, patient aged 38 with 0 chronic condition(s). C0015786: billed 99215, patient aged 39 with 1 chronic condition(s) (osteoarthritis).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000032.svg)

## Records-review sample so far

Documentation is on file for 21 claims (9% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 1 | 0 | 0.0% | 3.6% |
| 99214 | 16 | 5 | 31.2% | 6.1% |
| 99215 | 4 | 2 | 50.0% | 46.9% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0015805, C0015854, C0015729 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 29% address fewer problems than their level implies and 5% were signed late; request the audit trail for C0015805, C0015854, C0015729.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
