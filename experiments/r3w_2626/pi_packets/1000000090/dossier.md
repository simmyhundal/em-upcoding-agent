# Payment Integrity dossier: 1000000090

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 237 / 116 |
| Billed mix (99211 to 99215) | 3 / 2 / 48 / 118 / 66 |
| 99215 share | 27.8% |
| Expected 99215 share given patient complexity | 7.7% |
| Screen scores | z vs peers 3.56; risk-adjusted 4.37; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000090: 13 of 20 documented 99215 claims (65%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000090 billed 99215 on 27.8% of 237 claims against an expected 7.7% given patient complexity (risk-adjusted score 4.37; plain z-score vs peers 3.56). 18% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 13 (65%) were documented below the billed level, against 29% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 13%, late 7%, unsigned 0%, data 2%. No audit trail was received. 2 of 31 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0045930: billed 99215; documented MDM level moderate, 30 minutes. C0045971: billed 99215, patient aged 46 with 5 chronic condition(s) (type 2 diabetes;depression;hypertension;COPD;asthma); documented MDM level moderate, 38 minutes. C0045985: billed 99215, patient aged 44 with 0 chronic condition(s); documented MDM level moderate, 35 minutes. C0045964: billed 99215, patient aged 50 with 1 chronic condition(s) (hypothyroidism). C0045970: billed 99215, patient aged 43 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000090.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 5.0% |
| 99214 | 16 | 1 | 6.2% | 6.4% |
| 99215 | 20 | 13 | 65.0% | 29.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (34 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0045930, C0045971, C0045985 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 13% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0045930, C0045971, C0045985.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
