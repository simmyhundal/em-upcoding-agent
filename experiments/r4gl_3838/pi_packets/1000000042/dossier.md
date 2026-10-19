# Payment Integrity dossier: 1000000042

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 350 / 155 |
| Billed mix (99211 to 99215) | 8 / 5 / 104 / 160 / 73 |
| 99215 share | 20.9% |
| Expected 99215 share given patient complexity | 4.1% |
| Screen scores | z vs peers 2.68; risk-adjusted 6.49; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000042: 18 of 22 documented 99215 claims (82%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000042 billed 99215 on 20.9% of 350 claims against an expected 4.1% given patient complexity (risk-adjusted score 6.49; plain z-score vs peers 2.68). 64% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 22 documented 99215 claims, 18 (82%) were documented below the billed level, against 42% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 22%, late 2%, unsigned 0%, data 2%. No audit trail was received. 2 of 23 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0015041: billed 99215, patient aged 49 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0015187: billed 99215, patient aged 19 with 0 chronic condition(s); documented MDM level moderate, 39 minutes. C0015303: billed 99215; documented MDM level moderate, 39 minutes. C0014999: billed 99215, patient aged 45 with 1 chronic condition(s) (type 2 diabetes). C0015008: billed 99215, patient aged 42 with 0 chronic condition(s). C0015009: billed 99215, patient aged 43 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000042.svg)

## Records-review sample so far

Documentation is on file for 45 claims (13% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 0 | 0.0% | 3.1% |
| 99214 | 12 | 5 | 41.7% | 5.1% |
| 99215 | 22 | 18 | 81.8% | 42.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (36 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0015041, C0015187, C0015303 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 22% address fewer problems than their level implies and 2% were signed late; request the audit trail for C0015041, C0015187, C0015303.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
