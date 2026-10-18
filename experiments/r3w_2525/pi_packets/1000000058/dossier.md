# Payment Integrity dossier: 1000000058

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 243 / 122 |
| Billed mix (99211 to 99215) | 4 / 3 / 37 / 123 / 76 |
| 99215 share | 31.3% |
| Expected 99215 share given patient complexity | 3.8% |
| Screen scores | z vs peers 4.02; risk-adjusted 8.23; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000058: 1 of 11 documented 99215 claims (9%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000058 billed 99215 on 31.3% of 243 claims against an expected 3.8% given patient complexity (risk-adjusted score 8.23; plain z-score vs peers 4.02). 78% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 11 documented 99215 claims, 1 (9%) were documented below the billed level, against 46% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 57%, late 30%, unsigned 0%, data 20%. No audit trail was received. 6 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0025437: billed 99215; documented MDM level moderate, minutes not recorded. C0025403: billed 99215, patient aged 73 with 1 chronic condition(s) (type 2 diabetes). C0025410: billed 99215, patient aged 38 with 1 chronic condition(s) (type 2 diabetes); documented MDM level high, 48 minutes. C0025415: billed 99215, patient aged 31 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000058.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 2.8% |
| 99214 | 11 | 0 | 0.0% | 6.9% |
| 99215 | 11 | 1 | 9.1% | 45.8% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (37 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0025437, C0025403, C0025410 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 57% address fewer problems than their level implies and 30% were signed late; request the audit trail for C0025437, C0025403, C0025410.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
