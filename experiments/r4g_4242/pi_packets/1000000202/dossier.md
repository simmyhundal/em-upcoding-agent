# Payment Integrity dossier: 1000000202

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 151 / 76 |
| Billed mix (99211 to 99215) | 3 / 1 / 43 / 75 / 29 |
| 99215 share | 19.2% |
| Expected 99215 share given patient complexity | 5.5% |
| Screen scores | z vs peers 2.31; risk-adjusted 2.96; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000202: 1 of 10 documented 99215 claims (10%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000202 billed 99215 on 19.2% of 151 claims against an expected 5.5% given patient complexity (risk-adjusted score 2.96; plain z-score vs peers 2.31). 28% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 10 documented 99215 claims, 1 (10%) were documented below the billed level, against 41% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 13%, late 13%, unsigned 0%, data 3%, bulk created 0%, paste heavy 3%. 4 of 24 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0107366: billed 99215, patient aged 50 with 4 chronic condition(s) (type 2 diabetes;obesity;depression;heart failure); documented MDM level moderate, minutes not recorded. C0107288: billed 99215, patient aged 27 with 0 chronic condition(s). C0107292: billed 99215, patient aged 67 with 1 chronic condition(s) (obesity). C0107297: billed 99215, patient aged 27 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000202.svg)

## Records-review sample so far

Documentation is on file for 30 claims (20% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 6.5% |
| 99214 | 13 | 0 | 0.0% | 6.6% |
| 99215 | 10 | 1 | 10.0% | 41.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0107366, C0107288, C0107292 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 13% address fewer problems than their level implies and 13% were signed late; request the audit trail for C0107366, C0107288, C0107292.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
