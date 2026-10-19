# Payment Integrity dossier: 1000000085

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 336 / 164 |
| Billed mix (99211 to 99215) | 8 / 10 / 121 / 142 / 55 |
| 99215 share | 16.4% |
| Expected 99215 share given patient complexity | 3.6% |
| Screen scores | z vs peers 1.75; risk-adjusted 4.59; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000085: 19 of 21 documented 99215 claims (90%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000085 billed 99215 on 16.4% of 336 claims against an expected 3.6% given patient complexity (risk-adjusted score 4.59; plain z-score vs peers 1.75). 78% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 21 documented 99215 claims, 19 (90%) were documented below the billed level, against 48% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 38%, late 7%, unsigned 0%, data 4%. No audit trail was received. 2 of 26 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0035960: billed 99215; documented MDM level moderate, 31 minutes. C0036153: billed 99215; documented MDM level moderate, 31 minutes. C0036194: billed 99215; documented MDM level moderate, 36 minutes. C0035865: billed 99215, patient aged 43 with 0 chronic condition(s). C0035902: billed 99215, patient aged 44 with 0 chronic condition(s). C0035938: billed 99215, patient aged 57 with 1 chronic condition(s) (osteoarthritis).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000085.svg)

## Records-review sample so far

Documentation is on file for 45 claims (13% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 17 | 3 | 17.6% | 4.7% |
| 99214 | 7 | 2 | 28.6% | 4.7% |
| 99215 | 21 | 19 | 90.5% | 48.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (31 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0035960, C0036153, C0036194 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 38% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0035960, C0036153, C0036194.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
