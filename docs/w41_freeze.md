# Workflow v4.1 (W4.1): the freeze and the test declared before it is run

[Back to the README](../README.md) · [the v4.1 loop](w_loop_v41.md) · [confirmations and the control](w_loop_v41_confirm.md) · [ceiling benchmarks](ceiling_benchmarks_w41.md)

Declared 2026-10-22, before any run on the test seeds. Score S4.0, data D4.0. Free (no model calls).

## What is frozen
**W4.1 = H23 at N = 4**, exactly as `eval/w_loop.py` defines it (`VERSIONS["H23_n4"]`): workflow v4.0's pipeline (`eb_upper_t` ranking, the ask model `src/policy_40_ask.json`, 30 random charts, no escalation, demand floor at the cost of a demand) with H17's loosened chart test (at least 5 documented 99214 and 99215 charts, unsupported share of at least 10%, alpha 0.20), H16's near-miss extension (a second random request of 30 charts for a rules-called provider whose point estimate is at least twice the demand cost while its 90% lower bound is below it), and a list of the first 4 providers, so only those are summarized and triaged. Nothing is changed after the test below. Mechanical score gains are acceptable by decision of 2026-10-22 (CLAUDE.md); the control below separates them.

## The test
- **Seeds:** the ten seeds on which workflow v4.0 and agent v5.0 were tested (5555 to 6464, step 101, data `f4_<seed>`). They were used once before, for W4.0, A5.0 and the frozen v2.5; nothing in W4.1 was chosen on them, but the W4.0 result there (−$1,161 per seed) was known while W4.1 was being designed, so they are a second test, not fresh. The second fresh pool (6565 to 7474) is untouched.
- **Arms, run once each:** W4.1; and the control **W4.0 with the same 4-provider list** (`VERSIONS["H8_n4"]`), so that the triage saved by a short list is not credited to W4.1's rules.
- **Comparisons, paired by seed:** W4.1 minus W4.0 (the stored result in `experiments/v4_fresh_results.json`), W4.1 minus the control, and each against zero. One-sided exact sign-flip permutation test (n = 10).
- **"Marked improvement" is declared as:** W4.1 beats W4.0 by at least **+$500 per seed** AND the one-sided p-value against W4.0 is below **0.05**. The comparison with the control is reported and weighs on the reading but is not part of the criterion. If W4.1 clears this, agent v5.1 is built to mirror it (its fresh run is paid: estimate and approval first). If not, the result is reported as it is and the next step is decided then.
- On the development pool W4.1 led W4.0 by about +$677 per seed on 60 hold-out seeds; the fresh result of W4.0 was about $1,700 per seed below its development result, so a W4.1 result near zero or still negative would be consistent with that gap.

Code: `eval/run_v41_fresh.py`. Results: `experiments/v41_fresh_results.json`, written after the run.
