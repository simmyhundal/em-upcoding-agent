# Experiments

Folder names follow `YYMMDD_X_Y`:
- `YYMMDD`: the date of the run.
- `X`: the run number on that day (1, 2, 3 ...).
- `Y`: how the summaries were produced: **`api`** = the project's own pipeline calling the Anthropic API; **`cc`** = mimicked through Claude Code (a chat session or fresh Claude Code agents standing in for the API call, so not a real API run); **`code`** = code only, no AI step (v2 data, screen and rules baselines).

Each folder has a README saying what the run was and what it does and does not show. Results are not directly comparable across rows unless the README says the data and providers match.

| Folder | What it was | Data |
|---|---|---|
| `261008_1_cc` | Three summaries written by hand in a chat session, from the evidence packets only | seed 42, 3 providers |
| `261008_2_cc` | One agent wrote all 25 summaries (they came out templated) | seed 42, 25 providers |
| `261008_3_cc` | One fresh agent per provider, no records evidence | seed 42, 25 providers |
| `261008_4_cc` | One fresh agent per provider, with records-review evidence | seed 42, 25 providers |
| `261009_1_api` | First real API run (Claude Opus 5.5 writer, Claude Sonnet 5.5 judge) | seed 42, 25 providers |
| `261009_2_api` | Held-out run: pipeline frozen, fresh dataset, run once | seed 101, 25 providers |
| `261012_1_code` | v2 data: screen from derived risk, records request, two rules baselines (no AI) | v2 seed 42, 216 providers, half the upcoders clone notes |
| `261012_2_code` | Same, held-out seed (rule thresholds frozen from seed 42) | v2 seed 101, 216 providers |
| `261012_8_api` | v2 data with the AI step (rules plus Claude Opus 5.5 via the Batch API, judge Sonnet 5.5): screen from `261012_1_code` | v2 seed 42, half clone notes |
| `261012_9_api` | Same, held-out seed (screen from `261012_2_code`) | v2 seed 101 |
| `261012_10_api` / `_11_api` | Same, nobody clones notes / every upcoder clones (screens from `261012_6_code`, `_7_code`) | v2 seed 42 |
| `261012_15_api` to `_18_api` | Records-request sample-size sweep with the AI step: 10, 20, 60 and 100 charts per flagged provider (30 is `261012_8_api`); see `docs/sample_size_sweep.md` | v2 seed 42 |
| `261012_12_api` / `_13_` / `_14_` | Base-rate sweep with the AI step: 0.5%, 1%, 2% upcoders (screens and rules from `261012_3_code`, `_4_`, `_5_`) | v2 seed 7, 600 providers |
| `261012_6_code` / `_7_` | Cloned-notes sweep: nobody clones, everybody clones | v2 seed 42, 216 providers |

Each run folder is self-contained: its summaries and scores plus (built by `src/finalize_run.py`) `cases/`, `charts/` and `pi_packets/`, so a later run never overwrites them. The eval report for the main runs is `reports/eval_report.md`; `reports/charts` and `reports/pi_packets` are only the latest default output.

| `261013_1_code` / `_2_code` | Fixed-policy workflow against the simulated provider office (no AI) | v2 seed 42 / seed 101 |
