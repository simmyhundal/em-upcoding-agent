# Score 4.2: what is counted, with each parameter's source or "assumption"

[Back to the README](../README.md) · [score 4.0](score_40.md) · [score 4.1](score_41.md) · [data 4.2](data_v4_2.md) · [concepts](concepts/README.md) · code: `eval/score_42.py`, `src/recovery_42.py`

**What this page is.** The score (a dollar figure per synthetic dataset) the workflow and the agent are judged by on data 4.2: how much the payer recovers, minus what it costs the payer's staff, minus the cost to providers who did nothing wrong. It extends [score 4.0](score_40.md), which stays frozen, with two changes that data 4.2 needs. Wages, minutes per task and the abrasion prices are score 4.0's; their sources are on that page.

```
score = Recovered - StaffCost - Abrasion          (per dataset)

Recovered = for each provider sent a demand:
            [level] the 90% lower bound of the overpayment a random chart sample supports (score 4.0's estimate, claims outside the lane's sampled days)
          + [lane]  the 90% lower bound of the overpayment a random sample of the provider's claims on its high-volume days supports (that stratum only)
StaffCost = hours x loaded wage for triage, requests, chart review and demands (score 4.0), with the records copy fee at $0
Abrasion  = w(total true rate) x ($43.84 per request round + $2,000 per demand)
```

## What changed from score 4.0
| Change | Value | Source / status |
|---|---|---|
| Records copy fee | $0 per request round (was $90) | **assumption**: the commercial profile of score 4.1 (many commercial contracts require records for audits at no charge); not checked against contracts. Sweep: $90 returns score 4.0's profile |
| [Records not provided](concepts/records-not-provided.md) | a sampled claim the office reports it has no record of counts as overpaid at its full paid amount; silence counts for nothing | **verified**: Program Integrity Manual ch. 8, section 8.4.5, sampling units whose records were not provided are treated as overpayments (the line score 4.0 left as "not modeled") |
| [Stratified sample](concepts/stratified-sample.md) recovery | a random sample within a stratum (the claims on the days a provider billed 30 or more visits) extrapolates to that stratum only; the netting, the 15% error gate and the 90% lower bound are score 4.0's | method standard; the 30-visit cap and 30-claim sample are workflow v4.2's design choices, not score parameters |
| Abrasion weight | w uses the provider's **total** true rate: (visits billed above minus below the justified level, plus claims billed for visits never rendered) over (rendered plus never-rendered claims); w = 1 at 0 or below, falling to 0 at 15% | **assumption**, a consequence of data 4.2: under score 4.0's level-only rate a provider whose fault is billing for visits that never happened has a true rate of 0 and would count as honest |
| Demand and triage | $275.66 per demand, $13.13 triage per provider taken into the lane or the list, as score 4.0 | score 4.0 |

A provider with both a level demand and a lane demand gets **one** demand: both estimates count, the level one on the claims outside the sampled days so no claim is counted twice.

## What is the same
Netting (underpayments reduce the estimate), the extrapolation gate (assumption: 15% error rate), the t-based 90% lower bound, wages (BLS May 2025 medians x 1.4), minutes per task, $43.84 burden per round and $2,000 per demand: [score 4.0](score_40.md).

## Reported beside the score, not in it
Demands, lane providers flagged and right (providers with impossible-visit billing), lane providers wrong, level and lane recovery, providers justified at m = 1 that were sent a demand, true overpayment available and pursued, and the score under score 4.0 through the adapter (`eval/d42_truth.py`). The justification threshold *m* is not settled; the primary view is m = 1.

## The oracle
`eval/oracle_s42.py` computes the best conceivable score on the same datasets from the answer key, **inside score 4.2's recovery rules**. Per provider it may use a random chart sample of n claims (30, 60, 90, 150 or all of them) and, where the provider billed visits that never happened, a stratified sample drawn within exactly those claims (it knows which they are; n = 30, 60, 90 or all). It pays the charts received, the request rounds, one demand and one triage, and abrasion weighted by the provider's total true rate, and it pursues **any provider, honest or not, when the expected value is positive**. Values are expected 90% lower bounds averaged over 20 random samples. It assumes every office answers and the screen is perfect.

| Ten test datasets | Data 4.0 | Data 4.2 |
|---|---|---|
| Oracle score | $62,662 | $627,805 |
| Recovered | $100,688 | $699,963 (level only $57,522; impossible-day providers $477,256; other providers who billed visits never rendered $165,185) |
| Staff cost | $38,026 | $46,666 |
| Abrasion | $0 | $25,493 |
| Providers pursued | 39 | 102 (6 with a true rate under 5%) |

Workflow v4.2 recovered $395,924 on the same data: $370,474 of the oracle's $477,256 from impossible-day providers (78%), $25,450 of its $57,522 level dollars (44%), and nothing of the $165,185 from providers whose phantom visits are spread over patients (no volume signal; [#199](https://github.com/simmyhundal/em-upcoding-agent/issues/199)). An earlier version of the oracle reported $74,155 and $459,400; it averaged only 6 samples (choosing the best sample size from noisy estimates biases the oracle upward; the data 4.0 figure fell from $74,155 to $62,662 with 20 samples), and it considered only the impossible-day strata, not the other providers' phantom visits. It is an upper bound under these rules, not a target. It is not an upper bound on what a payer could recover with other rules: a targeted request for the exact claims known to be overbilled earns nothing here, because the score counts only random and stratified samples.

## Known weaknesses
- The copy-fee profile and the 15% gate are assumptions.
- A demand for fabricated visits is, in practice, usually a fraud referral and not a demand letter; scoring it as a demand with score 4.0's cost ($276) understates the real cost.
- **The lane's signal is clean by construction.** See [the volume screen](concepts/volume-screen.md).
- The ghost-member form of billing for visits never rendered is not separable in claims (up to 13 visits per member against an honest 12) and no arm reaches it.
- Providers do not change behavior after a request; the office's non-response is simulated (the lane gets nothing usable from about a quarter of impossible-day providers).
