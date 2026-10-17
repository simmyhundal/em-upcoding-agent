# 261017_1_api

The investigator agent v3.2 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `261016_1_code`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 15 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "261017_1_api",
 "version": "3.2",
 "screen_run": "261016_1_code",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 46,
 "estimated_usd": 0.3981,
 "providers_with_findings": 11,
 "providers_called_upcoding": 3,
 "upcoders_found": 3,
 "honest_called_upcoding": 0,
 "upcoders_total": 8,
 "records_requests_to_honest": 5,
 "records_requests_total": 11,
 "rounds_on_honest": 6,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_261016_1_code.json` (gitignored). Frozen workflow baseline: `v2.0`.
