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

## Known weaknesses
- The copy-fee profile and the 15% gate are assumptions.
- A demand for fabricated visits is, in practice, usually a fraud referral and not a demand letter; scoring it as a demand with score 4.0's cost ($276) understates the real cost.
- **The lane's signal is clean by construction.** See [the volume screen](concepts/volume-screen.md).
- The ghost-member form of billing for visits never rendered is not separable in claims (up to 13 visits per member against an honest 12) and no arm reaches it.
- Providers do not change behavior after a request; the office's non-response is simulated (the lane gets nothing usable from about a quarter of impossible-day providers).
