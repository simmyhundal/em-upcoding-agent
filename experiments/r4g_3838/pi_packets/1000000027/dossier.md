# Payment Integrity dossier: 1000000027

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 124 / 57 |
| Billed mix (99211 to 99215) | 0 / 0 / 19 / 64 / 41 |
| 99215 share | 33.1% |
| Expected 99215 share given patient complexity | 6.7% |
| Screen scores | z vs peers 4.98; risk-adjusted 4.84; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000027: 0 of 6 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000027 billed 99215 on 33.1% of 124 claims against an expected 6.7% given patient complexity (risk-adjusted score 4.84; plain z-score vs peers 4.98). 22% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 6 documented 99215 claims, 0 (0%) were documented below the billed level, against 42% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 13%, late 13%, unsigned 0%, data 0%, bulk created 0%, paste heavy 0%. 0 of 25 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0007863: billed 99214; documented MDM level low, 25 minutes. C0007796: billed 99215, patient aged 55 with 1 chronic condition(s) (hypertension); documented MDM level high, 52 minutes. C0007809: billed 99215, patient aged 65 with 1 chronic condition(s) (obesity). C0007832: billed 99215, patient aged 65 with 1 chronic condition(s) (obesity); documented MDM level high, 40 minutes.

## Evidence chart

![99215 share by patient complexity](../../charts/1000000027.svg)

## Records-review sample so far

Documentation is on file for 30 claims (24% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 3.1% |
| 99214 | 19 | 1 | 5.3% | 5.1% |
| 99215 | 6 | 0 | 0.0% | 42.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (26 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0007863, C0007796, C0007809 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 13% address fewer problems than their level implies and 13% were signed late; request the audit trail for C0007863, C0007796, C0007809.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
