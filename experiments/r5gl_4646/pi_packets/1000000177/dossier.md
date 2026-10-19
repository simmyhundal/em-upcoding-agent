# Payment Integrity dossier: 1000000177

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 113 |
| Billed mix (99211 to 99215) | 6 / 4 / 102 / 105 / 25 |
| 99215 share | 10.3% |
| Expected 99215 share given patient complexity | 3.4% |
| Screen scores | z vs peers 0.76; risk-adjusted 2.20; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000177: 2 of 12 documented 99214 and 99215 claims (17%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000177 billed 99215 on 10.3% of 242 claims against an expected 3.4% given patient complexity (risk-adjusted score 2.20; plain z-score vs peers 0.76). 72% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 27 claims. Of 3 documented 99215 claims, 0 (0%) were documented below the billed level, against 50% for the comparison providers. Note checks on 27 returned notes (share showing each sign): problems 52%, late 7%, unsigned 0%, data 26%, bulk created 4%, paste heavy 11%. 7 of 13 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0100726: billed 99214; documented MDM level low, minutes not recorded. C0100886: billed 99214; documented MDM level low, 29 minutes. C0100674: billed 99215, patient aged 18 with 1 chronic condition(s) (hyperlipidemia). C0100676: billed 99215, patient aged 47 with 1 chronic condition(s) (hypertension). C0100688: billed 99215, patient aged 18 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000177.svg)

## Records-review sample so far

Documentation is on file for 27 claims (11% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 15 | 0 | 0.0% | 3.7% |
| 99214 | 9 | 2 | 22.2% | 5.9% |
| 99215 | 3 | 0 | 0.0% | 50.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (25 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0100726, C0100886, C0100674 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 52% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0100726, C0100886, C0100674.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
