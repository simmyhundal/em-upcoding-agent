# Payment Integrity dossier: 1000000210

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 239 / 120 |
| Billed mix (99211 to 99215) | 4 / 9 / 84 / 108 / 34 |
| 99215 share | 14.2% |
| Expected 99215 share given patient complexity | 3.5% |
| Screen scores | z vs peers 1.67; risk-adjusted 3.55; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000210: 1 of 20 documented 99215 claims (5%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000210 billed 99215 on 14.2% of 239 claims against an expected 3.5% given patient complexity (risk-adjusted score 3.55; plain z-score vs peers 1.67). 79% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 44 claims. Of 20 documented 99215 claims, 1 (5%) were documented below the billed level, against 47% for the comparison providers. Note checks on 44 returned notes (share showing each sign): problems 55%, late 32%, unsigned 0%, data 30%, bulk created 7%, paste heavy 11%. 13 of 35 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0106388: billed 99215, patient aged 18 with 1 chronic condition(s) (hyperlipidemia); documented MDM level moderate, minutes not recorded. C0106383: billed 99215, patient aged 40 with 0 chronic condition(s). C0106384: billed 99215, patient aged 57 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000210.svg)

## Records-review sample so far

Documentation is on file for 44 claims (18% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 12 | 0 | 0.0% | 3.6% |
| 99214 | 9 | 0 | 0.0% | 6.1% |
| 99215 | 20 | 1 | 5.0% | 46.9% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (23 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0106388, C0106383, C0106384 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 55% address fewer problems than their level implies and 32% were signed late; request the audit trail for C0106388, C0106383, C0106384.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
