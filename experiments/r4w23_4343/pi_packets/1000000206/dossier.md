# Payment Integrity dossier: 1000000206

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 238 / 116 |
| Billed mix (99211 to 99215) | 5 / 8 / 83 / 107 / 35 |
| 99215 share | 14.7% |
| Expected 99215 share given patient complexity | 4.1% |
| Screen scores | z vs peers 1.43; risk-adjusted 3.47; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000206: 0 of 14 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000206 billed 99215 on 14.7% of 238 claims against an expected 4.1% given patient complexity (risk-adjusted score 3.47; plain z-score vs peers 1.43). 69% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 37 claims. Of 14 documented 99215 claims, 0 (0%) were documented below the billed level, against 22% for the comparison providers. Note checks on 37 returned notes (share showing each sign): problems 24%, late 22%, unsigned 0%, data 22%. No audit trail was received. 9 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0111081: billed 99213; documented MDM level straightforward, minutes not recorded. C0111092: billed 99215, patient aged 44 with 1 chronic condition(s) (type 2 diabetes). C0111107: billed 99215, patient aged 57 with 0 chronic condition(s). C0111109: billed 99215, patient aged 31 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000206.svg)

## Records-review sample so far

Documentation is on file for 37 claims (16% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 15 | 1 | 6.7% | 4.1% |
| 99214 | 6 | 0 | 0.0% | 5.0% |
| 99215 | 14 | 0 | 0.0% | 21.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (24 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0111081, C0111092, C0111107 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 24% address fewer problems than their level implies and 22% were signed late; request the audit trail for C0111081, C0111092, C0111107.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
