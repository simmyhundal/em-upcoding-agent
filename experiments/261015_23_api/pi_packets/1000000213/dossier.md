# Payment Integrity dossier: 1000000213

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,600 / 784 |
| Billed mix (99211 to 99215) | 4 / 6 / 195 / 918 / 477 |
| 99215 share | 29.8% |
| Expected 99215 share given patient complexity | 8.7% |
| Screen scores | z vs peers 4.40; risk-adjusted 9.78; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000213: 10 of 20 documented 99215 claims (50%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000213 billed 99215 on 29.8% of 1,600 claims against an expected 8.7% given patient complexity (risk-adjusted score 9.78; plain z-score vs peers 4.40). 5% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 10 (50%) were documented below the billed level, against 4% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 7%, late 0%, unsigned 0%, data 0%. No audit trail was received. 0 of 32 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0105042: billed 99215; documented MDM level moderate, 34 minutes. C0105800: billed 99215; documented MDM level moderate, minutes not recorded. C0105904: billed 99215, patient aged 40 with 1 chronic condition(s) (type 2 diabetes); documented MDM level moderate, 35 minutes. C0105010: billed 99215, patient aged 62 with 0 chronic condition(s). C0105031: billed 99215, patient aged 47 with 0 chronic condition(s). C0105034: billed 99215, patient aged 31 with 1 chronic condition(s) (depression).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000213.svg)

## Records-review sample so far

Documentation is on file for 45 claims (3% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 1 | 14.3% | 3.7% |
| 99214 | 18 | 1 | 5.6% | 2.1% |
| 99215 | 20 | 10 | 50.0% | 4.5% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (60 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0105042, C0105800, C0105904 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 7% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0105042, C0105800, C0105904.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
