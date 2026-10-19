# Payment Integrity dossier: 1000000010

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,410 / 1,203 |
| Billed mix (99211 to 99215) | 27 / 74 / 753 / 1,153 / 403 |
| 99215 share | 16.7% |
| Expected 99215 share given patient complexity | 4.1% |
| Screen scores | z vs peers 1.44; risk-adjusted 12.35; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000010: 0 of 6 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000010 billed 99215 on 16.7% of 2,410 claims against an expected 4.1% given patient complexity (risk-adjusted score 12.35; plain z-score vs peers 1.44). 65% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 6 documented 99215 claims, 0 (0%) were documented below the billed level, against 31% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 37%, late 20%, unsigned 0%, data 10%, bulk created 10%, paste heavy 10%. 5 of 18 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0006306: billed 99214; documented MDM level low, 25 minutes. C0006746: billed 99214; documented MDM level low, minutes not recorded. C0006278: billed 99215, patient aged 49 with 0 chronic condition(s). C0006354: billed 99215, patient aged 45 with 0 chronic condition(s). C0006471: billed 99215, patient aged 54 with 1 chronic condition(s) (depression).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000010.svg)

## Records-review sample so far

Documentation is on file for 30 claims (1% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 4.8% |
| 99214 | 15 | 2 | 13.3% | 4.6% |
| 99215 | 6 | 0 | 0.0% | 31.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (59 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0006306, C0006746, C0006278 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 37% address fewer problems than their level implies and 20% were signed late; request the audit trail for C0006306, C0006746, C0006278.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
