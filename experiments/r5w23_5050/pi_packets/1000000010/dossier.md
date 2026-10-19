# Payment Integrity dossier: 1000000010

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 419 / 218 |
| Billed mix (99211 to 99215) | 0 / 3 / 111 / 244 / 61 |
| 99215 share | 14.6% |
| Expected 99215 share given patient complexity | 3.8% |
| Screen scores | z vs peers 1.22; risk-adjusted 4.08; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000010: 1 of 6 documented 99215 claims (17%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000010 billed 99215 on 14.6% of 419 claims against an expected 3.8% given patient complexity (risk-adjusted score 4.08; plain z-score vs peers 1.22). 69% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 6 documented 99215 claims, 1 (17%) were documented below the billed level, against 58% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 53%, late 13%, unsigned 0%, data 0%, bulk created 0%, paste heavy 0%. 0 of 20 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0004004: billed 99215; documented MDM level moderate, minutes not recorded. C0003600: billed 99215, patient aged 30 with 0 chronic condition(s). C0003608: billed 99215, patient aged 50 with 0 chronic condition(s); documented MDM level high, minutes not recorded. C0003630: billed 99215, patient aged 49 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000010.svg)

## Records-review sample so far

Documentation is on file for 30 claims (7% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 3.1% |
| 99214 | 17 | 1 | 5.9% | 6.2% |
| 99215 | 6 | 1 | 16.7% | 57.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (33 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0004004, C0003600, C0003608 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 53% address fewer problems than their level implies and 13% were signed late; request the audit trail for C0004004, C0003600, C0003608.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
