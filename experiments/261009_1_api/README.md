# 261009_1_api: first real API run (seed 42)

The project's own pipeline calling the Anthropic API for all 25 flagged providers:
- Case summaries: `src/case_summary.py`, `claude-opus-5-5`, effort medium, one call per provider.
- Citation check: `src/guardrail.py`. Usefulness: `eval/judge_usefulness.py`, `claude-sonnet-5-5` (a different model from the writer).

Files: `case_summaries.jsonl` (raw), `case_summaries_checked.jsonl` (after the citation check), `usefulness.jsonl` (judge scores). Reviewer materials, built by `src/finalize_run.py`: `cases/` (one readable page per provider, starting at `cases/index.md`), `charts/` (the evidence charts) and `pi_packets/` (Payment Integrity packets with a simulated worked example).

## Results
25/25 summaries passed the citation check (261/261 citations valid); no templating detected. Leanings against the answer key: 8/8 upcoders called upcoding, 3/3 hard negatives called a high-acuity panel, 0/14 normal providers called upcoding (9 high-acuity, 5 inconclusive). Usefulness (LLM judge): mean 3.44 of 5, target 4 not met. Full tables are in `reports/eval_report.md`.

## Cost (from the Anthropic console, 9 Oct 2026, UTC; this run plus the two 3-provider test runs)
| | Billed |
|---|---|
| Claude Opus 5.5 (writer) | $1.49 |
| Claude Sonnet 5.5 (judge) | $0.65 |
| **Total** | **$2.14** |

Token usage was not logged by the scripts. Measured input (token-counting endpoint): writer about 157k tokens (about $0.63), judge about 183k tokens (about $0.37). By subtraction the rest, roughly $0.8 for the writer and $0.25 for the judge, is output plus thinking tokens (an estimate, not a measurement). See the cost milestone for the plan to log and reduce this.

## Caveats
Same as the README: synthetic data, the records evidence is generated from the same hidden truth that defines an upcoded visit, and the pipeline was tuned while looking at these same providers (see `261009_2_api` for the held-out check).
