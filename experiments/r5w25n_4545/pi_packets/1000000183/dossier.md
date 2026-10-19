# Payment Integrity dossier: 1000000183

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 116 |
| Billed mix (99211 to 99215) | 3 / 6 / 82 / 117 / 34 |
| 99215 share | 14.1% |
| Expected 99215 share given patient complexity | 4.4% |
| Screen scores | z vs peers 1.32; risk-adjusted 2.61; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000183: 0 of 19 documented 99214 and 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000183 billed 99215 on 14.1% of 242 claims against an expected 4.4% given patient complexity (risk-adjusted score 2.61; plain z-score vs peers 1.32). 68% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 5 documented 99215 claims, 0 (0%) were documented below the billed level, against 48% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 50%, late 20%, unsigned 0%, data 7%. No audit trail was received. 4 of 20 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0075768: billed 99213; documented MDM level straightforward, minutes not recorded. C0075775: billed 99213; documented MDM level straightforward, 13 minutes. C0075613: billed 99215, patient aged 52 with 0 chronic condition(s). C0075619: billed 99215, patient aged 35 with 0 chronic condition(s). C0075622: billed 99215, patient aged 59 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000183.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 2 | 20.0% | 4.7% |
| 99214 | 14 | 0 | 0.0% | 4.7% |
| 99215 | 5 | 0 | 0.0% | 48.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (23 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0075768, C0075775, C0075613 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 50% address fewer problems than their level implies and 20% were signed late; request the audit trail for C0075768, C0075775, C0075613.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
