# Payment Integrity dossier: 1000000041

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 302 / 145 |
| Billed mix (99211 to 99215) | 5 / 3 / 71 / 142 / 81 |
| 99215 share | 26.8% |
| Expected 99215 share given patient complexity | 2.0% |
| Screen scores | z vs peers 3.38; risk-adjusted 10.15; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000041 bills 99215 far above expectation, and the excess falls mostly on patients with few or no chronic conditions, which fits upcoding better than a sicker panel, though the chart review is not decisive.**

Leaning: pattern consistent with upcoding. Citations checked: 6/6 valid.

1000000041 billed 99215 on 26.8% of 302 claims against an expected 2.0% given patient complexity (risk-adjusted score 10.15; plain z-score vs peers 3.38). 65% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 61 claims. Of 17 documented 99215 claims, 3 (18%) were documented below the billed level, against 12% for the comparison providers. 15 of 41 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The elevated 99215 share appears in every complexity stratum, including 0-condition visits for presentations like UTI (N39.0), abdominal pain (R10.9) and follow-up (Z09), as in C0017213, C0017235 and C0017190; a legitimately complex panel would not look like this. The documentation does not settle it: the unsupported rate on documented 99215s is only modestly above the comparison providers, and on just 17 charts, while most reviewed 99215s were documented as high MDM. Those supporting notes may themselves be inflated, though. The rule check found many notes claiming moderate-or-higher data review with no lab or test line on the claim. One example is C0017371, a 0-condition UTI visit documented as high MDM, which deserves scrutiny as possibly templated or cloned. A reviewer should first pull the full notes for the documented 99215s on 0–1 condition patients (C0017371, C0017168, C0017256), compare them against each other for cloned language, and check whether the claimed data review is backed by orders or results. The next step would be a targeted records request for more of the undocumented low-complexity 99215 claims. Examples: C0017168: billed 99215, patient aged 49 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0017256: billed 99215, patient aged 48 with 0 chronic condition(s); documented MDM level moderate, minutes not recorded. C0017337: billed 99215; documented MDM level moderate, minutes not recorded. C0017076: billed 99215, patient aged 41 with 1 chronic condition(s) (COPD). C0017107: billed 99215, patient aged 41 with 0 chronic condition(s). C0017110: billed 99215, patient aged 58 with 1 chronic condition(s) (osteoarthritis).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000041.svg)

## Records-review sample so far

Documentation is on file for 61 claims (20% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 9 | 0 | 0.0% | 4.4% |
| 99214 | 31 | 1 | 3.2% | 3.4% |
| 99215 | 17 | 3 | 17.6% | 12.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (38 claims across 99215).
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
