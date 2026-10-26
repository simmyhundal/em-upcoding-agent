# Evaluation modes: the stage a run covers and the people at both ends

[Back to the README](../README.md) · [operating model](operating_model.md) · [score 4.2](score_42.md) · issue 207

**What this page is.** Every result so far is a **full run with both human gates set to "accept all, no delay"**: the arm takes the screen's shortlist straight to records requests and its drafts straight to demands. In the product a PI team reviews the shortlist and sends the requests (gate 1), then signs off each demand (gate 2). This page describes the harness parameters that let an evaluation say how much that matters. They belong to the harness, not to the arms (`eval/eval_modes.py`). The gates are a **model of a person**, an assumption, not evidence about how teams decide.

## The parameters
| Parameter | Values | What it does |
|---|---|---|
| Stage | `screen` (score the shortlist from the screen alone: dollars of true overpayment in the first k, ranking quality), `records` (start the records stage from a given list: the screen's, the oracle's or a human-edited one), `full` | Separates what the screen does from what the records stage does. |
| Gate 1 (shortlist) | accept all (every number so far), keep the top k, a person vetoes a seeded random fraction (level list and volume-lane providers alike) | How good the screen must be if people reject part of it. |
| Gate 2 (demand sign-off) | accept all, accept a demand only if its conservative estimate is at least a figure, reject a seeded random fraction | The same question at the other end. A rejected demand is not sent: no recovery, no demand cost, the review cost stays. |

Presets: `accept_all`, `veto_30` (a person drops 30% of the lists at random), `top_2_and_signoff` (keep the top 2 of the level list and sign off demands of $1,000 or more). Delay in days is not yet a parameter: score 4.2 has no cost of time, so a delay would change nothing until a score prices it (prepay does).

## An example: workflow v4.2 on the 20 first data 4.2 development seeds
Score 4.2, dollars per seed. Free, API-free.

| Preset | Mean | Median | Seeds above zero | Demands (20 seeds) | Demands rejected |
|---|---|---|---|---|---|
| accept_all | $32,662 | $30,165 | 20 of 20 | 68 | 0 |
| veto_30 | $22,086 | $21,571 | 20 of 20 | 46 | 0 |
| top_2_and_signoff | $18,569 | $19,269 | 20 of 20 | 37 | 2 |

Reading it: when a person drops 30% of the lists at random, the mean falls by about a third, because almost all of the money is in a few large volume-lane providers and each one dropped is lost; the third preset shows the cost of a strict gate (a short level list, and demands under $1,000 not sent). These numbers say what the harness does, not how people decide. Every results row written by the harness carries its stage and gate settings.

Code: `eval/eval_modes.py` (`run_full`, `screen_only`, `table`), `eval/score_42.py` (`gate2`), `src/fwa_lane.py` (the lane's `veto_fraction`), `eval/oracle_s42.py` (`_ids`, the oracle's pursued providers for the records stage). Tests: `tests/test_eval_modes.py`.
