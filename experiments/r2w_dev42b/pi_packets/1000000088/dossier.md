# Payment Integrity dossier: 1000000088

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 115 |
| Billed mix (99211 to 99215) | 1 / 1 / 55 / 104 / 80 |
| 99215 share | 33.2% |
| Expected 99215 share given patient complexity | 10.6% |
| Screen scores | z vs peers 4.36; risk-adjusted 4.34; flagged by eb_ratio |

## Case summary (advisory)

**1000000088: 8 of 11 documented 99215 claims (73%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000088 billed 99215 on 33.2% of 241 claims against an expected 10.6% given patient complexity (risk-adjusted score 4.34; plain z-score vs peers 4.36). 10% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 11 documented 99215 claims, 8 (73%) were documented below the billed level, against 54% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 17%, late 10%, unsigned 0%, data 3%. No audit trail was received. 2 of 23 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0049818: billed 99215, patient aged 53 with 1 chronic condition(s) (heart failure); documented MDM level moderate, 33 minutes. C0049912: billed 99215; documented MDM level moderate, minutes not recorded. C0049938: billed 99215; documented MDM level moderate, minutes not recorded. C0049846: billed 99215, patient aged 67 with 1 chronic condition(s) (type 2 diabetes). C0049854: billed 99215, patient aged 60 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000088.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 1 | 16.7% | 3.4% |
| 99214 | 13 | 0 | 0.0% | 8.5% |
| 99215 | 11 | 8 | 72.7% | 53.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (37 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0049818, C0049912, C0049938 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 17% address fewer problems than their level implies and 10% were signed late; request the audit trail for C0049818, C0049912, C0049938.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
