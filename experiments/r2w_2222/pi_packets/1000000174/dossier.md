# Payment Integrity dossier: 1000000174

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 126 |
| Billed mix (99211 to 99215) | 1 / 0 / 37 / 145 / 59 |
| 99215 share | 24.4% |
| Expected 99215 share given patient complexity | 7.1% |
| Screen scores | z vs peers 2.79; risk-adjusted 3.79; flagged by eb_ratio |

## Case summary (advisory)

**1000000174: 17 of 20 documented 99215 claims (85%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000174 billed 99215 on 24.4% of 242 claims against an expected 7.1% given patient complexity (risk-adjusted score 3.79; plain z-score vs peers 2.79). 17% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 17 (85%) were documented below the billed level, against 20% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 9%, late 4%, unsigned 0%, data 4%. No audit trail was received. 2 of 36 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0084371: billed 99215; documented MDM level moderate, 33 minutes. C0084386: billed 99215, patient aged 48 with 1 chronic condition(s) (atrial fibrillation); documented MDM level moderate, minutes not recorded. C0084406: billed 99215, patient aged 68 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0084328: billed 99215, patient aged 31 with 1 chronic condition(s) (type 2 diabetes). C0084336: billed 99215, patient aged 18 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000174.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 2 | 40.0% | 3.9% |
| 99214 | 20 | 1 | 5.0% | 5.9% |
| 99215 | 20 | 17 | 85.0% | 19.5% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (32 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0084371, C0084386, C0084406 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 9% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0084371, C0084386, C0084406.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
