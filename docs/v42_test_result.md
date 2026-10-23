# Release 4.2 and 5.2: the test on fresh seeds

[Back to the README](../README.md) · [workflow v4.2 freeze](w42_freeze.md) · [confirm read](w42_confirm_result.md) · [agent v5.2](agent_v52.md) · [score 4.2](score_42.md) · [seeds](seeds.md)

**What this page is.** The one read of workflow v4.2 and agent v5.2 on seeds nobody had run: ten seeds of data 4.2 (pool D4.2-TEST-1, seeds 4700 + 37j), score 4.2 in dollars. Workflow v4.1 was re-run on the same seeds (free); agent v5.1 was not (the project does not re-run earlier agents; the agent is compared with workflow v4.1 and workflow v4.2 on the same seeds instead). The agent ran once per seed, effort low, Opus 5.5, **$1.78 in all** (estimate $2.5, batch cap $3, release cap $4). Nothing in either version was chosen on these seeds.

## Results (ten seeds, dollars summed over the seeds)
| Version | Score 4.2, total | Per seed (mean / median) | Seeds above zero | Demands | Lane demands | Recovered | Staff cost | Abrasion |
|---|---|---|---|---|---|---|---|---|
| Workflow v4.1 | $17,713 | $1,771 / $313 | 5 of 10 | 8 | 0 | $25,450 | $7,737 | $0 |
| Workflow v4.2 | $375,031 | $37,503 / $39,498 | 10 of 10 | 38 | 30 | $395,924 | $17,842 | $3,051 |
| Agent v5.2 | $372,114 | $37,211 / $39,294 | 10 of 10 | 36 | 30 | $391,910 | $16,744 | $3,051 |

- **Workflow v4.2 minus workflow v4.1:** +$35,732 per seed, better on 10 of 10 seeds, one-sided exact p = 0.001.
- **Agent v5.2 minus workflow v4.2:** −$292 per seed, better on 2 of 10, p = 0.94: not distinguishable. **Agent v5.2 minus workflow v4.1:** +$35,440 per seed, 10 of 10.
- **Where the money comes from.** Of $395,924 recovered by workflow v4.2, **$370,474 (94%) is the claims-data lane** and $25,450 the level review, the same dollars workflow v4.1 recovers. The lane sent a demand to 30 of the 36 providers with impossible-day billing (83%) and to no other provider; the screen never missed one, and 6 returned nothing usable. Agent v5.2 sent the same 30 lane demands.
- **What is still out of reach.** Of $1.96 million true overpayment in these ten datasets, workflow v4.2 pursued providers holding $525,000 (27%) and recovered $396,000 (20%). It sent a demand to 38 of the 478 providers whose true overpayment is at least the cost of pursuing them (8%): level upcoding is as hard to reach as before.

## Reading it
1. The lane reproduces on fresh seeds what the development seeds showed (+$37,503 per seed; confirm pool +$35,080): the gain comes from code reading counts the generator planted as separable, then a records request. **That separation is built into the synthetic data.** The test shows a reviewer can turn a clean signal into recovery with a model or with code; it does not estimate what real claims would yield.
2. The agent matches the workflow here because both run the same lane code; the model's choices (which providers to take through the lane, whether to send each demand) followed the advice. The agent's model cost is under 18 cents per seed.
3. Level upcoding contributes the same $2,500 per seed it did in workflow v4.1; the version 4.1 and 5.1 lessons (second-use seeds, one seed carries the total) still apply to it.

Per-seed numbers: `experiments/v42_test_results.json`. Parity (scripted agent against the workflow): [agent v5.2](agent_v52.md).
