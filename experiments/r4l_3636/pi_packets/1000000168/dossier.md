# Payment Integrity dossier: 1000000168

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 124 |
| Billed mix (99211 to 99215) | 1 / 1 / 42 / 148 / 49 |
| 99215 share | 20.3% |
| Expected 99215 share given patient complexity | 6.1% |
| Screen scores | z vs peers 1.91; risk-adjusted 3.24; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000168: 0 of 23 documented 99214 and 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000168 billed 99215 on 20.3% of 241 claims against an expected 6.1% given patient complexity (risk-adjusted score 3.24; plain z-score vs peers 1.91). 31% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 4 documented 99215 claims, 0 (0%) were documented below the billed level, against 27% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 23%, late 17%, unsigned 0%, data 17%. No audit trail was received. 5 of 24 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0092150: billed 99215, patient aged 59 with 1 chronic condition(s) (hypertension). C0092158: billed 99215, patient aged 29 with 1 chronic condition(s) (hypertension). C0092167: billed 99215, patient aged 53 with 1 chronic condition(s) (osteoarthritis).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000168.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 0.0% |
| 99214 | 19 | 0 | 0.0% | 5.3% |
| 99215 | 4 | 0 | 0.0% | 26.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0092150, C0092158, C0092167 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 23% address fewer problems than their level implies and 17% were signed late; request the audit trail for C0092150, C0092158, C0092167.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
