# Payment Integrity dossier: 1000000134

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 291 / 144 |
| Billed mix (99211 to 99215) | 2 / 8 / 89 / 138 / 54 |
| 99215 share | 18.6% |
| Expected 99215 share given patient complexity | 4.2% |
| Screen scores | z vs peers 2.64; risk-adjusted 4.84; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000134: 14 of 19 documented 99215 claims (74%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000134 billed 99215 on 18.6% of 291 claims against an expected 4.2% given patient complexity (risk-adjusted score 4.84; plain z-score vs peers 2.64). 65% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 14 (74%) were documented below the billed level, against 47% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 29%, late 4%, unsigned 0%, data 2%. No audit trail was received. 2 of 24 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0059018: billed 99215, patient aged 37 with 1 chronic condition(s) (obesity); documented MDM level moderate, 28 minutes. C0059040: billed 99215; documented MDM level moderate, 36 minutes. C0059076: billed 99215; documented MDM level moderate, minutes not recorded. C0059002: billed 99215, patient aged 46 with 0 chronic condition(s). C0059016: billed 99215, patient aged 25 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000134.svg)

## Records-review sample so far

Documentation is on file for 45 claims (16% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 0 | 0.0% | 3.6% |
| 99214 | 15 | 8 | 53.3% | 6.1% |
| 99215 | 19 | 14 | 73.7% | 46.9% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (31 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0059018, C0059040, C0059076 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 29% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0059018, C0059040, C0059076.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
