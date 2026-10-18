# Payment Integrity dossier: 1000000168

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 114 |
| Billed mix (99211 to 99215) | 0 / 6 / 61 / 150 / 24 |
| 99215 share | 10.0% |
| Expected 99215 share given patient complexity | 3.1% |
| Screen scores | z vs peers 0.75; risk-adjusted 2.43; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000168: 0 of 17 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000168 billed 99215 on 10.0% of 241 claims against an expected 3.1% given patient complexity (risk-adjusted score 2.43; plain z-score vs peers 0.75). 83% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 17 documented 99215 claims, 0 (0%) were documented below the billed level, against 36% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 56%, late 20%, unsigned 0%, data 9%, bulk created 2%, paste heavy 2%. 5 of 38 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0072914: billed 99214; documented MDM level low, minutes not recorded. C0072872: billed 99215, patient aged 25 with 0 chronic condition(s). C0072874: billed 99215, patient aged 18 with 0 chronic condition(s). C0072885: billed 99215, patient aged 59 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000168.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 5.5% |
| 99214 | 18 | 1 | 5.6% | 8.1% |
| 99215 | 17 | 0 | 0.0% | 35.5% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (24 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0072914, C0072872, C0072874 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 56% address fewer problems than their level implies and 20% were signed late; request the audit trail for C0072914, C0072872, C0072874.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
