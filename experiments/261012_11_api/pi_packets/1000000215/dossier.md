# Payment Integrity dossier: 1000000215

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,055 / 529 |
| Billed mix (99211 to 99215) | 4 / 2 / 93 / 634 / 322 |
| 99215 share | 30.5% |
| Expected 99215 share given patient complexity | 5.1% |
| Screen scores | z vs peers 4.88; risk-adjusted 17.61; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000215's elevated 99215 rate persists across every complexity tier, including patients with no chronic conditions, which is consistent with upcoding, but the charts returned are too few to confirm it.**

Leaning: pattern consistent with upcoding. Citations checked: 4/4 valid.

1000000215 billed 99215 on 30.5% of 1,055 claims against an expected 5.1% given patient complexity (risk-adjusted score 17.61; plain z-score vs peers 4.88). 18% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 19 claims. Of 4 documented 99215 claims, 0 (0%) were documented below the billed level, against 0% for the comparison providers. 2 of 18 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The complexity table argues against a sicker-panel explanation: the 99215 share is several times the all-provider rate even for patients with 0 or 1 conditions. Sampled low-complexity 99215 claims carry minor acute or follow-up diagnoses such as upper respiratory infection or follow-up exam (C0095046, C0095258, C0094890, C0095175), and the heavy reliance on 99214 points the same way. The documentation does not confirm this, but it is too thin to judge either way: only 4 documented 99215 claims came back, all supported at high MDM (e.g., C0094596, C0094651), and one 99214 was documented low (C0095286). The 2 notes claiming moderate-or-higher data reviewed with no lab or test line on the claim are only weak evidence. Reviewers should first request charts for the sampled low-complexity 99215 claims, including whether patient M0039833's 99215 (C0094331) and 99214 (C0095430) visits differed clinically, and check notes for cloned or templated MDM language. Examples: C0095286: billed 99214; documented MDM level low, 24 minutes. C0094331: billed 99215, patient aged 76 with 1 chronic condition(s) (type 2 diabetes). C0094355: billed 99215, patient aged 38 with 0 chronic condition(s). C0094398: billed 99215, patient aged 52 with 1 chronic condition(s) (hyperlipidemia).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000215.svg)

## Records-review sample so far

Documentation is on file for 19 claims (2% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99214 | 15 | 1 | 6.7% | 3.4% |
| 99215 | 4 | 0 | 0.0% | 0.0% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (57 claims across 99215).
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
