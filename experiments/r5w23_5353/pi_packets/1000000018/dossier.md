# Payment Integrity dossier: 1000000018

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 765 / 377 |
| Billed mix (99211 to 99215) | 10 / 24 / 214 / 435 / 82 |
| 99215 share | 10.7% |
| Expected 99215 share given patient complexity | 4.1% |
| Screen scores | z vs peers 0.50; risk-adjusted 3.72; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000018: 9 of 16 documented 99215 claims (56%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000018 billed 99215 on 10.7% of 765 claims against an expected 4.1% given patient complexity (risk-adjusted score 3.72; plain z-score vs peers 0.50). 67% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 16 documented 99215 claims, 9 (56%) were documented below the billed level, against 29% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 42%, late 2%, unsigned 0%, data 4%, bulk created 0%, paste heavy 0%. 2 of 30 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0007644: billed 99215; documented MDM level moderate, minutes not recorded. C0007686: billed 99215, patient aged 58 with 1 chronic condition(s) (heart failure); documented MDM level moderate, minutes not recorded. C0007887: billed 99215; documented MDM level low, minutes not recorded. C0007523: billed 99215, patient aged 53 with 1 chronic condition(s) (hypothyroidism). C0007602: billed 99215, patient aged 71 with 0 chronic condition(s). C0007668: billed 99215, patient aged 18 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000018.svg)

## Records-review sample so far

Documentation is on file for 45 claims (6% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 0 | 0.0% | 4.6% |
| 99214 | 19 | 1 | 5.3% | 4.1% |
| 99215 | 16 | 9 | 56.2% | 28.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (38 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0007644, C0007686, C0007887 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 42% address fewer problems than their level implies and 2% were signed late; request the audit trail for C0007644, C0007686, C0007887.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
