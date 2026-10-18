# Payment Integrity dossier: 1000000088

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 238 / 116 |
| Billed mix (99211 to 99215) | 0 / 2 / 30 / 149 / 57 |
| 99215 share | 23.9% |
| Expected 99215 share given patient complexity | 6.7% |
| Screen scores | z vs peers 2.81; risk-adjusted 3.62; flagged by eb_ratio |

## Case summary (advisory)

**1000000088: 5 of 9 documented 99215 claims (56%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000088 billed 99215 on 23.9% of 238 claims against an expected 6.7% given patient complexity (risk-adjusted score 3.62; plain z-score vs peers 2.81). 25% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 9 documented 99215 claims, 5 (56%) were documented below the billed level, against 38% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 3%, late 7%, unsigned 0%, data 0%. No audit trail was received. 3 of 25 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0046878: billed 99215, patient aged 88 with 5 chronic condition(s) (hypothyroidism;type 2 diabetes;obesity;depression;osteoarthritis); documented MDM level moderate, 35 minutes. C0046895: billed 99215, patient aged 43 with 1 chronic condition(s) (obesity); documented MDM level moderate, 34 minutes. C0046932: billed 99215; documented MDM level low, minutes not recorded. C0046775: billed 99215, patient aged 36 with 1 chronic condition(s) (obesity). C0046796: billed 99215, patient aged 44 with 1 chronic condition(s) (heart failure). C0046798: billed 99215, patient aged 50 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000088.svg)

## Records-review sample so far

Documentation is on file for 30 claims (13% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 3 | 0 | 0.0% | 3.4% |
| 99214 | 17 | 2 | 11.8% | 8.3% |
| 99215 | 9 | 5 | 55.6% | 37.9% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (32 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0046878, C0046895, C0046932 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 3% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0046878, C0046895, C0046932.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
