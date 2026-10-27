# Score 4.3: the proposal

[Back to the README](../README.md) · [sources](score_43_sources.md) · [sources, addendum](score_43_sources_addendum.md) · [score 4.2](score_42.md) · issue 200 · [process](process.md)

**What this page is.** The values proposed for score 4.3 and what they do to every row of the results table, written for sign-off. Score 4.3 is score 4.2 with changes that make the dollar figure closer to what a payer would keep: [appeals](concepts/appeal-reduction.md "the share of a demand lost to provider appeals") reduce a demand, only part of what is demanded is [collected](concepts/collection-rate.md "the share of an estimated overpayment that ends as cash"), a [fraud case](concepts/fraud-referral.md "an SIU case, not a demand letter") costs far more than a demand letter, the [extrapolation gate](concepts/error-gate.md "extrapolate only if the sample's error is large enough") is measured in dollars, and handling appeals costs staff time. **Signed off by Simmy on 2026-10-27 with the values below as written; the final description is [score 4.3](score_43.md).** Scores 4.0, 4.1 and 4.2 stay frozen. Revised 2026-10-27 after a second, targeted search for collection figures ([addendum](score_43_sources_addendum.md)).

## Proposed parameters
| Parameter | Proposed | Range kept as sensitivity | Status | Source |
|---|---|---|---|---|
| Fraud referral cost (total per provider case, in place of a demand's $276 of staff work) | **$4,000** | $2,000, $15,000 | assumption anchored to NHCAA 2013 ($3,459 per closed SIU investigation) and a bottom-up of $4,251; no newer per-case source exists | [sources, 1](score_43_sources.md) |
| Collection rate, **claims-data lane** providers (**already net of appeals**) | **25%** | 16%, 45%, 65% | sourced: four series put payer-initiated fraud and abuse overpayments at 16% to 24% collected (Medicare FY2014 referral cohort 20%; Medicaid managed-care plans' own SIUs 22%; contractors 24%; analytics-found leads 16%) | [addendum, rows 1 to 4](score_43_sources_addendum.md) |
| Collection rate, ordinary demand (after the appeal reduction) | **68%** (was 85%) | 55%, 85%, 91% | sourced: the same Medicaid plans collected 68% of non-fraud overpayments; 85% had no source | [addendum, row 3](score_43_sources_addendum.md) |
| Appeal reduction of an ordinary demand | **15%** | 0%, 30% | sourced, Medicare analog (RAC FY2021 Level 1); not applied to the lane, whose rate is already net | [sources, 3](score_43_sources.md) |
| Payer cost of handling appeals | 17% of demands appealed x 3 coder hours | 2 to 4 hours | assumption | [sources, 3](score_43_sources.md) |
| Records copy fee per round | **$0** (unchanged) | $25, $90 | partly sourced | [sources, 4](score_43_sources.md) |
| Extrapolation gate | **net dollar error rate of 5%** (was 15% of claims) | none, 10% | assumption anchored to OIG integrity-agreement practice; does not change any row here | [sources, 5](score_43_sources.md) |
| Lower bound | two-sided 90% (unchanged) | one-sided 90%, 95% | sourced | [sources, 5](score_43_sources.md) |
| Look-back | not modeled | 180 days, 12 and 24 months | sourced, binding only once a demand date exists | [sources, 6](score_43_sources.md) |

Staff minutes, wages and abrasion prices ($43.84 per round, $2,000 per demand) are unchanged from score 4.0 and stay assumptions with sensitivity.

## What the second search found
The sources agree on why recovery from fraud-type cases is low and from ordinary ones is not: **when the provider stops billing the payer, there is nothing to offset against; when the case goes to law enforcement or the state, collection is frozen.** Plans that collect 22% of fraud-related overpayments collect 68% of non-fraud ones in the same year; where a state SIU's finding stood and the provider stayed, it collected about 91%. **No source supports 85% for the lane.** No commercial payer or vendor publishes identified-against-collected rates (vendors publish fee rates and marketing cases). Contingency fees are 8% to 17% for government audit contractors and 15% to 30% for commercial vendors; a payer working the case itself pays staff time, which the score already counts. The lane's choice therefore reduces to whether flagged providers leave or keep billing; the simulation has no exit, so 25% is the sourced single value and 45% and 65% show what an exit-or-offset mix would do.

## What it does to the results table
Dollars summed over each row's ten test seeds. The first row is the README table today; the second is the proposed defaults; the rest change one value at a time.

| Variant | Workflow v4.0 (4.0) | Workflow v4.1 (4.0) | Agent v5.0 (4.0) | Agent v5.1 (4.0) | Workflow v4.1 (4.2) | Workflow v4.2 (4.2) | Agent v5.2 (4.2) |
|---|---|---|---|---|---|---|---|
| score 4.2 (reference, as in the README) | -$6,212 | $15,791 | -$3,762 | $11,206 | $17,713 | $375,031 | $372,114 |
| score 4.3 defaults (lane collected at 25%, net of appeals) | -$7,865 | $4,603 | -$5,438 | $2,180 | $6,833 | -$25,962 | -$27,150 |
| lane collected at 16% | -$7,865 | $4,603 | -$5,438 | $2,180 | $6,833 | -$59,305 | -$60,492 |
| lane collected at 45% (a third to a half of providers exit, the rest offset) | -$7,865 | $4,603 | -$5,438 | $2,180 | $6,833 | $48,133 | $46,945 |
| lane collected at 65% (the plan offsets against a provider who keeps billing) | -$7,865 | $4,603 | -$5,438 | $2,180 | $6,833 | $122,228 | $121,040 |
| lane collected at 85% (no source supports it) | -$7,865 | $4,603 | -$5,438 | $2,180 | $6,833 | $196,322 | $195,135 |
| referral cost $2,000 | -$7,865 | $4,603 | -$5,438 | $2,180 | $6,833 | $34,038 | $32,850 |
| ordinary demand collected at 85% (the earlier assumption; no source) | -$7,317 | $8,380 | -$4,882 | $5,211 | $10,510 | -$22,284 | -$24,052 |
| ordinary demand collected at 91% (Vermont findings that stood) | -$7,124 | $9,713 | -$4,686 | $6,280 | $11,808 | -$20,986 | -$22,959 |
| no appeal reduction on ordinary demands | -$7,478 | $7,269 | -$5,045 | $4,319 | $9,429 | -$23,366 | -$24,963 |
| gate as score 4.2 (15% of claims) | -$7,865 | $4,603 | -$5,438 | $2,180 | $6,833 | -$25,962 | -$27,150 |
| copy fee $90 | -$13,265 | -$1,157 | -$9,488 | -$1,600 | $2,783 | -$36,492 | -$36,150 |

## The decision this needs
Under the sourced values **the volume lane stops paying**: workflow v4.2 on the ten data 4.2 test seeds scores **-$25,962** instead of $375,031, because each lane case collects about a quarter of its lower bound and costs $4,000. That is a finding, not a bug: with sourced collection and cost, chasing volume fraud pays only for cases whose lower bound is above about $16,000 (the break-even rule enforces it). The level-review rows shrink but stay positive (workflow v4.1 on data 4.0: $15,791 to $4,603). The gate does not matter in these runs.

**One question for Simmy:** approve the table above as the defaults of score 4.3 (lane collected at 25% net of appeals; ordinary demand 68% then a 15% appeal reduction; referral cost $4,000; the rest as written)? Alternatives: (B) keep the lane at 45% as a probability-weighted value if you want to credit providers who stay and are offset; (C) change any single value.

## What follows after sign-off
Re-score the references under the signed-off values and publish that table first; update the oracle for score 4.3 and data 4.3 and stress-test it; write `docs/score_43.md`, make `src/recovery_43.py` and `eval/score_43.py` final, add their tests, and use score 4.3 in the loop.
