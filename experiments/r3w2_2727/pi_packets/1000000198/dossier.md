# Payment Integrity dossier: 1000000198

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,539 / 776 |
| Billed mix (99211 to 99215) | 11 / 19 / 283 / 723 / 503 |
| 99215 share | 32.7% |
| Expected 99215 share given patient complexity | 5.6% |
| Screen scores | z vs peers 5.07; risk-adjusted 18.51; flagged by eb_ratio |

## Case summary (advisory)

**1000000198: 0 of 10 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000198 billed 99215 on 32.7% of 1,539 claims against an expected 5.6% given patient complexity (risk-adjusted score 18.51; plain z-score vs peers 5.07). 42% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 10 documented 99215 claims, 0 (0%) were documented below the billed level, against 47% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 37%, late 13%, unsigned 0%, data 13%, bulk created 7%, paste heavy 10%. 5 of 23 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0087224: billed 99215, patient aged 35 with 1 chronic condition(s) (hyperlipidemia). C0087388: billed 99215, patient aged 28 with 0 chronic condition(s). C0087417: billed 99215, patient aged 47 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000198.svg)

## Records-review sample so far

Documentation is on file for 30 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 2.0% |
| 99214 | 15 | 0 | 0.0% | 3.6% |
| 99215 | 10 | 0 | 0.0% | 47.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (60 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0087224, C0087388, C0087417 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 37% address fewer problems than their level implies and 13% were signed late; request the audit trail for C0087224, C0087388, C0087417.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
