# Payment Integrity dossier: 1000000115

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 945 / 451 |
| Billed mix (99211 to 99215) | 4 / 4 / 161 / 537 / 239 |
| 99215 share | 25.3% |
| Expected 99215 share given patient complexity | 2.3% |
| Screen scores | z vs peers 3.59; risk-adjusted 15.48; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000115 bills 99215 at a nearly flat rate across patient complexity, including healthy patients, but the documentation sample is too thin to confirm or refute upcoding.**

Leaning: pattern consistent with upcoding. Citations checked: 3/3 valid.

1000000115 billed 99215 on 25.3% of 945 claims against an expected 2.3% given patient complexity (risk-adjusted score 15.48; plain z-score vs peers 3.59). 72% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 5 documented 99215 claims, 0 (0%) were documented below the billed level, against 4% for the comparison providers. 3 of 22 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The claims pattern does not look like a sicker panel. The 99215 share stays at about a quarter for patients with 0, 1 or 2 chronic conditions, far above peers at each tier, and most 99215s fall on low-complexity patients. Sampled examples include single routine diagnoses such as J06.9 (C0058177, C0058391), N39.0 (C0057485) and I10 (C0057522), which would rarely support high-complexity decision-making. The documentation does not confirm this: the few documented 99215s were all supported, and some were high-complexity patients (for example C0058134). With records for only about 3% of claims and just 5 documented 99215s, the charts are too thin to judge either way, and the 3 moderate-plus data-reviewed notes without a lab or test line are only weak hints of templated notes. A reviewer should first request charts for the low-complexity 99215 claims listed (for example C0057485, C0058019, C0058420) and check whether the MDM and time in those notes reflect the visit or appear cloned. Examples: C0057485: billed 99215, patient aged 41 with 0 chronic condition(s). C0057501: billed 99215, patient aged 49 with 0 chronic condition(s). C0057522: billed 99215, patient aged 57 with 1 chronic condition(s) (hypertension).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000115.svg)

## Records-review sample so far

Documentation is on file for 30 claims (3% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 7 | 0 | 0.0% | 3.7% |
| 99214 | 18 | 0 | 0.0% | 2.1% |
| 99215 | 5 | 0 | 0.0% | 4.5% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (53 claims across 99215).
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
