# Payment Integrity dossier: 1000000128

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 467 / 223 |
| Billed mix (99211 to 99215) | 2 / 12 / 136 / 265 / 52 |
| 99215 share | 11.1% |
| Expected 99215 share given patient complexity | 4.7% |
| Screen scores | z vs peers 0.87; risk-adjusted 2.42; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000128: 8 of 17 documented 99215 claims (47%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000128 billed 99215 on 11.1% of 467 claims against an expected 4.7% given patient complexity (risk-adjusted score 2.42; plain z-score vs peers 0.87). 37% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 17 documented 99215 claims, 8 (47%) were documented below the billed level, against 24% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 33%, late 0%, unsigned 0%, data 2%. No audit trail was received. 2 of 33 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0062726: billed 99215; documented MDM level moderate, minutes not recorded. C0062748: billed 99215, patient aged 47 with 0 chronic condition(s); documented MDM level low, minutes not recorded. C0062837: billed 99215; documented MDM level moderate, 23 minutes. C0062571: billed 99215, patient aged 60 with 1 chronic condition(s) (depression). C0062607: billed 99215, patient aged 51 with 0 chronic condition(s). C0062674: billed 99215, patient aged 54 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000128.svg)

## Records-review sample so far

Documentation is on file for 45 claims (10% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 1.8% |
| 99214 | 22 | 1 | 4.5% | 5.2% |
| 99215 | 17 | 8 | 47.1% | 24.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (30 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0062726, C0062748, C0062837 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 33% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0062726, C0062748, C0062837.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
