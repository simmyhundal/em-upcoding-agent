# Payment Integrity dossier: 1000000190

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 238 / 113 |
| Billed mix (99211 to 99215) | 1 / 2 / 42 / 139 / 54 |
| 99215 share | 22.7% |
| Expected 99215 share given patient complexity | 5.4% |
| Screen scores | z vs peers 2.74; risk-adjusted 4.52; flagged by eb_ratio |

## Case summary (advisory)

**1000000190: 5 of 9 documented 99215 claims (56%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000190 billed 99215 on 22.7% of 238 claims against an expected 5.4% given patient complexity (risk-adjusted score 4.52; plain z-score vs peers 2.74). 37% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 26 claims. Of 9 documented 99215 claims, 5 (56%) were documented below the billed level, against 33% for the comparison providers. Note checks on 26 returned notes (share showing each sign): problems 19%, late 0%, unsigned 0%, data 0%. No audit trail was received. 0 of 18 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0103121: billed 99215; documented MDM level moderate, 31 minutes. C0103216: billed 99215, patient aged 45 with 1 chronic condition(s) (asthma); documented MDM level moderate, 31 minutes. C0103310: billed 99215; documented MDM level moderate, 31 minutes. C0103111: billed 99215, patient aged 50 with 1 chronic condition(s) (hypothyroidism). C0103113: billed 99215, patient aged 69 with 1 chronic condition(s) (hypothyroidism). C0103135: billed 99215, patient aged 61 with 1 chronic condition(s) (atrial fibrillation).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000190.svg)

## Records-review sample so far

Documentation is on file for 26 claims (11% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 3.2% |
| 99214 | 11 | 0 | 0.0% | 2.8% |
| 99215 | 9 | 5 | 55.6% | 33.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (31 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0103121, C0103216, C0103310 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 19% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0103121, C0103216, C0103310.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
