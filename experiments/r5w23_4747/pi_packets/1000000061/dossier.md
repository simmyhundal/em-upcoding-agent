# Payment Integrity dossier: 1000000061

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 245 / 130 |
| Billed mix (99211 to 99215) | 4 / 3 / 76 / 121 / 41 |
| 99215 share | 16.7% |
| Expected 99215 share given patient complexity | 4.4% |
| Screen scores | z vs peers 1.46; risk-adjusted 3.22; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000061: 0 of 19 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000061 billed 99215 on 16.7% of 245 claims against an expected 4.4% given patient complexity (risk-adjusted score 3.22; plain z-score vs peers 1.46). 59% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 0 (0%) were documented below the billed level, against 32% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 58%, late 24%, unsigned 0%, data 9%. No audit trail was received. 4 of 33 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0037209: billed 99214; documented MDM level low, minutes not recorded. C0037185: billed 99215, patient aged 39 with 1 chronic condition(s) (type 2 diabetes). C0037193: billed 99215, patient aged 64 with 1 chronic condition(s) (depression). C0037230: billed 99215, patient aged 47 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000061.svg)

## Records-review sample so far

Documentation is on file for 45 claims (18% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 2.8% |
| 99214 | 19 | 1 | 5.3% | 6.3% |
| 99215 | 19 | 0 | 0.0% | 32.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (26 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0037209, C0037185, C0037193 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 58% address fewer problems than their level implies and 24% were signed late; request the audit trail for C0037209, C0037185, C0037193.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
