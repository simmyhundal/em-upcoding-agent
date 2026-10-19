# Payment Integrity dossier: 1000000098

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 450 / 232 |
| Billed mix (99211 to 99215) | 3 / 8 / 119 / 218 / 102 |
| 99215 share | 22.7% |
| Expected 99215 share given patient complexity | 4.4% |
| Screen scores | z vs peers 2.71; risk-adjusted 6.70; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000098: 0 of 24 documented 99214 and 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000098 billed 99215 on 22.7% of 450 claims against an expected 4.4% given patient complexity (risk-adjusted score 6.70; plain z-score vs peers 2.71). 62% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 4 documented 99215 claims, 0 (0%) were documented below the billed level, against 40% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 40%, late 20%, unsigned 0%, data 23%, bulk created 10%, paste heavy 17%. 9 of 23 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0052033: billed 99215, patient aged 56 with 1 chronic condition(s) (osteoarthritis). C0052048: billed 99215, patient aged 72 with 0 chronic condition(s). C0052068: billed 99215, patient aged 67 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000098.svg)

## Records-review sample so far

Documentation is on file for 30 claims (7% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 2.9% |
| 99214 | 20 | 0 | 0.0% | 4.6% |
| 99215 | 4 | 0 | 0.0% | 40.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (41 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0052033, C0052048, C0052068 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 40% address fewer problems than their level implies and 20% were signed late; request the audit trail for C0052033, C0052048, C0052068.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
