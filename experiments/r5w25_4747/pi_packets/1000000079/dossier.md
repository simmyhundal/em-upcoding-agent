# Payment Integrity dossier: 1000000079

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 569 / 273 |
| Billed mix (99211 to 99215) | 8 / 25 / 183 / 239 / 114 |
| 99215 share | 20.0% |
| Expected 99215 share given patient complexity | 4.0% |
| Screen scores | z vs peers 1.99; risk-adjusted 6.89; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000079: 16 of 20 documented 99215 claims (80%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000079 billed 99215 on 20.0% of 569 claims against an expected 4.0% given patient complexity (risk-adjusted score 6.89; plain z-score vs peers 1.99). 82% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 16 (80%) were documented below the billed level, against 32% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 36%, late 2%, unsigned 0%, data 7%. No audit trail was received. 4 of 26 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0042735: billed 99215, patient aged 47 with 0 chronic condition(s); documented MDM level moderate, 33 minutes. C0042749: billed 99215; documented MDM level moderate, 39 minutes. C0042990: billed 99215; documented MDM level moderate, 38 minutes. C0042549: billed 99215, patient aged 18 with 0 chronic condition(s). C0042557: billed 99215, patient aged 57 with 0 chronic condition(s). C0042561: billed 99215, patient aged 67 with 1 chronic condition(s) (chronic kidney disease).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000079.svg)

## Records-review sample so far

Documentation is on file for 45 claims (8% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 12 | 0 | 0.0% | 2.8% |
| 99214 | 12 | 5 | 41.7% | 6.3% |
| 99215 | 20 | 16 | 80.0% | 32.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (43 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0042735, C0042749, C0042990 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 36% address fewer problems than their level implies and 2% were signed late; request the audit trail for C0042735, C0042749, C0042990.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
