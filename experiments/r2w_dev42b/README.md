# r2w_dev42b

v2 data, the full pipeline with the AI step (workflow v2.2 summaries: rules 2.2). dev seed 42 data 2.2: workflow v2.2 with the capped-peer rules.

- Screen from `experiments/261016_1_code/` (`flagged_threshold.csv`); records request in `documentation.csv` and `records_requests.csv`.
- Summaries: obvious cases decided and written by rules (`src/summary_rules.py`), the rest by Claude Opus 5.5 through the Batch API (headline, leaning and interpretation only). Each record says which (`source`) and what the rule said (`rule_leaning`).
- Judge: no LLM usefulness judge (release 2 uses the deterministic rule judge only, `usefulness_rules.jsonl`).
- Cost: `usage_writer.jsonl` and `usage_judge.jsonl` (estimated from list prices, batch at half). Answer key: `eval/answer_key/ground_truth_v2_261016_1_code.json` (gitignored).
