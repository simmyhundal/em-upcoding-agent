# Payment Integrity dossier: 1000000142

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 401 / 191 |
| Billed mix (99211 to 99215) | 0 / 6 / 81 / 218 / 96 |
| 99215 share | 23.9% |
| Expected 99215 share given patient complexity | 5.2% |
| Screen scores | z vs peers 3.07; risk-adjusted 6.29; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000142: 0 of 8 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000142 billed 99215 on 23.9% of 401 claims against an expected 5.2% given patient complexity (risk-adjusted score 6.29; plain z-score vs peers 3.07). 50% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 8 documented 99215 claims, 0 (0%) were documented below the billed level, against 21% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 30%, late 13%, unsigned 0%, data 10%, bulk created 10%, paste heavy 10%. 3 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0064568: billed 99214; documented MDM level low, minutes not recorded. C0064934: billed 99214; documented MDM level low, minutes not recorded. C0064522: billed 99215, patient aged 29 with 0 chronic condition(s). C0064530: billed 99215, patient aged 55 with 1 chronic condition(s) (type 2 diabetes). C0064559: billed 99215, patient aged 64 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000142.svg)

## Records-review sample so far

Documentation is on file for 30 claims (8% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 2.6% |
| 99214 | 17 | 2 | 11.8% | 6.4% |
| 99215 | 8 | 0 | 0.0% | 20.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (40 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0064568, C0064934, C0064522 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 30% address fewer problems than their level implies and 13% were signed late; request the audit trail for C0064568, C0064934, C0064522.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
