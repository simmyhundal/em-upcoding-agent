# Payment Integrity dossier: 1000000213

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 627 / 315 |
| Billed mix (99211 to 99215) | 5 / 9 / 152 / 304 / 157 |
| 99215 share | 25.0% |
| Expected 99215 share given patient complexity | 4.6% |
| Screen scores | z vs peers 2.58; risk-adjusted 9.40; flagged by eb_ratio |

## Case summary (advisory)

**1000000213: 0 of 6 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000213 billed 99215 on 25.0% of 627 claims against an expected 4.6% given patient complexity (risk-adjusted score 9.40; plain z-score vs peers 2.58). 56% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 6 documented 99215 claims, 0 (0%) were documented below the billed level, against 29% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 40%, late 7%, unsigned 0%, data 10%, bulk created 3%, paste heavy 13%. 3 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0107963: billed 99214; documented MDM level low, minutes not recorded. C0108144: billed 99214; documented MDM level low, minutes not recorded. C0107656: billed 99215, patient aged 26 with 1 chronic condition(s) (hypothyroidism). C0107705: billed 99215, patient aged 38 with 1 chronic condition(s) (heart failure). C0107759: billed 99215, patient aged 58 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000213.svg)

## Records-review sample so far

Documentation is on file for 30 claims (5% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 5.0% |
| 99214 | 16 | 2 | 12.5% | 7.6% |
| 99215 | 6 | 0 | 0.0% | 28.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (48 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0107963, C0108144, C0107656 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 40% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0107963, C0108144, C0107656.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
