# Payment Integrity dossier: 1000000019

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 238 / 114 |
| Billed mix (99211 to 99215) | 0 / 4 / 37 / 115 / 82 |
| 99215 share | 34.5% |
| Expected 99215 share given patient complexity | 4.6% |
| Screen scores | z vs peers 5.22; risk-adjusted 9.20; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000019: 0 of 26 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000019 billed 99215 on 34.5% of 238 claims against an expected 4.6% given patient complexity (risk-adjusted score 9.20; plain z-score vs peers 5.22). 62% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 26 documented 99215 claims, 0 (0%) were documented below the billed level, against 41% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 47%, late 24%, unsigned 0%, data 4%, bulk created 7%, paste heavy 9%. 4 of 41 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0009263: billed 99215, patient aged 49 with 1 chronic condition(s) (hyperlipidemia). C0009266: billed 99215, patient aged 37 with 1 chronic condition(s) (hypertension). C0009272: billed 99215, patient aged 43 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000019.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 3 | 0 | 0.0% | 6.5% |
| 99214 | 15 | 0 | 0.0% | 6.6% |
| 99215 | 26 | 0 | 0.0% | 41.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (38 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0009263, C0009266, C0009272 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 47% address fewer problems than their level implies and 24% were signed late; request the audit trail for C0009263, C0009266, C0009272.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
