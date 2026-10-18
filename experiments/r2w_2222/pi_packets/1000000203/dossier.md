# Payment Integrity dossier: 1000000203

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 563 / 269 |
| Billed mix (99211 to 99215) | 4 / 5 / 115 / 292 / 147 |
| 99215 share | 26.1% |
| Expected 99215 share given patient complexity | 4.5% |
| Screen scores | z vs peers 3.08; risk-adjusted 9.07; flagged by eb_ratio |

## Case summary (advisory)

**1000000203: 5 of 9 documented 99215 claims (56%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000203 billed 99215 on 26.1% of 563 claims against an expected 4.5% given patient complexity (risk-adjusted score 9.07; plain z-score vs peers 3.08). 61% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 9 documented 99215 claims, 5 (56%) were documented below the billed level, against 20% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 37%, late 7%, unsigned 0%, data 3%, bulk created 0%, paste heavy 0%. 1 of 20 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0097523: billed 99215; documented MDM level moderate, minutes not recorded. C0097617: billed 99215; documented MDM level moderate, minutes not recorded. C0097665: billed 99215, patient aged 35 with 0 chronic condition(s); documented MDM level moderate, 36 minutes. C0097378: billed 99215, patient aged 43 with 1 chronic condition(s) (hypertension). C0097380: billed 99215, patient aged 18 with 0 chronic condition(s). C0097382: billed 99215, patient aged 23 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000203.svg)

## Records-review sample so far

Documentation is on file for 30 claims (5% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 3 | 42.9% | 3.9% |
| 99214 | 14 | 0 | 0.0% | 5.9% |
| 99215 | 9 | 5 | 55.6% | 19.5% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (47 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0097523, C0097617, C0097665 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 37% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0097523, C0097617, C0097665.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
