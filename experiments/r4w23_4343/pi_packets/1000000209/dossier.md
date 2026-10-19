# Payment Integrity dossier: 1000000209

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 375 / 183 |
| Billed mix (99211 to 99215) | 2 / 6 / 83 / 210 / 74 |
| 99215 share | 19.7% |
| Expected 99215 share given patient complexity | 5.0% |
| Screen scores | z vs peers 2.35; risk-adjusted 5.48; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000209: 12 of 19 documented 99215 claims (63%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000209 billed 99215 on 19.7% of 375 claims against an expected 5.0% given patient complexity (risk-adjusted score 5.48; plain z-score vs peers 2.35). 58% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 12 (63%) were documented below the billed level, against 22% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 29%, late 7%, unsigned 0%, data 9%. No audit trail was received. 6 of 33 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0112016: billed 99215, patient aged 41 with 0 chronic condition(s); documented MDM level moderate, 32 minutes. C0112105: billed 99215, patient aged 57 with 1 chronic condition(s) (obesity); documented MDM level moderate, 36 minutes. C0112148: billed 99215; documented MDM level moderate, 32 minutes. C0111898: billed 99215, patient aged 63 with 0 chronic condition(s); documented MDM level high, 30 minutes. C0111913: billed 99215, patient aged 43 with 0 chronic condition(s). C0111924: billed 99215, patient aged 50 with 0 chronic condition(s); documented MDM level high, 30 minutes.

## Evidence chart

![99215 share by patient complexity](../../charts/1000000209.svg)

## Records-review sample so far

Documentation is on file for 45 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 4.1% |
| 99214 | 19 | 3 | 15.8% | 5.0% |
| 99215 | 19 | 12 | 63.2% | 21.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (36 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0112016, C0112105, C0112148 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 29% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0112016, C0112105, C0112148.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
