# Payment Integrity dossier: 1000000124

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 909 / 450 |
| Billed mix (99211 to 99215) | 6 / 17 / 225 / 575 / 86 |
| 99215 share | 9.5% |
| Expected 99215 share given patient complexity | 3.5% |
| Screen scores | z vs peers 0.33; risk-adjusted 3.67; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000124: 4 of 21 documented 99214 and 99215 claims (19%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000124 billed 99215 on 9.5% of 909 claims against an expected 3.5% given patient complexity (risk-adjusted score 3.67; plain z-score vs peers 0.33). 76% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 2 documented 99215 claims, 1 (50%) were documented below the billed level, against 21% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 47%, late 13%, unsigned 0%, data 17%, bulk created 0%, paste heavy 0%. 5 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0062784: billed 99215; documented MDM level moderate, minutes not recorded. C0062600: billed 99215, patient aged 68 with 1 chronic condition(s) (osteoarthritis). C0062612: billed 99215, patient aged 49 with 0 chronic condition(s). C0062667: billed 99215, patient aged 41 with 1 chronic condition(s) (COPD).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000124.svg)

## Records-review sample so far

Documentation is on file for 30 claims (3% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 0 | 0.0% | 2.2% |
| 99214 | 19 | 3 | 15.8% | 8.9% |
| 99215 | 2 | 1 | 50.0% | 20.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (39 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0062784, C0062600, C0062612 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 47% address fewer problems than their level implies and 13% were signed late; request the audit trail for C0062784, C0062600, C0062612.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
