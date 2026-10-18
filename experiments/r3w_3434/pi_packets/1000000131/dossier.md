# Payment Integrity dossier: 1000000131

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 238 / 113 |
| Billed mix (99211 to 99215) | 3 / 7 / 57 / 108 / 63 |
| 99215 share | 26.5% |
| Expected 99215 share given patient complexity | 4.5% |
| Screen scores | z vs peers 2.72; risk-adjusted 5.47; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000131: 12 of 18 documented 99215 claims (67%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000131 billed 99215 on 26.5% of 238 claims against an expected 4.5% given patient complexity (risk-adjusted score 5.47; plain z-score vs peers 2.72). 70% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 18 documented 99215 claims, 12 (67%) were documented below the billed level, against 35% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 31%, late 2%, unsigned 0%, data 7%. No audit trail was received. 3 of 27 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0058403: billed 99215, patient aged 54 with 1 chronic condition(s) (hyperlipidemia); documented MDM level moderate, 39 minutes. C0058530: billed 99215; documented MDM level moderate, 25 minutes. C0058558: billed 99215; documented MDM level low, minutes not recorded. C0058353: billed 99215, patient aged 19 with 1 chronic condition(s) (obesity). C0058362: billed 99215, patient aged 35 with 1 chronic condition(s) (type 2 diabetes). C0058375: billed 99215, patient aged 60 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000131.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 0 | 0.0% | 5.0% |
| 99214 | 14 | 6 | 42.9% | 0.5% |
| 99215 | 18 | 12 | 66.7% | 34.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (33 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0058403, C0058530, C0058558 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 31% address fewer problems than their level implies and 2% were signed late; request the audit trail for C0058403, C0058530, C0058558.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
