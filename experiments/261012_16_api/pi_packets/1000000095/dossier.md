# Payment Integrity dossier: 1000000095

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 242 / 121 |
| Billed mix (99211 to 99215) | 4 / 0 / 47 / 138 / 53 |
| 99215 share | 21.9% |
| Expected 99215 share given patient complexity | 2.0% |
| Screen scores | z vs peers 2.60; risk-adjusted 7.20; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000095's 99215 use is concentrated on low-complexity patients far beyond peers, a pattern consistent with upcoding, but chart documentation is too thin to confirm it.**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000095 billed 99215 on 21.9% of 242 claims against an expected 2.0% given patient complexity (risk-adjusted score 7.20; plain z-score vs peers 2.60). 81% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 17 claims. Of 1 documented 99215 claims, 0 (0%) were documented below the billed level, against 5% for the comparison providers. 1 of 11 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The billing pattern points toward upcoding rather than a sicker panel. The excess 99215 billing sits mainly in patients with 0 or 1 chronic conditions, where this provider's 99215 share runs several times the all-provider share. Sampled low-complexity 99215 claims carry routine single diagnoses such as nonspecific abdominal pain, low back pain, rash or urinary tract infection (e.g., C0053304, C0053313, C0053349, C0053492), which do not obviously call for high-complexity decision-making. The main ambiguity is documentation: only one 99215 claim was charted (C0053505, supported at high MDM with 48 minutes), so the records neither confirm nor refute upcoding. The single unsupported 99213 and one data-reviewed note without a lab line are too few to weigh. A reviewer should first request charts for a targeted sample of the low-complexity 99215 claims listed in the packet, checking whether documented MDM and time support level 5 and whether notes look templated or cloned. Examples: C0053381: billed 99213; documented MDM level straightforward, minutes not recorded. C0053291: billed 99215, patient aged 51 with 1 chronic condition(s) (type 2 diabetes). C0053304: billed 99215, patient aged 46 with 0 chronic condition(s). C0053311: billed 99215, patient aged 62 with 1 chronic condition(s) (osteoarthritis).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000095.svg)

## Records-review sample so far

Documentation is on file for 17 claims (7% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 5 | 1 | 20.0% | 7.9% |
| 99214 | 11 | 0 | 0.0% | 4.0% |
| 99215 | 1 | 0 | 0.0% | 4.8% |

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
