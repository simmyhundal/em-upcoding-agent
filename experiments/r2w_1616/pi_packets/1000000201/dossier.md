# Payment Integrity dossier: 1000000201

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 336 / 165 |
| Billed mix (99211 to 99215) | 5 / 6 / 114 / 145 / 66 |
| 99215 share | 19.6% |
| Expected 99215 share given patient complexity | 3.3% |
| Screen scores | z vs peers 2.18; risk-adjusted 7.13; flagged by eb_ratio |

## Case summary (advisory)

**1000000201: 6 of 8 documented 99215 claims (75%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000201 billed 99215 on 19.6% of 336 claims against an expected 3.3% given patient complexity (risk-adjusted score 7.13; plain z-score vs peers 2.18). 86% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 24 claims. Of 8 documented 99215 claims, 6 (75%) were documented below the billed level, against 43% for the comparison providers. Note checks on 24 returned notes (share showing each sign): problems 29%, late 0%, unsigned 0%, data 4%. No audit trail was received. 1 of 14 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0114807: billed 99215, patient aged 23 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0114864: billed 99215; documented MDM level moderate, 36 minutes. C0114865: billed 99215, patient aged 46 with 0 chronic condition(s); documented MDM level moderate, 30 minutes. C0114736: billed 99215, patient aged 71 with 1 chronic condition(s) (hypertension). C0114749: billed 99215, patient aged 37 with 0 chronic condition(s). C0114769: billed 99215, patient aged 55 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000201.svg)

## Records-review sample so far

Documentation is on file for 24 claims (7% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 3.4% |
| 99214 | 12 | 5 | 41.7% | 6.1% |
| 99215 | 8 | 6 | 75.0% | 42.9% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (34 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0114807, C0114864, C0114865 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 29% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0114807, C0114864, C0114865.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
