# Payment Integrity dossier: 1000000005

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 123 |
| Billed mix (99211 to 99215) | 2 / 6 / 85 / 113 / 35 |
| 99215 share | 14.5% |
| Expected 99215 share given patient complexity | 5.1% |
| Screen scores | z vs peers 1.31; risk-adjusted 2.50; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000005: 7 of 19 documented 99214 and 99215 claims (37%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000005 billed 99215 on 14.5% of 241 claims against an expected 5.1% given patient complexity (risk-adjusted score 2.50; plain z-score vs peers 1.31). 40% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 3 documented 99215 claims, 2 (67%) were documented below the billed level, against 33% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 33%, late 0%, unsigned 0%, data 0%. No audit trail was received. 0 of 14 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0002187: billed 99215, patient aged 64 with 1 chronic condition(s) (asthma); documented MDM level moderate, 21 minutes. C0002251: billed 99215, patient aged 67 with 0 chronic condition(s); documented MDM level moderate, 36 minutes. C0002084: billed 99215, patient aged 21 with 0 chronic condition(s). C0002110: billed 99215, patient aged 42 with 0 chronic condition(s). C0002122: billed 99215, patient aged 73 with 1 chronic condition(s) (obesity); documented MDM level high, 46 minutes.

## Evidence chart

![99215 share by patient complexity](../../charts/1000000005.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 1 | 10.0% | 3.4% |
| 99214 | 16 | 5 | 31.2% | 3.0% |
| 99215 | 3 | 2 | 66.7% | 33.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (24 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0002187, C0002251, C0002084 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 33% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0002187, C0002251, C0002084.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
