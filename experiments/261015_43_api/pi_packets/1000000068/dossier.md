# Payment Integrity dossier: 1000000068

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 275 / 132 |
| Billed mix (99211 to 99215) | 0 / 0 / 54 / 147 / 74 |
| 99215 share | 26.9% |
| Expected 99215 share given patient complexity | 2.1% |
| Screen scores | z vs peers 3.70; risk-adjusted 9.19; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000068: 0 of 6 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000068 billed 99215 on 26.9% of 275 claims against an expected 2.1% given patient complexity (risk-adjusted score 9.19; plain z-score vs peers 3.70). 69% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 24 claims. Of 6 documented 99215 claims, 0 (0%) were documented below the billed level, against 0% for the comparison providers. Note checks on 24 returned notes (share showing each sign): problems 38%, late 25%, unsigned 0%, data 8%, bulk created 17%, paste heavy 8%. 3 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0041853: billed 99215, patient aged 49 with 1 chronic condition(s) (type 2 diabetes). C0041869: billed 99215, patient aged 33 with 1 chronic condition(s) (atrial fibrillation). C0041898: billed 99215, patient aged 45 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000068.svg)

## Records-review sample so far

Documentation is on file for 24 claims (9% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 2 | 0 | 0.0% | 1.6% |
| 99214 | 16 | 0 | 0.0% | 3.3% |
| 99215 | 6 | 0 | 0.0% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (36 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0041853, C0041869, C0041898 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 38% address fewer problems than their level implies and 25% were signed late; request the audit trail for C0041853, C0041869, C0041898.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
