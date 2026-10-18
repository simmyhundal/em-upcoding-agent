# Payment Integrity dossier: 1000000106

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 114 |
| Billed mix (99211 to 99215) | 3 / 4 / 46 / 145 / 44 |
| 99215 share | 18.2% |
| Expected 99215 share given patient complexity | 3.7% |
| Screen scores | z vs peers 1.84; risk-adjusted 3.99; flagged by eb_ratio |

## Case summary (advisory)

**1000000106: 1 of 7 documented 99215 claims (14%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000106 billed 99215 on 18.2% of 242 claims against an expected 3.7% given patient complexity (risk-adjusted score 3.99; plain z-score vs peers 1.84). 70% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 7 documented 99215 claims, 1 (14%) were documented below the billed level, against 38% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 43%, late 10%, unsigned 0%, data 0%, bulk created 7%, paste heavy 10%. 0 of 21 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0055421: billed 99215; documented MDM level moderate, minutes not recorded. C0055358: billed 99215, patient aged 59 with 1 chronic condition(s) (obesity). C0055359: billed 99215, patient aged 37 with 1 chronic condition(s) (heart failure). C0055360: billed 99215, patient aged 71 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000106.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 1 | 12.5% | 3.4% |
| 99214 | 15 | 0 | 0.0% | 8.3% |
| 99215 | 7 | 1 | 14.3% | 37.9% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (27 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0055421, C0055358, C0055359 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 43% address fewer problems than their level implies and 10% were signed late; request the audit trail for C0055421, C0055358, C0055359.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
