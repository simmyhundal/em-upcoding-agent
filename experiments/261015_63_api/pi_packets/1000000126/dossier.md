# Payment Integrity dossier: 1000000126

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 356 / 174 |
| Billed mix (99211 to 99215) | 0 / 2 / 109 / 197 / 48 |
| 99215 share | 13.5% |
| Expected 99215 share given patient complexity | 1.9% |
| Screen scores | z vs peers 1.68; risk-adjusted 5.82; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000126: 0 of 20 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000126 billed 99215 on 13.5% of 356 claims against an expected 1.9% given patient complexity (risk-adjusted score 5.82; plain z-score vs peers 1.68). 60% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 44 claims. Of 20 documented 99215 claims, 0 (0%) were documented below the billed level, against 9% for the comparison providers. Note checks on 44 returned notes (share showing each sign): problems 46%, late 14%, unsigned 0%, data 9%. No audit trail was received. 6 of 33 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0082285: billed 99215, patient aged 39 with 0 chronic condition(s). C0082338: billed 99215, patient aged 67 with 1 chronic condition(s) (type 2 diabetes). C0082349: billed 99215, patient aged 70 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000126.svg)

## Records-review sample so far

Documentation is on file for 44 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 4.3% |
| 99214 | 19 | 0 | 0.0% | 3.5% |
| 99215 | 20 | 0 | 0.0% | 9.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0082285, C0082338, C0082349 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 46% address fewer problems than their level implies and 14% were signed late; request the audit trail for C0082285, C0082338, C0082349.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
