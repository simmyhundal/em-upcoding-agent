# Payment Integrity dossier: 1000000363

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,103 / 533 |
| Billed mix (99211 to 99215) | 5 / 1 / 109 / 872 / 116 |
| 99215 share | 10.5% |
| Expected 99215 share given patient complexity | 2.2% |
| Screen scores | z vs peers 1.11; risk-adjusted 6.88; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000363's elevated 99215 billing appears across every complexity tier, including simple acute visits, which looks more like upcoding than a sicker panel, though chart evidence is too thin to confirm it.**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000363 billed 99215 on 10.5% of 1,103 claims against an expected 2.2% given patient complexity (risk-adjusted score 6.88; plain z-score vs peers 1.11). 51% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 30 claims. Of 1 documented 99215 claims, 0 (0%) were documented below the billed level, against 9% for the comparison providers. 1 of 14 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The excess 99215 share holds in every complexity tier, including patients with zero or one chronic condition, so a sicker panel does not explain it. The sampled low-complexity 99215 claims include routine presentations such as upper respiratory infection (C0212917, C0212922, C0213237) and low back pain (C0213409, C0213693), which rarely support high-complexity decision making. The overall mix is also unusually concentrated in 99214. The records review cannot settle the question: only one 99215 was documented (C0213394, supported at high complexity), and the single note with moderate-or-higher data reviewed but no lab or test line is weak evidence of inflated documentation. A reviewer should first request charts for the sampled low-complexity 99215 claims, especially the URI and back-pain visits, and check whether the notes are templated or cloned. If those charts support the billed level, the leaning should be revisited. Examples: C0212816: billed 99213; documented MDM level straightforward, minutes not recorded. C0213724: billed 99214; documented MDM level low, minutes not recorded. C0212756: billed 99215, patient aged 48 with 1 chronic condition(s) (osteoarthritis). C0212854: billed 99215, patient aged 51 with 1 chronic condition(s) (hyperlipidemia). C0212908: billed 99215, patient aged 25 with 0 chronic condition(s).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000363.svg)

## Records-review sample so far

Documentation is on file for 30 claims (3% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 10 | 1 | 10.0% | 4.3% |
| 99214 | 19 | 1 | 5.3% | 3.5% |
| 99215 | 1 | 0 | 0.0% | 9.1% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (43 claims across 99215).
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
