# Payment Integrity dossier: 1000000099

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 775 / 377 |
| Billed mix (99211 to 99215) | 6 / 9 / 193 / 399 / 168 |
| 99215 share | 21.7% |
| Expected 99215 share given patient complexity | 5.1% |
| Screen scores | z vs peers 2.78; risk-adjusted 8.83; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000099: 0 of 7 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000099 billed 99215 on 21.7% of 775 claims against an expected 5.1% given patient complexity (risk-adjusted score 8.83; plain z-score vs peers 2.78). 51% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 7 documented 99215 claims, 0 (0%) were documented below the billed level, against 41% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 37%, late 27%, unsigned 0%, data 17%, bulk created 13%, paste heavy 10%. 6 of 20 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0057938: billed 99213; documented MDM level straightforward, minutes not recorded. C0058296: billed 99214; documented MDM level low, minutes not recorded. C0058500: billed 99214; documented MDM level low, minutes not recorded. C0057936: billed 99215, patient aged 53 with 1 chronic condition(s) (osteoarthritis). C0057950: billed 99215, patient aged 40 with 1 chronic condition(s) (hypertension). C0057957: billed 99215, patient aged 28 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000099.svg)

## Records-review sample so far

Documentation is on file for 30 claims (4% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 2 | 22.2% | 6.5% |
| 99214 | 13 | 2 | 15.4% | 6.6% |
| 99215 | 7 | 0 | 0.0% | 41.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (49 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0057938, C0058296, C0058500 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 37% address fewer problems than their level implies and 27% were signed late; request the audit trail for C0057938, C0058296, C0058500.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
