# Payment Integrity dossier: 1000000176

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,424 / 1,187 |
| Billed mix (99211 to 99215) | 28 / 57 / 830 / 1,285 / 224 |
| 99215 share | 9.2% |
| Expected 99215 share given patient complexity | 4.4% |
| Screen scores | z vs peers 0.58; risk-adjusted 5.08; flagged by eb_ratio |

## Case summary (advisory)

**1000000176: 1 of 19 documented 99215 claims (5%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000176 billed 99215 on 9.2% of 2,424 claims against an expected 4.4% given patient complexity (risk-adjusted score 5.08; plain z-score vs peers 0.58). 63% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 1 (5%) were documented below the billed level, against 32% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 42%, late 22%, unsigned 0%, data 16%. No audit trail was received. 7 of 37 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0072288: billed 99215; documented MDM level moderate, minutes not recorded. C0071823: billed 99215, patient aged 38 with 1 chronic condition(s) (hypothyroidism). C0071863: billed 99215, patient aged 56 with 1 chronic condition(s) (hypertension). C0072021: billed 99215, patient aged 23 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000176.svg)

## Records-review sample so far

Documentation is on file for 45 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 0 | 0.0% | 3.3% |
| 99214 | 17 | 0 | 0.0% | 5.9% |
| 99215 | 19 | 1 | 5.3% | 32.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (53 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0072288, C0071823, C0071863 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 42% address fewer problems than their level implies and 22% were signed late; request the audit trail for C0072288, C0071823, C0071863.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
