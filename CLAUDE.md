# CLAUDE.md: start here

Proof of concept that finds likely **E/M upcoding** (billing office-visit codes 99211-99215 higher than the visit justified) on **synthetic** Medicare-style claims. Read `README.md` first (plain English, with figures), then this file. The user keeps the work organized as GitHub issues grouped in milestones; follow that.

## What the system is (get this framing right)
Statistics screen, the AI filters and explains, code checks the AI, people decide. It is a **workflow with one LLM step**, not an autonomous agent: code controls the flow, the model gets no tools and is called once per flagged provider.
1. `baseline_zscore.py`, `baseline_riskadj.py`, `flagging.py`: the statistical screen. Flags the top 25 (default) or everyone at or above `--min-suspicion S`.
2. `case_summary.py`: one API call per flagged provider. The model reads an evidence packet and returns a cited summary plus an advisory **leaning** (upcoding / high-acuity panel / inconclusive). **The leaning is the second filter**: providers it calls upcoding are the suspected upcoders and the only ones that get recovery packets.
3. `guardrail.py`: rejects summaries citing claims that do not exist or belong to another provider. It does NOT check that a cited claim supports the sentence citing it.
4. `evidence_chart.py`, `case_report.py`, `pi_packet.py`, `pi_estimate.py`, `finalize_run.py`: reviewer materials and the Payment Integrity packet. Draft material for humans; never letters, findings or accusations.
5. `eval/`: scores everything against an answer key (`run_eval.py`, `scoreboard.py`, `judge_usefulness.py`, `template_check.py`, `threshold_sweep.py`).

**Known big limitation (state it, never hide it):** the AI is given a records-review sample (`documentation.csv`) before it decides. A real payer has only claims at screening time; records arrive after it requests them from the physician. Without that sample the AI accused 14 of 17 honest doctors; with it, 0 of 17. Results are therefore a ceiling. Milestone 5 rebuilds the inputs realistically.

## Run, test, regenerate
```bash
for t in tests/test_*.py; do python3 $t >/dev/null 2>&1 && echo ok $t || echo FAIL $t; done   # no pytest installed; tests are plain scripts
python3 docs/update_readme.py          # refresh the generated scoreboard and roadmap blocks in README.md (test fails if stale)
python3 docs/make_figures.py           # rebuild README figures from saved outputs
# gitignored data and answer keys, regenerate from seeds (needed by eval code and some tests):
python3 src/generate_synthetic.py data/synthetic --seed 42
python3 src/generate_synthetic.py data/synthetic_s101 --seed 101 --answer-key eval/answer_key/ground_truth_s101.json
python3 src/finalize_run.py RUN_DIR DATA_DIR FLAGGED_CSV CHECKED_SUMMARIES   # charts/, cases/, pi_packets/ inside a run folder
```
Full pipeline for a run: generate data, `flagging.py`, `case_summary.py` (API), `guardrail.py`, `judge_usefulness.py` (API), `run_eval.py`, `finalize_run.py`.

## Rules that matter
- **Answer key is eval-only.** `eval/answer_key/` is gitignored and outside `data/`. Only `eval/` code may read it. Never put roles, "justified" levels or labels in anything an agent or the model sees; tests check this.
- **Money and keys.** The API step costs about $1.85 to $2.14 per full run (25 writer calls on Opus 5.5 plus 25 judge calls on Sonnet 5.5) and takes about 6 plus 3 minutes. Do not start paid runs without the user's OK. The key is in `.env` (gitignored): never print, log, commit or ask for it; do not paste keys into chat.
- **Be honest in outputs.** Report misses (usefulness is below its 4.0 target), say what is easier by construction (the documentation signal is generated from the same hidden truth that defines an upcoded visit), and say what is simulated. Do not tune a run after seeing it and then call it held out.
- **Experiments are named `YYMMDD_X_Y`** (date, run number that day, `api` = the real pipeline, `cc` = mimicked with Claude Code agents). Each run folder is self-contained and never overwritten; `experiments/README.md` has the index, `experiments/runs.json` feeds the scoreboard. The held-out run used tag `heldout-freeze-261009`.
- **Work through issues.** One issue per change, tied to a milestone, closed from the commit message (`Closes #N`). End every commit with `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. Commit and push only when asked or when the pattern in the conversation clearly calls for it.
- **Scoreboard thresholds** (README "Eval"): false negative rate and false positive rate at most 12.5% (false positive rate counts honest doctors a step actually faced), precision of "upcoding" calls at least 80% (proposed), citations 100%, usefulness at least 4, no templating.

## Where things are
| Path | What |
|---|---|
| `src/` | pipeline code (screen, flagging, summaries, guardrail, charts, packets) |
| `eval/` | harness, scoreboard, judge, rubric, templating check, sweeps; `answer_key/` is gitignored |
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

## Open work
Milestone 4 reduces API cost (log usage first: Issue 21). Milestone 5 makes inputs realistic (v2 data model, records requests as a later step). Issues 18 and 19 improve the claim-support check and calibrate the AI grader against a person. Path A (LLM judges free-text clinical notes) is parked as Milestone 2.
