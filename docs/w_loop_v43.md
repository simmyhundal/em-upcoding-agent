# Workflow v4.3 development loop (data 4.3, score 4.3)

[Back to the README](../README.md) · [score 4.3](score_43.md) · [decision log](decision_log.md) · [seeds](seeds.md)

The loop for the next workflow version, run on data 4.3 development seeds and scored with [score 4.3](score_43.md). Free: every version is API-free and no model is called. Runner: `eval/w_loop_43.py` (serial; the process pool deadlocked once). The bar, set by Simmy: significantly better than the previous version on the current data and score, and a mechanical gain counts if reported as one, with the control that gets the same saving.

## Versions
| Name | What it is |
|---|---|
| W41 | Workflow v4.1, the level review only (the previous version) |
| W42 | Workflow v4.2: W41 plus the volume lane |
| H29 | W41 with the demand floor at score 4.3's collected value |
| H30 to H32 | H29 plus the lane with a break-even rule, a probe, or at most 3 providers |
| D7 | Diagnostic, not a hypothesis: every listed provider is asked (the data the ask models are fitted on) |
| H33 | W41 with the ask-or-skip model refitted under score 4.3 prices on batches 1 to 4 (`eval/fit_ask_43.py`) |
| H34 | H33 with the provider's paid dollars added to the ask model |
| H0 | Control: the same list, asking nobody |

## Results on batches 1 to 4 (40 seeds, fit seeds for the ask models)
| Version | S4.3 per seed |
|---|---|
| W42 | -$5,632 |
| D7 | -$5,212 |
| W41 | -$652 |
| H29 | -$1,181 (20 seeds) |
| H30 / H31 / H32 | -$4,190 / -$2,914 / -$2,196 (20 seeds) |
| H0 | -$52 |
| H33 / H34 | +$264 |

One seed (2438, one provider worth $19,119) carries the H33 mean; every arm finds it, H33 with 29 charts against W41's 89. Without it H33 is -$203 per seed. 
## Held-out read: batches 5 to 10 (60 seeds the ask model never saw, role *confirm* for H33)
| Version | S4.3 per seed | Median | Mean without the best seed | Seeds above zero | Charts per seed |
|---|---|---|---|---|---|
| W41 | -$767 | -$944 | -$855 | 6 | 90 |
| H0, ask nobody | -$52 | -$52 | -$52 | 0 | 0 |
| H33 | -$66 | -$52 | -$155 | 3 | 12 |
| H34 | -$66 | -$52 | -$155 | 3 | 12 |

- H33 beats the previous version W41 by **+$701 per seed**, on 55 of 60 seeds (one-sided permutation p below 0.001).
- It is a **mechanical gain**: it asks for 12 charts per seed against 90, and the saving is mostly in not asking. The control is H0: H33 minus H0 is -$13 per seed (p = 0.50), so H33 is no better than asking nobody. The product's value under score 4.3 on this data is that it does not lose money by chasing; the money is in rare large providers.
- H34 (paid-dollar features) made the same decisions as H33 and is dropped.

## Margin sweep (batches 1 to 4)
Asking more than the model recommends makes it worse: a margin of -100, -250, -500 and -1000 dollars scored +$149, -$230, -$593 and -$603 per seed, against +$264 at 0 (H33). The model's own margin stays.

## Choice
Workflow v4.3 is H33: workflow v4.1 with the ask-or-skip model of `experiments/w_loop_43/ask_model43_b1to4.json` and the demand floor of score 4.3 (`cost43`), no volume lane. Under score 4.3 every lane variant (H30 to H32) lost money on data 4.3 because the busiest-day signal flags almost only honest providers (about 2% of flagged providers are right), so the lane stays out of v4.3; see `docs/w_loop_v43.md` rows above. Freeze declaration: [w43_freeze.md](w43_freeze.md).

