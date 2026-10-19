# Payment Integrity dossier: 1000000038

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 239 / 116 |
| Billed mix (99211 to 99215) | 1 / 2 / 47 / 144 / 45 |
| 99215 share | 18.8% |
| Expected 99215 share given patient complexity | 4.1% |
| Screen scores | z vs peers 2.16; risk-adjusted 4.42; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000038: 0 of 21 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000038 billed 99215 on 18.8% of 239 claims against an expected 4.1% given patient complexity (risk-adjusted score 4.42; plain z-score vs peers 2.16). 73% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 21 documented 99215 claims, 0 (0%) were documented below the billed level, against 20% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 47%, late 24%, unsigned 0%, data 13%. No audit trail was received. 8 of 36 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0014821: billed 99214; documented MDM level low, minutes not recorded. C0014869: billed 99213; documented MDM level straightforward, minutes not recorded. C0014751: billed 99215, patient aged 46 with 0 chronic condition(s). C0014758: billed 99215, patient aged 59 with 1 chronic condition(s) (heart failure). C0014774: billed 99215, patient aged 44 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000038.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 1 | 20.0% | 3.2% |
| 99214 | 19 | 1 | 5.3% | 5.0% |
| 99215 | 21 | 0 | 0.0% | 20.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (28 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0014821, C0014869, C0014751 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 47% address fewer problems than their level implies and 24% were signed late; request the audit trail for C0014821, C0014869, C0014751.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
