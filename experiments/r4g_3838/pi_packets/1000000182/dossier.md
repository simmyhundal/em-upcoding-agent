# Payment Integrity dossier: 1000000182

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 873 / 414 |
| Billed mix (99211 to 99215) | 12 / 19 / 207 / 398 / 237 |
| 99215 share | 27.1% |
| Expected 99215 share given patient complexity | 4.2% |
| Screen scores | z vs peers 3.87; risk-adjusted 14.20; flagged by eb_ratio_t |

## Case summary (advisory)

**Provider 1000000182 bills 99215 well above expectation in every complexity band, mostly on patients with few or no chronic conditions, and the limited records reviewed point to over-coding, especially at 99214.**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000182 billed 99215 on 27.1% of 873 claims against an expected 4.2% given patient complexity (risk-adjusted score 14.20; plain z-score vs peers 3.87). 66% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 8 documented 99215 claims, 5 (62%) were documented below the billed level, against 42% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 50%, late 0%, unsigned 0%, data 10%, bulk created 0%, paste heavy 3%. 4 of 13 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The excess 99215 billing shows up even on patients with no chronic conditions, and the sampled low-complexity 99215s are mostly routine diagnoses such as upper respiratory infection (J06.9), low back pain (M54.50) and follow-up (Z09). That pattern is consistent with upcoding rather than a sicker panel. The documentation points the same way but is thin: only 30 charts came back, and only 8 were 99215s. The 99215 unsupported rate is only modestly above a comparison rate that is already high, so the stronger signal is the 99214 mismatch (7 of 16, far above the all-provider rate). Some 99215s on genuinely complex patients are supported, for example C0089782, so not all high-level billing looks unjustified. Cloning signals are a concern: a third of notes are flagged as duplicates, some repeat visit times, and 4 notes claim moderate-or-higher data reviewed with no lab or test line on the claim. That is weak evidence that even 'supported' notes may be inflated. A reviewer should first request a larger chart sample focused on 0–1 condition 99215 claims (for example C0089578, already documented at moderate MDM, and C0089057), and compare the duplicate-flagged notes side by side for templated content. Examples: C0088974: billed 99215; documented MDM level moderate, 22 minutes. C0089218: billed 99215; documented MDM level moderate, 31 minutes. C0089543: billed 99215; documented MDM level moderate, minutes not recorded. C0088965: billed 99215, patient aged 20 with 0 chronic condition(s). C0088986: billed 99215, patient aged 70 with 1 chronic condition(s) (depression). C0089057: billed 99215, patient aged 38 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000182.svg)

## Records-review sample so far

Documentation is on file for 30 claims (3% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 6 | 0 | 0.0% | 3.1% |
| 99214 | 16 | 7 | 43.8% | 5.1% |
| 99215 | 8 | 5 | 62.5% | 42.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (53 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Request the full charts for C0088974, C0089218, C0089543 and have a certified coder re-score each against the current E/M rules (medical decision making or total time).
- If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample.
- Look at the notes themselves: 50% address fewer problems than their level implies and 0% were signed late; request the audit trail for C0088974, C0089218, C0089543.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
