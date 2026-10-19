# Payment Integrity dossier: 1000000031

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 235 / 114 |
| Billed mix (99211 to 99215) | 3 / 8 / 78 / 100 / 46 |
| 99215 share | 19.6% |
| Expected 99215 share given patient complexity | 3.9% |
| Screen scores | z vs peers 2.38; risk-adjusted 5.12; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000031: 0 of 7 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000031 billed 99215 on 19.6% of 235 claims against an expected 3.9% given patient complexity (risk-adjusted score 5.12; plain z-score vs peers 2.38). 78% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 24 claims. Of 7 documented 99215 claims, 0 (0%) were documented below the billed level, against 41% for the comparison providers. Note checks on 24 returned notes (share showing each sign): problems 62%, late 21%, unsigned 0%, data 17%, bulk created 21%, paste heavy 29%. 5 of 13 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0018362: billed 99215, patient aged 45 with 0 chronic condition(s). C0018363: billed 99215, patient aged 64 with 1 chronic condition(s) (obesity). C0018387: billed 99215, patient aged 76 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000031.svg)

## Records-review sample so far

Documentation is on file for 24 claims (10% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 6.5% |
| 99214 | 9 | 0 | 0.0% | 6.6% |
| 99215 | 7 | 0 | 0.0% | 41.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (28 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0018362, C0018363, C0018387 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 62% address fewer problems than their level implies and 21% were signed late; request the audit trail for C0018362, C0018363, C0018387.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
