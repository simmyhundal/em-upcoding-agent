# Payment Integrity dossier: 1000000215

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 246 / 115 |
| Billed mix (99211 to 99215) | 4 / 6 / 63 / 125 / 48 |
| 99215 share | 19.5% |
| Expected 99215 share given patient complexity | 4.5% |
| Screen scores | z vs peers 2.04; risk-adjusted 4.26; flagged by eb_ratio |

## Case summary (advisory)

**1000000215: 6 of 8 documented 99215 claims (75%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000215 billed 99215 on 19.5% of 246 claims against an expected 4.5% given patient complexity (risk-adjusted score 4.26; plain z-score vs peers 2.04). 54% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 28 claims. Of 8 documented 99215 claims, 6 (75%) were documented below the billed level, against 54% for the comparison providers. Note checks on 28 returned notes (share showing each sign): problems 18%, late 4%, unsigned 0%, data 11%. No audit trail was received. 3 of 17 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0126031: billed 99215, patient aged 42 with 1 chronic condition(s) (hypertension); documented MDM level moderate, 39 minutes. C0126048: billed 99215; documented MDM level low, minutes not recorded. C0126132: billed 99215; documented MDM level moderate, 38 minutes. C0126021: billed 99215, patient aged 76 with 1 chronic condition(s) (asthma). C0126027: billed 99215, patient aged 42 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000215.svg)

## Records-review sample so far

Documentation is on file for 28 claims (11% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 3.4% |
| 99214 | 14 | 1 | 7.1% | 8.5% |
| 99215 | 8 | 6 | 75.0% | 53.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0126031, C0126048, C0126132 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 18% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0126031, C0126048, C0126132.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
