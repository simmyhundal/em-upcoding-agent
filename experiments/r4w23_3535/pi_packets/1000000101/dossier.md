# Payment Integrity dossier: 1000000101

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 117 |
| Billed mix (99211 to 99215) | 5 / 6 / 67 / 115 / 49 |
| 99215 share | 20.2% |
| Expected 99215 share given patient complexity | 5.0% |
| Screen scores | z vs peers 1.97; risk-adjusted 4.11; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000101: 0 of 19 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000101 billed 99215 on 20.2% of 242 claims against an expected 5.0% given patient complexity (risk-adjusted score 4.11; plain z-score vs peers 1.97). 45% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 19 documented 99215 claims, 0 (0%) were documented below the billed level, against 24% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 38%, late 20%, unsigned 0%, data 22%, bulk created 9%, paste heavy 13%. 10 of 36 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0052364: billed 99214; documented MDM level low, 23 minutes. C0052350: billed 99215, patient aged 39 with 1 chronic condition(s) (obesity). C0052376: billed 99215, patient aged 54 with 0 chronic condition(s). C0052383: billed 99215, patient aged 40 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000101.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 8 | 0 | 0.0% | 2.7% |
| 99214 | 17 | 1 | 5.9% | 7.1% |
| 99215 | 19 | 0 | 0.0% | 23.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (29 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0052364, C0052350, C0052376 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 38% address fewer problems than their level implies and 20% were signed late; request the audit trail for C0052364, C0052350, C0052376.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
