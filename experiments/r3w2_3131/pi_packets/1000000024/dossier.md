# Payment Integrity dossier: 1000000024

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 457 / 214 |
| Billed mix (99211 to 99215) | 1 / 3 / 93 / 206 / 154 |
| 99215 share | 33.7% |
| Expected 99215 share given patient complexity | 4.8% |
| Screen scores | z vs peers 4.67; risk-adjusted 11.18; flagged by eb_ratio |

## Case summary (advisory)

**1000000024: 5 of 10 documented 99215 claims (50%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000024 billed 99215 on 33.7% of 457 claims against an expected 4.8% given patient complexity (risk-adjusted score 11.18; plain z-score vs peers 4.67). 55% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 25 claims. Of 10 documented 99215 claims, 5 (50%) were documented below the billed level, against 33% for the comparison providers. Note checks on 25 returned notes (share showing each sign): problems 24%, late 8%, unsigned 0%, data 4%. No audit trail was received. 1 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0014843: billed 99215; documented MDM level moderate, 36 minutes. C0014883: billed 99215, patient aged 18 with 1 chronic condition(s) (osteoarthritis); documented MDM level moderate, 33 minutes. C0015000: billed 99215; documented MDM level moderate, minutes not recorded. C0014699: billed 99215, patient aged 37 with 1 chronic condition(s) (type 2 diabetes). C0014700: billed 99215, patient aged 31 with 1 chronic condition(s) (chronic kidney disease). C0014705: billed 99215, patient aged 68 with 0 chronic condition(s); documented MDM level high, 33 minutes.

## Evidence chart

![99215 share by patient complexity](../../charts/1000000024.svg)

## Records-review sample so far

Documentation is on file for 25 claims (6% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 3 | 0 | 0.0% | 3.2% |
| 99214 | 12 | 4 | 33.3% | 2.8% |
| 99215 | 10 | 5 | 50.0% | 33.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (48 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0014843, C0014883, C0015000 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 24% address fewer problems than their level implies and 8% were signed late; request the audit trail for C0014843, C0014883, C0015000.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
