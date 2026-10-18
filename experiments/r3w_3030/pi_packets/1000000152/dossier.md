# Payment Integrity dossier: 1000000152

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 245 / 120 |
| Billed mix (99211 to 99215) | 4 / 10 / 98 / 103 / 30 |
| 99215 share | 12.2% |
| Expected 99215 share given patient complexity | 4.2% |
| Screen scores | z vs peers 0.70; risk-adjusted 2.31; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000152: 7 of 19 documented 99214 and 99215 claims (37%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000152 billed 99215 on 12.2% of 245 claims against an expected 4.2% given patient complexity (risk-adjusted score 2.31; plain z-score vs peers 0.70). 77% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 5 documented 99215 claims, 4 (80%) were documented below the billed level, against 30% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 30%, late 3%, unsigned 0%, data 3%. No audit trail was received. 1 of 14 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0073211: billed 99215, patient aged 58 with 1 chronic condition(s) (obesity); documented MDM level moderate, minutes not recorded. C0073271: billed 99215; documented MDM level moderate, 36 minutes. C0073335: billed 99215; documented MDM level moderate, minutes not recorded. C0073132: billed 99215, patient aged 29 with 0 chronic condition(s). C0073136: billed 99215, patient aged 38 with 1 chronic condition(s) (type 2 diabetes). C0073148: billed 99215, patient aged 42 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000152.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 0 | 0.0% | 5.1% |
| 99214 | 14 | 3 | 21.4% | 7.5% |
| 99215 | 5 | 4 | 80.0% | 30.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (30 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0073211, C0073271, C0073335 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 30% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0073211, C0073271, C0073335.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
