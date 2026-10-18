# Payment Integrity dossier: 1000000052

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 306 / 155 |
| Billed mix (99211 to 99215) | 6 / 4 / 93 / 136 / 67 |
| 99215 share | 21.9% |
| Expected 99215 share given patient complexity | 3.9% |
| Screen scores | z vs peers 2.53; risk-adjusted 6.07; flagged by eb_ratio |

## Case summary (advisory)

**1000000052: 17 of 19 documented 99215 claims (90%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000052 billed 99215 on 21.9% of 306 claims against an expected 3.9% given patient complexity (risk-adjusted score 6.07; plain z-score vs peers 2.53). 75% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 17 (90%) were documented below the billed level, against 31% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 47%, late 7%, unsigned 0%, data 2%. No audit trail was received. 3 of 23 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0029410: billed 99215, patient aged 55 with 0 chronic condition(s); documented MDM level moderate, 33 minutes. C0029431: billed 99215; documented MDM level moderate, minutes not recorded. C0029460: billed 99215; documented MDM level moderate, minutes not recorded. C0029166: billed 99215, patient aged 40 with 0 chronic condition(s). C0029174: billed 99215, patient aged 46 with 1 chronic condition(s) (obesity). C0029176: billed 99215, patient aged 45 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000052.svg)

## Records-review sample so far

Documentation is on file for 45 claims (15% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 1 | 16.7% | 4.9% |
| 99214 | 19 | 5 | 26.3% | 6.6% |
| 99215 | 19 | 17 | 89.5% | 30.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (34 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0029410, C0029431, C0029460 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 47% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0029410, C0029431, C0029460.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
