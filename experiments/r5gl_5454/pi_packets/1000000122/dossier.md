# Payment Integrity dossier: 1000000122

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 229 / 121 |
| Billed mix (99211 to 99215) | 0 / 4 / 48 / 120 / 57 |
| 99215 share | 24.9% |
| Expected 99215 share given patient complexity | 5.4% |
| Screen scores | z vs peers 2.73; risk-adjusted 5.36; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000122: 17 of 20 documented 99215 claims (85%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000122 billed 99215 on 24.9% of 229 claims against an expected 5.4% given patient complexity (risk-adjusted score 5.36; plain z-score vs peers 2.73). 51% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 17 (85%) were documented below the billed level, against 22% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 18%, late 9%, unsigned 0%, data 7%, bulk created 0%, paste heavy 2%. 5 of 36 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0059002: billed 99215; documented MDM level moderate, 30 minutes. C0059046: billed 99215, patient aged 44 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0059084: billed 99215; documented MDM level moderate, 30 minutes. C0058982: billed 99215, patient aged 28 with 1 chronic condition(s) (osteoarthritis). C0058989: billed 99215, patient aged 51 with 0 chronic condition(s). C0058992: billed 99215, patient aged 55 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000122.svg)

## Records-review sample so far

Documentation is on file for 45 claims (20% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 4.1% |
| 99214 | 20 | 4 | 20.0% | 7.3% |
| 99215 | 20 | 17 | 85.0% | 22.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (32 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0059002, C0059046, C0059084 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 18% address fewer problems than their level implies and 9% were signed late; request the audit trail for C0059002, C0059046, C0059084.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
