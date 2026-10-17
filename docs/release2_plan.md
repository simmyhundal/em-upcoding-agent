# Release 2 evaluation plan (proposal)

[Back to the README](../README.md)

Status: **proposal, nothing run.** No paid run starts, and no seed above 1414 is generated, until Simmy approves this plan and the cap on the evaluation issue. Decisions already made: `eb_ratio` and
`priority` are the release 2 candidate screens for both streams ([screen_methods.md](screen_methods.md)); some runs use data with defects ([data_v2_2.md](data_v2_2.md#defect-profiles-for-the-evaluation-runs-with-defects)).

## What is wired (all free, tested offline)
| Piece | Workflow v2.2 | Agent v3.2 |
|---|---|---|
| Screen | `flagging.py --method eb_ratio` or `priority` (top 25); `make_v2_runs.run(screens=("eb_ratio", "priority"))` writes `flagged_<method>.csv`; arms send records to that list | `screen_providers(method="eb_ratio")` and `method="priority"` (unrounded, the same scores), `riskadj` still the default |
| Office and summaries | office 2.1, the fixed v2.1 policy, v2.1 summaries (unchanged) | office 2.1, note tools, lint (unchanged) |
| Data quality | pre-flight, the data caveat on affected summaries, an upcoding leaning without 8 charts becomes inconclusive (`ai.run(preflight=True)`) | `data_quality`, `flag_data_issue`, hold in `submit_findings` |

Not exercised live: `ai.run(preflight=True)` and the v3.2 prompt have only offline tests; the first paid run is their first real use, so the first dataset should be a single-seed smoke run.

## Arms (per dataset, same data and seed)
| Arm | What | Approx. cost per dataset (from #61) |
|---|---|---|
| W2.1 | workflow v2.1, `riskadj` threshold 5 (the control) | $0.19 |
| W2.2-eb, W2.2-pri | workflow v2.2 with `eb_ratio`, with `priority` (top 25) | $0.19 each |
| A3.1 | agent v3.1 (the control) | $0.53 |
| A3.2-eb, A3.2-pri | agent v3.2, task text names the same default method | $0.53 each (the agent chooses its own cutoff; the default method is only its starting point) |

About $2.2 for six arms per 216-doctor dataset (600-doctor datasets cost somewhat more per arm). The v3.2 agent may choose any screen; the plan fixes only its default and records which it used.

## Datasets (proposed seeds named here, generated only after approval)
| Group | Datasets | Notes |
|---|---|---|
| Clean, 3.7% upcoders | 10 fresh seeds, proposed 1515, 1616, 1717, 1818, 1919, 2020, 2121, 2222, 2323, 2424 | data 2.2 default noise, group billing, corrections |
| Low base rate | 3 datasets at 0.5%, 1%, 2% (600 doctors), proposed seed 2525 | descriptive only, as in #61 |
| With defects | the same seeds as 4 of the clean ones (1515, 1616: `moderate`; 1717, 1818: `severe`), each paired with its clean twin | the same claims, defects added, so the difference is the defects |
| Noise sensitivity (free, code only) | the clean seeds regenerated with `honest_miscode_rate` 0.05 and 0.15 | screens only, to see how the ranking metrics move |

Estimated spend: 10 clean seeds about $22, three low-base-rate datasets about $9, four defect datasets about $9, so **about $40 to $45 for the whole set** (about 100 arm-runs, roughly $0.43 each on average), not per run. Measured from the release 1 run folders, one workflow arm on one dataset is about $0.25 ($0.14 writer, $0.11 judge) and one agent arm about $0.55 ($0.43 run, $0.12 judge). A single smoke dataset with all six arms is about $2.40. The free screen-only work costs nothing.

**This full set is too expensive to run as is.** Lowering it is tracked in [#90](https://github.com/simmyhundal/em-upcoding-agent/issues/90) (evaluation design: decide the screen for free, agent arms for one candidate only, sequential seeds, fewer defect twins), [#91](https://github.com/simmyhundal/em-upcoding-agent/issues/91) (workflow arms: shared cache, judge on a sample) and [#92](https://github.com/simmyhundal/em-upcoding-agent/issues/92) (agent arms: cheaper model or effort, smaller tool results, caps). Combined, a lean plan is roughly $10 to $12 (my estimate from the measured per-arm costs; the savings from #91 and #92 are not yet measured). The cap on the evaluation issue is set only after those are decided.

## Free comparison after the live runs: new screens against the originals
On every fresh dataset (clean, low base rate, defect twins) and on the 14 release-1 datasets, score `zscore`, `riskadj`, `priority` and `eb_ratio` with `eval/screen_methods_eval.py`: upcoders in the top 25,
honest doctors in the top 25 (hard negatives and ordinary separately), AUPRC, precision at 10 and 25, recall at a longer list, by upcoder tier. `docs/screen_metrics.md` already reports the first four on the
release-1 data. The 14 release-1 datasets are development data now; only the fresh seeds can confirm a choice.

## Decision rules (proposed, to be fixed on the issue before any run)
1. **Screen:** adopt a candidate as the default screen if, over the 10 clean fresh seeds, its paired difference in upcoders found in the top 25 against `riskadj` has a 95% interval above zero **and** it puts no more honest doctors in the top 25 in total. If both candidates qualify, take the one with the higher AUPRC; if neither qualifies, `riskadj` stays.
2. **Streams:** compare W2.2 against W2.1 and A3.2 against A3.1 on upcoders found and honest doctors accused, paired by seed, with the same 95% intervals as #61; report records burden (honest practices asked, request rounds) next to it. No claim of improvement from a single seed or a one-doctor gap.
3. **Defects:** on defect twins report, per arm, upcoders found, honest doctors accused, and findings held by the data-quality hold; the question is whether held findings protect against false accusations without losing upcoders, so the loss must be shown, not assumed.
4. **Honesty:** results state what is easier by construction (billed level depends on patient complexity; the answer-key labels come from the generator) and what only a few seeds show. The upcoder definition ([data_v2_2.md](data_v2_2.md#a-proposed-upcoder-definition-not-built-awaiting-simmys-decision)) must be settled before any seed is generated.

## What needs a decision before anything runs
- The upcoder definition (margin as built, or the planted-pattern definition proposed).
- The spending cap and the seed list.
- Whether the agent arms get a fixed default method or are left free (proposed: default stated in the task text, free to change, reported).
