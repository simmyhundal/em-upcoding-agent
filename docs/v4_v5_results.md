# Results of workflow v4.0 and agent v5.0

[Back to the README](../README.md)

Ten fresh seeds (5555 to 6464) of data 4.0, scored by score 4.0 ([score_40.md](score_40.md)): dollars recovered, minus staff-hours cost, minus provider abrasion. Asking nobody scores 0. Rendered from `experiments/v4_fresh_results.json`; the seeds were never used to tune anything, and were generated after workflow v4.0 was frozen.

| Version | Net $, ten seeds in all | Upcoders found | Honest providers accused | Request rounds per seed | Seeds above 0 |
|---|---|---|---|---|---|
| Workflow v2.5 (frozen) | -$111,847 | 1 of 80 | 3 | 47.8 | 0 of 10 |
| Workflow v4.0 | -$11,612 | 3 of 80 | 0 | 6.0 | 1 of 10 |
| Agent v5.0 | -$7,812 | 3 of 80 | 0 | 4.5 | 1 of 10 |

Net dollars per seed:

| Seed | Workflow v2.5 | Workflow v4.0 | Agent v5.0 |
|---|---|---|---|
| 5555 | -$8,726 | -$1,788 | -$1,341 |
| 5656 | -$9,703 | -$758 | -$377 |
| 5757 | -$11,513 | -$1,696 | -$1,113 |
| 5858 | -$10,423 | -$2,109 | -$1,886 |
| 5959 | -$13,211 | -$758 | -$377 |
| 6060 | -$13,394 | -$2,644 | -$2,261 |
| 6161 | -$13,426 | $1,410 | $1,934 |
| 6262 | -$12,461 | -$1,539 | -$1,290 |
| 6363 | -$7,736 | -$969 | -$601 |
| 6464 | -$11,255 | -$762 | -$500 |

## What is behind each term (dollars summed over the ten fresh seeds)

![Score waterfall](images/score_waterfall.svg)

**Agent v5.0:**

- **Recovery +$3,847:** 3 of 80 upcoders found, 3 demands, about $1,282 recovered per demand.
- **Staff cost -$11,440:** chart review $5,473 (636 charts), requests and copy fees $4,746 (45 rounds), demand work $827, triage and model dollars $395.
- **Abrasion -$218:** the cost to providers of requests and demands; no honest provider was demanded from.
- **Net score -$7,812** over ten seeds.

**Workflow v4.0:**

- **Recovery +$3,792:** 3 of 80 upcoders found, 3 demands, about $1,264 recovered per demand.
- **Staff cost -$15,343:** chart review $5,301 (616 charts), requests and copy fees $6,327 (60 rounds), demand work $827, triage and model dollars $2,887.
- **Abrasion -$61:** the cost to providers of requests and demands; no honest provider was demanded from.
- **Net score -$11,612** over ten seeds.

## What to take from it

- **Neither new version is above zero.** One seed in ten is above zero (seed 6161: $1,410 for v4.0, $1,934 for v5.0). Staff time alone costs $758 to $2,583 per seed for v4.0 ($377 to $2,043 for v5.0), and a demand needs a recovery the payer can defend (a 90% lower bound from a random sample, with underpayments netted and a gate that skips extrapolation below a 15% error rate).
- **Most of the gain over v2.5 is that the new versions stop asking.** v2.5 sent about 48 request rounds per seed and found 1 upcoder; v4.0 sent 6 and the agent 4.5. The frozen screen cannot see data 4.0's habits, so v2.5 spent staff time on providers it could not tell apart.
- **The agent and the workflow are not reliably different.** They find the same 3 of 80; the agent is $380 per seed ahead, on 10 of 10 seeds, through lower staff cost; the same three upcoders were found, so one more seed set would have to confirm it.
- **Recall is 4%.** The ceiling is the recovery, not the screen: see [ceiling_v4.md](ceiling_v4.md). On the 100 development seeds workflow v4.0 scored +$549 per seed (77 of 800 upcoders found), so there is a gap between development and fresh seeds that [#132](https://github.com/simmyhundal/em-upcoding-agent/issues/132) will measure on a second fresh pool.
- **By construction.** Data 4.0 is synthetic; the lab line that the chosen screen (`eb_upper_t`) uses is linked to the true visit level by the generator ([screens_v4.md](screens_v4.md)); and the answer key defines which providers upcode.

## Where the pieces are

[Data 4.0](data_v4_0.md) · [score 4.0](score_40.md) · [screens](screens_v4.md) · [the development loop that froze workflow v4.0](w_loop_v4.md) · [the plan](v4_v5_plan.md) · next: v4.1 and v5.1 ([#132](https://github.com/simmyhundal/em-upcoding-agent/issues/132) to [#137](https://github.com/simmyhundal/em-upcoding-agent/issues/137))
