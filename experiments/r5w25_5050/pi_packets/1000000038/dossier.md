# Payment Integrity dossier: 1000000038

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 119 |
| Billed mix (99211 to 99215) | 1 / 9 / 47 / 135 / 50 |
| 99215 share | 20.7% |
| Expected 99215 share given patient complexity | 4.2% |
| Screen scores | z vs peers 2.25; risk-adjusted 4.53; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000038: 17 of 20 documented 99215 claims (85%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000038 billed 99215 on 20.7% of 242 claims against an expected 4.2% given patient complexity (risk-adjusted score 4.53; plain z-score vs peers 2.25). 70% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 17 (85%) were documented below the billed level, against 58% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 36%, late 9%, unsigned 0%, data 2%. No audit trail was received. 2 of 30 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0016765: billed 99215, patient aged 54 with 1 chronic condition(s) (asthma); documented MDM level moderate, 34 minutes. C0016797: billed 99215, patient aged 38 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0016820: billed 99215, patient aged 59 with 1 chronic condition(s) (hypertension); documented MDM level moderate, minutes not recorded. C0016751: billed 99215, patient aged 60 with 0 chronic condition(s). C0016759: billed 99215, patient aged 59 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000038.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 3.1% |
| 99214 | 19 | 1 | 5.3% | 6.2% |
| 99215 | 20 | 17 | 85.0% | 57.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0016765, C0016797, C0016820 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 36% address fewer problems than their level implies and 9% were signed late; request the audit trail for C0016765, C0016797, C0016820.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
