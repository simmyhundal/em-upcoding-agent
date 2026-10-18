# r3a_3131

The investigator agent v3.3 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `r3_3131`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 22 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "r3a_3131",
 "version": "3.3",
 "screen_run": "r3_3131",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 25,
 "estimated_usd": 0.181,
 "providers_with_findings": 12,
 "providers_called_upcoding": 1,
 "upcoders_found": 1,
 "honest_called_upcoding": 0,
 "upcoders_total": 8,
 "records_requests_to_honest": 7,
 "records_requests_total": 12,
 "rounds_on_honest": 10,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_r3_3131.json` (gitignored). Frozen workflow baseline: `v2.0`.
