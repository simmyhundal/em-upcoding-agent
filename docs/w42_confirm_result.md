# Workflow v4.2: the confirm read

[Back to the README](../README.md) · [freeze declaration](w42_freeze.md) · [development loop](w_loop_v42.md) · [score 4.2](score_42.md)

**What this page is.** The one read of workflow v4.2 on seeds it was never tuned on, run exactly as declared in the [freeze declaration](w42_freeze.md) (committed before the run). 100 seeds of data 4.2 (pool D4.2-CONFIRM, seeds 1002 + 37j), free and API-free, score 4.2 in dollars per seed. Because data 4.2 has no earlier test seeds, this run is also the final development run of the [process](process.md).

| | Workflow v4.2 | Workflow v4.1 |
|---|---|---|
| Mean per seed | $35,080 | $1,479 |
| Median per seed | $32,067 | $-83 |
| Seeds above zero | 97 of 100 | 37 of 100 |

Paired difference (v4.2 minus v4.1): **+$33,601 per seed**, standard deviation $20,839, better on 95 of 100 seeds, one-sided permutation p < 0.0001.

The [volume screen](concepts/volume-screen.md) lane sent a demand to 277 of 321 providers with impossible-day billing (86%) and took in 0 providers without it.

## Criteria declared in advance
1. Gain of at least +$500 per seed with p < 0.0125: **met**.
2. The lane demands at least 70% of impossible-day providers: **met**.
3. At most 0.5 providers per seed without impossible-day billing taken in: **met**.

**Passed.** What this does not show is in the [freeze declaration](w42_freeze.md): the volume signal is clean by construction in the synthetic data, so the gain is the gain from a clean signal, not an estimate of what a payer would find in real claims.
