# Payment Integrity dossier: 1000000212

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 680 / 328 |
| Billed mix (99211 to 99215) | 2 / 11 / 142 / 422 / 103 |
| 99215 share | 15.1% |
| Expected 99215 share given patient complexity | 3.8% |
| Screen scores | z vs peers 1.21; risk-adjusted 5.25; flagged by eb_ratio |

## Case summary (advisory)

**1000000212: 9 of 20 documented 99215 claims (45%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000212 billed 99215 on 15.1% of 680 claims against an expected 3.8% given patient complexity (risk-adjusted score 5.25; plain z-score vs peers 1.21). 75% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 9 (45%) were documented below the billed level, against 29% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 47%, late 4%, unsigned 0%, data 9%, bulk created 0%, paste heavy 0%. 5 of 34 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0111746: billed 99215; documented MDM level moderate, 35 minutes. C0111910: billed 99215; documented MDM level moderate, 34 minutes. C0111939: billed 99215, patient aged 54 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0111455: billed 99215, patient aged 51 with 1 chronic condition(s) (hypothyroidism). C0111505: billed 99215, patient aged 55 with 1 chronic condition(s) (hypertension). C0111561: billed 99215, patient aged 27 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000212.svg)

## Records-review sample so far

Documentation is on file for 45 claims (7% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 2.2% |
| 99214 | 20 | 1 | 5.0% | 3.8% |
| 99215 | 20 | 9 | 45.0% | 28.6% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (42 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0111746, C0111910, C0111939 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 47% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0111746, C0111910, C0111939.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
