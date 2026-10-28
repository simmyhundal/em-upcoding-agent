# Workflow v4.3 (W4.3) and agent v5.3: freeze declaration

[Back to the README](../README.md) · [loop results](w_loop_v43.md) · [score 4.3](score_43.md) · [process](process.md) · [seeds](seeds.md)

Written 2026-10-28, **before** any run on the confirm pool. This page lists what is frozen, what will be run on which seeds, and what counts as passing.

## What is frozen
Workflow v4.3 is `H33` in `eval/w_loop_43.py`: workflow v4.1 (`H23_n4`, list of 4 providers) with its ask-or-skip model refitted under score 4.3 prices on data 4.3 development batches 1 to 4 (`experiments/w_loop_43/ask_model43_b1to4.json`, ridge on the features of `policy_40.ask_vector_41`) and the demand floor `cost43` (the break-even rule uses score 4.3's collected value). No volume lane. The agent line is agent v5.3: the agent v5.2 tools with the gate of `docs/evaluation_modes.md` mirroring workflow v4.3, run as two arms declared together: **A5.3-O** (Claude Opus 5.5) and **A5.3-S** (Claude Sonnet 5.5), each at the same prompt, caps and a $1 cap per run.

## What was tried (the Bonferroni count)
Seven hypotheses on development batches 1 to 4: H29, H30, H31, H32 (the lane variants), H33, H34 and the margin sweep (one family). The bar is 0.05 / 7 = 0.007. H33 was read out of sample on batches 5 to 10 (role *confirm*): +$701 per seed over workflow v4.1 on 55 of 60 seeds, p below 0.001, and no better than asking nobody (-$13, p = 0.50).

## What will be run, once
On the confirm pool (data 4.3, seeds 1004 + 41j, j = 0 to 99, role *confirm*, built, never run): W4.3 (`H33`), workflow v4.1 (`W41`) and workflow v4.2 (`W42`) as references, and the ask-nobody control (`H0`). All free and API-free. Score 4.3 is primary.
Then, once, on the test pool (data 4.3, seeds 6003 + 41j, j = 0 to 9, never generated before this declaration): W4.3 free; **A5.3-O and A5.3-S paid**, one run per seed, at most $1 each. Estimate before spending: about $1.8 for A5.3-O and $0.9 for A5.3-S; release cap $4.

## Passing
On the confirm pool W4.3 passes if both hold:
1. W4.3 minus workflow v4.1 is at least **+$400 per seed** with a one-sided permutation p below **0.007**.
2. W4.3 is reported against the control: the score minus H0 is stated beside it, and if it is not above zero the result is described as a saving, not a recovery.

## What it cannot show
The gain over W4.1 is mostly not asking. It does not show the product recovers more than it costs on data 4.3: the oracle under score 4.3 is about $1.6k per seed and the control that asks nobody is -$52. Nothing here tests real claims.
