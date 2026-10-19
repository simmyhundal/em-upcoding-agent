# Payment Integrity dossier: 1000000086

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 250 / 126 |
| Billed mix (99211 to 99215) | 2 / 4 / 46 / 138 / 60 |
| 99215 share | 24.0% |
| Expected 99215 share given patient complexity | 4.5% |
| Screen scores | z vs peers 2.56; risk-adjusted 5.89; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000086: 0 of 6 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000086 billed 99215 on 24.0% of 250 claims against an expected 4.5% given patient complexity (risk-adjusted score 5.89; plain z-score vs peers 2.56). 62% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 6 documented 99215 claims, 0 (0%) were documented below the billed level, against 31% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 45%, late 17%, unsigned 0%, data 21%, bulk created 14%, paste heavy 24%. 6 of 21 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0045685: billed 99215, patient aged 32 with 0 chronic condition(s). C0045692: billed 99215, patient aged 37 with 0 chronic condition(s). C0045707: billed 99215, patient aged 35 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000086.svg)

## Records-review sample so far

Documentation is on file for 29 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 3 | 0 | 0.0% | 4.8% |
| 99214 | 17 | 0 | 0.0% | 4.6% |
| 99215 | 6 | 0 | 0.0% | 31.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (33 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0045685, C0045692, C0045707 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 45% address fewer problems than their level implies and 17% were signed late; request the audit trail for C0045685, C0045692, C0045707.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
