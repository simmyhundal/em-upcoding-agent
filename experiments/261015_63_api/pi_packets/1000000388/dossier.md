# Payment Integrity dossier: 1000000388

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,301 / 645 |
| Billed mix (99211 to 99215) | 11 / 5 / 217 / 715 / 353 |
| 99215 share | 27.1% |
| Expected 99215 share given patient complexity | 1.7% |
| Screen scores | z vs peers 4.29; risk-adjusted 26.46; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000388: 4 of 8 documented 99215 claims (50%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000388 billed 99215 on 27.1% of 1,301 claims against an expected 1.7% given patient complexity (risk-adjusted score 26.46; plain z-score vs peers 4.29). 84% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 8 documented 99215 claims, 4 (50%) were documented below the billed level, against 9% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 43%, late 0%, unsigned 0%, data 0%, bulk created 0%, paste heavy 0%. 2 of 18 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0224209: billed 99215; documented MDM level moderate, 35 minutes. C0224643: billed 99215; documented MDM level moderate, 25 minutes. C0224876: billed 99215; documented MDM level moderate, minutes not recorded. C0224228: billed 99215, patient aged 41 with 1 chronic condition(s) (heart failure). C0224288: billed 99215, patient aged 66 with 1 chronic condition(s) (atrial fibrillation). C0224318: billed 99215, patient aged 47 with 1 chronic condition(s) (asthma).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000388.svg)

## Records-review sample so far

Documentation is on file for 30 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 4.3% |
| 99214 | 14 | 3 | 21.4% | 3.5% |
| 99215 | 8 | 4 | 50.0% | 9.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (57 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0224209, C0224643, C0224876 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 43% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0224209, C0224643, C0224876.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
