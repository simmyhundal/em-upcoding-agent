# Payment Integrity dossier: 1000000151

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 234 / 115 |
| Billed mix (99211 to 99215) | 2 / 3 / 58 / 120 / 51 |
| 99215 share | 21.8% |
| Expected 99215 share given patient complexity | 3.1% |
| Screen scores | z vs peers 2.81; risk-adjusted 5.86; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000151: 7 of 8 documented 99215 claims (88%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000151 billed 99215 on 21.8% of 234 claims against an expected 3.1% given patient complexity (risk-adjusted score 5.86; plain z-score vs peers 2.81). 47% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 8 documented 99215 claims, 7 (88%) were documented below the billed level, against 0% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 17%, late 7%, unsigned 0%, data 0%. No audit trail was received. 1 of 17 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0067627: billed 99215, patient aged 54 with 1 chronic condition(s) (atrial fibrillation); documented MDM level moderate, 33 minutes. C0067638: billed 99215; documented MDM level moderate, 33 minutes. C0067726: billed 99215; documented MDM level moderate, 23 minutes. C0067581: billed 99215, patient aged 27 with 0 chronic condition(s). C0067593: billed 99215, patient aged 70 with 0 chronic condition(s). C0067596: billed 99215, patient aged 73 with 1 chronic condition(s) (depression).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000151.svg)

## Records-review sample so far

Documentation is on file for 29 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 0 | 0.0% | 4.7% |
| 99214 | 13 | 4 | 30.8% | 2.4% |
| 99215 | 8 | 7 | 87.5% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (30 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0067627, C0067638, C0067726 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 17% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0067627, C0067638, C0067726.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
