# Payment Integrity dossier: 1000000094

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 374 / 190 |
| Billed mix (99211 to 99215) | 8 / 20 / 136 / 166 / 44 |
| 99215 share | 11.8% |
| Expected 99215 share given patient complexity | 3.6% |
| Screen scores | z vs peers 0.90; risk-adjusted 3.71; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000094: 0 of 18 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000094 billed 99215 on 11.8% of 374 claims against an expected 3.6% given patient complexity (risk-adjusted score 3.71; plain z-score vs peers 0.90). 77% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 18 documented 99215 claims, 0 (0%) were documented below the billed level, against 42% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 51%, late 16%, unsigned 0%, data 13%, bulk created 9%, paste heavy 9%. 6 of 28 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0042218: billed 99213; documented MDM level straightforward, minutes not recorded. C0042000: billed 99215, patient aged 31 with 1 chronic condition(s) (obesity). C0042024: billed 99215, patient aged 25 with 0 chronic condition(s). C0042025: billed 99215, patient aged 38 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000094.svg)

## Records-review sample so far

Documentation is on file for 45 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 15 | 1 | 6.7% | 3.9% |
| 99214 | 11 | 0 | 0.0% | 7.0% |
| 99215 | 18 | 0 | 0.0% | 42.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (27 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0042218, C0042000, C0042024 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 51% address fewer problems than their level implies and 16% were signed late; request the audit trail for C0042218, C0042000, C0042024.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
