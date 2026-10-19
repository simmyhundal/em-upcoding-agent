# r5a_5454

The investigator agent v3.5 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `r5_5454`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 22 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "r5a_5454",
 "version": "3.5",
 "screen_run": "r5_5454",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 28,
 "estimated_usd": 0.3871,
 "providers_with_findings": 12,
 "providers_called_upcoding": 5,
 "upcoders_found": 5,
 "honest_called_upcoding": 0,
 "upcoders_total": 8,
 "records_requests_to_honest": 5,
 "records_requests_total": 12,
 "rounds_on_honest": 8,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_r5_5454.json` (gitignored). Frozen workflow baseline: `v2.0`.
