# Payment Integrity dossier: 1000000213

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,390 / 1,189 |
| Billed mix (99211 to 99215) | 5 / 30 / 475 / 1,533 / 347 |
| 99215 share | 14.5% |
| Expected 99215 share given patient complexity | 3.6% |
| Screen scores | z vs peers 1.05; risk-adjusted 11.54; flagged by eb_ratio |

## Case summary (advisory)

**1000000213: 4 of 6 documented 99215 claims (67%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000213 billed 99215 on 14.5% of 2,390 claims against an expected 3.6% given patient complexity (risk-adjusted score 11.54; plain z-score vs peers 1.05). 80% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 6 documented 99215 claims, 4 (67%) were documented below the billed level, against 39% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 48%, late 3%, unsigned 0%, data 3%, bulk created 0%, paste heavy 3%. 1 of 20 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0108460: billed 99215; documented MDM level moderate, 26 minutes. C0109467: billed 99215; documented MDM level moderate, 38 minutes. C0109601: billed 99215; documented MDM level moderate, minutes not recorded. C0108416: billed 99215, patient aged 36 with 0 chronic condition(s). C0108766: billed 99215, patient aged 77 with 1 chronic condition(s) (osteoarthritis). C0108852: billed 99215, patient aged 49 with 1 chronic condition(s) (depression).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000213.svg)

## Records-review sample so far

Documentation is on file for 29 claims (1% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 3.6% |
| 99214 | 18 | 2 | 11.1% | 4.2% |
| 99215 | 6 | 4 | 66.7% | 39.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (57 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0108460, C0109467, C0109601 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 48% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0108460, C0109467, C0109601.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
