# Payment Integrity dossier: 1000000166

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 259 / 128 |
| Billed mix (99211 to 99215) | 4 / 2 / 46 / 139 / 68 |
| 99215 share | 26.3% |
| Expected 99215 share given patient complexity | 5.5% |
| Screen scores | z vs peers 3.48; risk-adjusted 6.47; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000166: 6 of 7 documented 99215 claims (86%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000166 billed 99215 on 26.3% of 259 claims against an expected 5.5% given patient complexity (risk-adjusted score 6.47; plain z-score vs peers 3.48). 51% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 7 documented 99215 claims, 6 (86%) were documented below the billed level, against 42% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 33%, late 0%, unsigned 0%, data 7%. No audit trail was received. 2 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0078233: billed 99215; documented MDM level moderate, 31 minutes. C0078343: billed 99215; documented MDM level moderate, 37 minutes. C0078376: billed 99215, patient aged 72 with 1 chronic condition(s) (hypertension); documented MDM level moderate, 36 minutes. C0078229: billed 99215, patient aged 67 with 1 chronic condition(s) (asthma). C0078253: billed 99215, patient aged 18 with 0 chronic condition(s). C0078257: billed 99215, patient aged 38 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000166.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 3.9% |
| 99214 | 18 | 3 | 16.7% | 7.0% |
| 99215 | 7 | 6 | 85.7% | 42.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (35 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0078233, C0078343, C0078376 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 33% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0078233, C0078343, C0078376.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
