# Payment Integrity dossier: 1000000166

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 246 / 119 |
| Billed mix (99211 to 99215) | 1 / 5 / 42 / 133 / 65 |
| 99215 share | 26.4% |
| Expected 99215 share given patient complexity | 8.4% |
| Screen scores | z vs peers 3.04; risk-adjusted 3.67; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000166: 0 of 10 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000166 billed 99215 on 26.4% of 246 claims against an expected 8.4% given patient complexity (risk-adjusted score 3.67; plain z-score vs peers 3.04). 20% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 10 documented 99215 claims, 0 (0%) were documented below the billed level, against 28% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 10%, late 13%, unsigned 0%, data 3%. No audit trail was received. 1 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0103158: billed 99214; documented MDM level low, minutes not recorded. C0102963: billed 99215, patient aged 31 with 1 chronic condition(s) (COPD). C0102975: billed 99215, patient aged 54 with 0 chronic condition(s). C0102980: billed 99215, patient aged 38 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000166.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 3 | 0 | 0.0% | 1.9% |
| 99214 | 15 | 1 | 6.7% | 4.7% |
| 99215 | 10 | 0 | 0.0% | 28.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (34 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0103158, C0102963, C0102975 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 10% address fewer problems than their level implies and 13% were signed late; request the audit trail for C0103158, C0102963, C0102975.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
