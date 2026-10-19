# r4a_3636

The investigator agent v3.4 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `r4_3636`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 22 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "r4a_3636",
 "version": "3.4",
 "screen_run": "r4_3636",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 30,
 "estimated_usd": 0.2792,
 "providers_with_findings": 13,
 "providers_called_upcoding": 3,
 "upcoders_found": 3,
 "honest_called_upcoding": 0,
 "upcoders_total": 8,
 "records_requests_to_honest": 8,
 "records_requests_total": 13,
 "rounds_on_honest": 11,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_r4_3636.json` (gitignored). Frozen workflow baseline: `v2.0`.
