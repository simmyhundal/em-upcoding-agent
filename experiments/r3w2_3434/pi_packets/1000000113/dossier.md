# Payment Integrity dossier: 1000000113

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 240 / 118 |
| Billed mix (99211 to 99215) | 0 / 1 / 30 / 136 / 73 |
| 99215 share | 30.4% |
| Expected 99215 share given patient complexity | 6.8% |
| Screen scores | z vs peers 3.29; risk-adjusted 4.95; flagged by eb_ratio |

## Case summary (advisory)

**1000000113: 5 of 10 documented 99215 claims (50%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000113 billed 99215 on 30.4% of 240 claims against an expected 6.8% given patient complexity (risk-adjusted score 4.95; plain z-score vs peers 3.29). 42% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 10 documented 99215 claims, 5 (50%) were documented below the billed level, against 32% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 30%, late 3%, unsigned 0%, data 10%. No audit trail was received. 4 of 23 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0050693: billed 99215; documented MDM level moderate, 38 minutes. C0050755: billed 99215; documented MDM level moderate, 30 minutes. C0050784: billed 99215; documented MDM level moderate, 32 minutes. C0050706: billed 99215, patient aged 45 with 1 chronic condition(s) (type 2 diabetes). C0050708: billed 99215, patient aged 42 with 0 chronic condition(s). C0050714: billed 99215, patient aged 50 with 1 chronic condition(s) (hypertension); documented MDM level high, 34 minutes.

## Evidence chart

![99215 share by patient complexity](../../charts/1000000113.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 3 | 0 | 0.0% | 4.6% |
| 99214 | 16 | 1 | 6.2% | 0.8% |
| 99215 | 10 | 5 | 50.0% | 32.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (36 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0050693, C0050755, C0050784 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 30% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0050693, C0050755, C0050784.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
