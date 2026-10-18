# Payment Integrity dossier: 1000000120

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 307 / 146 |
| Billed mix (99211 to 99215) | 2 / 4 / 82 / 183 / 36 |
| 99215 share | 11.7% |
| Expected 99215 share given patient complexity | 3.5% |
| Screen scores | z vs peers 1.03; risk-adjusted 3.06; flagged by eb_ratio |

## Case summary (advisory)

**1000000120: 14 of 18 documented 99215 claims (78%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000120 billed 99215 on 11.7% of 307 claims against an expected 3.5% given patient complexity (risk-adjusted score 3.06; plain z-score vs peers 1.03). 69% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 18 documented 99215 claims, 14 (78%) were documented below the billed level, against 43% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 36%, late 7%, unsigned 0%, data 4%. No audit trail was received. 4 of 31 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0060104: billed 99215, patient aged 64 with 1 chronic condition(s) (type 2 diabetes); documented MDM level moderate, minutes not recorded. C0060153: billed 99215, patient aged 60 with 0 chronic condition(s); documented MDM level moderate, 39 minutes. C0060262: billed 99215, patient aged 35 with 1 chronic condition(s) (hyperlipidemia); documented MDM level moderate, 28 minutes. C0060108: billed 99215, patient aged 50 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000120.svg)

## Records-review sample so far

Documentation is on file for 45 claims (15% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 12 | 0 | 0.0% | 2.4% |
| 99214 | 14 | 0 | 0.0% | 4.8% |
| 99215 | 18 | 14 | 77.8% | 43.3% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (24 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0060104, C0060153, C0060262 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 36% address fewer problems than their level implies and 7% were signed late; request the audit trail for C0060104, C0060153, C0060262.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
