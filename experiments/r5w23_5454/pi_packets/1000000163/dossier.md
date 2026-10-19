# Payment Integrity dossier: 1000000163

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 943 / 449 |
| Billed mix (99211 to 99215) | 4 / 30 / 290 / 512 / 107 |
| 99215 share | 11.3% |
| Expected 99215 share given patient complexity | 3.9% |
| Screen scores | z vs peers 0.58; risk-adjusted 4.78; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000163: 2 of 19 documented 99215 claims (10%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000163 billed 99215 on 11.3% of 943 claims against an expected 3.9% given patient complexity (risk-adjusted score 4.78; plain z-score vs peers 0.58). 84% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 2 (10%) were documented below the billed level, against 22% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 56%, late 24%, unsigned 0%, data 16%, bulk created 2%, paste heavy 2%. 8 of 33 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0077769: billed 99215; documented MDM level moderate, minutes not recorded. C0077880: billed 99215; documented MDM level moderate, 35 minutes. C0077090: billed 99215, patient aged 57 with 1 chronic condition(s) (hypertension). C0077128: billed 99215, patient aged 49 with 1 chronic condition(s) (osteoarthritis). C0077185: billed 99215, patient aged 40 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000163.svg)

## Records-review sample so far

Documentation is on file for 45 claims (5% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 11 | 0 | 0.0% | 4.1% |
| 99214 | 15 | 2 | 13.3% | 7.3% |
| 99215 | 19 | 2 | 10.5% | 22.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (42 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0077769, C0077880, C0077090 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 56% address fewer problems than their level implies and 24% were signed late; request the audit trail for C0077769, C0077880, C0077090.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
