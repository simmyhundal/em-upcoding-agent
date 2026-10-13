# Payment Integrity dossier: 1000000195

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 243 / 118 |
| Billed mix (99211 to 99215) | 0 / 1 / 50 / 141 / 51 |
| 99215 share | 21.0% |
| Expected 99215 share given patient complexity | 4.1% |
| Screen scores | z vs peers 3.03; risk-adjusted 5.55; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000195: 1 of 5 documented 99215 claims (20%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000195 billed 99215 on 21.0% of 243 claims against an expected 4.1% given patient complexity (risk-adjusted score 5.55; plain z-score vs peers 3.03). 43% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 18 claims. Of 5 documented 99215 claims, 1 (20%) were documented below the billed level, against 0% for the comparison providers. 0 of 12 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0085405: billed 99215, patient aged 78 with 5 chronic condition(s) (obesity;hyperlipidemia;depression;hypertension;atrial fibrillation); documented MDM level moderate, 36 minutes. C0085259: billed 99215, patient aged 57 with 1 chronic condition(s) (hyperlipidemia). C0085267: billed 99215, patient aged 52 with 1 chronic condition(s) (obesity). C0085268: billed 99215, patient aged 36 with 1 chronic condition(s) (depression).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000195.svg)

## Records-review sample so far

Documentation is on file for 18 claims (7% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 2 | 0 | 0.0% | 0.7% |
| 99214 | 11 | 3 | 27.3% | 3.7% |
| 99215 | 5 | 1 | 20.0% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (30 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full records for the cited claims and have a certified coder re-score each against current E/M documentation rules (medical decision making or total time).
- If the re-scoring confirms the pattern, use the sampling plan in the recovery packet to review a statistical sample of this provider's 99215 claims.
- Check whether notes for the cited claims look copied forward, and whether documented minutes repeat from visit to visit.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
