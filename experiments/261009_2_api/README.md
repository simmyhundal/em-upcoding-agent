# 261009_2_api: held-out run (seed 101, pipeline frozen, run once)

**Purpose:** the seed-42 results came from data I built and a prompt and evidence page I refined while looking at those same providers. This run checks the pipeline on a fresh dataset it had never seen, with nothing changed.

**Protocol followed**
- Everything was committed and tagged `heldout-freeze-261009` (commit `25f5ade`) before the data was generated. At the end, `src/`, `eval/` and the figure code were verified unchanged against the tag.
- Data: `python src/generate_synthetic.py data/synthetic_s101 --seed 101 --answer-key eval/answer_key/ground_truth_s101.json` (the CSVs and the answer key are gitignored and regenerate from the seed).
- Run once, in this order: screen and flagging (`baseline_zscore`, `baseline_riskadj`, `flagging`), 25 API summaries (`case_summary.py`, `claude-opus-5-5`), citation check, templating check, usefulness judge (`claude-sonnet-5-5`), `run_eval.py`. No test calls and no retries.

Files: `flagged.csv` and the two ranking files, `case_summaries.jsonl`, `case_summaries_checked.jsonl`, `usefulness.jsonl`, `eval_report.md` (full tables). Reviewer materials were built after the run with `src/finalize_run.py` (no API calls, no change to the frozen pipeline): `cases/`, `charts/`, `pi_packets/`. The simulated recovery estimates covered the true overpayment in 8 of 8 packets.

## Results (seed 101) next to seed 42
| | Seed 42 (tuned on) | Seed 101 (held out) |
|---|---|---|
| Upcoders in the top 25 (combined screen) | 8 / 8 | 8 / 8 |
| Honest providers in the top 25 | 17 (3 sicker-panel, 14 normal) | 17 (1 sicker-panel, 16 normal) |
| Upcoders called upcoding by the AI | 8 / 8 | 8 / 8 |
| Honest providers called upcoding | 0 / 17 | 0 / 17 |
| Citations valid | 261 / 261 | 278 / 278 |
| Templating | none | none |
| Usefulness (LLM judge, mean of 5; target 4) | 3.44 | 3.24 (not met) |

Seed 101 leanings: upcoders 8 upcoding; the one sicker-panel provider read as a heavy panel; normal providers 13 high-acuity panel and 3 inconclusive.

## What this does and does not show
- The result held on a fresh dataset: nothing about the headline numbers depended on having looked at seed 42's particular providers.
- It is **not** an independent test of the design. Seed 101 comes from the same generator, so the records evidence is still generated from the same hidden truth that defines an upcoded visit, and the risk adjustment still uses the variable the generator uses. A real dataset would be harder.
- One fresh seed, 25 providers, only 1 sicker-panel doctor among the flagged. Small counts.
- Usefulness is below target again, with the same kind of complaint (small numeric slips, cited claims that do not quite fit their sentences). The judge is an LLM; see issues #18 and #19.
- Cost: **$1.85** from the console. The scripts do not log usage (the freeze ruled out adding it), so this was estimated beforehand: measured input of about $0.95 (writer 150,215 tokens, judge 176,206) plus output inferred from the seed-42 bill gave about $1.86 (range $1.63 to $2.09). The close match supports the inferred output size of roughly 1,400 tokens per writer call and 850 per judge call.
