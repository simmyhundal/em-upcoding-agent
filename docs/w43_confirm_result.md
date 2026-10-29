# Workflow v4.3: the confirm read

[Back to the README](../README.md) · [freeze declaration](w43_freeze.md) · [loop](w_loop_v43.md) · [seeds](seeds.md)

Read once on 2026-10-28 on the 100 data 4.3 confirm seeds (1004 + 41j), scored with [score 4.3](score_43.md), after the [freeze declaration](w43_freeze.md) was merged. Free and API-free (`eval/run_confirm_43.py`, `experiments/w43_confirm_results.json`).

| Arm | Score 4.3 per seed | Median | Seeds above zero | Charts per seed |
|---|---|---|---|---|
| W4.3 (H33) | -$194 | -$165 | 2 | 22 |
| Workflow v4.1 | -$810 | -$1,024 | 9 | 90 |
| Workflow v4.2 | -$4,910 | -$4,466 | 2 | 302 |
| Ask nobody (control) | -$52 | -$52 | 0 | 0 |

| Paired difference | Per seed | Better on | One-sided p |
|---|---|---|---|
| W4.3 minus workflow v4.1 | +$616 | 90 of 100 | below 0.001 |
| W4.3 minus workflow v4.2 | +$4,716 | 99 of 100 | below 0.001 |
| W4.3 minus ask nobody | -$141 | 2 of 100 | 0.96 |

## Passing
1. **Pass.** W4.3 minus workflow v4.1 is +$616 per seed (bar +$400), one-sided p below 0.001 (bar 0.007).
2. **Reported, not passed.** Against the control that asks nobody, W4.3 is $141 per seed worse. The gain over the previous version is a saving (it asks for 22 charts per seed instead of 90 and no longer chases the lane), not a recovery: no version is above zero on this data.

## What it says
Under score 4.3 on data 4.3, the previous workflows lose money by asking too many providers and by sending referrals the lane cannot pay for. W4.3 loses far less. What a person should take from it: the most that could be recovered on this data is small (the oracle is about $1.6k per seed) and rests on a few large providers, so a version that asks rarely is close to the best available.
