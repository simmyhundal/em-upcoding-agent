# Payment Integrity dossier: 1000000113

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,385 / 669 |
| Billed mix (99211 to 99215) | 15 / 10 / 260 / 651 / 449 |
| 99215 share | 32.4% |
| Expected 99215 share given patient complexity | 4.4% |
| Screen scores | z vs peers 3.73; risk-adjusted 21.05; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000113: 14 of 21 documented 99215 claims (67%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000113 billed 99215 on 32.4% of 1,385 claims against an expected 4.4% given patient complexity (risk-adjusted score 21.05; plain z-score vs peers 3.73). 58% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 21 documented 99215 claims, 14 (67%) were documented below the billed level, against 29% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 27%, late 4%, unsigned 0%, data 2%. No audit trail was received. 1 of 32 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0052379: billed 99215; documented MDM level moderate, 38 minutes. C0052605: billed 99215; documented MDM level moderate, 30 minutes. C0052727: billed 99215, patient aged 30 with 1 chronic condition(s) (obesity); documented MDM level moderate, 34 minutes. C0052190: billed 99215, patient aged 67 with 0 chronic condition(s). C0052216: billed 99215, patient aged 60 with 0 chronic condition(s). C0052245: billed 99215, patient aged 71 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000113.svg)

## Records-review sample so far

Documentation is on file for 45 claims (3% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 4.6% |
| 99214 | 18 | 3 | 16.7% | 4.1% |
| 99215 | 21 | 14 | 66.7% | 28.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (59 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0052379, C0052605, C0052727 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 27% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0052379, C0052605, C0052727.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
