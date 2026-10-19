# Payment Integrity dossier: 1000000036

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 126 |
| Billed mix (99211 to 99215) | 0 / 2 / 30 / 119 / 90 |
| 99215 share | 37.3% |
| Expected 99215 share given patient complexity | 6.8% |
| Screen scores | z vs peers 4.61; risk-adjusted 7.30; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000036: 9 of 16 documented 99215 claims (56%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000036 billed 99215 on 37.3% of 241 claims against an expected 6.8% given patient complexity (risk-adjusted score 7.30; plain z-score vs peers 4.61). 38% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 16 documented 99215 claims, 9 (56%) were documented below the billed level, against 24% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 33%, late 3%, unsigned 0%, data 3%. No audit trail was received. 3 of 23 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0018382: billed 99215; documented MDM level moderate, minutes not recorded. C0018483: billed 99215; documented MDM level moderate, 25 minutes. C0018513: billed 99215; documented MDM level moderate, minutes not recorded. C0018401: billed 99215, patient aged 56 with 1 chronic condition(s) (heart failure); documented MDM level high, 51 minutes. C0018415: billed 99215, patient aged 53 with 0 chronic condition(s). C0018422: billed 99215, patient aged 32 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000036.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 2 | 0 | 0.0% | 2.7% |
| 99214 | 12 | 2 | 16.7% | 7.1% |
| 99215 | 16 | 9 | 56.2% | 23.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (39 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0018382, C0018483, C0018513 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 33% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0018382, C0018483, C0018513.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
