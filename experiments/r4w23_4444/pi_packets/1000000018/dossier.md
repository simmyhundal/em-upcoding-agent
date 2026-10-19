# Payment Integrity dossier: 1000000018

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 371 / 170 |
| Billed mix (99211 to 99215) | 3 / 6 / 101 / 221 / 40 |
| 99215 share | 10.8% |
| Expected 99215 share given patient complexity | 4.5% |
| Screen scores | z vs peers 0.53; risk-adjusted 2.23; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000018: 10 of 19 documented 99215 claims (53%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000018 billed 99215 on 10.8% of 371 claims against an expected 4.5% given patient complexity (risk-adjusted score 2.23; plain z-score vs peers 0.53). 52% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 10 (53%) were documented below the billed level, against 31% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 33%, late 7%, unsigned 0%, data 2%. No audit trail was received. 2 of 34 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0013382: billed 99215, patient aged 48 with 4 chronic condition(s) (hyperlipidemia;hypertension;heart failure;osteoarthritis); documented MDM level moderate, 33 minutes. C0013407: billed 99215, patient aged 33 with 1 chronic condition(s) (depression); documented MDM level moderate, 31 minutes. C0013538: billed 99215, patient aged 18 with 0 chronic condition(s); documented MDM level moderate, 31 minutes. C0013368: billed 99215, patient aged 41 with 0 chronic condition(s). C0013379: billed 99215, patient aged 24 with 1 chronic condition(s) (type 2 diabetes).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000018.svg)

## Records-review sample so far

Documentation is on file for 45 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 1 | 14.3% | 4.8% |
| 99214 | 18 | 1 | 5.6% | 4.6% |
| 99215 | 19 | 10 | 52.6% | 31.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (26 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0013382, C0013407, C0013538 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 33% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0013382, C0013407, C0013538.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
