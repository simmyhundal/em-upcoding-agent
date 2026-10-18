# r2a_1515

The investigator agent v3.2 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `r2_1515`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 15 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "r2a_1515",
 "version": "3.2",
 "screen_run": "r2_1515",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 21,
 "estimated_usd": 0.1401,
 "providers_with_findings": 11,
 "providers_called_upcoding": 1,
 "upcoders_found": 0,
 "honest_called_upcoding": 1,
 "upcoders_total": 7,
 "records_requests_to_honest": 8,
 "records_requests_total": 11,
 "rounds_on_honest": 10,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_r2_1515.json` (gitignored). Frozen workflow baseline: `v2.0`.
