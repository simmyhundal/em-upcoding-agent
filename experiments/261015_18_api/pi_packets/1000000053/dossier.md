# Payment Integrity dossier: 1000000053

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 539 / 271 |
| Billed mix (99211 to 99215) | 7 / 8 / 165 / 258 / 101 |
| 99215 share | 18.7% |
| Expected 99215 share given patient complexity | 1.9% |
| Screen scores | z vs peers 2.15; risk-adjusted 11.15; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000053: 7 of 7 documented 99215 claims (100%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000053 billed 99215 on 18.7% of 539 claims against an expected 1.9% given patient complexity (risk-adjusted score 11.15; plain z-score vs peers 2.15). 77% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 7 documented 99215 claims, 7 (100%) were documented below the billed level, against 5% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 50%, late 0%, unsigned 0%, data 3%, bulk created 0%, paste heavy 0%. 1 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0027887: billed 99215; documented MDM level moderate, 32 minutes. C0028082: billed 99215, patient aged 76 with 1 chronic condition(s) (hypertension); documented MDM level moderate, 30 minutes. C0028122: billed 99215; documented MDM level moderate, 39 minutes. C0027890: billed 99215, patient aged 46 with 1 chronic condition(s) (heart failure). C0027895: billed 99215, patient aged 33 with 0 chronic condition(s). C0027912: billed 99215, patient aged 44 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000053.svg)

## Records-review sample so far

Documentation is on file for 30 claims (6% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 1.6% |
| 99214 | 17 | 4 | 23.5% | 3.0% |
| 99215 | 7 | 7 | 100.0% | 4.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (41 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0027887, C0028082, C0028122 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 50% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0027887, C0028082, C0028122.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
