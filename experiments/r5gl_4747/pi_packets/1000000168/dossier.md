# Payment Integrity dossier: 1000000168

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,116 / 542 |
| Billed mix (99211 to 99215) | 27 / 38 / 448 / 474 / 129 |
| 99215 share | 11.6% |
| Expected 99215 share given patient complexity | 4.1% |
| Screen scores | z vs peers 0.63; risk-adjusted 4.37; flagged by eb_ratio_t |

## Case summary (advisory)

**1000000168: 11 of 18 documented 99215 claims (61%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000168 billed 99215 on 11.6% of 1,116 claims against an expected 4.1% given patient complexity (risk-adjusted score 4.37; plain z-score vs peers 0.63). 65% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 18 documented 99215 claims, 11 (61%) were documented below the billed level, against 32% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 24%, late 4%, unsigned 0%, data 0%. No audit trail was received. 2 of 24 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0080727: billed 99215; documented MDM level moderate, 32 minutes. C0081124: billed 99215; documented MDM level moderate, minutes not recorded. C0081537: billed 99215; documented MDM level moderate, 20 minutes. C0080772: billed 99215, patient aged 55 with 0 chronic condition(s). C0080774: billed 99215, patient aged 18 with 1 chronic condition(s) (chronic kidney disease). C0080880: billed 99215, patient aged 35 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000168.svg)

## Records-review sample so far

Documentation is on file for 45 claims (4% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 18 | 0 | 0.0% | 2.8% |
| 99214 | 9 | 4 | 44.4% | 6.3% |
| 99215 | 18 | 11 | 61.1% | 32.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (45 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0080727, C0081124, C0081537 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 24% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0080727, C0081124, C0081537.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
