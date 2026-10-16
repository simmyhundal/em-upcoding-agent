# Payment Integrity dossier: 1000000086

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 240 / 118 |
| Billed mix (99211 to 99215) | 1 / 5 / 72 / 111 / 51 |
| 99215 share | 21.2% |
| Expected 99215 share given patient complexity | 1.7% |
| Screen scores | z vs peers 2.74; risk-adjusted 7.42; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000086: 0 of 20 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000086 billed 99215 on 21.2% of 240 claims against an expected 1.7% given patient complexity (risk-adjusted score 7.42; plain z-score vs peers 2.74). 71% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 0 (0%) were documented below the billed level, against 0% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 44%, late 22%, unsigned 0%, data 7%, bulk created 9%, paste heavy 4%. 5 of 33 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0053286: billed 99215, patient aged 50 with 0 chronic condition(s). C0053300: billed 99215, patient aged 26 with 1 chronic condition(s) (atrial fibrillation). C0053316: billed 99215, patient aged 33 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000086.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 12 | 0 | 0.0% | 1.6% |
| 99214 | 12 | 0 | 0.0% | 3.3% |
| 99215 | 20 | 0 | 0.0% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (30 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0053286, C0053300, C0053316 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 44% address fewer problems than their level implies and 22% were signed late; request the audit trail for C0053286, C0053300, C0053316.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
