# Score 4.3: what is counted, with each parameter's source or "assumption"

[Back to the README](../README.md) · [score 4.2](score_42.md) · [sources](score_43_sources.md) and [addendum](score_43_sources_addendum.md) · [the proposal that was signed off](score_43_proposal.md) · [concepts](concepts/README.md) · code: `eval/score_43.py`, `src/recovery_43.py`

**What this page is.** The score (a dollar figure per synthetic dataset) the workflow and the agent are judged by from release 4.3: how much cash the payer expects to collect, minus what the payer's staff spend, minus the cost to providers who did nothing wrong. It extends [score 4.2](score_42.md), which stays frozen, with the changes that make a demand closer to money in the bank. Simmy signed the values off on 2026-10-27. Wages, minutes per task and the abrasion prices are score 4.0's; their sources are in [score 4.0](score_40.md).

```
score = Collected - StaffCost - Abrasion          (per dataset)

Collected = for each provider sent a demand or a fraud referral, the conservative estimate of what its sample supports,
            less appeals, times the share collected
StaffCost = hours x loaded wage for triage, requests, chart review and demands; a referral costs $4,000 in place of a demand's work; expected appeal handling
Abrasion  = w(total true rate) x ($43.84 per request round + $2,000 per demand), as in score 4.2
```

## What changed from score 4.2
| Change | Value | Status | Source |
|---|---|---|---|
| A provider found by the [volume screen](concepts/volume-screen.md "flag providers by claims per day from claims alone"), or whose chart sample includes claims for visits that never happened, is a **[fraud referral](concepts/fraud-referral.md "an SIU case, not a demand letter")**, not an ordinary demand | cost **$4,000** in place of a demand's $276 | assumption anchored to $3,459 per closed investigation (an industry survey, 2013) and a bottom-up of $4,251 | [sources, 1](score_43_sources.md) |
| **[Collection rate](concepts/collection-rate.md "the share of an estimated overpayment that ends as cash")** for a referral | **25%**, already net of appeals | sourced: 16% to 24% for payer-initiated fraud and abuse overpayments (Medicare cohort 20%, Medicaid plans' SIUs 22%) | [addendum](score_43_sources_addendum.md) |
| Collection rate for an ordinary demand | **68%** after the appeal reduction | sourced: Medicaid plans collected 68% of non-fraud overpayments; the earlier 85% had no source | [addendum, row 3](score_43_sources_addendum.md) |
| **[Appeal reduction](concepts/appeal-reduction.md "the share of a demand lost to provider appeals")** of an ordinary demand | **15%** | sourced, Medicare analog (overturned dollars at the first appeal level, fiscal year 2021) | [sources, 3](score_43_sources.md) |
| **[Error gate](concepts/error-gate.md "extrapolate only if the sample's error is large enough")** (the *dollar gate*) | extrapolate only if the sample's net overpayment is **5% or more of the paid dollars** of the reviewed claims (was: 15% of claims overpaid) | assumption anchored to inspector-general integrity-agreement practice; changes no row so far | [sources, 5](score_43_sources.md) |
| Payer cost of handling appeals | 17% of demands appealed x 3 hours of a certified coder | assumption (17% derived from Medicare data) | [sources, 3](score_43_sources.md) |

## What is the same
The [conservative estimate](concepts/conservative-estimate.md "the 90% lower bound") (netting, the two-sided 90% lower bound), [records not provided](concepts/records-not-provided.md "a visit the office has no record of counts as overpaid"), the [stratified sample](concepts/stratified-sample.md "a random sample within one slice of a provider's claims") of the volume lane, the copy fee of $0, wages, minutes per task, and the abrasion prices ($43.84 per request round, $2,000 per demand, weighted by the provider's total true rate; see *Provider abrasion* in the [glossary](glossary.md)). Look-back windows are not modeled (the data has one year and no demand date).

## Reported beside the score
Dollars collected against dollars of conservative estimate, demands and referrals sent, true overpayment available and pursued, and the score under score 4.2. The sensitivity table of the proposal ([score 4.3 proposal](score_43_proposal.md)) shows how each value moves each row: the per-chart review cost ($8.61) is the assumption that moves scores most, and no source supports it.

## The [oracle](concepts/oracle.md "the best conceivable score from the answer key")
`eval/oracle_s43.py` repeats the oracle of score 4.2 under score 4.3's rules: per provider, the better of a random chart sample of any size or a sample drawn only from the claims it knows are for visits that never happened; it pursues a provider only when the expected value after collection, staff cost, referral cost and abrasion is positive. The results and the stress test are in [the re-scored table](score_43_rescored.md).

## Known weaknesses
- The collection rates are borrowed from government programs and Medicaid managed care; no commercial payer or vendor publishes identified-against-collected figures. The lane's 25% is the largest single uncertainty (16% to 85% across the sensitivity table).
- The 15% appeal reduction is probably low for demands extrapolated from a small sample; 40% is kept as a sensitivity.
- Per-chart review cost, staff minutes and the $4,000 referral cost are assumptions.
- Providers do not leave the network or change behavior after a demand; the simulation has no exit, which is the reason referral collection is low in the sources.
