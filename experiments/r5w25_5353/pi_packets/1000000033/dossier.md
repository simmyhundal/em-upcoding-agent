# Payment Integrity dossier: 1000000033

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 112 |
| Billed mix (99211 to 99215) | 2 / 6 / 72 / 116 / 45 |
| 99215 share | 18.7% |
| Expected 99215 share given patient complexity | 4.1% |
| Screen scores | z vs peers 1.68; risk-adjusted 4.62; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000033: 12 of 18 documented 99215 claims (67%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000033 billed 99215 on 18.7% of 241 claims against an expected 4.1% given patient complexity (risk-adjusted score 4.62; plain z-score vs peers 1.68). 67% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 18 documented 99215 claims, 12 (67%) were documented below the billed level, against 29% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 33%, late 0%, unsigned 0%, data 4%. No audit trail was received. 2 of 30 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0016468: billed 99215, patient aged 51 with 0 chronic condition(s); documented MDM level moderate, 35 minutes. C0016581: billed 99215, patient aged 50 with 1 chronic condition(s) (hypertension); documented MDM level moderate, minutes not recorded. C0016589: billed 99215; documented MDM level moderate, 33 minutes. C0016421: billed 99215, patient aged 25 with 0 chronic condition(s). C0016435: billed 99215, patient aged 27 with 0 chronic condition(s). C0016436: billed 99215, patient aged 54 with 1 chronic condition(s) (atrial fibrillation); documented MDM level high, 41 minutes.

## Evidence chart

![99215 share by patient complexity](../../charts/1000000033.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 11 | 0 | 0.0% | 4.6% |
| 99214 | 16 | 3 | 18.8% | 4.1% |
| 99215 | 18 | 12 | 66.7% | 28.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (28 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0016468, C0016581, C0016589 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 33% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0016468, C0016581, C0016589.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
