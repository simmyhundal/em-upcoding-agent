# Prepay repository: copy-list

[Back to the README](../README.md) · [discovery note](prepay_discovery.md)

Draft, 2026-10-23, from source commit `23ea979` on `main`. Three groups: copy as-is, copy and adapt, build new. Not listed means not copied (the postpay-only history: releases 1 to 5, the judges, the v1/v2.x office versions, the screens' evaluation scripts, the figures). The new repository records the source commit in `LINEAGE.md` and stays free to diverge; a fix that matters to both is made twice by hand.

## 1. Copy as-is

| Path | Why |
|---|---|
| `LICENSE` | MIT, same copyright |
| `.claude/skills/run-release/SKILL.md` | The release skill; edit only the names of the arms and the score |
| `docs/process.md` | Release steps 1 to 7, who decides, `/run-release paid cap=N` |
| `docs/decision_log.md` | Keep the format; start the table empty with one row for the new repository |
| `docs/seeds.md`, `experiments/seed_registry.json` (start empty), `src/seed_registry.py`, `eval/seed_registry_report.py`, `tests/test_seed_registry.py` | Seed roles (fit, select, confirm, test, burned, fresh, reserved) and the check that refuses a reused seed |
| `docs/glossary.md` | Start from it; add pend, prompt-pay, wrongful pend |
| `tests/test_readme_sync.py` | README length cap and link check; change the cap to the new README's |
| `CLAUDE.md` | Conventions only (honesty, paid-run rule, frozen versions, answer key eval-only); rewrite the product sections |
| `.gitignore`, `.env.example` if present | Key and answer-key handling |

## 2. Copy and adapt

| Path | What changes |
|---|---|
| `src/provider_sim.py` (office 4.2 with `NO_RECORD`) | Respond to one chart request per claim with a due date; add response delay in days |
| `src/records.py` | Per-claim request and chart reading instead of a provider-level sample |
| `src/note_checks.py`, `src/notes_v21.py` | Claim-versus-note signals feed the pend decision and the chart rules |
| `src/summary_rules.py`, `src/summary_lint.py`, `src/summary_numbers.py`, `src/guardrail.py` | Facts, citations and number checks; text becomes a pend reason and a payment determination, not a case summary |
| `src/policy_40.py`, `src/policy_40_ask.json`, `eval/fit_ask_41.py` | Ask-or-skip becomes pend-or-pay; refit on per-claim features |
| `src/screen_methods_v4.py` (`eb_upper_t`), `src/derive.py` | The provider score becomes a prior on each arriving claim, updated as the stream goes |
| `src/recovery_40.py`, `src/recovery_41.py`, `eval/score_40.py`, `docs/score_40.md`, `docs/score_41.md` | Replace recovery and abrasion with the prepay score; keep the staff-hours cost structure and the assumption-plus-sensitivity style |
| `src/agent.py`, `src/agent_tools.py`, `docs/agent_tools.md` | New tools: `next_claim`, `pend`, `pay`, `adjust`, `read_chart`; keep caps, budget status and the rule that findings need support |
| `src/llm.py` | Batch API with response cache and cost log, unchanged except the model default |
| `eval/w_loop.py`, `eval/dev_pool_v42.py`, `eval/make_d42_dev.py`, `eval/run_d42_reference.py`, `eval/d42_reference_report.py` | Development loop, pool layout and reference-arm report, over a claim stream |
| `eval/metrics_d42.py`, `eval/d42_truth.py` | Per-claim truth (justified level) and metrics; add wrongful-pend and delay counts |
| `eval/release_table.py`, `docs/make_figures.py`, `docs/update_readme.py` | README results rendering and figures, once there are results |
| `tests/test_data_v42.py`, `tests/test_d40_regression.py`, `tests/test_agent_51.py` | As templates for the new data, regression hashes and agent tests |

## 3. Depend on, not copy

The data generators: `src/generate_v2.py`, `src/generate_v4.py`, `src/generate_v42.py`, `src/defects_v22.py`, `src/build_baselines.py`, `data/baselines/`, with their regression hashes (`tests/generator_hashes*.json`). Pin to a commit of this repository (a git dependency or a submodule). Copying them would fork the data, and the prepay repository's claim of "starts on D4.2" depends on D4.2 staying identical. When the prepay repository needs a claim stream with arrival and pend dates, it adds a thin layer over the generator's output, and any change that needs the generator itself goes into this repository as data 4.3 (or a prepay flag), behind a version.

## 4. Build new

| What | Notes |
|---|---|
| `src/claim_stream.py` | Arrival order and dates over a D4.2 dataset, prompt-pay deadline per claim, daily pend cap |
| `src/prepay_env.py` | The environment: next claim, pay, pend, adjust, deny; clock; office response delays |
| `src/edit_rules.py` | Point 3 baseline: claim-edit rules with no chart |
| `src/level_adjust.py` | Point 6 competitor: automatic one-level adjustment, with a wrongful-adjustment cost |
| `eval/score_prepay.py`, `docs/score_prepay.md` | Prepay score 1.0 and sources for each parameter |
| `eval/run_prepay_reference.py` | Pay-all, claim edits, workflow, agent, automatic adjustment on development seeds |
| `docs/prepay_plan.md` | Spec, as `docs/v4_v5_plan.md` was for this repository |
| `LINEAGE.md` | Source repository, commit `23ea979`, what was copied, what was changed |
| `README.md` | Short front door, same 7K cap; first line says prepay |

## 5. Order of work

1. Create the repository (name to confirm; public, MIT); add group 1; write `LINEAGE.md`.
2. Add the generator dependency; check that a D4.2 dataset builds and the hashes match.
3. Claim stream and environment; pay-all and claim-edit arms; score 1.0; seed registry with the pools declared before any run.
4. Workflow arm, then agent arm, per `docs/process.md`.
