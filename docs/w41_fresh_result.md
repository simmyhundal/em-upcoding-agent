# Workflow v4.1 (W4.1) on the W4.0 test seeds: the result of the test declared in docs/w41_freeze.md

[Back to the README](../README.md) · [the freeze and criteria](w41_freeze.md) · [the v4.1 loop](w_loop_v41.md) · [confirmations and the control](w_loop_v41_confirm.md)

Score S4.0, data D4.0, seeds 5555 to 6464 (step 101, ten seeds, 80 planted upcoders; the test seeds of W4.0 and A5.0, second use; see the caveat on seed roles in [issue 176](https://github.com/simmyhundal/em-upcoding-agent/issues/176)). Free, run once (`eval/run_v41_fresh.py`, results in `experiments/v41_fresh_results.json`).

| Arm | Score per seed | Found of 80 | Honest called | Demands | Rounds | Recovered | Staff cost |
|---|---|---|---|---|---|---|---|
| Frozen W2.5 | −11,185 | 1 | 3 | 4 | 478 | $44 | $93,243 |
| W4.0 | −1,161 | 3 | 0 | 3 | 60 | $3,792 | $15,343 |
| W4.0 with the same 4-provider list (control) | −779 | 3 | 0 | 3 | 52 | $3,792 | $11,586 |
| **W4.1 (H23, list of 4)** | **+1,003** | **9** | **0** | **9** | 64 | $26,136 | $16,106 |

Paired by seed (one-sided exact sign-flip permutation test, n = 10):
- **W4.1 minus W4.0: +$2,164 per seed, better on 10 of 10 seeds, p = 0.0010.** This meets the criterion declared in advance for "marked improvement" (at least +$500 per seed and p < 0.05).
- **W4.1 minus the control: +$1,782 per seed**, better on 5, worse on 2, tied on 3, p = 0.031. The control alone is +$382 per seed over W4.0 (the shorter list; better on 10 of 10).
- **W4.1 against zero: +$1,003 per seed, p = 0.27.** It is not distinguishable from zero on ten seeds.

Per seed (W4.0 / control / W4.1): 5555 −1,788 / −1,551 / −1,551; 5656 −758 / −522 / −522; 5757 −1,696 / −1,460 / +188; 5858 −2,109 / −1,412 / −1,882; 5959 −758 / −522 / +10,549; 6060 −2,644 / −1,412 / −1,882; 6161 +1,410 / +1,646 / +3,835; 6262 −1,539 / −1,303 / +1,516; 6363 −969 / −732 / +304; 6464 −762 / −526 / −526.

## Reading
- **One seed carries the mean.** Seed 5959 scored +$10,549 for W4.1 (a single large recovery). Without it W4.1 averages −$58 per seed across the other nine, against −$1,206 for W4.0 on the same nine: still ahead on every seed, but about zero, not a profit.
- **Where the gain comes from:** the looser chart rules and near-miss extension turned 3 demands into 9 (6 more upcoders found, no honest providers called) and recovery rose from $3,792 to $26,136, at about the same staff cost. The shorter list is worth a few hundred dollars per seed.
- **It is still a second look at these seeds.** W4.0's result here (−$1,161) was known while W4.1 was designed. The second fresh pool (6565 to 7474) has not been touched.
- **Honest-provider safety** remains thin: honest providers are rarely asked, so zero called is weak evidence for the loosened rules.
