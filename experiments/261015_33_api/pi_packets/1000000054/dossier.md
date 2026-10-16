# Payment Integrity dossier: 1000000054

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 243 / 117 |
| Billed mix (99211 to 99215) | 1 / 2 / 51 / 132 / 57 |
| 99215 share | 23.5% |
| Expected 99215 share given patient complexity | 4.4% |
| Screen scores | z vs peers 3.06; risk-adjusted 5.03; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000054: 0 of 9 documented 99215 claims (0%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000054 billed 99215 on 23.5% of 243 claims against an expected 4.4% given patient complexity (risk-adjusted score 5.03; plain z-score vs peers 3.06). 40% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 9 documented 99215 claims, 0 (0%) were documented below the billed level, against 14% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 37%, late 7%, unsigned 0%, data 13%, bulk created 7%, paste heavy 17%. 6 of 29 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0029214: billed 99215, patient aged 45 with 1 chronic condition(s) (COPD). C0029225: billed 99215, patient aged 18 with 1 chronic condition(s) (obesity). C0029234: billed 99215, patient aged 64 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000054.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99214 | 21 | 0 | 0.0% | 2.5% |
| 99215 | 9 | 0 | 0.0% | 14.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (32 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0029214, C0029225, C0029234 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 37% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0029214, C0029225, C0029234.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
