# 261015_62_api

v2 data, the full pipeline with the AI step. issue 61: fresh seed 1414, 1% upcoders (6 of 600), half clone notes; workflow 2.0 on the provider office.

- Screen from `experiments/261015_61_code/` (`flagged_threshold.csv`); records request in `documentation.csv` and `records_requests.csv`.
- Summaries: obvious cases decided and written by rules (`src/summary_rules.py`), the rest by Claude Opus 5.5 through the Batch API (headline, leaning and interpretation only). Each record says which (`source`) and what the rule said (`rule_leaning`).
- Judge: Claude Sonnet 5.5 through the Batch API, with a deterministic number check; templating is no longer checked.
- Cost: `usage_writer.jsonl` and `usage_judge.jsonl` (estimated from list prices, batch at half). Answer key: `eval/answer_key/ground_truth_v2_261015_61_code.json` (gitignored).
