# Payment Integrity dossier: 1000000029

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 113 |
| Billed mix (99211 to 99215) | 1 / 7 / 64 / 105 / 64 |
| 99215 share | 26.6% |
| Expected 99215 share given patient complexity | 5.3% |
| Screen scores | z vs peers 4.26; risk-adjusted 6.54; flagged by eb_ratio |

## Case summary (advisory)

**1000000029: 9 of 10 documented 99215 claims (90%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000029 billed 99215 on 26.6% of 241 claims against an expected 5.3% given patient complexity (risk-adjusted score 6.54; plain z-score vs peers 4.26). 53% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 10 documented 99215 claims, 9 (90%) were documented below the billed level, against 32% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 17%, late 3%, unsigned 0%, data 7%. No audit trail was received. 3 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0012118: billed 99215; documented MDM level moderate, 30 minutes. C0012123: billed 99215, patient aged 41 with 4 chronic condition(s) (hyperlipidemia;depression;asthma;osteoarthritis); documented MDM level moderate, 34 minutes. C0012151: billed 99215; documented MDM level moderate, minutes not recorded. C0012130: billed 99215, patient aged 61 with 1 chronic condition(s) (hypertension). C0012136: billed 99215, patient aged 59 with 0 chronic condition(s). C0012147: billed 99215, patient aged 25 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000029.svg)

## Records-review sample so far

Documentation is on file for 29 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 3.3% |
| 99214 | 13 | 0 | 0.0% | 5.9% |
| 99215 | 10 | 9 | 90.0% | 32.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (34 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0012118, C0012123, C0012151 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 17% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0012118, C0012123, C0012151.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
