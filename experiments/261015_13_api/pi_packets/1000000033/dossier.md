# Payment Integrity dossier: 1000000033

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,655 / 809 |
| Billed mix (99211 to 99215) | 18 / 10 / 333 / 837 / 457 |
| 99215 share | 27.6% |
| Expected 99215 share given patient complexity | 2.2% |
| Screen scores | z vs peers 3.84; risk-adjusted 31.01; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000033: 7 of 8 documented 99215 claims (88%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000033 billed 99215 on 27.6% of 1,655 claims against an expected 2.2% given patient complexity (risk-adjusted score 31.01; plain z-score vs peers 3.84). 72% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 8 documented 99215 claims, 7 (88%) were documented below the billed level, against 3% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 37%, late 3%, unsigned 0%, data 0%, bulk created 0%, paste heavy 0%. 0 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0014070: billed 99215; documented MDM level moderate, 36 minutes. C0014152: billed 99215; documented MDM level moderate, minutes not recorded. C0014357: billed 99215; documented MDM level moderate, minutes not recorded. C0013976: billed 99215, patient aged 59 with 1 chronic condition(s) (hyperlipidemia). C0014021: billed 99215, patient aged 74 with 1 chronic condition(s) (atrial fibrillation). C0014053: billed 99215, patient aged 50 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000033.svg)

## Records-review sample so far

Documentation is on file for 30 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 3.0% |
| 99214 | 16 | 4 | 25.0% | 3.9% |
| 99215 | 8 | 7 | 87.5% | 3.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (60 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0014070, C0014152, C0014357 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 37% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0014070, C0014152, C0014357.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
