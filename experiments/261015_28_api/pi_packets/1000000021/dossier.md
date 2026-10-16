# Payment Integrity dossier: 1000000021

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 238 / 115 |
| Billed mix (99211 to 99215) | 4 / 1 / 52 / 135 / 46 |
| 99215 share | 19.3% |
| Expected 99215 share given patient complexity | 1.8% |
| Screen scores | z vs peers 2.34; risk-adjusted 7.91; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000021: 0 of 19 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000021 billed 99215 on 19.3% of 238 claims against an expected 1.8% given patient complexity (risk-adjusted score 7.91; plain z-score vs peers 2.34). 80% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 44 claims. Of 19 documented 99215 claims, 0 (0%) were documented below the billed level, against 0% for the comparison providers. Note checks on 44 returned notes (share showing each sign): problems 50%, late 18%, unsigned 0%, data 18%, bulk created 0%, paste heavy 4%. 8 of 35 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0013199: billed 99215, patient aged 56 with 1 chronic condition(s) (atrial fibrillation). C0013202: billed 99215, patient aged 36 with 1 chronic condition(s) (asthma). C0013208: billed 99215, patient aged 24 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000021.svg)

## Records-review sample so far

Documentation is on file for 44 claims (18% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 1.2% |
| 99214 | 17 | 0 | 0.0% | 3.1% |
| 99215 | 19 | 0 | 0.0% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (28 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0013199, C0013202, C0013208 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 50% address fewer problems than their level implies and 18% were signed late; request the audit trail for C0013199, C0013202, C0013208.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
