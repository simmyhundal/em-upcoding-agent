# Payment Integrity dossier: 1000000085

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,143 / 552 |
| Billed mix (99211 to 99215) | 9 / 13 / 351 / 542 / 228 |
| 99215 share | 19.9% |
| Expected 99215 share given patient complexity | 5.1% |
| Screen scores | z vs peers 1.85; risk-adjusted 8.22; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000085: 3 of 24 documented 99215 claims (12%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000085 billed 99215 on 19.9% of 1,143 claims against an expected 5.1% given patient complexity (risk-adjusted score 8.22; plain z-score vs peers 1.85). 52% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 24 documented 99215 claims, 3 (12%) were documented below the billed level, against 27% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 33%, late 22%, unsigned 0%, data 11%, bulk created 9%, paste heavy 11%. 5 of 34 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0045739: billed 99215; documented MDM level moderate, minutes not recorded. C0046104: billed 99215; documented MDM level moderate, minutes not recorded. C0046244: billed 99215; documented MDM level moderate, 31 minutes. C0045171: billed 99215, patient aged 33 with 1 chronic condition(s) (type 2 diabetes). C0045201: billed 99215, patient aged 63 with 1 chronic condition(s) (hyperlipidemia). C0045222: billed 99215, patient aged 50 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000085.svg)

## Records-review sample so far

Documentation is on file for 45 claims (4% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 1 | 14.3% | 0.0% |
| 99214 | 13 | 0 | 0.0% | 5.3% |
| 99215 | 24 | 3 | 12.5% | 26.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (53 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0045739, C0046104, C0046244 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 33% address fewer problems than their level implies and 22% were signed late; request the audit trail for C0045739, C0046104, C0046244.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
