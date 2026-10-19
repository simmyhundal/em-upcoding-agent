# Payment Integrity dossier: 1000000093

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 403 / 198 |
| Billed mix (99211 to 99215) | 4 / 6 / 132 / 184 / 77 |
| 99215 share | 19.1% |
| Expected 99215 share given patient complexity | 3.9% |
| Screen scores | z vs peers 2.26; risk-adjusted 5.71; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000093: 18 of 23 documented 99215 claims (78%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000093 billed 99215 on 19.1% of 403 claims against an expected 3.9% given patient complexity (risk-adjusted score 5.71; plain z-score vs peers 2.26). 75% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 44 claims. Of 23 documented 99215 claims, 18 (78%) were documented below the billed level, against 48% for the comparison providers. Note checks on 44 returned notes (share showing each sign): problems 43%, late 4%, unsigned 0%, data 2%, bulk created 0%, paste heavy 0%. 4 of 34 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0039033: billed 99215; documented MDM level moderate, 37 minutes. C0039079: billed 99215; documented MDM level moderate, minutes not recorded. C0039357: billed 99215; documented MDM level moderate, 37 minutes. C0038999: billed 99215, patient aged 42 with 0 chronic condition(s). C0039013: billed 99215, patient aged 42 with 1 chronic condition(s) (obesity); documented MDM level high, 33 minutes. C0039036: billed 99215, patient aged 31 with 1 chronic condition(s) (hypothyroidism).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000093.svg)

## Records-review sample so far

Documentation is on file for 44 claims (11% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 1 | 25.0% | 4.7% |
| 99214 | 17 | 4 | 23.5% | 4.7% |
| 99215 | 23 | 18 | 78.3% | 48.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (37 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0039033, C0039079, C0039357 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 43% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0039033, C0039079, C0039357.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
