# Payment Integrity dossier: 1000000118

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 239 / 110 |
| Billed mix (99211 to 99215) | 1 / 7 / 64 / 100 / 67 |
| 99215 share | 28.0% |
| Expected 99215 share given patient complexity | 4.9% |
| Screen scores | z vs peers 3.23; risk-adjusted 6.82; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000118: 0 of 6 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000118 billed 99215 on 28.0% of 239 claims against an expected 4.9% given patient complexity (risk-adjusted score 6.82; plain z-score vs peers 3.23). 60% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 6 documented 99215 claims, 0 (0%) were documented below the billed level, against 22% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 37%, late 20%, unsigned 0%, data 20%, bulk created 7%, paste heavy 17%. 7 of 20 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0055906: billed 99214; documented MDM level low, minutes not recorded. C0055806: billed 99215, patient aged 35 with 0 chronic condition(s). C0055841: billed 99215, patient aged 47 with 1 chronic condition(s) (hypertension). C0055842: billed 99215, patient aged 27 with 0 chronic condition(s); documented MDM level high, minutes not recorded.

## Evidence chart

![99215 share by patient complexity](../../charts/1000000118.svg)

## Records-review sample so far

Documentation is on file for 30 claims (13% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 0 | 0.0% | 4.1% |
| 99214 | 14 | 1 | 7.1% | 7.3% |
| 99215 | 6 | 0 | 0.0% | 22.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (34 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0055906, C0055806, C0055841 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 37% address fewer problems than their level implies and 20% were signed late; request the audit trail for C0055906, C0055806, C0055841.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
