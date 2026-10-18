# Payment Integrity dossier: 1000000111

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 245 / 120 |
| Billed mix (99211 to 99215) | 3 / 4 / 36 / 108 / 94 |
| 99215 share | 38.4% |
| Expected 99215 share given patient complexity | 5.6% |
| Screen scores | z vs peers 5.21; risk-adjusted 8.28; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000111: 12 of 13 documented 99215 claims (92%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000111 billed 99215 on 38.4% of 245 claims against an expected 5.6% given patient complexity (risk-adjusted score 8.28; plain z-score vs peers 5.21). 47% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 13 documented 99215 claims, 12 (92%) were documented below the billed level, against 46% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 17%, late 3%, unsigned 0%, data 7%. No audit trail was received. 3 of 25 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0051428: billed 99215; documented MDM level moderate, minutes not recorded. C0051485: billed 99215; documented MDM level moderate, 32 minutes. C0051571: billed 99215; documented MDM level moderate, minutes not recorded. C0051412: billed 99215, patient aged 40 with 1 chronic condition(s) (type 2 diabetes). C0051416: billed 99215, patient aged 65 with 1 chronic condition(s) (asthma). C0051420: billed 99215, patient aged 58 with 1 chronic condition(s) (atrial fibrillation).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000111.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 1 | 0 | 0.0% | 2.8% |
| 99214 | 15 | 4 | 26.7% | 6.9% |
| 99215 | 13 | 12 | 92.3% | 45.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (40 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0051428, C0051485, C0051571 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 17% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0051428, C0051485, C0051571.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
