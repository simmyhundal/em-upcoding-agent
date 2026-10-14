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
| `seed`, `seed_status` | The data seed, and whether it was a **development** seed (used to build and tune the workflow) **held-out** (generated or scored after those settings were frozen), or **reserved** (held back, never looked at, until the Milestone 6 evaluation). |
| `source` | `api` = the project's own pipeline calling the API; `cc` = mimicked with Claude Code agents; `code` = no model. |
| `agents` | Separate model calls or chat agents that wrote summaries, for AI rows. Summaries written by code do not count. |
| `data_version`, `data_description` | Which data model the run used and what it contains (`runs.json` holds the text). |
| `upcoder_rate` | The share of providers that are real upcoders (prevalence), with counts. "Baseline" is reserved for a comparison arm. |
| `upcoder_clone_level` | The share of upcoders whose notes are cloned to match the bill (`n/a` on version 1, which had no cloning). |
| `fn_*`, `fp_*`, `precision*`, `citations_*`, `usefulness*` | The raw numbers behind each eval and a `pass`/`fail` against its threshold (blank = not scored). |
| `usefulness_rules`, `usefulness_rules_version` | Mean score from the deterministic rule judge (`eval/judge_rules.py`; version in the second column, currently j2.2): fully deterministic, no model, 1 to 5, subtracting points for auditable defects. Informational: not one of the counted evals, and only weakly correlated with the LLM judge (Pearson about 0.22 over 374 summaries with v2.2, 0.15 with v2.1; `eval/compare_judges.py`). It measures defects, not holistic usefulness. |
| `judge_version` | Which usefulness judge scored the row: `j1` = evidence card only (all runs so far), `j2` = card plus the tool outputs the author saw. Blank when no usefulness was scored. |
| `evals_score_of_5` | Evals passed scaled to a five-point score: 5 x passed / applicable (3 of 4 becomes 3.75). Usefulness itself is always scored 1 to 5, so it needs no conversion. |
| `evals_passed`, `evals_applicable` | Evals passed and the denominator, how many evals applied to the row (the README shows them as "Evals passed" and "Evals scored"). Screen rows have 3; AI rows have 4, or 5 when the usefulness judge ran. Earlier tables had one more eval (templating, since removed), so old scores like 5/5 are now 4/4. |
| `honest_requested` | Honest doctors who received a records request (the burden on honest practices). Blank where the stage sent none (the screen) or where requests were not simulated (version 1). |
| `request_rounds_total`, `request_rounds_honest`, `request_rounds_called` | Request rounds (the first request plus each follow-up) in total, on honest doctors, and on providers the stage finally called upcoding. Single-draw runs count one round per provider; runs with the provider office count its transcript. Rounds after the final flag (the recovery sample) are not simulated yet (see the recovery-phase issue). |
| `overpaid_usd` | Dollars the upcoders were paid above what the justified levels would have paid (answer key; evaluation only). Uses each claim's own allowed and paid amounts on version 2; fee-schedule averages at an 80% paid share on version 1. |
| `reached_usd`, `reached_share` | The same dollars for only the upcoders that row's stage called, and that as a share of `overpaid_usd`: an upper bound on what recovery could reach, not money recovered. |
| `notes` | Free text about the run. |

Adding a run: add it to `experiments/runs.json` (dataset, source, notes, pointers to its outputs), run `python eval/scoreboard.py --write`, then `python docs/update_readme.py`.
