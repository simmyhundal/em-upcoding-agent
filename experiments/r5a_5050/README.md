# r5a_5050

The investigator agent v3.5 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `r5_5050`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 22 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "r5a_5050",
 "version": "3.5",
 "screen_run": "r5_5050",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 22,
 "estimated_usd": 0.2412,
 "providers_with_findings": 10,
 "providers_called_upcoding": 4,
 "upcoders_found": 3,
 "honest_called_upcoding": 1,
 "upcoders_total": 8,
 "records_requests_to_honest": 5,
 "records_requests_total": 10,
 "rounds_on_honest": 7,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_r5_5050.json` (gitignored). Frozen workflow baseline: `v2.0`.
