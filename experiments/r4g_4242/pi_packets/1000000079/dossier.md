# Payment Integrity dossier: 1000000079

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 941 / 490 |
| Billed mix (99211 to 99215) | 22 / 20 / 345 / 433 / 121 |
| 99215 share | 12.9% |
| Expected 99215 share given patient complexity | 4.0% |
| Screen scores | z vs peers 1.09; risk-adjusted 5.76; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000079: 15 of 20 documented 99215 claims (75%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000079 billed 99215 on 12.9% of 941 claims against an expected 4.0% given patient complexity (risk-adjusted score 5.76; plain z-score vs peers 1.09). 72% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 15 (75%) were documented below the billed level, against 41% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 44%, late 4%, unsigned 0%, data 2%, bulk created 0%, paste heavy 0%. 2 of 28 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0046498: billed 99215; documented MDM level moderate, minutes not recorded. C0046603: billed 99215, patient aged 45 with 0 chronic condition(s); documented MDM level low, minutes not recorded. C0047193: billed 99215; documented MDM level moderate, 32 minutes. C0046288: billed 99215, patient aged 43 with 0 chronic condition(s). C0046296: billed 99215, patient aged 43 with 1 chronic condition(s) (atrial fibrillation). C0046299: billed 99215, patient aged 78 with 1 chronic condition(s) (depression).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000079.svg)

## Records-review sample so far

Documentation is on file for 45 claims (5% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 11 | 2 | 18.2% | 6.5% |
| 99214 | 14 | 6 | 42.9% | 6.6% |
| 99215 | 20 | 15 | 75.0% | 41.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (44 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0046498, C0046603, C0047193 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 44% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0046498, C0046603, C0047193.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
