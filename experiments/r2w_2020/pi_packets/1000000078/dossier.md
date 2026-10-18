# Payment Integrity dossier: 1000000078

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,405 / 1,162 |
| Billed mix (99211 to 99215) | 38 / 80 / 804 / 1,134 / 349 |
| 99215 share | 14.5% |
| Expected 99215 share given patient complexity | 4.6% |
| Screen scores | z vs peers 1.08; risk-adjusted 8.40; flagged by eb_ratio |

## Case summary (advisory)

**1000000078: 13 of 19 documented 99215 claims (68%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000078 billed 99215 on 14.5% of 2,405 claims against an expected 4.6% given patient complexity (risk-adjusted score 8.40; plain z-score vs peers 1.08). 49% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 21 claims. Of 19 documented 99215 claims, 13 (68%) were documented below the billed level, against 15% for the comparison providers. Note checks on 21 returned notes (share showing each sign): problems 29%, late 5%, unsigned 0%, data 5%. No audit trail was received. 2 of 16 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0038353: billed 99215, patient aged 63 with 1 chronic condition(s) (type 2 diabetes); documented MDM level moderate, minutes not recorded. C0039416: billed 99215; documented MDM level moderate, 32 minutes. C0039473: billed 99215; documented MDM level moderate, minutes not recorded. C0038312: billed 99215, patient aged 53 with 0 chronic condition(s). C0038832: billed 99215, patient aged 47 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000078.svg)

## Records-review sample so far

Documentation is on file for 21 claims (1% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99214 | 2 | 1 | 50.0% | 4.5% |
| 99215 | 19 | 13 | 68.4% | 15.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (57 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0038353, C0039416, C0039473 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 29% address fewer problems than their level implies and 5% were signed late; request the audit trail for C0038353, C0039416, C0039473.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
