# Results table: the source of truth

`experiments/results.csv` is the one place results live. The README table is rendered from it (`python docs/update_readme.py`); nothing in the README is recomputed or typed by hand. One row per run and stage (Screen, Rules, AI, Hybrid).

Rebuild the file from the saved run outputs and the answer keys (gitignored) with `python eval/scoreboard.py --write`. A test fails if the file is stale against those outputs (when the answer keys are present) or if the README table differs from the file.

| Column | Meaning |
|---|---|
| `run_id` | The run's id only (`YYMMDD_X_Y`, or `screen_v1_sNN` for a screen-only run). Descriptions go in `notes`. |
| `stage` | Screen, Rules (the chart rules), AI (the summary step), or Hybrid (chart rule first, then summary rules and model). |
| `tuning` | How the list was chosen at that stage. |
| `records_evidence` | Whether the stage used chart evidence (the screen never does). |
| `code_version` | `v1.0` or `v2.0` (see `docs/versioning.md`). |
| `seed`, `seed_status` | The data seed, and whether it was a **development** seed (used to build and tune the workflow) or **held-out** (generated or scored after those settings were frozen). |
| `source` | `api` = the project's own pipeline calling the API; `cc` = mimicked with Claude Code agents; `code` = no model. |
| `agents` | Separate model calls or chat agents that wrote summaries, for AI rows. Summaries written by code do not count. |
| `data_version`, `data_description` | Which data model the run used and what it contains (`runs.json` holds the text). |
| `upcoder_baseline` | The share of providers that are real upcoders, with counts. |
| `upcoder_clone_level` | The share of upcoders whose notes are cloned to match the bill (`n/a` on version 1, which had no cloning). |
| `fn_*`, `fp_*`, `precision*`, `citations_*`, `usefulness*` | The raw numbers behind each eval and a `pass`/`fail` against its threshold (blank = not scored). |
| `evals_passed`, `evals_applicable` | The count shown in the README's last column. |
| `notes` | Free text about the run. |

Adding a run: add it to `experiments/runs.json` (dataset, source, notes, pointers to its outputs), run `python eval/scoreboard.py --write`, then `python docs/update_readme.py`.
