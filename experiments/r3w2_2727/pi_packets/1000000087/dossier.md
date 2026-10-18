# Payment Integrity dossier: 1000000087

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 232 / 121 |
| Billed mix (99211 to 99215) | 1 / 5 / 40 / 118 / 68 |
| 99215 share | 29.3% |
| Expected 99215 share given patient complexity | 4.8% |
| Screen scores | z vs peers 4.40; risk-adjusted 6.96; flagged by eb_ratio |

## Case summary (advisory)

**1000000087: 11 of 20 documented 99215 claims (55%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000087 billed 99215 on 29.3% of 232 claims against an expected 4.8% given patient complexity (risk-adjusted score 6.96; plain z-score vs peers 4.40). 71% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 11 (55%) were documented below the billed level, against 47% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 31%, late 0%, unsigned 0%, data 0%. No audit trail was received. 3 of 34 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0034175: billed 99215; documented MDM level moderate, minutes not recorded. C0034218: billed 99215, patient aged 42 with 1 chronic condition(s) (obesity); documented MDM level moderate, 26 minutes. C0034356: billed 99215, patient aged 46 with 0 chronic condition(s); documented MDM level moderate, 31 minutes. C0034202: billed 99215, patient aged 58 with 1 chronic condition(s) (hyperlipidemia). C0034206: billed 99215, patient aged 40 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000087.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 0 | 0.0% | 2.0% |
| 99214 | 17 | 3 | 17.6% | 3.6% |
| 99215 | 20 | 11 | 55.0% | 47.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (35 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0034175, C0034218, C0034356 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 31% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0034175, C0034218, C0034356.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
