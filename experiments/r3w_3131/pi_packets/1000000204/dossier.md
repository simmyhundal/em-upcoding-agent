# Payment Integrity dossier: 1000000204

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 279 / 132 |
| Billed mix (99211 to 99215) | 3 / 7 / 95 / 142 / 32 |
| 99215 share | 11.5% |
| Expected 99215 share given patient complexity | 4.8% |
| Screen scores | z vs peers 0.78; risk-adjusted 1.91; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000204: 5 of 20 documented 99214 and 99215 claims (25%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000204 billed 99215 on 11.5% of 279 claims against an expected 4.8% given patient complexity (risk-adjusted score 1.91; plain z-score vs peers 0.78). 47% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 4 documented 99215 claims, 2 (50%) were documented below the billed level, against 33% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 17%, late 3%, unsigned 0%, data 0%. No audit trail was received. 0 of 17 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0107264: billed 99215, patient aged 56 with 1 chronic condition(s) (chronic kidney disease); documented MDM level moderate, minutes not recorded. C0107284: billed 99215; documented MDM level moderate, minutes not recorded. C0107083: billed 99215, patient aged 40 with 1 chronic condition(s) (type 2 diabetes). C0107094: billed 99215, patient aged 34 with 0 chronic condition(s). C0107112: billed 99215, patient aged 39 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000204.svg)

## Records-review sample so far

Documentation is on file for 30 claims (11% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 0 | 0.0% | 3.4% |
| 99214 | 16 | 3 | 18.8% | 3.0% |
| 99215 | 4 | 2 | 50.0% | 33.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (22 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0107264, C0107284, C0107083 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 17% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0107264, C0107284, C0107083.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
