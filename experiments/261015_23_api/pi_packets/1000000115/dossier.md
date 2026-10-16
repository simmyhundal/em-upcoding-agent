# Payment Integrity dossier: 1000000115

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 945 / 451 |
| Billed mix (99211 to 99215) | 4 / 4 / 161 / 537 / 239 |
| 99215 share | 25.3% |
| Expected 99215 share given patient complexity | 2.3% |
| Screen scores | z vs peers 3.59; risk-adjusted 15.48; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000115: 0 of 20 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000115 billed 99215 on 25.3% of 945 claims against an expected 2.3% given patient complexity (risk-adjusted score 15.48; plain z-score vs peers 3.59). 72% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 0 (0%) were documented below the billed level, against 4% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 42%, late 16%, unsigned 0%, data 4%, bulk created 0%, paste heavy 2%. 4 of 37 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0057485: billed 99215, patient aged 41 with 0 chronic condition(s). C0057501: billed 99215, patient aged 49 with 0 chronic condition(s). C0057522: billed 99215, patient aged 57 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000115.svg)

## Records-review sample so far

Documentation is on file for 45 claims (5% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 3.7% |
| 99214 | 18 | 0 | 0.0% | 2.1% |
| 99215 | 20 | 0 | 0.0% | 4.5% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (53 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0057485, C0057501, C0057522 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 42% address fewer problems than their level implies and 16% were signed late; request the audit trail for C0057485, C0057501, C0057522.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
