# Payment Integrity dossier: 1000000421

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 235 / 111 |
| Billed mix (99211 to 99215) | 1 / 1 / 25 / 134 / 74 |
| 99215 share | 31.5% |
| Expected 99215 share given patient complexity | 3.5% |
| Screen scores | z vs peers 5.03; risk-adjusted 9.15; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000421: 5 of 6 documented 99215 claims (83%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000421 billed 99215 on 31.5% of 235 claims against an expected 3.5% given patient complexity (risk-adjusted score 9.15; plain z-score vs peers 5.03). 42% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 6 documented 99215 claims, 5 (83%) were documented below the billed level, against 9% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 33%, late 0%, unsigned 0%, data 0%. No audit trail was received. 1 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0232704: billed 99215; documented MDM level moderate, minutes not recorded. C0232726: billed 99215; documented MDM level moderate, 38 minutes. C0232763: billed 99215, patient aged 71 with 5 chronic condition(s) (type 2 diabetes;obesity;hyperlipidemia;hypertension;osteoarthritis); documented MDM level low, minutes not recorded. C0232721: billed 99215, patient aged 55 with 1 chronic condition(s) (hyperlipidemia). C0232723: billed 99215, patient aged 44 with 1 chronic condition(s) (hypothyroidism). C0232725: billed 99215, patient aged 43 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000421.svg)

## Records-review sample so far

Documentation is on file for 30 claims (13% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 2 | 0 | 0.0% | 3.0% |
| 99214 | 22 | 1 | 4.5% | 3.3% |
| 99215 | 6 | 5 | 83.3% | 8.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (36 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0232704, C0232726, C0232763 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 33% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0232704, C0232726, C0232763.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
