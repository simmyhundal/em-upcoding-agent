# 261013_11_api

The investigator agent (`src/agent.py`, model claude-opus-5-5) on the v2 data of `261013_5_code`, WITHOUT the statistical screen tool. Caps: $3.00, 60 tool calls, records for at most 15 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "261013_11_api",
 "screen_run": "261013_5_code",
 "screen_tool": false,
 "stop_reason": "submitted",
 "tool_calls": 47,
 "estimated_usd": 0.3006,
 "providers_with_findings": 18,
 "providers_called_upcoding": 2,
 "upcoders_found": 2,
 "honest_called_upcoding": 0,
 "upcoders_total": 8,
 "records_requests_to_honest": 4,
 "records_requests_total": 9,
 "rounds_on_honest": 5,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_261013_5_code.json` (gitignored). Frozen workflow baseline: `v2.0`.
