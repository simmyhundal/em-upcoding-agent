# Payment Integrity dossier: 1000000128

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 318 / 156 |
| Billed mix (99211 to 99215) | 1 / 2 / 65 / 169 / 81 |
| 99215 share | 25.5% |
| Expected 99215 share given patient complexity | 4.2% |
| Screen scores | z vs peers 3.77; risk-adjusted 7.70; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000128: 0 of 13 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000128 billed 99215 on 25.5% of 318 claims against an expected 4.2% given patient complexity (risk-adjusted score 7.70; plain z-score vs peers 3.77). 59% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 13 documented 99215 claims, 0 (0%) were documented below the billed level, against 43% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 41%, late 21%, unsigned 0%, data 10%, bulk created 14%, paste heavy 14%. 5 of 24 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0064998: billed 99213; documented MDM level straightforward, minutes not recorded. C0064677: billed 99215, patient aged 18 with 0 chronic condition(s). C0064692: billed 99215, patient aged 39 with 1 chronic condition(s) (type 2 diabetes). C0064701: billed 99215, patient aged 54 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000128.svg)

## Records-review sample so far

Documentation is on file for 29 claims (9% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 1 | 16.7% | 2.4% |
| 99214 | 10 | 0 | 0.0% | 4.8% |
| 99215 | 13 | 0 | 0.0% | 43.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (38 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0064998, C0064677, C0064692 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 41% address fewer problems than their level implies and 21% were signed late; request the audit trail for C0064998, C0064677, C0064692.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
