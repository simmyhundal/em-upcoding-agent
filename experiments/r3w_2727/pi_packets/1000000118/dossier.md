# Payment Integrity dossier: 1000000118

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 122 |
| Billed mix (99211 to 99215) | 4 / 3 / 61 / 120 / 53 |
| 99215 share | 22.0% |
| Expected 99215 share given patient complexity | 6.2% |
| Screen scores | z vs peers 2.96; risk-adjusted 4.06; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000118: 0 of 9 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000118 billed 99215 on 22.0% of 241 claims against an expected 6.2% given patient complexity (risk-adjusted score 4.06; plain z-score vs peers 2.96). 36% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 29 claims. Of 9 documented 99215 claims, 0 (0%) were documented below the billed level, against 47% for the comparison providers. Note checks on 29 returned notes (share showing each sign): problems 28%, late 14%, unsigned 0%, data 7%, bulk created 7%, paste heavy 7%. 3 of 20 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0054987: billed 99214; documented MDM level low, minutes not recorded. C0054971: billed 99215, patient aged 51 with 0 chronic condition(s); documented MDM level high, 45 minutes. C0054979: billed 99215, patient aged 62 with 1 chronic condition(s) (obesity). C0054984: billed 99215, patient aged 31 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000118.svg)

## Records-review sample so far

Documentation is on file for 29 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 2.1% |
| 99214 | 13 | 1 | 7.7% | 3.4% |
| 99215 | 9 | 0 | 0.0% | 46.7% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (30 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0054987, C0054971, C0054979 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 28% address fewer problems than their level implies and 14% were signed late; request the audit trail for C0054987, C0054971, C0054979.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
