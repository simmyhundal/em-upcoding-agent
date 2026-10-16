# Payment Integrity dossier: 1000000128

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 302 / 145 |
| Billed mix (99211 to 99215) | 6 / 2 / 70 / 155 / 69 |
| 99215 share | 22.8% |
| Expected 99215 share given patient complexity | 1.9% |
| Screen scores | z vs peers 3.04; risk-adjusted 11.87; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000128: 0 of 13 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000128 billed 99215 on 22.8% of 302 claims against an expected 1.9% given patient complexity (risk-adjusted score 11.87; plain z-score vs peers 3.04). 91% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 13 documented 99215 claims, 0 (0%) were documented below the billed level, against 3% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 57%, late 17%, unsigned 0%, data 7%, bulk created 13%, paste heavy 20%. 5 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0068352: billed 99214; documented MDM level low, 21 minutes. C0068179: billed 99215, patient aged 40 with 1 chronic condition(s) (hyperlipidemia). C0068185: billed 99215, patient aged 63 with 1 chronic condition(s) (hypertension). C0068200: billed 99215, patient aged 55 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000128.svg)

## Records-review sample so far

Documentation is on file for 30 claims (10% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 3.0% |
| 99214 | 10 | 1 | 10.0% | 3.9% |
| 99215 | 13 | 0 | 0.0% | 3.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (35 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0068352, C0068179, C0068185 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 57% address fewer problems than their level implies and 17% were signed late; request the audit trail for C0068352, C0068179, C0068185.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
