# Payment Integrity dossier: 1000000108

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 743 / 370 |
| Billed mix (99211 to 99215) | 2 / 9 / 130 / 410 / 192 |
| 99215 share | 25.8% |
| Expected 99215 share given patient complexity | 6.3% |
| Screen scores | z vs peers 2.73; risk-adjusted 7.92; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000108: 16 of 23 documented 99215 claims (70%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000108 billed 99215 on 25.8% of 743 claims against an expected 6.3% given patient complexity (risk-adjusted score 7.92; plain z-score vs peers 2.73). 37% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 23 documented 99215 claims, 16 (70%) were documented below the billed level, against 27% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 16%, late 2%, unsigned 0%, data 4%. No audit trail was received. 6 of 35 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0058390: billed 99215; documented MDM level moderate, 39 minutes. C0058540: billed 99215; documented MDM level moderate, 34 minutes. C0058724: billed 99215; documented MDM level moderate, 35 minutes. C0058170: billed 99215, patient aged 18 with 0 chronic condition(s). C0058187: billed 99215, patient aged 38 with 1 chronic condition(s) (type 2 diabetes). C0058235: billed 99215, patient aged 72 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000108.svg)

## Records-review sample so far

Documentation is on file for 45 claims (6% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 0.0% |
| 99214 | 18 | 4 | 22.2% | 5.3% |
| 99215 | 23 | 16 | 69.6% | 26.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (51 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0058390, C0058540, C0058724 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 16% address fewer problems than their level implies and 2% were signed late; request the audit trail for C0058390, C0058540, C0058724.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
