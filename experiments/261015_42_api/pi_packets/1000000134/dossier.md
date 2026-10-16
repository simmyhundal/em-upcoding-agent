# Payment Integrity dossier: 1000000134

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,203 / 580 |
| Billed mix (99211 to 99215) | 14 / 18 / 462 / 587 / 122 |
| 99215 share | 10.1% |
| Expected 99215 share given patient complexity | 1.8% |
| Screen scores | z vs peers 0.87; risk-adjusted 6.80; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000134's 99215 use is elevated in every complexity band and concentrated on patients with few or no chronic conditions, a billing pattern consistent with upcoding, though too few charts came back to confirm it.**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000134 billed 99215 on 10.1% of 1,203 claims against an expected 1.8% given patient complexity (risk-adjusted score 6.80; plain z-score vs peers 0.87). 59% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 27 claims. Of 2 documented 99215 claims, 0 (0%) were documented below the billed level, against 0% for the comparison providers. 2 of 14 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The excess 99215 billing is not explained by a sicker panel. The share runs well above the all-provider rate in every condition band, especially at 0–1 conditions. The sampled low-complexity 99215 claims are mostly simple acute or follow-up diagnoses such as rash, upper respiratory infection, low back pain and Z09 (e.g., C0082612, C0083027, C0082963), so the concern does not rest on a few complex outliers. Documentation is too thin to confirm or refute this. Only 2 documented 99215 claims came back, both supported, and one of them (C0083074) records high MDM for a 68-year-old with no chronic conditions and a URI diagnosis, which a reviewer should read closely for cloned or inflated content. The one below-billed 99213 and the 2 data-reviewed notes without a lab line are small, weak signals. A reviewer should first request charts for the sampled low-complexity 99215 claims to see whether the notes support high-complexity MDM or qualifying time. Examples: C0083217: billed 99213; documented MDM level straightforward, minutes not recorded. C0082480: billed 99215, patient aged 57 with 1 chronic condition(s) (chronic kidney disease). C0082546: billed 99215, patient aged 53 with 0 chronic condition(s). C0082553: billed 99215, patient aged 58 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000134.svg)

## Records-review sample so far

Documentation is on file for 27 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 1 | 10.0% | 1.6% |
| 99214 | 14 | 0 | 0.0% | 3.3% |
| 99215 | 2 | 0 | 0.0% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (44 claims across 99215).
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
