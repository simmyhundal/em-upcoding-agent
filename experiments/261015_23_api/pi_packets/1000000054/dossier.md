# Payment Integrity dossier: 1000000054

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 239 / 116 |
| Billed mix (99211 to 99215) | 0 / 2 / 59 / 132 / 46 |
| 99215 share | 19.2% |
| Expected 99215 share given patient complexity | 2.1% |
| Screen scores | z vs peers 2.50; risk-adjusted 5.81; flagged by suspicion>=5 |

## Case summary (advisory)

**1000000054: 10 of 20 documented 99215 claims (50%) are documented below the billed level**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000054 billed 99215 on 19.2% of 239 claims against an expected 2.1% given patient complexity (risk-adjusted score 5.81; plain z-score vs peers 2.50). 76% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 45 claims. Of 20 documented 99215 claims, 10 (50%) were documented below the billed level, against 4% for the comparison providers. Note checks on 45 returned notes (share showing each sign): problems 40%, late 4%, unsigned 0%, data 2%, bulk created 0%, paste heavy 2%. 3 of 33 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. This pattern is consistent with upcoding. It is a reason to review the records, not a finding. Examples: C0028361: billed 99215, patient aged 37 with 0 chronic condition(s); documented MDM level moderate, 32 minutes. C0028397: billed 99215, patient aged 45 with 1 chronic condition(s) (obesity); documented MDM level moderate, minutes not recorded. C0028403: billed 99215, patient aged 64 with 1 chronic condition(s) (depression); documented MDM level moderate, minutes not recorded. C0028365: billed 99215, patient aged 52 with 0 chronic condition(s); documented MDM level high, minutes not recorded. C0028382: billed 99215, patient aged 45 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000054.svg)

## Records-review sample so far

Documentation is on file for 45 claims (19% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 3.7% |
| 99214 | 18 | 0 | 0.0% | 2.1% |
| 99215 | 20 | 10 | 50.0% | 4.5% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (28 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0028361, C0028397, C0028403 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 40% address fewer problems than their level implies and 4% were signed late; request the audit trail for C0028361, C0028397, C0028403.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
