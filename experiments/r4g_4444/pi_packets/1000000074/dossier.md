# Payment Integrity dossier: 1000000074

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 445 / 216 |
| Billed mix (99211 to 99215) | 1 / 8 / 99 / 222 / 115 |
| 99215 share | 25.8% |
| Expected 99215 share given patient complexity | 4.2% |
| Screen scores | z vs peers 2.85; risk-adjusted 8.98; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000074: 0 of 7 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000074 billed 99215 on 25.8% of 445 claims against an expected 4.2% given patient complexity (risk-adjusted score 8.98; plain z-score vs peers 2.85). 64% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 7 documented 99215 claims, 0 (0%) were documented below the billed level, against 31% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 43%, late 10%, unsigned 0%, data 20%, bulk created 3%, paste heavy 13%. 7 of 20 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0040526: billed 99215, patient aged 56 with 0 chronic condition(s). C0040545: billed 99215, patient aged 55 with 1 chronic condition(s) (heart failure). C0040551: billed 99215, patient aged 39 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000074.svg)

## Records-review sample so far

Documentation is on file for 30 claims (7% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 4.8% |
| 99214 | 17 | 0 | 0.0% | 4.6% |
| 99215 | 7 | 0 | 0.0% | 31.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (43 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0040526, C0040545, C0040551 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 43% address fewer problems than their level implies and 10% were signed late; request the audit trail for C0040526, C0040545, C0040551.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
