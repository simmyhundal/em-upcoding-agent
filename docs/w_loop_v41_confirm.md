# Workflow v4.1 loop: H17, H16 and their combination H22 on the untouched development batches 7 to 10

[Back to the README](../README.md) · [the loop's report](w_loop_v41.md) · [workflow v4.0's loop](w_loop_v4.md)

Free (API-free). The 40 seeds of batches 7 to 10 (`eval/dev_pool_v4.py`) were never used to choose H16's or H17's setting or to fit the ask model, so they are out of sample for all three. Each was run once at the setting chosen earlier on batches 1 to 4 (H17 at L3: at least 5 documented charts, unsupported share of at least 10%, alpha 0.20; H16 at c = 2: a second random request of 30 charts for a rules-called provider whose point estimate is at least twice the demand cost while its 90% lower bound is below it). H22 combines the two with no new parameter (`eval/w_loop_h22.py`, declared before it was run). Paired against H8 (workflow v4.0); the permutation test is one-sided. H22 is the tenth hypothesis tried (H13 to H20, H20c, H22), so the bar named for it was p below 0.005; none of the comparisons below clears it, or 0.05.

| | H8 (v4.0) | H17 | H16 | H22 (H16 + H17) |
|---|---|---|---|---|
| Score 4.0 per seed | 279 | 440 | 313 | 584 |
| Difference against H8 | | +161 (p = 0.063; better on 4, worse on 0, same on 36) | +34 (p = 0.40; better on 3 of 40) | +304 (p = 0.070; better on 9, worse on 13, same on 18) |
| Upcoders found of 320 | 26 | 30 | 33 | 43 |
| Rounds | 230 | 230 | 270 | 282 |
| Honest providers called | 0 | 0 | 0 | 0 |

H22 against H17 alone: +143 per seed (p = 0.20). H22 against H16 alone: +271 per seed (p = 0.024).

Totals over the 40 seeds for H22 against H8: recovered $105,511 against $76,915; staff cost $82,168 against $65,742.

## Reading
- **No result clears the bar.** Per-seed differences have a spread of about $830 (H17) to $1,270 (H22) against means of $160 to $300: at $304 per seed H22 would need about 108 seeds for 80% power at 0.05 and about 205 at 0.005.
- **H17 never loses to H8** (14 seeds better and none worse across all 100 development seeds), which is mechanical: looser rules only add calls, and the demand floor still blocks weak ones. H17 alone is worth about $160 to $190 per seed.
- **H22 finds many more upcoders (43 against 26) but pays for it unevenly**: better on 9 seeds and worse on 13, the worst by $938. Extra charts only pay when they turn a near-miss into a demand.
- **The safety evidence is thin.** Honest providers are almost never asked (1 of 145 asked providers in batches 1 to 6 was not an upcoder), so zero honest providers called says little about false accusations under loosened rules.
- Not run: fresh seeds. H22 is a lead, not a result.
