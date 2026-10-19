# Payment Integrity dossier: 1000000137

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 240 / 112 |
| Billed mix (99211 to 99215) | 2 / 0 / 53 / 135 / 50 |
| 99215 share | 20.8% |
| Expected 99215 share given patient complexity | 6.7% |
| Screen scores | z vs peers 2.14; risk-adjusted 3.29; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000137: 1 of 20 documented 99215 claims (5%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000137 billed 99215 on 20.8% of 240 claims against an expected 6.7% given patient complexity (risk-adjusted score 3.29; plain z-score vs peers 2.14). 22% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 1 (5%) were documented below the billed level, against 21% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 20%, late 20%, unsigned 0%, data 9%. No audit trail was received. 6 of 34 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0069606: billed 99215, patient aged 75 with 5 chronic condition(s) (hypothyroidism;type 2 diabetes;hypertension;osteoarthritis;chronic kidney disease); documented MDM level moderate, minutes not recorded. C0069391: billed 99215, patient aged 21 with 1 chronic condition(s) (hyperlipidemia). C0069403: billed 99215, patient aged 42 with 1 chronic condition(s) (depression). C0069424: billed 99215, patient aged 43 with 0 chronic condition(s); documented MDM level high, 51 minutes.

## Evidence chart

![99215 share by patient complexity](../../charts/1000000137.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 1 | 14.3% | 2.2% |
| 99214 | 18 | 0 | 0.0% | 8.9% |
| 99215 | 20 | 1 | 5.0% | 20.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0069606, C0069391, C0069403 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 20% address fewer problems than their level implies and 20% were signed late; request the audit trail for C0069606, C0069391, C0069403.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
