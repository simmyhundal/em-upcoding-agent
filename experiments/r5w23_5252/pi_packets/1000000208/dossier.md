# Payment Integrity dossier: 1000000208

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 523 / 253 |
| Billed mix (99211 to 99215) | 2 / 10 / 133 / 268 / 110 |
| 99215 share | 21.0% |
| Expected 99215 share given patient complexity | 4.2% |
| Screen scores | z vs peers 2.80; risk-adjusted 7.27; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000208: 0 of 20 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000208 billed 99215 on 21.0% of 523 claims against an expected 4.2% given patient complexity (risk-adjusted score 7.27; plain z-score vs peers 2.80). 64% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 43 claims. Of 20 documented 99215 claims, 0 (0%) were documented below the billed level, against 24% for the comparison providers. Note checks on 43 returned notes (share showing each sign): problems 37%, late 12%, unsigned 0%, data 19%, bulk created 9%, paste heavy 12%. 9 of 32 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0101061: billed 99215, patient aged 37 with 1 chronic condition(s) (atrial fibrillation). C0101101: billed 99215, patient aged 52 with 0 chronic condition(s). C0101102: billed 99215, patient aged 32 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000208.svg)

## Records-review sample so far

Documentation is on file for 43 claims (8% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 0 | 0.0% | 1.8% |
| 99214 | 13 | 0 | 0.0% | 5.2% |
| 99215 | 20 | 0 | 0.0% | 24.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (43 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0101061, C0101101, C0101102 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 37% address fewer problems than their level implies and 12% were signed late; request the audit trail for C0101061, C0101101, C0101102.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
