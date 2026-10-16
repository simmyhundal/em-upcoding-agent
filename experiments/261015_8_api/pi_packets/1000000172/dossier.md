# Payment Integrity dossier: 1000000172

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 108 |
| Billed mix (99211 to 99215) | 3 / 1 / 48 / 118 / 72 |
| 99215 share | 29.8% |
| Expected 99215 share given patient complexity | 4.3% |
| Screen scores | z vs peers 4.87; risk-adjusted 7.83; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000172: 9 of 12 documented 99215 claims (75%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000172 billed 99215 on 29.8% of 242 claims against an expected 4.3% given patient complexity (risk-adjusted score 7.83; plain z-score vs peers 4.87). 22% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 12 documented 99215 claims, 9 (75%) were documented below the billed level, against 7% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 14%, late 0%, unsigned 0%, data 0%. No audit trail was received. 0 of 21 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0092176: billed 99215, patient aged 35 with 1 chronic condition(s) (hyperlipidemia); documented MDM level moderate, 34 minutes. C0092224: billed 99215; documented MDM level moderate, 39 minutes. C0092254: billed 99215, patient aged 46 with 1 chronic condition(s) (hyperlipidemia); documented MDM level moderate, minutes not recorded. C0092174: billed 99215, patient aged 35 with 1 chronic condition(s) (hypertension). C0092234: billed 99215, patient aged 65 with 1 chronic condition(s) (depression).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000172.svg)

## Records-review sample so far

Documentation is on file for 29 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 3.8% |
| 99214 | 10 | 1 | 10.0% | 2.2% |
| 99215 | 12 | 9 | 75.0% | 6.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (36 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0092176, C0092224, C0092254 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 14% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0092176, C0092224, C0092254.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
