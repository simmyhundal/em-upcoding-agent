# r2a_1919

The investigator agent v3.2 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `r2_1919`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 15 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "r2a_1919",
 "version": "3.2",
 "screen_run": "r2_1919",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 24,
 "estimated_usd": 0.1966,
 "providers_with_findings": 10,
 "providers_called_upcoding": 2,
 "upcoders_found": 2,
 "honest_called_upcoding": 0,
 "upcoders_total": 8,
 "records_requests_to_honest": 5,
 "records_requests_total": 10,
 "rounds_on_honest": 7,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_r2_1919.json` (gitignored). Frozen workflow baseline: `v2.0`.
