# Payment Integrity dossier: 1000000133

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 451 / 229 |
| Billed mix (99211 to 99215) | 8 / 15 / 140 / 214 / 74 |
| 99215 share | 16.4% |
| Expected 99215 share given patient complexity | 4.4% |
| Screen scores | z vs peers 1.44; risk-adjusted 4.75; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000133: 0 of 6 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000133 billed 99215 on 16.4% of 451 claims against an expected 4.4% given patient complexity (risk-adjusted score 4.75; plain z-score vs peers 1.44). 61% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 6 documented 99215 claims, 0 (0%) were documented below the billed level, against 21% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 27%, late 27%, unsigned 0%, data 27%. No audit trail was received. 9 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0067330: billed 99214; documented MDM level low, minutes not recorded. C0067616: billed 99214; documented MDM level low, minutes not recorded. C0067248: billed 99215, patient aged 18 with 0 chronic condition(s). C0067257: billed 99215, patient aged 47 with 0 chronic condition(s). C0067271: billed 99215, patient aged 58 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000133.svg)

## Records-review sample so far

Documentation is on file for 30 claims (7% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 2.2% |
| 99214 | 15 | 2 | 13.3% | 8.9% |
| 99215 | 6 | 0 | 0.0% | 20.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (36 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0067330, C0067616, C0067248 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 27% address fewer problems than their level implies and 27% were signed late; request the audit trail for C0067330, C0067616, C0067248.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
