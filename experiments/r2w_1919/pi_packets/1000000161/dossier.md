# Payment Integrity dossier: 1000000161

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 363 / 172 |
| Billed mix (99211 to 99215) | 2 / 10 / 105 / 200 / 46 |
| 99215 share | 12.7% |
| Expected 99215 share given patient complexity | 3.6% |
| Screen scores | z vs peers 1.16; risk-adjusted 3.73; flagged by eb_ratio |

## Case summary (advisory)

**1000000161: 0 of 20 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000161 billed 99215 on 12.7% of 363 claims against an expected 3.6% given patient complexity (risk-adjusted score 3.73; plain z-score vs peers 1.16). 70% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 0 (0%) were documented below the billed level, against 35% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 56%, late 16%, unsigned 0%, data 0%, bulk created 2%, paste heavy 4%. 1 of 36 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0078141: billed 99213; documented MDM level straightforward, minutes not recorded. C0077901: billed 99215, patient aged 79 with 0 chronic condition(s); documented MDM level high, 47 minutes. C0077903: billed 99215, patient aged 43 with 1 chronic condition(s) (hypertension). C0077915: billed 99215, patient aged 69 with 1 chronic condition(s) (atrial fibrillation).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000161.svg)

## Records-review sample so far

Documentation is on file for 45 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 1 | 25.0% | 3.4% |
| 99214 | 20 | 0 | 0.0% | 4.6% |
| 99215 | 20 | 0 | 0.0% | 34.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (28 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0078141, C0077901, C0077903 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 56% address fewer problems than their level implies and 16% were signed late; request the audit trail for C0078141, C0077901, C0077903.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
