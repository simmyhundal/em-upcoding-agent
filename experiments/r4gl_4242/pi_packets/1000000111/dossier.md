# Payment Integrity dossier: 1000000111

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 243 / 113 |
| Billed mix (99211 to 99215) | 2 / 4 / 48 / 145 / 44 |
| 99215 share | 18.1% |
| Expected 99215 share given patient complexity | 4.9% |
| Screen scores | z vs peers 2.10; risk-adjusted 3.90; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000111: 0 of 7 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000111 billed 99215 on 18.1% of 243 claims against an expected 4.9% given patient complexity (risk-adjusted score 3.90; plain z-score vs peers 2.10). 55% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 7 documented 99215 claims, 0 (0%) were documented below the billed level, against 41% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 40%, late 20%, unsigned 0%, data 27%, bulk created 20%, paste heavy 13%. 8 of 23 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0062039: billed 99213; documented MDM level straightforward, minutes not recorded. C0062089: billed 99214; documented MDM level low, minutes not recorded. C0061949: billed 99215, patient aged 30 with 1 chronic condition(s) (obesity). C0061964: billed 99215, patient aged 27 with 1 chronic condition(s) (COPD); documented MDM level high, 44 minutes. C0061977: billed 99215, patient aged 45 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000111.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 1 | 20.0% | 6.5% |
| 99214 | 17 | 1 | 5.9% | 6.6% |
| 99215 | 7 | 0 | 0.0% | 41.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (27 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0062039, C0062089, C0061949 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 40% address fewer problems than their level implies and 20% were signed late; request the audit trail for C0062039, C0062089, C0061949.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
