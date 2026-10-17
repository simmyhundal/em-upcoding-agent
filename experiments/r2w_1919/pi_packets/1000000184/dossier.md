# Payment Integrity dossier: 1000000184

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 243 / 112 |
| Billed mix (99211 to 99215) | 4 / 2 / 54 / 133 / 50 |
| 99215 share | 20.6% |
| Expected 99215 share given patient complexity | 4.6% |
| Screen scores | z vs peers 2.64; risk-adjusted 4.87; flagged by eb_ratio |

## Case summary (advisory)

**1000000184: 13 of 19 documented 99215 claims (68%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000184 billed 99215 on 20.6% of 243 claims against an expected 4.6% given patient complexity (risk-adjusted score 4.87; plain z-score vs peers 2.64). 46% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 13 (68%) were documented below the billed level, against 35% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 20%, late 2%, unsigned 0%, data 4%. No audit trail was received. 3 of 33 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0087504: billed 99215, patient aged 63 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0087543: billed 99215, patient aged 44 with 1 chronic condition(s) (atrial fibrillation); documented MDM level moderate, 37 minutes. C0087715: billed 99215, patient aged 50 with 1 chronic condition(s) (type 2 diabetes); documented MDM level moderate, 38 minutes. C0087483: billed 99215, patient aged 18 with 0 chronic condition(s). C0087501: billed 99215, patient aged 44 with 1 chronic condition(s) (asthma).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000184.svg)

## Records-review sample so far

Documentation is on file for 45 claims (18% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 3.4% |
| 99214 | 22 | 6 | 27.3% | 4.6% |
| 99215 | 19 | 13 | 68.4% | 34.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0087504, C0087543, C0087715 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 20% address fewer problems than their level implies and 2% were signed late; request the audit trail for C0087504, C0087543, C0087715.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
