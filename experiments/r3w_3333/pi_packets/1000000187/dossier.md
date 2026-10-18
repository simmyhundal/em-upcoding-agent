# Payment Integrity dossier: 1000000187

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 237 / 113 |
| Billed mix (99211 to 99215) | 8 / 5 / 70 / 115 / 39 |
| 99215 share | 16.5% |
| Expected 99215 share given patient complexity | 5.1% |
| Screen scores | z vs peers 1.68; risk-adjusted 2.88; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000187: 12 of 20 documented 99215 claims (60%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000187 billed 99215 on 16.5% of 237 claims against an expected 5.1% given patient complexity (risk-adjusted score 2.88; plain z-score vs peers 1.68). 49% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 12 (60%) were documented below the billed level, against 21% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 13%, late 0%, unsigned 0%, data 2%. No audit trail was received. 2 of 25 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0085930: billed 99215, patient aged 52 with 0 chronic condition(s); documented MDM level moderate, 37 minutes. C0085986: billed 99215, patient aged 47 with 1 chronic condition(s) (hypertension); documented MDM level moderate, minutes not recorded. C0085994: billed 99215; documented MDM level low, minutes not recorded. C0085882: billed 99215, patient aged 46 with 1 chronic condition(s) (obesity); documented MDM level high, 47 minutes. C0085909: billed 99215, patient aged 43 with 0 chronic condition(s). C0085915: billed 99215, patient aged 34 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000187.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 15 | 1 | 6.7% | 2.6% |
| 99214 | 7 | 2 | 28.6% | 6.4% |
| 99215 | 20 | 12 | 60.0% | 20.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (25 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0085930, C0085986, C0085994 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 13% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0085930, C0085986, C0085994.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
