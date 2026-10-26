# Versions and what is frozen

[Back to the README](../README.md) · [feature parity](feature_parity.md) · [release notes](releases/) · [seeds](seeds.md) · [patches to frozen versions](frozen_patches.md) · [glossary](glossary.md)

**What this page is.** Which versions of the project exist, what each one pairs with, and what "frozen" means. It lists versions in the order they were built. What each version changed is in its [release notes](releases/); what each stream built is in [feature parity](feature_parity.md).

## How versions are named
Four things carry version numbers, each on its own track:
- **Workflow** (code fixes the order of the steps): `v1.x`, `v2.x`, `v4.x`.
- **Agent** (a model chooses its own steps within caps): `v3.x`, `v5.x`.
- **Data** (the generator, schemas and simulated provider office): `1`, `2.0`, `2.1`, `2.2`, `4.0`, `4.2`.
- **Score** (how a run is judged): `evals`, `points`, `2.5`, `4.0`, `4.1`, `4.2`.

Short names used in tables and issues: **W4.2** is workflow v4.2, **A5.2** agent v5.2, **D4.2** data 4.2, **S4.2** score 4.2.

The major number says what the thing is, not that it performs better: workflow v1 to v2 changed the data model, v2 to v3 changed who decides the next step (the agent), and the v4 and v5 line began with dollars as the score and a data model with provider upcoding rates. The minor number is **shared** within a line: workflow v2.Y pairs with agent v3.Y, workflow v4.Y with agent v5.Y, and a pair is evaluated together on the same fresh seeds. Data and score move on their own track, so a pair can reuse the previous data (v2.3 to v2.5 and v3.3 to v3.5 ran on data 2.2; v4.1 and v5.1 on data 4.0).

## Versions at a glance
| Workflow | Agent | Data | Score | What it is | Results |
|---|---|---|---|---|---|
| `v1.0` | | 1 | evals | One model step on version-1 tables; a records sample handed over up front. | [v1.0](releases/v1.0.md) |
| `v2.0` | `v3.0` | 2.0 | evals | Plan-shaped data, conditions derived from claims, charts only on request; the agent chooses its own tools. | [v2.0](releases/v2.0.md), [v3.0](releases/v3.0.md) |
| `v2.1` | `v3.1` | 2.1 | evals | Note package (signatures, orders, results), a second request, the summary lint. | [eval61.md](eval61.md) |
| `v2.2` | `v3.2` | 2.2 | evals | Honest coding noise, group billing, truncated diagnoses, injected data defects; data-quality pre-flight. | [release2_results.md](release2_results.md) |
| `v2.3` | `v3.3` | 2.2 | evals | Cloned-notes detection, `eb_ratio_t` screen, a wider list with a light tier. | [release3_results.md](release3_results.md) |
| `v2.4` | `v3.4` | 2.2 | points | A narrower list, a learned stop-or-escalate, the advisor tool. | [release4_results.md](release4_results.md) |
| `v2.5` | `v3.5` | 2.2 | dollars (2.5) | API-free workflow; advice inside the agent's tool results; dollars as the primary score. | [release5_results.md](release5_results.md) |
| `v4.0` | `v5.0` | 4.0 | 4.0 | Provider upcoding rates and habits; the `eb_upper_t` screen; a request recommendation fitted on score 4.0; break-even rule. | [v4_v5_results.md](v4_v5_results.md) |
| `v4.1` | `v5.1` | 4.0 | 4.0 | A list of 4, a looser chart test, one second sample for borderline cases. | [w41_fresh_result.md](w41_fresh_result.md), [a51_fresh_result.md](a51_fresh_result.md) |
| `v4.2` | `v5.2` | 4.2 | 4.2 | No planted upcoder; fraud as well; the claims-data lane (visits per day). | [v42_test_result.md](v42_test_result.md) |

Every row has a tag with the version's name (`v4.2`, `v5.2`, and so on) and notes in [releases/](releases/). The README table puts v4.0 to v5.2 on one score ([score 4.2](score_42.md)) beside the oracle of each data set.

## Data versions
| Data | What it adds | Document |
|---|---|---|
| 1 | Provider, patient and claim tables with a stored condition count. | [archive](archive-version-1.md) |
| 2.0 | Plan-shaped tables; conditions derived from claims; a visit's level from the three MDM elements (the second highest) or minutes; charts only by request; some upcoders clone notes. | [v2_schemas.md](v2_schemas.md) |
| 2.1 | A templated note package: signatures, orders and results, an audit trail, tunable clone signs. | [data_v2_1.md](data_v2_1.md) |
| 2.2 | Honest coding noise (an upcoder is billing above the honest baseline by a margin), group and incident-to billing, truncated diagnoses, claims lag, level-changing corrections, injected defects. | [data_v2_2.md](data_v2_2.md) |
| 4.0 | Every provider has a net upcoding rate; exactly 8 upcoders per dataset at 15% to 40% with one of three habits. | [data_v4_0.md](data_v4_0.md) |
| 4.2 | No planted upcoder: a continuous true rate for everyone, plus fraud, waste and abuse (visits never rendered, impossible days, unbundling) and office 4.2. | [data_v4_2.md](data_v4_2.md) |

## Score versions
| Score | What it counts | Document |
|---|---|---|
| evals | Recall, false accusations, citations, usefulness against thresholds. | [results-and-evaluation.md](results-and-evaluation.md) |
| points | +1 per upcoder found, -1 per honest provider flagged, -0.05 per extra round to an honest provider. | [release4_results.md](release4_results.md) |
| 2.5 (dollars) | The overpayment a records sample supports (90% lower bound) minus request and false-accusation costs. | [release5_dollar_baseline.md](release5_dollar_baseline.md) |
| 4.0 | Recovery minus staff-hours cost minus provider abrasion. | [score_40.md](score_40.md) |
| 4.1 | Score 4.0 with plan-type profiles (copy fee $0 for commercial). | [score_41.md](score_41.md) |
| 4.2 | Score 4.1's commercial profile, records not provided counted as overpaid, stratified recovery, abrasion on the total true rate. | [score_42.md](score_42.md) |

## Judge versions
Judges are named after the version they belong to. `j1`: LLM judge on the evidence card. `j2`: LLM judge plus the tool outputs the author saw. `j2.1` to `j2.3`: the deterministic rule judge (`eval/judge_rules.py`), release 1. **`j3.2`: the rule judge of release 2** (data 2.2, workflow v2.2, agent v3.2), built in [#93](https://github.com/simmyhundal/em-upcoding-agent/issues/93) as `eval/judge_rules_32.py` (`judge_rules.py` stays j2.3, unchanged): its own evidence tiers instead of the writer's rule, citation support, dollar honesty, the note package in the packet, and a reviewer checklist beside the score ([rule_judge_32.md](rule_judge_32.md)); the release 2 evaluation uses it as its only usefulness judge. Not yet checked against a person ([human_spot_check.md](human_spot_check.md)). **`j3.3`: the rule judge of release 3** (`eval/judge_rules_33.py`, built on j3.2 and leaving it unchanged): j3.2 deducted 1.5 from every upcoding call resting on cloned-notes signs with supportive charts, the case release 3 added, so j3.3 adds a "cloning signs" evidence tier ([judge_release3.md](judge_release3.md)). A judge version never changes after it is used: a change ships as a new version, and `experiments/results.csv` records the version beside each score.

## What "frozen" means
- A frozen version's behavior lives behind its version flag (`Office(version="2.1")`, `Environment(version="5.1")`, `case_summary.py --v21`, data `--data-version 2.1`). New work adds new flags and leaves the frozen paths alone, so a frozen version still reproduces from its response cache.
- A tagged version is never edited. A small fix to code a frozen version runs is allowed only if every recorded result is unchanged (checked by regenerating or replaying); each one is listed in [frozen_patches.md](frozen_patches.md).
- Thresholds were not re-tuned on seeds that were used to set them or that were seen afterwards: see [seeds.md](seeds.md) for which seeds were fitted, selected, confirmed or tested for each arm.
- Results from `v1.0` cannot be reproduced on current code (the prompt, packet format and checks changed); their run folders hold the outputs.

## Seeds
[seeds.md](seeds.md), generated from `experiments/seed_registry.json`, names every pool by data version and seed list and records what was fitted, selected, confirmed and tested on it. A seed that anything was tuned on is never reported as held out.

## Reproduction
`python eval/make_v2_runs.py` rebuilds the code-only runs; `python eval/make_v2_ai_runs.py` reruns the AI step (the response caches in each run folder make unchanged runs free). Later versions reproduce from their own scripts, named in their release notes.
