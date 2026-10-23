# Workflow v4.2 development loop (data 4.2, score 4.2)

[Back to the README](../README.md) · [freeze declaration](w42_freeze.md) · [score 4.2](score_42.md) · [data 4.2](data_v4_2.md) · [volume screen](concepts/volume-screen.md)

**What this page is.** The record of what was tried to improve the workflow on data 4.2 before it was frozen: five hypotheses, each run on the same 40 development seeds (batches 1 to 4 of pool D4.2-DEV, role *select*) and compared in pairs, seed by seed, with a one-sided sign-flip permutation test. Numbers are score 4.2 in dollars per seed. Code: `eval/w_loop_42.py` (free, no model calls).

## Why the loop changed
Workflow v4.1 recovers a median of about nothing per seed on data 4.2 (+$694 mean, median −$68 over the 40 seeds, score 4.2). It can only recover from providers billing the wrong level, and the oracle for that kind of recovery is about $5,000 per seed. Data 4.2 also holds billing for visits that never took place: about $82,000 per dataset, of which $47,000 is on days where a provider billed an impossible number of visits. No earlier arm had a way to find or recover it.

## The claims-data lane
[Volume screen](concepts/volume-screen.md) plus a [stratified sample](concepts/stratified-sample.md) plus [records not provided](concepts/records-not-provided.md) (`src/fwa_lane.py`, `src/recovery_42.py`). Cap of 30 visits per service date, chosen from five seeds before any scoring; on all 100 development seeds the busiest honest day is at most 26 visits and the least busy impossible-days provider's busiest day is 33, so any cap from 28 to 32 flags the same 319 providers and no honest one. **That separation is built into the synthetic data; real claims will not separate this cleanly.**

## Results (40 seeds, score 4.2 per seed)
| Version | What it is | Mean | Median | Seeds above zero | Against | Difference per seed | Better on | p |
|---|---|---|---|---|---|---|---|---|
| W4.1 (`H23_n4`) | workflow v4.1 | 694 | −68 | 14 of 40 | | | | |
| H24 | W4.1 plus the lane | 28,165 | 22,248 | 38 | W4.1 | +27,470 | 37 of 40 | < 0.0001 |
| H25 | H24, list of 3 | 28,162 | 22,200 | 38 | H24 | −3 | 39 of 40 | 0.50 |
| H26 | H24, list of 2 | 28,232 | 22,241 | 39 | H24 | +67 | 38 of 40 | 0.13 |
| H27 | H24, sample of 20 claims | 27,426 | 22,322 | 38 | H24 | −739 | 7 of 40 | 0.999 |
| H28 | H24, up to 3 more follow-ups when nothing usable came back | 31,201 | 25,202 | 39 | H24 | +3,036 | 9 of 40 | 0.0042 |

Five hypotheses were tried, so the bar is 0.05 / 5 = 0.01: H24 and H28 pass; H25 to H27 do not. List size (the original issue 166) does not matter once the lane exists: the lane, not the level review, earns the money. H28 wins on only 9 of 40 seeds but the wins are large (providers whose office finally answers after a second or third follow-up).

## Where the lane stops (H24, 123 impossible-day providers on 40 seeds)
91 sent a demand; 31 returned nothing usable after one follow-up (the office never answered, or objected); 1 had a lower bound below the cost of a demand; none was missed by the screen and no provider without impossible-day billing was taken in. With H28: 101 of 123.

## What this does not show
Everything above depends on a signal the generator made clean and on simulated offices that answer or not by a fixed table. The claim-level fraud of billing for visits never rendered on ghost members is not reachable (no volume signal). Level upcoding is still weak: the older workflow's recoveries are small. The numbers measure how well a reviewer can use a clean signal, not how large the real-world volume of such fraud is.
