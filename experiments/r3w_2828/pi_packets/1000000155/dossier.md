# Payment Integrity dossier: 1000000155

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 116 |
| Billed mix (99211 to 99215) | 5 / 5 / 108 / 100 / 24 |
| 99215 share | 9.9% |
| Expected 99215 share given patient complexity | 3.6% |
| Screen scores | z vs peers 0.66; risk-adjusted 2.00; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000155: 8 of 15 documented 99214 and 99215 claims (53%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000155 billed 99215 on 9.9% of 242 claims against an expected 3.6% given patient complexity (risk-adjusted score 2.00; plain z-score vs peers 0.66). 67% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 3 documented 99215 claims, 3 (100%) were documented below the billed level, against 43% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 24%, late 3%, unsigned 0%, data 0%. No audit trail was received. 1 of 11 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0080058: billed 99215, patient aged 34 with 1 chronic condition(s) (osteoarthritis); documented MDM level moderate, 37 minutes. C0080194: billed 99215, patient aged 54 with 1 chronic condition(s) (hypertension); documented MDM level moderate, 39 minutes. C0080213: billed 99215; documented MDM level moderate, minutes not recorded. C0080031: billed 99215, patient aged 40 with 1 chronic condition(s) (hyperlipidemia). C0080065: billed 99215, patient aged 44 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000155.svg)

## Records-review sample so far

Documentation is on file for 29 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 12 | 0 | 0.0% | 2.4% |
| 99214 | 12 | 5 | 41.7% | 4.8% |
| 99215 | 3 | 3 | 100.0% | 43.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (24 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0080058, C0080194, C0080213 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 24% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0080058, C0080194, C0080213.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
