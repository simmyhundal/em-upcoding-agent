# Payment Integrity dossier: 1000000098

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 241 / 122 |
| Billed mix (99211 to 99215) | 2 / 3 / 55 / 105 / 76 |
| 99215 share | 31.5% |
| Expected 99215 share given patient complexity | 3.6% |
| Screen scores | z vs peers 3.78; risk-adjusted 8.31; flagged by eb_ratio |

## Case summary (advisory)

**1000000098: 8 of 10 documented 99215 claims (80%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000098 billed 99215 on 31.5% of 241 claims against an expected 3.6% given patient complexity (risk-adjusted score 8.31; plain z-score vs peers 3.78). 78% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 10 documented 99215 claims, 8 (80%) were documented below the billed level, against 15% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 37%, late 3%, unsigned 0%, data 3%, bulk created 0%, paste heavy 0%. 1 of 19 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0048309: billed 99215; documented MDM level moderate, 34 minutes. C0048316: billed 99215, patient aged 61 with 1 chronic condition(s) (hypertension); documented MDM level moderate, 37 minutes. C0048378: billed 99215; documented MDM level moderate, 38 minutes. C0048273: billed 99215, patient aged 46 with 0 chronic condition(s). C0048284: billed 99215, patient aged 20 with 0 chronic condition(s). C0048291: billed 99215, patient aged 39 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000098.svg)

## Records-review sample so far

Documentation is on file for 30 claims (12% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 4 | 0 | 0.0% | 3.9% |
| 99214 | 16 | 5 | 31.2% | 4.5% |
| 99215 | 10 | 8 | 80.0% | 15.4% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (37 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0048309, C0048316, C0048378 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 37% address fewer problems than their level implies and 3% were signed late; request the audit trail for C0048309, C0048316, C0048378.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
