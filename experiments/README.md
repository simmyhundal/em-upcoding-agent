# Experiments

Folder names follow `YYMMDD_X_Y`:
- `YYMMDD`: the date of the run.
- `X`: the run number on that day (1, 2, 3 ...).
- `Y`: how the summaries were produced: **`api`** = the project's own pipeline calling the Anthropic API; **`cc`** = mimicked through Claude Code (a chat session or fresh Claude Code agents standing in for the API call, so not a real API run).

Each folder has a README saying what the run was and what it does and does not show. Results are not directly comparable across rows unless the README says the data and providers match.

| Folder | What it was | Data |
|---|---|---|
| `261008_1_cc` | Three summaries written by hand in a chat session, from the evidence packets only | seed 42, 3 providers |
| `261008_2_cc` | One agent wrote all 25 summaries (they came out templated) | seed 42, 25 providers |
| `261008_3_cc` | One fresh agent per provider, no records evidence | seed 42, 25 providers |
| `261008_4_cc` | One fresh agent per provider, with records-review evidence | seed 42, 25 providers |
| `261009_1_api` | First real API run (Claude Opus 5.5 writer, Claude Sonnet 5.5 judge) | seed 42, 25 providers |
| `261009_2_api` | Held-out run: pipeline frozen, fresh dataset, run once | seed 101, 25 providers |

Each run folder is self-contained: its summaries and scores plus (built by `src/finalize_run.py`) `cases/`, `charts/` and `pi_packets/`, so a later run never overwrites them. The eval report for the main runs is `reports/eval_report.md`; `reports/charts` and `reports/pi_packets` are only the latest default output.
