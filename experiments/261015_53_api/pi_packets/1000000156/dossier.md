# Payment Integrity dossier: 1000000156

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 373 / 174 |
| Billed mix (99211 to 99215) | 2 / 0 / 40 / 219 / 112 |
| 99215 share | 30.0% |
| Expected 99215 share given patient complexity | 9.9% |
| Screen scores | z vs peers 4.25; risk-adjusted 5.92; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000156 bills 99215 well above expectation across every complexity stratum, and most of the small sample of documented 99215 claims do not support the billed level.**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000156 billed 99215 on 30.0% of 373 claims against an expected 9.9% given patient complexity (risk-adjusted score 5.92; plain z-score vs peers 4.25). 4% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 20 claims. Of 10 documented 99215 claims, 6 (60%) were documented below the billed level, against 17% for the comparison providers. Note checks on 20 returned notes (share showing each sign): problems 0%, late 5%, unsigned 0%, data 10%. No audit trail was received. 4 of 13 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The panel is genuinely complex, with most 99215s on multi-condition patients (e.g., C0079330, C0079348), but the 99215 share runs roughly two to four times the all-provider rate in every complexity band, so patient acuity alone does not explain the excess. The stronger signal is documentation: 6 of the 10 documented 99215 claims were documented below the billed level (e.g., C0079308 and C0079613 at low MDM), far above the comparison rate, while only four (e.g., C0079337, C0079649) showed high MDM. Records exist for only 20 claims, so the sample is small. The finding rests on 10 documented 99215s and should be treated as directional, not conclusive. The data-reviewed claims on notes with no lab or test line (e.g., C0079556, C0079613) are weak evidence of templated or inflated notes, and no audit trail was received to check how the notes were created. A reviewer should first request a larger, targeted sample of 99215 charts, prioritizing the low-complexity 99215s such as C0079334, C0079655 and C0079573, and obtain EHR audit logs to test for cloned documentation. Examples: C0079308: billed 99215; documented MDM level low, minutes not recorded. C0079556: billed 99215; documented MDM level moderate, minutes not recorded. C0079574: billed 99215; documented MDM level moderate, 36 minutes. C0079334: billed 99215, patient aged 51 with 1 chronic condition(s) (hypertension). C0079344: billed 99215, patient aged 75 with 1 chronic condition(s) (hypothyroidism). C0079573: billed 99215, patient aged 25 with 1 chronic condition(s) (obesity).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000156.svg)

## Records-review sample so far

Documentation is on file for 20 claims (5% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 1 | 0 | 0.0% | 6.2% |
| 99214 | 8 | 1 | 12.5% | 2.6% |
| 99215 | 10 | 6 | 60.0% | 17.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (43 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0079308, C0079556, C0079574 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 0% address fewer problems than their level implies and 5% were signed late; request the audit trail for C0079308, C0079556, C0079574.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
