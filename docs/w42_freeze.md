# Workflow v4.2 (W4.2): freeze declaration

[Back to the README](../README.md) · [loop results](w_loop_v42.md) · [score 4.2](score_42.md) · [process](process.md) · [seeds](seeds.md)

Written 2026-10-23, **before** any run on the confirm pool. What this page is: the list of what is frozen, what will be run on which seeds, and what counts as passing, so the result cannot be read to fit.

## What is frozen
Workflow v4.2 is `H28` in `eval/w_loop_42.py`: workflow v4.1 (`H23` at a list of 4) plus the [claims-data lane](concepts/volume-screen.md) of `src/fwa_lane.py`: flag a provider with 30 or more visits on one service date (`day_max` 30), draw a [stratified random sample](concepts/stratified-sample.md) of 30 of its claims on those dates, request the charts through the data 4.2 office (one follow-up on a fixable deficiency, then up to three more while the office has given nothing usable), price the sample with [score 4.2](score_42.md) (a visit the office has no record of counts as overpaid, [records not provided](concepts/records-not-provided.md)), and send a demand only when the [conservative estimate](concepts/conservative-estimate.md) covers the cost of a demand ([break-even rule](concepts/break-even-rule.md)). At most 10 providers go through the lane. Nothing else changed from workflow v4.1.

## What was tried (the Bonferroni count)
Five hypotheses on development batches 1 to 4 (40 seeds, role *select*): H24 the lane; H25 and H26 the lane with a list of 3 and of 2; H27 the lane with a sample of 20; H28 the lane that keeps following up while the office has given nothing usable (H24 plus up to three more follow-ups; 31 of the 123 impossible-day providers in H24 returned nothing usable). The bar is 0.05 / 5 = 0.01. H24 (p < 0.0001 against workflow v4.1) and H28 (p = 0.0042 against H24; better on 9 of 40 seeds, the gain comes from a few large providers) passed it; H25 to H27 did not and are not part of W4.2. W4.2 is H28. The lane's volume cap (30) was fixed from the first five seeds before any scoring and checked on the 100 development seeds from claims alone (`docs/w_loop_v42.md`).

## What will be run, once
On the confirm pool (data 4.2, seeds 1002 + 37j, j = 0 to 99, role *confirm*, built, never run): W4.2 (`H28`), workflow v4.1 (`H23_n4`) as the paired reference, and the do-nothing arm (zero). Both are free and API-free. Score 4.2 is primary; score 4.0 through the adapter is reported beside it. Because data 4.2 has no earlier test seeds, this run is also the final development run of process step 4.

## Passing
W4.2 passes if all of these hold on the confirm pool:
1. W4.2 minus workflow v4.1 is at least **+$500 per seed** with a one-sided permutation p below **0.0125**.
2. The lane sends a demand to at least **70%** of the providers with impossible-day billing (the 70% reflects offices that never answer; 82% on batches 1 to 4).
3. The lane takes **no more than 0.5 providers per seed** that have no impossible-day billing (0 of 123 on batches 1 to 4).

## What it cannot show
The volume signal is **clean by construction** in this synthetic data: on the 100 development seeds the busiest honest day is at most 26 visits and every impossible-days provider's busiest day is at least 33. A pass shows the lane works when the signal is that clean and the office behaves as simulated. It does not show real claims separate that cleanly. The claim-level fraud kind of billing for visits that never happened, spread across ghost members, is not reachable by this lane (no volume signal separates it in the data).
