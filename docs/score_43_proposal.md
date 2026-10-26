# Score 4.3: the proposal

[Back to the README](../README.md) · [sources](score_43_sources.md) · [score 4.2](score_42.md) · issue 200 · [process](process.md)

**What this page is.** The values proposed for score 4.3 and what they do to every row of the results table, written for sign-off. Score 4.3 is score 4.2 with five changes that make the dollar figure closer to what a payer would keep: appeals reduce a demand, only part of what is demanded is collected, a fraud case costs far more than a demand letter, the extrapolation gate uses dollars, and handling appeals costs staff time. Nothing here is final until Simmy signs it off; the code (`src/recovery_43.py`, `eval/score_43.py`) is a prototype that reads the values below. Scores 4.0, 4.1 and 4.2 stay frozen.

## Proposed parameters
| Parameter | Proposed | Range kept as sensitivity | Status | Source |
|---|---|---|---|---|
| Fraud referral cost (total per provider case, in place of a demand's $276 of staff work) | **$4,000** | $0, $2,000, $5,000, $15,000 | assumption anchored to NHCAA 2013 ($3,459 per closed SIU investigation) and a bottom-up of $4,251 | [sources, 1](score_43_sources.md) |
| Collection rate, ordinary demand (after appeals) | **85%** | 55% to 95% | assumption; low end OIG's 55% of sustained Medicare overpayments | [sources, 2](score_43_sources.md) |
| Collection rate, fraud referral (after appeals) | **25%** | 10% to 85% (see the question below) | sourced in kind: Medicare benefit-integrity contractors recovered about 24% of what they referred | [sources, 2](score_43_sources.md) |
| Appeal reduction of demanded dollars | **15%** | 9% to 30% | sourced, Medicare analog: Level 1 overturned dollars over collected dollars, RAC FY2021 | [sources, 3](score_43_sources.md) |
| Payer cost of handling appeals | 17% of demands appealed x 3 coder hours | 2 to 4 hours | assumption (appeal rate derived from RAC FY2021) | [sources, 3](score_43_sources.md) |
| Records copy fee per round | **$0** (unchanged) | $25, $90 | partly sourced: commercial contract language, HIPAA sets no fee for payer audits | [sources, 4](score_43_sources.md) |
| Extrapolation gate | **net dollar error rate of 5%** (was 15% of claims) | none, 10% | assumption anchored to OIG integrity-agreement practice | [sources, 5](score_43_sources.md) |
| Lower bound | two-sided 90% (unchanged) | one-sided 90%, 95% | sourced (2025 OIG integrity agreement) | [sources, 5](score_43_sources.md) |
| Look-back | not modeled | 180 days, 12 and 24 months | sourced from state statutes, but binding only once a demand date exists | [sources, 6](score_43_sources.md) |

Staff minutes, wages, abrasion prices ($43.84 per round, $2,000 per demand) are unchanged from score 4.0 and stay assumptions with sensitivity.

## What it does to the results table
Dollars summed over each row's ten test seeds. The score 4.2 row is the README table today; the second row is the proposed defaults; the rest change one value at a time from the proposal.

| Variant | Workflow v4.0 (4.0) | Workflow v4.1 (4.0) | Agent v5.0 (4.0) | Agent v5.1 (4.0) | Workflow v4.1 (4.2) | Workflow v4.2 (4.2) | Agent v5.2 (4.2) |
|---|---|---|---|---|---|---|---|
| score 4.2 (reference, as in the README) | -$6,212 | $15,791 | -$3,762 | $11,206 | $17,713 | $375,031 | $372,114 |
| score 4.3 defaults | -$7,317 | $8,380 | -$4,882 | $5,211 | $10,510 | -$36,177 | -$37,945 |
| referral collection 85% (the payer recoups by offset itself) | -$7,317 | $8,380 | -$4,882 | $5,211 | $10,510 | $152,765 | $150,997 |
| referral cost $2,000 | -$7,317 | $8,380 | -$4,882 | $5,211 | $10,510 | $23,823 | $22,055 |
| referral cost $0 (as score 4.2) | -$7,317 | $8,380 | -$4,882 | $5,211 | $10,510 | $75,543 | $73,775 |
| no appeal reduction | -$6,834 | $11,712 | -$4,391 | $7,884 | $13,755 | -$19,039 | -$21,319 |
| demand collection 55% | -$8,284 | $1,715 | -$5,863 | -$137 | $4,020 | -$42,667 | -$43,411 |
| gate as score 4.2 (15% of claims) | -$7,317 | $8,380 | -$4,882 | $5,211 | $10,510 | -$36,177 | -$37,945 |
| no gate (0%) | -$7,317 | $8,380 | -$4,882 | $5,211 | $10,510 | -$36,177 | -$37,945 |
| copy fee $90 | -$12,717 | $2,620 | -$8,932 | $1,431 | $6,460 | -$46,707 | -$46,945 |

## The decision this needs
Two things stand out.
1. **Everything shrinks.** Collection and appeals cut every row (data 4.1's workflow, for example, falls from $15,791 to $8,380 on data 4.0), which is the point: a demand is not the money in the bank.
2. **The volume lane's result depends on one choice.** With the sourced fraud-referral collection of **25%** and the $4,000 referral cost, workflow v4.2 scores **-$36,177** instead of $375,031: each referral recovers about $2,800 on average and costs $4,000. With a collection rate of **85%** (the payer recoups by offset against the provider's own claims, as it does for an ordinary demand) it scores **$152,765**. The 25% figure measures Medicare contractors' cases passed to law enforcement and recovered through a long pipeline; the payer's own recoupment of visits that never happened is closer to the 85% case, but a provider that is terminated or disappears recovers less. The gate does not matter in these runs (the three gate variants are identical).

**One question for Simmy:** which collection rate applies to the volume lane's providers?
- **(A) 25%**, the sourced referral figure. The lane then loses money and the release's agent comparisons are about whether anything is worth pursuing.
- **(B) 85%**, the same as an ordinary demand, with the $4,000 referral cost. Proposed: the lane remains the main source of recovery, at a lower level than before.
- **(C) 55%**, between them (the share of sustained Medicare overpayments OIG reported collected).
My recommendation is **(B)** with (A) and (C) reported in the sensitivity columns, because the lane's recoveries in this simulation are claims the payer itself recoups. Everything else in the table above is proposed as written; say which values to change.

## What follows after sign-off
Re-score the references under the signed-off values and publish that table first; update the oracle for score 4.3 and data 4.3 and stress-test it; write `docs/score_43.md`, make `src/recovery_43.py` and `eval/score_43.py` final, add their tests, and use score 4.3 in the loop.
