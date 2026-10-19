# Payment Integrity dossier: 1000000163

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,195 / 575 |
| Billed mix (99211 to 99215) | 2 / 21 / 261 / 636 / 275 |
| 99215 share | 23.0% |
| Expected 99215 share given patient complexity | 5.4% |
| Screen scores | z vs peers 2.77; risk-adjusted 9.72; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000163: 2 of 8 documented 99215 claims (25%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000163 billed 99215 on 23.0% of 1,195 claims against an expected 5.4% given patient complexity (risk-adjusted score 9.72; plain z-score vs peers 2.77). 37% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 8 documented 99215 claims, 2 (25%) were documented below the billed level, against 40% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 23%, late 13%, unsigned 0%, data 3%, bulk created 0%, paste heavy 0%. 2 of 24 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0083677: billed 99215; documented MDM level moderate, minutes not recorded. C0084479: billed 99215; documented MDM level moderate, 39 minutes. C0083616: billed 99215, patient aged 38 with 0 chronic condition(s). C0083656: billed 99215, patient aged 52 with 0 chronic condition(s). C0083747: billed 99215, patient aged 31 with 1 chronic condition(s) (hypothyroidism).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000163.svg)

## Records-review sample so far

Documentation is on file for 30 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 2.9% |
| 99214 | 18 | 2 | 11.1% | 4.6% |
| 99215 | 8 | 2 | 25.0% | 40.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (55 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0083677, C0084479, C0083616 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 23% address fewer problems than their level implies and 13% were signed late; request the audit trail for C0083677, C0084479, C0083616.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
