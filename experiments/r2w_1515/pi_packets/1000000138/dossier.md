# Payment Integrity dossier: 1000000138

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 245 / 123 |
| Billed mix (99211 to 99215) | 2 / 3 / 51 / 134 / 55 |
| 99215 share | 22.4% |
| Expected 99215 share given patient complexity | 5.1% |
| Screen scores | z vs peers 2.21; risk-adjusted 5.04; flagged by eb_ratio |

## Case summary (advisory)

**1000000138: 0 of 9 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000138 billed 99215 on 22.4% of 245 claims against an expected 5.1% given patient complexity (risk-adjusted score 5.04; plain z-score vs peers 2.21). 56% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 9 documented 99215 claims, 0 (0%) were documented below the billed level, against 39% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 47%, late 17%, unsigned 0%, data 7%, bulk created 13%, paste heavy 13%. 2 of 24 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0069945: billed 99215, patient aged 43 with 0 chronic condition(s). C0069952: billed 99215, patient aged 71 with 1 chronic condition(s) (obesity). C0069955: billed 99215, patient aged 34 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000138.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 3.6% |
| 99214 | 15 | 0 | 0.0% | 4.2% |
| 99215 | 9 | 0 | 0.0% | 39.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (31 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0069945, C0069952, C0069955 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 47% address fewer problems than their level implies and 17% were signed late; request the audit trail for C0069945, C0069952, C0069955.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
