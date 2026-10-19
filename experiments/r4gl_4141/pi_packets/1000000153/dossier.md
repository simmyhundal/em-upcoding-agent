# Payment Integrity dossier: 1000000153

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 124 |
| Billed mix (99211 to 99215) | 8 / 7 / 96 / 99 / 31 |
| 99215 share | 12.9% |
| Expected 99215 share given patient complexity | 4.7% |
| Screen scores | z vs peers 1.09; risk-adjusted 2.31; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000153: 2 of 16 documented 99214 and 99215 claims (12%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000153 billed 99215 on 12.9% of 241 claims against an expected 4.7% given patient complexity (risk-adjusted score 2.31; plain z-score vs peers 1.09). 58% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 3 documented 99215 claims, 1 (33%) were documented below the billed level, against 20% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 47%, late 20%, unsigned 0%, data 23%, bulk created 13%, paste heavy 23%. 9 of 18 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0076548: billed 99215, patient aged 46 with 1 chronic condition(s) (depression); documented MDM level moderate, 35 minutes. C0076331: billed 99215, patient aged 78 with 1 chronic condition(s) (COPD). C0076335: billed 99215, patient aged 74 with 1 chronic condition(s) (type 2 diabetes). C0076349: billed 99215, patient aged 69 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000153.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 13 | 1 | 7.7% | 3.2% |
| 99214 | 13 | 1 | 7.7% | 5.0% |
| 99215 | 3 | 1 | 33.3% | 20.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (22 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0076548, C0076331, C0076335 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 47% address fewer problems than their level implies and 20% were signed late; request the audit trail for C0076548, C0076331, C0076335.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
