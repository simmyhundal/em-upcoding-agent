# Payment Integrity dossier: 1000000150

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 646 / 315 |
| Billed mix (99211 to 99215) | 11 / 17 / 232 / 303 / 83 |
| 99215 share | 12.8% |
| Expected 99215 share given patient complexity | 3.9% |
| Screen scores | z vs peers 1.17; risk-adjusted 4.82; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000150: 0 of 15 documented 99214 and 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000150 billed 99215 on 12.8% of 646 claims against an expected 3.9% given patient complexity (risk-adjusted score 4.82; plain z-score vs peers 1.17). 64% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 3 documented 99215 claims, 0 (0%) were documented below the billed level, against 42% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 30%, late 10%, unsigned 0%, data 13%, bulk created 10%, paste heavy 10%. 5 of 16 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0073433: billed 99215, patient aged 40 with 1 chronic condition(s) (heart failure). C0073445: billed 99215, patient aged 52 with 0 chronic condition(s). C0073459: billed 99215, patient aged 63 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000150.svg)

## Records-review sample so far

Documentation is on file for 30 claims (5% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 15 | 0 | 0.0% | 3.1% |
| 99214 | 12 | 0 | 0.0% | 5.1% |
| 99215 | 3 | 0 | 0.0% | 42.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (38 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0073433, C0073445, C0073459 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 30% address fewer problems than their level implies and 10% were signed late; request the audit trail for C0073433, C0073445, C0073459.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
