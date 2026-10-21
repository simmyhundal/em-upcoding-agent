# Score 4.0: every parameter, with its source or "assumption"

[Back to the README](../README.md) · [the v4/v5 plan](v4_v5_plan.md) · code: `eval/score_40.py` · tests: `tests/test_score_40.py`

Score 4.0 (issue #125) is the score of the v4/v5 line: **dollars recovered - staff-hours cost - provider abrasion**, per seed. The release 5 score (`eval/dollar_reward.py`) stays frozen; this module only imports its helpers. Sources below were checked on 2026-10-20; anything not checked is marked **assumption** and has a sensitivity range.

## Formula
```
score = Recovered - StaffCost - Abrasion

Recovered = sum over providers sent a demand of the 90% lower bound of the overpayment extrapolated from the provider's random sample
            (level-difference basis, underpayments netted, not capped at the true overpayment)
StaffCost = triage + request admin + chart review + demand work (hours x loaded wage) + $90 per request round + the arm's API dollars
Abrasion  = sum over providers of w(r) x (request rounds x $43.84 + $2,000 if a demand was sent),  r = the provider's TRUE net upcoding rate
w(r)      = 1 for r <= 0, falling linearly to 0 at r >= 15%
```
A **demand** is a provider the arm called upcoding in its checked summaries, whatever its `role`. **Listed** providers are those with a checked summary (every provider on the workflow's list; for the agent, those it submitted a finding for). **True net rate** and **true overpayment** are computed from the answer key's `justified_cpt_by_claim` against the billed claims, with the same pricing function as the estimate, so "estimate minus truth" measures the estimate and not a pricing difference. They differ from the key's own `true_upcode_rate` minus `downcode_rate` by 0.002 on average and up to 0.07 for small panels, because the key counts visits before corrections and claims lag.

Reported beside the score, not in it: upcoders found (binary `role`), dollar-weighted recall (true overpayment dollars of providers sent a demand over those of all providers, each provider's true net overpayment floored at 0), demands by true-rate band, recovery from non-upcoders and the abrasion they carry, and how far estimates exceed true overpayment (a diagnostic).

## Recovery
| Parameter | Value | Source / status | Sensitivity |
|---|---|---|---|
| Basis | level difference: the allowed amount of the billed level minus that of the supported level, scaled by the share the plan paid | same arithmetic as `src/pi_estimate.py` (release 5 option 1) | none |
| Netting (`NETTING`) | on: a sampled claim supported above its billed level counts as a negative overpayment | **verified**: Program Integrity Manual (PIM) chapter 8, section 8.4.5 (Rev. 13762, issued 05-27-26): sampling units found to be underpayments "are recorded as negative overpayments and shall be used in calculating the estimated overpayment" | off |
| Extrapolation gate (`GATE`) | extrapolate only when the sample's error rate (share of reviewed claims overpaid) is at least `GATE_ERROR_RATE`; below it recover only the sampled claims' own netted overpayment, floored at 0 | **verified in kind, number is an assumption**: PIM 8.4.1.2 and 8.4.1.4 and Social Security Act 1893(f)(3) require "a determination of sustained or high level of payment error" (or documented failed education) before extrapolating; the manual lists means of determining it (a high error rate against similar providers, prior history, a payment suspension, law-enforcement information, allegations) and gives **no numeric threshold** | `GATE_ERROR_RATE` 0.15; sweep 0.10, 0.25, 0.40 and gate off |
| Full denial (`FULL_DENIAL`) | off | for a documentation failure that cannot be cured. In data 2.2 every returned note is signed, e-signed or attested after the follow-up, so there is none to deny; template text alone never triggers it | n/a |
| Lower bound (`BOUND`) | `two_sided_90` (release 5's: t for a two-sided 90% interval) | **finding**: the manual asks for "the lower limit of a one-sided 90 percent confidence interval" (8.4.5), a less conservative figure than ours (one-sided 95%); the estimator in `src/pi_estimate.py` and the agent tool use the two-sided table. Kept as the default so score 4.0 reproduces release 5's recovery when its two changes are off (tested) | `one_sided_90` |
| Records not provided | not modeled here | PIM 8.4.5: sampling units whose records were not provided are treated as overpayments. Belongs with non-response (#68) | |

## Staff-hours cost
| Parameter | Value | Source / status | Sensitivity |
|---|---|---|---|
| Hours per year, benefit factor | 2,080; wage x 1.4 | **assumption** (wage plus roughly 30% benefits; not checked this session) | 1.3 to 1.5 |
| Analyst (triage) wage | $78,000 | BLS Occupational Outlook Handbook, May 2025 median for claims adjusters, examiners and investigators (SOC 13-1031): $78,000. **Proxy** for a PI analyst. https://www.bls.gov/ooh/business-and-financial/claims-adjusters-appraisers-examiners-and-investigators.htm | |
| Investigator wage | $78,000 | same occupation | |
| Nurse wage | $97,550 | BLS OOH, registered nurses (SOC 29-1141), May 2025 median. https://www.bls.gov/ooh/healthcare/registered-nurses.htm | |
| Coder wage | $51,140 | BLS OOH, medical records specialists (SOC 29-2072), May 2025 median. **Proxy** for a certified coder: the page does not give a coder-specific wage or certification premium, so a coder is likely understated. https://www.bls.gov/ooh/healthcare/medical-records-and-health-information-technicians.htm | x1.0 to x1.3 |
| Admin wage | $45,930 | BLS OOH, medical secretaries and administrative assistants (SOC 43-6013), May 2025 median. https://www.bls.gov/ooh/office-and-administrative-support/secretaries-and-administrative-assistants.htm | |
| Minutes | triage 15 per listed provider; admin 30 per request round; coder 15 per distinct chart received; investigator 240 and nurse 60 per demand | **assumptions** (the v4/v5 plan) | x0.5 to x2 |
| Chart review, GAO range | $158 per distinct chart received | **verified**: GAO-16-394 (2016), Table 7: Recovery Auditors were paid an average of $158 per **claim review** in 2013 and 2014 (1,980,113 claim reviews, $312.2 million in contingency fees). So the figure is per claim, not per case or provider. It is a fee paid by CMS (inpatient-heavy), not a staff cost. https://www.gao.gov/assets/gao-16-394.pdf | reported as the high end of the chart-review range (`REVIEW_COST_MODEL = "gao_per_claim"`) |
| Copy fee | $90 per request round | release 5 (CMS Transmittal 786: $0.15 per page, up to $15 per record; 30 records x about 20 pages) | |
| API dollars | the run's recorded model spend | measured | |

**Consequence for release 5.** Release 5 charged the GAO $158 once per provider whose charts came back (`C_REVIEW`). Per claim review it would be about $158 per chart, so release 5 understated review cost under that reading. Score 4.0 prices review per chart and shows both readings.

## Abrasion
| Parameter | Value | Source / status | Sensitivity |
|---|---|---|---|
| Weight w(r) | 1 at r <= 0, linear to 0 at r >= 15% | **assumption**; 15% is data 4.0's upcoder floor | end point 10% to 25% |
| Per request round | $43.84 | release 5: Premier 2022 survey, average cost to fight a denied claim | |
| Per demand | $2,000 | release 5 **assumption** | $0 and $10,000 |

## What is easier or different by construction
Truth is exact in the simulation (a payer never has it), and the abrasion weight uses it on purpose: it is the only thing that penalizes going after providers that did not upcode, since recovery is not capped. Data 2.2 has no habits and a narrower honest noise than data 4.0, so scoring stored runs isolates the score, not the data.
