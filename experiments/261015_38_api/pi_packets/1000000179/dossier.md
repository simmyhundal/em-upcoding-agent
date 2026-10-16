# Payment Integrity dossier: 1000000179

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 369 / 180 |
| Billed mix (99211 to 99215) | 1 / 3 / 59 / 180 / 126 |
| 99215 share | 34.1% |
| Expected 99215 share given patient complexity | 2.7% |
| Screen scores | z vs peers 4.88; risk-adjusted 13.50; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000179: 0 of 8 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000179 billed 99215 on 34.1% of 369 claims against an expected 2.7% given patient complexity (risk-adjusted score 13.50; plain z-score vs peers 4.88). 52% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 8 documented 99215 claims, 0 (0%) were documented below the billed level, against 0% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 45%, late 14%, unsigned 0%, data 7%. No audit trail was received. 2 of 23 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0083453: billed 99215, patient aged 56 with 0 chronic condition(s). C0083454: billed 99215, patient aged 41 with 0 chronic condition(s). C0083465: billed 99215, patient aged 64 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000179.svg)

## Records-review sample so far

Documentation is on file for 29 claims (8% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 2 | 0 | 0.0% | 4.7% |
| 99214 | 19 | 0 | 0.0% | 2.4% |
| 99215 | 8 | 0 | 0.0% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (45 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0083453, C0083454, C0083465 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 45% address fewer problems than their level implies and 14% were signed late; request the audit trail for C0083453, C0083454, C0083465.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
