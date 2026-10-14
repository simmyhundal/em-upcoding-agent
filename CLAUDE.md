# CLAUDE.md: start here

Proof of concept that finds likely **E/M upcoding** (billing office-visit codes 99211-99215 higher than the visit justified) on **synthetic** Medicare-style claims. Read `README.md` first (plain English, with figures), then this file. The user keeps the work organized as GitHub issues grouped in milestones; follow that.

## What the system is (get this framing right)
Statistics screen, the AI filters and explains, code checks the AI, people decide. It is a **workflow with one LLM step**, not an autonomous agent: code controls the flow, the model gets no tools and is called at most once per flagged provider.
1. `baseline_zscore.py`, `baseline_riskadj.py`, `flagging.py`: the statistical screen. Flags the top 25 (default) or everyone at or above `--min-suspicion S`.
2. `case_summary.py` (with `summary_rules.py`): rules decide lopsided cases and write the summary by code; for the rest one model call per provider. The model reads a compact evidence card and returns a headline, an interpretation and an advisory **leaning** (upcoding / high-acuity panel / inconclusive). **The leaning is the second filter**: providers it calls upcoding are the suspected upcoders and the only ones that get recovery packets.
3. `guardrail.py`: rejects summaries citing claims that do not exist or belong to another provider. It does NOT check that a cited claim supports the sentence citing it.
4. `evidence_chart.py`, `case_report.py`, `pi_packet.py`, `pi_estimate.py`, `finalize_run.py`: reviewer materials and the Payment Integrity packet. Draft material for humans; never letters, findings or accusations.
5. `eval/`: scores everything against an answer key (`run_eval.py`, `scoreboard.py`, `judge_usefulness.py`, `numcheck.py`, `threshold_sweep.py`).

**Known big limitation (state it, never hide it):** the AI is given a records-review sample (`documentation.csv`) before it decides. A real payer has only claims at screening time; records arrive after it requests them from the physician. Without that sample the AI accused 14 of 17 honest doctors; with it, 0 of 17. Results are therefore a ceiling. Version 2 data (`src/generate_v2.py`, `src/derive.py`, `src/records.py`, `docs/v2_schemas.md`) models records requests realistically; the AI has not yet been re-run on it.

## Run, test, regenerate
```bash
for t in tests/test_*.py; do python3 $t >/dev/null 2>&1 && echo ok $t || echo FAIL $t; done   # no pytest installed; tests are plain scripts
python3 eval/scoreboard.py --write     # recompute experiments/results.csv (the source of truth for results) from saved outputs; needs the answer keys
python3 docs/update_readme.py          # render the README scoreboard from results.csv and refresh the roadmap (test fails if stale)
python3 docs/make_figures.py           # rebuild README figures from saved outputs
# gitignored data and answer keys, regenerate from seeds (needed by eval code and some tests):
python3 src/generate_synthetic.py data/synthetic --seed 42
python3 src/generate_synthetic.py data/synthetic_s101 --seed 101 --answer-key eval/answer_key/ground_truth_s101.json
python3 src/finalize_run.py RUN_DIR DATA_DIR FLAGGED_CSV CHECKED_SUMMARIES   # charts/, cases/, pi_packets/ inside a run folder
```
Full pipeline for a run: generate data, `flagging.py`, `case_summary.py` (API), `guardrail.py`, `judge_usefulness.py` (API), `run_eval.py`, `finalize_run.py`.

## Rules that matter
- **Answer key is eval-only.** `eval/answer_key/` is gitignored and outside `data/`. Only `eval/` code may read it. Never put roles, "justified" levels or labels in anything an agent or the model sees; tests check this.
- **Money and keys.** Model calls go through the Batch API by default (half price) with a response cache under each run folder, and token usage plus estimated dollars are written next to the outputs (`usage_writer.jsonl`, `usage_judge.jsonl`). Code writes the numeric facts, cited claims and next steps, and decides obvious leanings by rule (`src/summary_rules.py`); the model sees a compact card and writes only a headline, a leaning and an interpretation for ambiguous cases. Run `python src/case_summary.py ... --estimate` first (token counting is free) and expect roughly $0.15 to $0.30 for a v2 writer run; the older v1 runs cost about $2. Do not start paid runs without the user's OK. The key is in `.env` (gitignored): never print, log, commit or ask for it; do not paste keys into chat.
- **Be honest in outputs.** Report misses (usefulness is below its 4.0 target), say what is easier by construction (the documentation signal is generated from the same hidden truth that defines an upcoded visit), and say what is simulated. Do not tune a run after seeing it and then call it held out.
- **Experiments are named `YYMMDD_X_Y`** (date, run number that day, `api` = the real pipeline, `cc` = mimicked with Claude Code agents). Each run folder is self-contained and never overwritten; `experiments/README.md` has the index, `experiments/runs.json` registers runs and `experiments/results.csv` holds their results (`docs/results_table.md`). The held-out run used tag `heldout-freeze-261009`.
- **Work through issues.** One issue per change, tied to a milestone, closed from the commit message (`Closes #N`). End every commit with `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. Commit and push only when asked or when the pattern in the conversation clearly calls for it.
- **Scoreboard thresholds** (README "Eval"): false negative rate and false positive rate at most 12.5% (false positive rate counts honest doctors a step actually faced), precision of "upcoding" calls at least 80% (proposed), citations 100%, usefulness at least 4. Templated or code-written summary text is fine (the templating check was removed on purpose).

## Where things are
| Path | What |
|---|---|
| `src/` | pipeline code (screen, flagging, summaries, guardrail, charts, packets); v2: `generate_v2.py`, `derive.py` (conditions and risk from claims, detector view), `records.py` (records requests, rules baselines) |
| `eval/` | harness, scoreboard, judge, rubric, number check, sweeps; `answer_key/` is gitignored |
| `data/baselines/` | small CMS-derived files (specialty mix, allowed amounts); `data/synthetic*/` gitignored |
| `experiments/` | one folder per run plus `runs.json` and an index README |
| `reports/` | latest screen and eval outputs (`flagged.csv`, `eval_report.md`), default charts and packets |
| `docs/` | `synthetic_data.md`, `payment_integrity.md`, `threshold_sweep.md`, figures and the scripts that build them |
| `tests/` | one script per area |

## Gotchas learned the hard way
- macOS: `sed -i` needs `sed -i ''`; simplest is to edit files with Python. The shell resets its working directory between calls, so use absolute paths. `python3 -I` ignores user site-packages (numpy is installed there), so do not use `-I` for pipeline scripts.
- `load_dotenv()` with no path fails in a stdin script; pass `../.env` or an explicit path.
- The installed `anthropic` SDK (0.105) rejects a `fallbacks=` keyword; `case_summary.py` passes it via `extra_body`. Opus 5.5 accepts no sampling-temperature settings, so identical re-runs need a response cache (Issue 26). Check the `claude-api` skill before changing API calls.
- No matplotlib: charts and figures are hand-written SVG. To look at one, serve the folder (`python3 -m http.server`) and open it in the browser pane; `qlmanage` thumbnails crop wide images.
- The `gh` token has no `workflow` scope, so GitHub Actions files cannot be pushed. README freshness is enforced by `tests/test_scoreboard.py` and `docs/update_readme.py` instead.
- Public CMS pages (ameli, data.cms.gov documents) may block scripted downloads; do not try to bypass bot checks.
- The CMS file hides rows with 10 or fewer patients (small-cell suppression), so real shares are biased; the generator is calibrated only to the upper tail. Issue 8 is deprioritized on purpose.

## The agent (Milestone 6)
`src/agent.py` (loop, caps, audit log), `src/agent_tools.py` (tools; payer-visible data only), `src/provider_sim.py` (simulated provider office), `eval/run_agent.py` (runs and scores one agent run; costs real money, capped at $3 by default; ask first), `docs/agent_tools.md`. The agent may never read `eval/answer_key/`; a test enforces it. The workflow baseline is `v2.0`.

## Versions (read before changing code or data)
`v1.0` is the held-out freeze of the version-1 workflow (commit 25f5ade); `v2.0` is the version-2 workflow (plan-shaped data, records requests, code-written summary parts, rules plus model); `v3.0` is the agent design on the v2 data model (the workflow stays frozen as the comparison arm). Every scoreboard row carries its code version. After `v2.0` the workflow is frozen: change it only as a `v2.x` patch that re-runs the affected rows, and never tune thresholds on the seeds already used (42, 101, 7). Seeds 202 and 303 were used in the Milestone 6 evaluation and are retired; 404, 505 and 606 are reserved, ungenerated. Details: `docs/versioning.md`.

## Two streams (v2.x workflow, v3.x agent)
Built in parallel with mirrored features; milestone "v2.1 and v3.1: parallel workflow and agent builds". Rule: a change lands in both streams or is marked one-stream-only with a reason in `docs/versioning.md`. Baselines `v2.0` and `v3.0` are frozen and never edited; evaluate new work on fresh seeds (404, 505, 606 and later) with the decision rules fixed in advance (#61); tune only on development seeds.

## Open work
Milestone 4 reduces API cost (log usage first: Issue 21). Milestone 5 is built and the AI has been run on v2 data (`eval/make_v2_runs.py` builds the code-only runs, `eval/make_v2_ai_runs.py` the AI runs, about $0.25 each); #36 (AI at low base rates) and #37 (sample-size sweep) stay open. Milestone 6 (agent) is built and evaluated once on reserved seeds 202 and 303 (README, "The agent"); open: usefulness of the agent's summaries, the recovery-phase simulation (#52), screen-tuning prompts (#48), the hybrid variants (#49). Do not re-tune on seeds 202 or 303 now that they have been seen. M6 is frozen at `v3.0`. Issues 18 and 19 improve the claim-support check and calibrate the AI grader against a person. Path A (LLM judges free-text clinical notes) is parked as Milestone 2.
