# Payment Integrity dossier: 1000000029

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 433 / 208 |
| Billed mix (99211 to 99215) | 2 / 4 / 75 / 274 / 78 |
| 99215 share | 18.0% |
| Expected 99215 share given patient complexity | 4.5% |
| Screen scores | z vs peers 2.01; risk-adjusted 5.30; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000029: 10 of 20 documented 99215 claims (50%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000029 billed 99215 on 18.0% of 433 claims against an expected 4.5% given patient complexity (risk-adjusted score 5.30; plain z-score vs peers 2.01). 62% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 10 (50%) were documented below the billed level, against 20% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 44%, late 0%, unsigned 0%, data 7%, bulk created 0%, paste heavy 0%. 3 of 38 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0010044: billed 99215; documented MDM level moderate, 30 minutes. C0010087: billed 99215, patient aged 43 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0010118: billed 99215; documented MDM level moderate, minutes not recorded. C0010024: billed 99215, patient aged 45 with 0 chronic condition(s). C0010037: billed 99215, patient aged 43 with 1 chronic condition(s) (hypertension). C0010054: billed 99215, patient aged 30 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000029.svg)

## Records-review sample so far

Documentation is on file for 45 claims (10% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 3 | 0 | 0.0% | 3.2% |
| 99214 | 22 | 0 | 0.0% | 5.0% |
| 99215 | 20 | 10 | 50.0% | 20.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (37 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0010044, C0010087, C0010118 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 44% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0010044, C0010087, C0010118.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
