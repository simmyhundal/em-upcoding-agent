# Payment Integrity dossier: 1000000029

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 527 / 258 |
| Billed mix (99211 to 99215) | 5 / 12 / 166 / 252 / 92 |
| 99215 share | 17.5% |
| Expected 99215 share given patient complexity | 4.4% |
| Screen scores | z vs peers 1.29; risk-adjusted 6.02; flagged by eb_ratio |

## Case summary (advisory)

**1000000029: 11 of 20 documented 99215 claims (55%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000029 billed 99215 on 17.5% of 527 claims against an expected 4.4% given patient complexity (risk-adjusted score 6.02; plain z-score vs peers 1.29). 61% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 11 (55%) were documented below the billed level, against 16% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 27%, late 4%, unsigned 0%, data 2%. No audit trail was received. 1 of 30 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0010929: billed 99215, patient aged 70 with 5 chronic condition(s) (type 2 diabetes;obesity;hypertension;heart failure;COPD); documented MDM level moderate, 35 minutes. C0011003: billed 99215, patient aged 32 with 1 chronic condition(s) (asthma); documented MDM level moderate, 32 minutes. C0011169: billed 99215; documented MDM level moderate, 37 minutes. C0010836: billed 99215, patient aged 20 with 1 chronic condition(s) (depression). C0010862: billed 99215, patient aged 46 with 1 chronic condition(s) (asthma). C0010887: billed 99215, patient aged 53 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000029.svg)

## Records-review sample so far

Documentation is on file for 45 claims (8% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 1 | 12.5% | 1.9% |
| 99214 | 16 | 4 | 25.0% | 4.5% |
| 99215 | 20 | 11 | 55.0% | 16.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (40 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0010929, C0011003, C0011169 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 27% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0010929, C0011003, C0011169.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
