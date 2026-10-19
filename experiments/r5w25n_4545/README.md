# r5w25n_4545

v2 data, the full pipeline with the AI step (workflow v2.2 summaries: rules 2.2). release 5 evaluation (issue 109): seed 4545, 216 doctors, 8 planted upcoders, half clone notes, data 2.2 defaults; workflow W2.5 API-free.

- Screen from `experiments/r5_4545/` (`flagged_threshold.csv`); records request in `documentation.csv` and `records_requests.csv`.
- Summaries: obvious cases decided and written by rules (`src/summary_rules.py`), the rest by Claude Opus 5.5 through the Batch API (headline, leaning and interpretation only). Each record says which (`source`) and what the rule said (`rule_leaning`).
- Judge: no LLM usefulness judge (release 2 uses the deterministic rule judge only, `usefulness_rules.jsonl`).
- Cost: `usage_writer.jsonl` and `usage_judge.jsonl` (estimated from list prices, batch at half). Answer key: `eval/answer_key/ground_truth_v2_r5_4545.json` (gitignored).
