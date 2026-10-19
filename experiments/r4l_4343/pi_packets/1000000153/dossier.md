# Payment Integrity dossier: 1000000153

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 111 |
| Billed mix (99211 to 99215) | 3 / 3 / 58 / 130 / 48 |
| 99215 share | 19.8% |
| Expected 99215 share given patient complexity | 5.9% |
| Screen scores | z vs peers 2.37; risk-adjusted 3.87; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000153: 1 of 7 documented 99215 claims (14%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000153 billed 99215 on 19.8% of 242 claims against an expected 5.9% given patient complexity (risk-adjusted score 3.87; plain z-score vs peers 2.37). 33% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 7 documented 99215 claims, 1 (14%) were documented below the billed level, against 22% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 38%, late 21%, unsigned 0%, data 17%, bulk created 17%, paste heavy 21%. 5 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0080602: billed 99215; documented MDM level moderate, minutes not recorded. C0080573: billed 99215, patient aged 70 with 1 chronic condition(s) (hyperlipidemia); documented MDM level high, 48 minutes. C0080579: billed 99215, patient aged 53 with 0 chronic condition(s). C0080588: billed 99215, patient aged 65 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000153.svg)

## Records-review sample so far

Documentation is on file for 29 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 4.1% |
| 99214 | 15 | 1 | 6.7% | 5.0% |
| 99215 | 7 | 1 | 14.3% | 21.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0080602, C0080573, C0080579 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 38% address fewer problems than their level implies and 21% were signed late; request the audit trail for C0080602, C0080573, C0080579.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
