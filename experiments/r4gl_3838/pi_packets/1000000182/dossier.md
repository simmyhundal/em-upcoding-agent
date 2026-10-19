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

**Provider 1000000182's elevated 99215 billing falls mostly on low-complexity patients, and the limited records show billed levels above documentation, especially at 99214, a pattern consistent with upcoding.**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000182 billed 99215 on 27.1% of 873 claims against an expected 4.2% given patient complexity (risk-adjusted score 14.20; plain z-score vs peers 3.87). 66% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 8 documented 99215 claims, 5 (62%) were documented below the billed level, against 42% for the comparison providers. Note checks on 30 returned notes (share showing each sign): problems 50%, late 0%, unsigned 0%, data 10%, bulk created 0%, paste heavy 3%. 4 of 13 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The excess 99215 share appears in every complexity stratum, including patients with zero conditions, and most 99215 claims fall on 0–1 condition patients. The sample includes simple visits billed at 99215, such as C0088965 for low back pain only, C0089057 for a URI only and C0089310 for a follow-up (Z09). One of these, C0089578 (a URI-only visit), came back documented at moderate MDM. Sicker patients like M0037523 do account for some 99215s, and C0089782 was documented at high MDM, so not all high-level billing is unsupported. The documented 99215 mismatch rate exceeds the comparison rate, but it rests on only 8 charts and the all-provider rate is itself high, so on its own it is suggestive rather than strong. The stronger signal is the 99214 mismatch rate, which is far above peers on a somewhat larger base. Note signals add weak concern, chiefly the one-third duplicate-note rate, the repeated-time rate and data-review claims without lab lines on the claim. Documentation covers only a small share of claims, so a reviewer should first request charts for the low-complexity 99215 and 99214 claims and check the duplicated notes for cloning. Examples: C0088974: billed 99215; documented MDM level moderate, 22 minutes. C0089218: billed 99215; documented MDM level moderate, 31 minutes. C0089543: billed 99215; documented MDM level moderate, minutes not recorded. C0088965: billed 99215, patient aged 20 with 0 chronic condition(s). C0088986: billed 99215, patient aged 70 with 1 chronic condition(s) (depression). C0089057: billed 99215, patient aged 38 with 0 chronic condition(s).

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
