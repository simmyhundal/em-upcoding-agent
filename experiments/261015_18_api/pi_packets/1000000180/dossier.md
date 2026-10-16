# Payment Integrity dossier: 1000000180

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 988 / 489 |
| Billed mix (99211 to 99215) | 18 / 15 / 322 / 453 / 180 |
| 99215 share | 18.2% |
| Expected 99215 share given patient complexity | 4.4% |
| Screen scores | z vs peers 2.07; risk-adjusted 8.35; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000180: 11 of 14 documented 99215 claims (79%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000180 billed 99215 on 18.2% of 988 claims against an expected 4.4% given patient complexity (risk-adjusted score 8.35; plain z-score vs peers 2.07). 21% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 34 claims. Of 14 documented 99215 claims, 11 (79%) were documented below the billed level, against 5% for the comparison providers. Note checks on 34 returned notes (share showing each sign): problems 18%, late 3%, unsigned 0%, data 6%. No audit trail was received. 2 of 16 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0085805: billed 99215, patient aged 94 with 4 chronic condition(s) (hypothyroidism;type 2 diabetes;depression;hypertension); documented MDM level moderate, 35 minutes. C0085943: billed 99215; documented MDM level moderate, 31 minutes. C0086118: billed 99215; documented MDM level moderate, 36 minutes. C0085576: billed 99215, patient aged 42 with 1 chronic condition(s) (hypertension). C0085628: billed 99215, patient aged 55 with 0 chronic condition(s). C0085650: billed 99215, patient aged 27 with 1 chronic condition(s) (osteoarthritis).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000180.svg)

## Records-review sample so far

Documentation is on file for 34 claims (3% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 11 | 0 | 0.0% | 1.6% |
| 99214 | 8 | 3 | 37.5% | 3.0% |
| 99215 | 14 | 11 | 78.6% | 4.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (50 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0085805, C0085943, C0086118 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 18% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0085805, C0085943, C0086118.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
