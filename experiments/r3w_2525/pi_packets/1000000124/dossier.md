# Payment Integrity dossier: 1000000124

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 425 / 204 |
| Billed mix (99211 to 99215) | 3 / 3 / 136 / 183 / 100 |
| 99215 share | 23.5% |
| Expected 99215 share given patient complexity | 3.9% |
| Screen scores | z vs peers 2.71; risk-adjusted 7.74; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000124: 17 of 19 documented 99215 claims (90%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000124 billed 99215 on 23.5% of 425 claims against an expected 3.9% given patient complexity (risk-adjusted score 7.74; plain z-score vs peers 2.71). 76% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 17 (90%) were documented below the billed level, against 46% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 44%, late 2%, unsigned 0%, data 2%, bulk created 0%, paste heavy 0%. 1 of 27 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0056857: billed 99215, patient aged 66 with 0 chronic condition(s); documented MDM level moderate, 25 minutes. C0056959: billed 99215, patient aged 50 with 1 chronic condition(s) (atrial fibrillation); documented MDM level moderate, minutes not recorded. C0057078: billed 99215; documented MDM level low, minutes not recorded. C0056863: billed 99215, patient aged 32 with 0 chronic condition(s). C0056868: billed 99215, patient aged 23 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000124.svg)

## Records-review sample so far

Documentation is on file for 45 claims (11% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 0 | 0.0% | 2.8% |
| 99214 | 17 | 5 | 29.4% | 6.9% |
| 99215 | 19 | 17 | 89.5% | 45.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (41 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0056857, C0056959, C0057078 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 44% address fewer problems than their level implies and 2% were signed late; request the audit trail for C0056857, C0056959, C0057078.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
