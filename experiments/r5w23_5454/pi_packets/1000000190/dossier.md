# Payment Integrity dossier: 1000000190

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 906 / 448 |
| Billed mix (99211 to 99215) | 3 / 7 / 114 / 398 / 384 |
| 99215 share | 42.4% |
| Expected 99215 share given patient complexity | 7.4% |
| Screen scores | z vs peers 5.52; risk-adjusted 16.94; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000190: 1 of 11 documented 99215 claims (9%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000190 billed 99215 on 42.4% of 906 claims against an expected 7.4% given patient complexity (risk-adjusted score 16.94; plain z-score vs peers 5.52). 26% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 26 claims. Of 11 documented 99215 claims, 1 (9%) were documented below the billed level, against 22% for the comparison providers. Note checks on 26 returned notes (share showing each sign): problems 23%, late 15%, unsigned 0%, data 15%, bulk created 0%, paste heavy 0%. 4 of 21 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0089303: billed 99215; documented MDM level moderate, minutes not recorded. C0088571: billed 99215, patient aged 26 with 0 chronic condition(s). C0088574: billed 99215, patient aged 40 with 0 chronic condition(s). C0088589: billed 99215, patient aged 44 with 1 chronic condition(s) (type 2 diabetes).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000190.svg)

## Records-review sample so far

Documentation is on file for 26 claims (3% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99214 | 14 | 1 | 7.1% | 7.3% |
| 99215 | 11 | 1 | 9.1% | 22.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (58 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0089303, C0088571, C0088574 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 23% address fewer problems than their level implies and 15% were signed late; request the audit trail for C0089303, C0088571, C0088574.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
