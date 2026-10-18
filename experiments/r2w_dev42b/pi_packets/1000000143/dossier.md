# Payment Integrity dossier: 1000000143

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,372 / 1,155 |
| Billed mix (99211 to 99215) | 5 / 7 / 210 / 1,393 / 757 |
| 99215 share | 31.9% |
| Expected 99215 share given patient complexity | 6.7% |
| Screen scores | z vs peers 4.14; risk-adjusted 19.32; flagged by eb_ratio |

## Case summary (advisory)

**1000000143: 6 of 9 documented 99215 claims (67%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000143 billed 99215 on 31.9% of 2,372 claims against an expected 6.7% given patient complexity (risk-adjusted score 19.32; plain z-score vs peers 4.14). 32% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 9 documented 99215 claims, 6 (67%) were documented below the billed level, against 54% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 13%, late 10%, unsigned 0%, data 3%. No audit trail was received. 3 of 24 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0077174: billed 99215; documented MDM level moderate, 32 minutes. C0077337: billed 99215; documented MDM level moderate, 36 minutes. C0077551: billed 99215; documented MDM level moderate, minutes not recorded. C0076642: billed 99215, patient aged 38 with 0 chronic condition(s). C0076702: billed 99215, patient aged 36 with 0 chronic condition(s). C0076710: billed 99215, patient aged 58 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000143.svg)

## Records-review sample so far

Documentation is on file for 30 claims (1% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 3 | 0 | 0.0% | 3.4% |
| 99214 | 18 | 2 | 11.1% | 8.5% |
| 99215 | 9 | 6 | 66.7% | 53.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (63 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0077174, C0077337, C0077551 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 13% address fewer problems than their level implies and 10% were signed late; request the audit trail for C0077174, C0077337, C0077551.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
