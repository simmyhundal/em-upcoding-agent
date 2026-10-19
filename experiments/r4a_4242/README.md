# r4a_4242

The investigator agent v3.4 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `r4_4242`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 22 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "r4a_4242",
 "version": "3.4",
 "screen_run": "r4_4242",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 22,
 "estimated_usd": 0.1902,
 "providers_with_findings": 12,
 "providers_called_upcoding": 7,
 "upcoders_found": 6,
 "honest_called_upcoding": 1,
 "upcoders_total": 8,
 "records_requests_to_honest": 6,
 "records_requests_total": 12,
 "rounds_on_honest": 8,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_r4_4242.json` (gitignored). Frozen workflow baseline: `v2.0`.
