# Payment Integrity dossier: 1000000388

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 129 |
| Billed mix (99211 to 99215) | 3 / 1 / 64 / 130 / 43 |
| 99215 share | 17.8% |
| Expected 99215 share given patient complexity | 2.5% |
| Screen scores | z vs peers 2.48; risk-adjusted 5.97; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000388: 12 of 17 documented 99215 claims (71%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000388 billed 99215 on 17.8% of 241 claims against an expected 2.5% given patient complexity (risk-adjusted score 5.97; plain z-score vs peers 2.48). 65% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 44 claims. Of 17 documented 99215 claims, 12 (71%) were documented below the billed level, against 9% for the comparison providers. Note checks on 44 returned notes (share showing each sign): problems 25%, late 4%, unsigned 0%, data 2%. No audit trail was received. 4 of 32 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0218626: billed 99215, patient aged 96 with 5 chronic condition(s) (obesity;depression;heart failure;asthma;osteoarthritis); documented MDM level moderate, minutes not recorded. C0218679: billed 99215, patient aged 52 with 4 chronic condition(s) (obesity;hyperlipidemia;depression;hypertension); documented MDM level moderate, minutes not recorded. C0218709: billed 99215, patient aged 54 with 0 chronic condition(s); documented MDM level low, 20 minutes. C0218610: billed 99215, patient aged 21 with 0 chronic condition(s); documented MDM level high, minutes not recorded. C0218614: billed 99215, patient aged 21 with 0 chronic condition(s). C0218616: billed 99215, patient aged 44 with 1 chronic condition(s) (osteoarthritis).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000388.svg)

## Records-review sample so far

Documentation is on file for 44 claims (18% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 0 | 0.0% | 3.0% |
| 99214 | 18 | 3 | 16.7% | 3.3% |
| 99215 | 17 | 12 | 70.6% | 8.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (27 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0218626, C0218679, C0218709 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 25% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0218626, C0218679, C0218709.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
