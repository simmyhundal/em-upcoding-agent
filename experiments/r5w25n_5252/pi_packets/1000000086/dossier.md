# Payment Integrity dossier: 1000000086

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 243 / 120 |
| Billed mix (99211 to 99215) | 1 / 2 / 34 / 122 / 84 |
| 99215 share | 34.6% |
| Expected 99215 share given patient complexity | 3.5% |
| Screen scores | z vs peers 5.45; risk-adjusted 10.00; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000086: 15 of 26 documented 99215 claims (58%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000086 billed 99215 on 34.6% of 243 claims against an expected 3.5% given patient complexity (risk-adjusted score 10.00; plain z-score vs peers 5.45). 88% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 26 documented 99215 claims, 15 (58%) were documented below the billed level, against 24% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 58%, late 0%, unsigned 0%, data 4%. No audit trail was received. 3 of 36 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0042047: billed 99215; documented MDM level moderate, 22 minutes. C0042055: billed 99215; documented MDM level moderate, 35 minutes. C0042057: billed 99215, patient aged 46 with 1 chronic condition(s) (atrial fibrillation); documented MDM level moderate, 36 minutes. C0041937: billed 99215, patient aged 55 with 0 chronic condition(s). C0041943: billed 99215, patient aged 78 with 1 chronic condition(s) (hyperlipidemia). C0041964: billed 99215, patient aged 35 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000086.svg)

## Records-review sample so far

Documentation is on file for 45 claims (18% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 1 | 0 | 0.0% | 1.8% |
| 99214 | 17 | 2 | 11.8% | 5.2% |
| 99215 | 26 | 15 | 57.7% | 24.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (38 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0042047, C0042055, C0042057 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 58% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0042047, C0042055, C0042057.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
