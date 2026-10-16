# Payment Integrity dossier: 1000000145

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 239 / 117 |
| Billed mix (99211 to 99215) | 0 / 1 / 38 / 137 / 63 |
| 99215 share | 26.4% |
| Expected 99215 share given patient complexity | 2.1% |
| Screen scores | z vs peers 3.51; risk-adjusted 10.16; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000145: 0 of 17 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000145 billed 99215 on 26.4% of 239 claims against an expected 2.1% given patient complexity (risk-adjusted score 10.16; plain z-score vs peers 3.51). 79% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 21 claims. Of 17 documented 99215 claims, 0 (0%) were documented below the billed level, against 0% for the comparison providers. Note checks on 21 returned notes (share showing each sign): problems 57%, late 29%, unsigned 0%, data 14%, bulk created 29%, paste heavy 29%. 3 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0077611: billed 99214; documented MDM level low, minutes not recorded. C0077450: billed 99215, patient aged 29 with 1 chronic condition(s) (type 2 diabetes). C0077455: billed 99215, patient aged 46 with 1 chronic condition(s) (hypothyroidism). C0077462: billed 99215, patient aged 38 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000145.svg)

## Records-review sample so far

Documentation is on file for 21 claims (9% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99214 | 4 | 1 | 25.0% | 3.1% |
| 99215 | 17 | 0 | 0.0% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (33 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0077611, C0077450, C0077455 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 57% address fewer problems than their level implies and 29% were signed late; request the audit trail for C0077611, C0077450, C0077455.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
