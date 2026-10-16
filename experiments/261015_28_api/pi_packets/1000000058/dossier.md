# Payment Integrity dossier: 1000000058

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 125 |
| Billed mix (99211 to 99215) | 0 / 1 / 14 / 132 / 95 |
| 99215 share | 39.3% |
| Expected 99215 share given patient complexity | 10.2% |
| Screen scores | z vs peers 5.65; risk-adjusted 5.79; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000058: 7 of 13 documented 99215 claims (54%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000058 billed 99215 on 39.3% of 242 claims against an expected 10.2% given patient complexity (risk-adjusted score 5.79; plain z-score vs peers 5.65). 4% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 13 documented 99215 claims, 7 (54%) were documented below the billed level, against 0% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 10%, late 3%, unsigned 0%, data 7%. No audit trail was received. 2 of 24 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0034797: billed 99215; documented MDM level moderate, 33 minutes. C0034819: billed 99215; documented MDM level moderate, minutes not recorded. C0034884: billed 99215; documented MDM level moderate, 38 minutes. C0034781: billed 99215, patient aged 54 with 0 chronic condition(s). C0034821: billed 99215, patient aged 52 with 0 chronic condition(s). C0034848: billed 99215, patient aged 45 with 1 chronic condition(s) (hypothyroidism).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000058.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 2 | 0 | 0.0% | 1.2% |
| 99214 | 15 | 1 | 6.7% | 3.1% |
| 99215 | 13 | 7 | 53.8% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (40 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0034797, C0034819, C0034884 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 10% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0034797, C0034819, C0034884.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
