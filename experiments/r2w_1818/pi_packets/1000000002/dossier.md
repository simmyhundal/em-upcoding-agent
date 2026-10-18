# Payment Integrity dossier: 1000000002

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 120 |
| Billed mix (99211 to 99215) | 6 / 7 / 66 / 113 / 49 |
| 99215 share | 20.3% |
| Expected 99215 share given patient complexity | 4.0% |
| Screen scores | z vs peers 2.94; risk-adjusted 5.68; flagged by eb_ratio |

## Case summary (advisory)

**1000000002: 15 of 20 documented 99215 claims (75%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000002 billed 99215 on 20.3% of 241 claims against an expected 4.0% given patient complexity (risk-adjusted score 5.68; plain z-score vs peers 2.94). 78% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 44 claims. Of 20 documented 99215 claims, 15 (75%) were documented below the billed level, against 32% for the comparison providers. Note checks on 44 returned notes (share showing each sign): problems 32%, late 0%, unsigned 0%, data 2%. No audit trail was received. 2 of 28 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0000362: billed 99215, patient aged 65 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0000402: billed 99215, patient aged 67 with 0 chronic condition(s); documented MDM level moderate, 25 minutes. C0000472: billed 99215; documented MDM level moderate, 33 minutes. C0000342: billed 99215, patient aged 43 with 1 chronic condition(s) (hypothyroidism). C0000345: billed 99215, patient aged 32 with 1 chronic condition(s) (depression). C0000351: billed 99215, patient aged 83 with 1 chronic condition(s) (type 2 diabetes).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000002.svg)

## Records-review sample so far

Documentation is on file for 44 claims (18% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 0 | 0.0% | 3.3% |
| 99214 | 16 | 8 | 50.0% | 5.9% |
| 99215 | 20 | 15 | 75.0% | 32.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0000362, C0000402, C0000472 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 32% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0000362, C0000402, C0000472.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
