# Payment Integrity dossier: 1000000072

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 503 / 251 |
| Billed mix (99211 to 99215) | 2 / 2 / 81 / 287 / 131 |
| 99215 share | 26.0% |
| Expected 99215 share given patient complexity | 6.8% |
| Screen scores | z vs peers 3.30; risk-adjusted 6.12; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000072: 0 of 22 documented 99214 and 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000072 billed 99215 on 26.0% of 503 claims against an expected 6.8% given patient complexity (risk-adjusted score 6.12; plain z-score vs peers 3.30). 20% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 4 documented 99215 claims, 0 (0%) were documented below the billed level, against 40% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 27%, late 17%, unsigned 0%, data 20%, bulk created 10%, paste heavy 10%. 6 of 21 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0038599: billed 99215, patient aged 57 with 1 chronic condition(s) (atrial fibrillation). C0038650: billed 99215, patient aged 64 with 1 chronic condition(s) (hyperlipidemia). C0038688: billed 99215, patient aged 70 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000072.svg)

## Records-review sample so far

Documentation is on file for 30 claims (6% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 2.9% |
| 99214 | 18 | 0 | 0.0% | 4.6% |
| 99215 | 4 | 0 | 0.0% | 40.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (45 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0038599, C0038650, C0038688 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 27% address fewer problems than their level implies and 17% were signed late; request the audit trail for C0038599, C0038650, C0038688.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
