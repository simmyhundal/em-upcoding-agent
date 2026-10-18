# Payment Integrity dossier: 1000000152

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 245 / 121 |
| Billed mix (99211 to 99215) | 0 / 1 / 56 / 136 / 52 |
| 99215 share | 21.2% |
| Expected 99215 share given patient complexity | 5.5% |
| Screen scores | z vs peers 2.57; risk-adjusted 3.99; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000152: 6 of 9 documented 99215 claims (67%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000152 billed 99215 on 21.2% of 245 claims against an expected 5.5% given patient complexity (risk-adjusted score 3.99; plain z-score vs peers 2.57). 40% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 9 documented 99215 claims, 6 (67%) were documented below the billed level, against 21% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 30%, late 10%, unsigned 0%, data 3%. No audit trail was received. 2 of 18 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0068112: billed 99215, patient aged 45 with 1 chronic condition(s) (hyperlipidemia); documented MDM level moderate, 23 minutes. C0068246: billed 99215; documented MDM level moderate, minutes not recorded. C0068277: billed 99215, patient aged 42 with 1 chronic condition(s) (obesity); documented MDM level moderate, 25 minutes. C0068086: billed 99215, patient aged 47 with 1 chronic condition(s) (atrial fibrillation). C0068088: billed 99215, patient aged 45 with 1 chronic condition(s) (heart failure). C0068097: billed 99215, patient aged 43 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000152.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 2.6% |
| 99214 | 16 | 2 | 12.5% | 6.4% |
| 99215 | 9 | 6 | 66.7% | 20.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (30 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0068112, C0068246, C0068277 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 30% address fewer problems than their level implies and 10% were signed late; request the audit trail for C0068112, C0068246, C0068277.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
