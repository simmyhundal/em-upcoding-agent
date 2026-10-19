# Payment Integrity dossier: 1000000166

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,405 / 1,175 |
| Billed mix (99211 to 99215) | 30 / 54 / 696 / 1,105 / 520 |
| 99215 share | 21.6% |
| Expected 99215 share given patient complexity | 4.1% |
| Screen scores | z vs peers 2.18; risk-adjusted 16.70; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000166: 16 of 19 documented 99215 claims (84%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000166 billed 99215 on 21.6% of 2,405 claims against an expected 4.1% given patient complexity (risk-adjusted score 16.70; plain z-score vs peers 2.18). 72% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 16 (84%) were documented below the billed level, against 24% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 53%, late 7%, unsigned 0%, data 0%, bulk created 0%, paste heavy 2%. 2 of 28 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0086770: billed 99215; documented MDM level moderate, 38 minutes. C0086820: billed 99215; documented MDM level moderate, 33 minutes. C0086879: billed 99215; documented MDM level moderate, 30 minutes. C0085597: billed 99215, patient aged 30 with 0 chronic condition(s). C0085778: billed 99215, patient aged 66 with 1 chronic condition(s) (hypertension). C0085826: billed 99215, patient aged 31 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000166.svg)

## Records-review sample so far

Documentation is on file for 45 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 2.7% |
| 99214 | 19 | 6 | 31.6% | 7.1% |
| 99215 | 19 | 16 | 84.2% | 23.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (60 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0086770, C0086820, C0086879 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 53% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0086770, C0086820, C0086879.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
