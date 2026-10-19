# Payment Integrity dossier: 1000000005

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,381 / 676 |
| Billed mix (99211 to 99215) | 8 / 22 / 293 / 782 / 276 |
| 99215 share | 20.0% |
| Expected 99215 share given patient complexity | 5.0% |
| Screen scores | z vs peers 2.00; risk-adjusted 9.89; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000005: 1 of 8 documented 99215 claims (12%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000005 billed 99215 on 20.0% of 1,381 claims against an expected 5.0% given patient complexity (risk-adjusted score 9.89; plain z-score vs peers 2.00). 53% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 8 documented 99215 claims, 1 (12%) were documented below the billed level, against 21% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 30%, late 17%, unsigned 0%, data 27%, bulk created 10%, paste heavy 10%. 8 of 27 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0001766: billed 99215; documented MDM level moderate, minutes not recorded. C0001029: billed 99215, patient aged 48 with 1 chronic condition(s) (osteoarthritis). C0001159: billed 99215, patient aged 65 with 0 chronic condition(s). C0001299: billed 99215, patient aged 80 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000005.svg)

## Records-review sample so far

Documentation is on file for 30 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 2.2% |
| 99214 | 16 | 2 | 12.5% | 8.9% |
| 99215 | 8 | 1 | 12.5% | 20.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (55 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0001766, C0001029, C0001159 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 30% address fewer problems than their level implies and 17% were signed late; request the audit trail for C0001766, C0001029, C0001159.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
