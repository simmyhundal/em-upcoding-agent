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

## H23: H22 with a shorter list (declared in `eval/w_loop_v41_decl.py` before any run)

H22's pipeline with the list size N in place of 22 (`list_k`: same `eb_upper_t` ranking, only the first N rows flagged; `eval/w_loop.py` versions `H23_n<N>`, with `H22` registered there at the unchanged spec of `eval/w_loop_h22.py`). Score 4.0 charges triage (about $13.125) for every provider with a checked summary, so a list of 22 costs about $289 per seed; H22 asks about 3. The ask model (`src/policy_40_ask.json`, features from the provider's own row, rank and screen score kept in the shorter file) was fitted on 22-provider lists; in a short list it asks exactly the providers it asked in H22 among the first N. Free, real workflow runs. Analysis: `python eval/w_loop_h23.py lobo | cmp N BATCHES`. H23 is the eleventh hypothesis tried, so the Bonferroni bar is 0.05 / 11 = 0.0045 per look.

**Grid and choice (batches 1 to 4 only, leave-one-batch-out, ties to the larger list).** Score 4.0 per seed:

| N | batch 1 | batch 2 | batch 3 | batch 4 | mean of 40 | found of 320 |
|---|---|---|---|---|---|---|
| 4 | -6 | 3,941 | 188 | 1,771 | 1,473 | 52 |
| 6 | 156 | 3,858 | 26 | 1,687 | 1,432 | 55 |
| 8 | 129 | 3,832 | 0 | 1,661 | 1,406 | 55 |
| 11 | 54 | 3,793 | -40 | 1,622 | 1,357 | 55 |
| 15 | -52 | 3,740 | -92 | 1,569 | 1,291 | 54 |
| 22 (H22) | -144 | 3,648 | -184 | 1,477 | 1,199 | 54 |

Every held-out batch chose N = 4 on the other three (realized -6, 3,941, 188, 1,771; leave-one-batch-out mean 1,473 against H22's 1,199). The score falls steadily as the list grows, so the grid's smallest value wins: **N = 4 is on the edge of the grid** (N of 1 is known from H20c to lose recovery; 2 and 3 were not tried, which the grid did not allow). Honest providers called: 0 in every setting.

**Out of sample, N = 4 run once** (never adjusted):

| | batches 5 and 6 (20 seeds) | batches 7 to 10 (40 seeds) |
|---|---|---|
| H23 (N = 4) score per seed | 1,381 | 965 |
| H22 | 1,203 | 584 |
| H8 (v4.0) | 719 | 279 |
| Against H22 | +179 (p = 0.024; better 19, worse 1) | +381 (p < 0.0001; better 39, worse 1) |
| Against H8 | +663 (p = 0.027; better 16, worse 4) | +685 (p = 0.0001; better 34, worse 6) |
| Found (H23 / H22 / H8) | 24 / 26 / 17 | 39 / 43 / 26 |
| Rounds (H23 / H22 / H8) | 129 / 141 / 118 | 237 / 282 / 230 |
| Recovered per seed (H23 / H22) | 3,115 / 3,315 | 2,527 / 2,638 |
| Staff cost per seed (H23 / H22) | 1,734 / 2,113 | 1,562 / 2,054 |
| Triage per seed (H23 / H22) | 52 / 289 | 52 / 289 |
| Honest providers called | 0 / 0 / 0 | 0 / 0 / 0 |

**How much of the gain is triage saved.** Listing 4 instead of 22 saves 18 x $13.125 = $236 per seed on every seed, which is mechanical and the reason for the near-zero p-values against H22 (39 of 40 seeds better). Against H22 the gain of +179 (batches 5 and 6) is +236 triage and -58 from asking and recall (p = 0.62, 2 seeds better, 2 worse); the gain of +381 (batches 7 to 10) is +236 triage and +145 other (p = 0.036, 13 better and 1 worse; this is above 0.0045). The "other" part comes from the 18 providers H22 asked at ranks 5 to 22 that H23 does not (6 on batches 5 and 6): those asks cost more in staff time than they recovered (recovered -111 per seed, staff cost -492 per seed in 7 to 10), but 4 demands made by H22 on batches 7 to 10 (2 on 5 and 6) are lost, and found falls from 43 to 39 (26 to 24). Against H8 the other part is +426 (p = 0.097) and +449 (p = 0.018).

**Reading.** The list can be cut to 4 without losing what the ask model asks about in the top 4; almost all the gain over H22 is the triage no longer charged, and the rest is a lead on a handful of seeds, not a result at 0.0045 (and the tuning picked an edge of the grid). Caveats: the ask model was fitted on 22-provider lists; the list's cut-off is only as good as the `eb_upper_t` ranking (the top 4 hold all but 18 of the asks across 40 seeds); the seeds are development data, not fresh seeds; H8 and H22 comparisons share the same 60 seeds; honest providers are almost never asked, so zero honest called says little. The triage saving would apply to H8 as well (H8 with a list of 4 was not run).
