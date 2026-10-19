# Payment Integrity dossier: 1000000210

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 246 / 109 |
| Billed mix (99211 to 99215) | 2 / 1 / 47 / 129 / 67 |
| 99215 share | 27.2% |
| Expected 99215 share given patient complexity | 5.8% |
| Screen scores | z vs peers 3.66; risk-adjusted 5.57; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000210: 0 of 8 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000210 billed 99215 on 27.2% of 246 claims against an expected 5.8% given patient complexity (risk-adjusted score 5.57; plain z-score vs peers 3.66). 42% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 8 documented 99215 claims, 0 (0%) were documented below the billed level, against 20% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 33%, late 13%, unsigned 0%, data 7%, bulk created 3%, paste heavy 10%. 5 of 25 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0106389: billed 99215, patient aged 41 with 1 chronic condition(s) (hypertension). C0106395: billed 99215, patient aged 34 with 1 chronic condition(s) (depression). C0106397: billed 99215, patient aged 65 with 1 chronic condition(s) (COPD).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000210.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 3.2% |
| 99214 | 17 | 0 | 0.0% | 5.0% |
| 99215 | 8 | 0 | 0.0% | 20.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (34 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0106389, C0106395, C0106397 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 33% address fewer problems than their level implies and 13% were signed late; request the audit trail for C0106389, C0106395, C0106397.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
