# 261015_24_api

The investigator agent v3.0 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `261015_21_code`, with the statistical screen tool. Caps: $3.00, 60 tool calls, records for at most 15 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "261015_24_api",
 "version": "3.0",
 "screen_run": "261015_21_code",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 49,
 "estimated_usd": 0.3495,
 "providers_with_findings": 13,
 "providers_called_upcoding": 0,
 "upcoders_found": 0,
 "honest_called_upcoding": 0,
 "upcoders_total": 8,
 "records_requests_to_honest": 6,
 "records_requests_total": 11,
 "rounds_on_honest": 9,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_261015_21_code.json` (gitignored). Frozen workflow baseline: `v2.0`.
