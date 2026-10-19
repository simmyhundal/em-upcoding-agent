# Payment Integrity dossier: 1000000147

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 244 / 116 |
| Billed mix (99211 to 99215) | 2 / 8 / 74 / 110 / 50 |
| 99215 share | 20.5% |
| Expected 99215 share given patient complexity | 5.6% |
| Screen scores | z vs peers 3.02; risk-adjusted 4.57; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000147: 3 of 24 documented 99215 claims (12%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000147 billed 99215 on 20.5% of 244 claims against an expected 5.6% given patient complexity (risk-adjusted score 4.57; plain z-score vs peers 3.02). 38% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 24 documented 99215 claims, 3 (12%) were documented below the billed level, against 30% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 16%, late 24%, unsigned 0%, data 9%. No audit trail was received. 6 of 34 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0084387: billed 99215, patient aged 59 with 5 chronic condition(s) (hypothyroidism;hyperlipidemia;heart failure;COPD;osteoarthritis); documented MDM level moderate, minutes not recorded. C0084479: billed 99215, patient aged 45 with 1 chronic condition(s) (hyperlipidemia); documented MDM level moderate, minutes not recorded. C0084491: billed 99215, patient aged 49 with 1 chronic condition(s) (obesity); documented MDM level moderate, minutes not recorded. C0084332: billed 99215, patient aged 46 with 1 chronic condition(s) (hyperlipidemia). C0084384: billed 99215, patient aged 67 with 1 chronic condition(s) (hyperlipidemia). C0084385: billed 99215, patient aged 27 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000147.svg)

## Records-review sample so far

Documentation is on file for 45 claims (18% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 0 | 0.0% | 4.7% |
| 99214 | 10 | 0 | 0.0% | 4.4% |
| 99215 | 24 | 3 | 12.5% | 30.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0084387, C0084479, C0084491 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 16% address fewer problems than their level implies and 24% were signed late; request the audit trail for C0084387, C0084479, C0084491.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
