# Payment Integrity dossier: 1000000188

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 239 / 124 |
| Billed mix (99211 to 99215) | 0 / 3 / 70 / 130 / 36 |
| 99215 share | 15.1% |
| Expected 99215 share given patient complexity | 4.0% |
| Screen scores | z vs peers 1.35; risk-adjusted 3.21; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000188: 1 of 18 documented 99215 claims (6%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000188 billed 99215 on 15.1% of 239 claims against an expected 4.0% given patient complexity (risk-adjusted score 3.21; plain z-score vs peers 1.35). 81% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 18 documented 99215 claims, 1 (6%) were documented below the billed level, against 29% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 44%, late 20%, unsigned 0%, data 31%. No audit trail was received. 15 of 36 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0095067: billed 99215, patient aged 43 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0094984: billed 99215, patient aged 69 with 0 chronic condition(s). C0094990: billed 99215, patient aged 52 with 1 chronic condition(s) (hypertension). C0094996: billed 99215, patient aged 64 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000188.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 11 | 0 | 0.0% | 5.0% |
| 99214 | 15 | 1 | 6.7% | 6.4% |
| 99215 | 18 | 1 | 5.6% | 29.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (24 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0095067, C0094984, C0094990 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 44% address fewer problems than their level implies and 20% were signed late; request the audit trail for C0095067, C0094984, C0094990.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
