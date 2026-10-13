# Payment Integrity dossier: 1000000254

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 401 / 200 |
| Billed mix (99211 to 99215) | 0 / 0 / 55 / 301 / 45 |
| 99215 share | 11.2% |
| Expected 99215 share given patient complexity | 2.0% |
| Screen scores | z vs peers 1.19; risk-adjusted 5.16; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000254 bills 99215 well above its risk-adjusted expectation, mostly on patients with few or no chronic conditions, but no documented 99215 claims exist to confirm or refute support.**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000254 billed 99215 on 11.2% of 401 claims against an expected 2.0% given patient complexity (risk-adjusted score 5.16; plain z-score vs peers 1.19). 73% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 18 claims. No documented 99215 claims came back. 1 of 13 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The claims pattern points away from a sicker panel. The 99215 share runs several times the all-provider rate in the 0- and 1-condition strata, and most sampled 99215 claims carry single acute or nonspecific diagnoses such as low back pain (C0133878, C0133986), abdominal pain (C0133935, C0134161) and UTI (C0133898, C0134254), which would not usually call for high-complexity decision-making. The documentation cannot settle the question because none of the returned charts were 99215 claims. Among the 99214 charts, one claim (C0134093) was documented below its billed level and only one moderate-plus data-review note lacked a lab line, so the records neither strongly support nor contradict the billing. A reviewer should first request records for a targeted sample of 99215 claims on 0–1 condition patients, starting with the listed low-complexity examples, and check whether the documented MDM and time support level 5 or show signs of templated or cloned notes. Examples: C0134093: billed 99214; documented MDM level low, 20 minutes. C0133878: billed 99215, patient aged 60 with 0 chronic condition(s). C0133898: billed 99215, patient aged 66 with 0 chronic condition(s). C0133935: billed 99215, patient aged 55 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000254.svg)

## Records-review sample so far

Documentation is on file for 18 claims (4% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 0 | 0.0% | 1.6% |
| 99214 | 13 | 1 | 7.7% | 3.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (28 claims across 99215).
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
