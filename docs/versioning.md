# Versions and what is frozen

| Version | What it is | Tag |
|---|---|---|
| `v1.0` | Workflow with one LLM step on version-1 synthetic data (provider, patient, claim and documentation tables). Held-out run 261009_2_api. | `v1.0` (commit 25f5ade; also `heldout-freeze-261009`) |
| `v2.0` | Version-2 workflow: plan-shaped data (`docs/v2_schemas.md`), conditions derived from claims, records requests with limits, code-written summary parts, rule-decided clear cases, Batch API, cache, number check. Runs `261012_8_api` to `261012_18_api` and the code-only runs `261012_*_code`. | `v2.0` |

| `v3.0` | The investigator **agent** design (Milestone 6): a model that chooses its own tools and steps, with a simulated provider office, guardrails, audit log, the results table (`experiments/results.csv`) and the new metrics. Runs `261013_8_api` to `261013_11_api` and the repeats `261013_16_api` to `261013_19_api`. The workflow stays in the repository frozen as `v2.0` and is the comparison arm. | `v3.0` |

A major version marks a change in what the product is (v1 to v2: the data model; v2 to v3: who decides the next step), not a claim that it performs better; on the reserved seeds the agent found fewer upcoders than the workflow.

## What "frozen" means
- Code under `src/` and `eval/` that produces the v2 results does not change except through a `v2.x` patch: a commit that says what changed and re-runs the affected scoreboard rows.
- Thresholds (screen cutoff 5, rule cutoffs in `src/summary_rules.py` and `src/records.py`) are not re-tuned on seeds 42, 101 or 7. They were set by looking at seed 42 and have been seen on all three since.
- Results from `v1.0` cannot be reproduced on current code (the prompt, packet format and checks changed); their run folders hold the outputs.

## Reserved seeds
Seeds 202 and 303 were reserved and have now been used and seen (the Milestone 6 evaluation); they are retired. Seeds 404, 505 and 606 are the new reserved seeds: not generated or looked at, for the next version's evaluation. Generate them only for that evaluation, with the settings in `eval/make_v2_runs.py`.

## Known limits carried into v2.0
- Synthetic data from one generator family; 8 upcoders per run.
- The v2 schemas (`docs/v2_schemas.md`) were written from general knowledge and have not been reviewed by someone who works with 837, 834 and 835 data (issue 32, backlog).
- The justified level is still drawn first and the MDM elements are built to fit it (issue 45 notes this).
- The AI step makes false accusations at low base rates; the screen sends only part of the upcoders on; usefulness is 3.3 to 3.7 against a target of 4.

## Reproduction
`python eval/make_v2_runs.py` rebuilds the code-only runs (checked: rebuilding run 261012_1_code reproduced the committed files exactly). `python eval/make_v2_ai_runs.py` reruns the AI step; the response caches in each run folder make unchanged runs free.

## Patches since v2.0 (no results changed)
- `summary_rules._rule_headline` crashed or mis-worded when the pooled 99214/99215 rule decided; it now states the pooled counts. Four stored headlines (runs 261012_9_api and 261012_10_api) kept their older wording; no leaning, citation or score changed (regenerated from the response cache and compared).
- `summary_rules.pick_citations` always cites something from the packet's own samples, so a rule-decided summary can no longer be rejected for citing nothing.
- `records.read_chart` was split out of `request_records` so the provider simulator reads charts the same way (outputs verified identical).
