# Payment Integrity dossier: 1000000530

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 2,405 / 1,183 |
| Billed mix (99211 to 99215) | 12 / 14 / 749 / 1,399 / 231 |
| 99215 share | 9.6% |
| Expected 99215 share given patient complexity | 2.4% |
| Screen scores | z vs peers 0.96; risk-adjusted 8.24; flagged by suspicion>=5 |

## Case summary (advisory)

**Provider 1000000530's 99215 rate stays elevated even among patients with no chronic conditions, a claims pattern consistent with upcoding, but documentation is too thin to confirm it.**

Leaning: pattern consistent with upcoding. Citations checked: 5/5 valid.

1000000530 billed 99215 on 9.6% of 2,405 claims against an expected 2.4% given patient complexity (risk-adjusted score 8.24; plain z-score vs peers 0.96). 40% of this provider's 99215 claims were on patients with 0 or 1 chronic conditions. Records came back for 15 claims. No documented 99215 claims came back. 1 of 11 notes claiming moderate-or-higher data reviewed had no lab or test line on the claim. The sicker-panel explanation is weakened because the elevated 99215 share holds in every complexity stratum, not just the complex ones, and the sampled low-complexity 99215s include routine presentations such as upper respiratory infection (C0259752, C0260660, C0260846) and rash (C0259580). These are hard to square with high-complexity decision-making. The sampled high-complexity 99215s look plausible, and the modest peer z-score suggests the peer group may also bill high, which keeps some ambiguity. Documentation cannot settle the question: no 99215 charts came back, and the 99214 mismatches (C0259975, C0260481, both documented as low MDM) come from too few records to read as a pattern. A reviewer should first pursue a targeted records request for the low-complexity 99215 claims listed, starting with the acute upper respiratory infection and rash visits, and compare documented MDM and time against the billed level. Examples: C0259975: billed 99214; documented MDM level low, 27 minutes. C0260481: billed 99214; documented MDM level low, 21 minutes. C0259371: billed 99215, patient aged 60 with 0 chronic condition(s). C0259469: billed 99215, patient aged 30 with 1 chronic condition(s) (type 2 diabetes). C0259544: billed 99215, patient aged 30 with 1 chronic condition(s) (type 2 diabetes).

## Evidence chart

![99215 share by patient complexity](../../charts/1000000530.svg)

## Records-review sample so far

Documentation is on file for 15 claims (1% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 3 | 0 | 0.0% | 5.0% |
| 99214 | 12 | 2 | 16.7% | 3.0% |

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
