# Payment Integrity dossier: 1000000177

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 239 / 112 |
| Billed mix (99211 to 99215) | 5 / 9 / 102 / 94 / 29 |
| 99215 share | 12.1% |
| Expected 99215 share given patient complexity | 3.5% |
| Screen scores | z vs peers 0.96; risk-adjusted 2.77; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000177: 16 of 19 documented 99215 claims (84%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000177 billed 99215 on 12.1% of 239 claims against an expected 3.5% given patient complexity (risk-adjusted score 2.77; plain z-score vs peers 0.96). 83% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 16 (84%) were documented below the billed level, against 20% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 40%, late 4%, unsigned 0%, data 2%. No audit trail was received. 3 of 17 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0089102: billed 99215, patient aged 29 with 1 chronic condition(s) (hyperlipidemia); documented MDM level moderate, 31 minutes. C0089103: billed 99215; documented MDM level moderate, 35 minutes. C0089271: billed 99215, patient aged 50 with 0 chronic condition(s); documented MDM level moderate, 39 minutes. C0089055: billed 99215, patient aged 81 with 1 chronic condition(s) (hyperlipidemia). C0089081: billed 99215, patient aged 66 with 1 chronic condition(s) (osteoarthritis). C0089089: billed 99215, patient aged 47 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000177.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 16 | 2 | 12.5% | 3.2% |
| 99214 | 7 | 3 | 42.9% | 5.0% |
| 99215 | 19 | 16 | 84.2% | 20.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0089102, C0089103, C0089271 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 40% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0089102, C0089103, C0089271.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
