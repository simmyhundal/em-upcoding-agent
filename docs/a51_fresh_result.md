# Agent v5.1 (A5.1) on the ten test seeds: the result

[Back to the README](../README.md) · [agent v5.1](agent_v51.md) · [W4.1's result](w41_fresh_result.md) · [seed roles](seeds.md)

Score S4.0, data D4.0, seeds 5555 to 6464 (step 101; the test seeds of W4.0, A5.0 and W4.1; the agent line's second use, recorded in `experiments/seed_registry.json`). A5.1 was run once with Opus 5.5 at low effort, a $1 cap per run and a $4 batch cap (`eval/run_v51_fresh_agent.py`, approved by Simmy after the $1.7 estimate). **It cost $1.242 for the ten runs**, below the estimate. Results: `experiments/v51_fresh_results.json`.

| Arm | Score per seed | Found of 80 | Honest called | Demands | Rounds | Recovered | Staff cost |
|---|---|---|---|---|---|---|---|
| A5.0 | −781 | 3 | 0 | 3 | 45 | $3,847 | $11,440 |
| W4.0 | −1,161 | 3 | 0 | 3 | 60 | $3,792 | $15,343 |
| W4.1 | +1,003 | 9 | 0 | 9 | 64 | $26,136 | $16,106 |
| **A5.1** | **+743** | **10** | **0** | **10** | 42 | $20,972 | $13,470 |

Paired by seed (one-sided exact sign-flip permutation test, n = 10):
- **A5.1 minus A5.0: +$1,524 per seed**, better on 7 seeds, worse on 3, p = 0.0078.
- **A5.1 minus W4.1: −$260 per seed**, better on 8, worse on 2, p = 0.53. The agent and the workflow are not distinguishable; the agent found one more upcoder (10 against 9) and asked less (42 rounds against 64).
- **A5.1 minus W4.0: +$1,904**, better on 10 of 10, p = 0.0010. Against the same-list control (W4.0 with a 4-provider list): +$1,522, better on 10 of 10, p = 0.0010.
- **A5.1 against zero: +$743 per seed, p = 0.15.** Not distinguishable from zero on ten seeds.

## Reading
- **One seed carries the mean.** Seed 5959 scored +$5,002 (W4.1: +$10,549). Without it A5.1 averages about +$270 per seed across the other nine.
- **A5.1 mirrors W4.1's gain.** The same three changes (a 4-provider list, loosened chart rules, one near-miss extension) lifted the agent from 3 to 10 upcoders found with no honest provider called, as they lifted the workflow from 3 to 9.
- **Agent against workflow** stays a tie, as in every release since release 3.
- **Caveats:** these are the second-use test seeds (A5.0 was first), ten seeds, one run per seed, a real model that can ignore advice, and a scoring difference that favours the agent by about $13 per provider it does not triage. Honest providers are rarely asked, so zero called is weak evidence for the loosened rules.
