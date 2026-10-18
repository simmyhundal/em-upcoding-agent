# r3a_3333

The investigator agent v3.3 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `r3_3333`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 22 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "r3a_3333",
 "version": "3.3",
 "screen_run": "r3_3333",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 30,
 "estimated_usd": 0.2668,
 "providers_with_findings": 14,
 "providers_called_upcoding": 4,
 "upcoders_found": 4,
 "honest_called_upcoding": 0,
 "upcoders_total": 8,
 "records_requests_to_honest": 10,
 "records_requests_total": 14,
 "rounds_on_honest": 14,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_r3_3333.json` (gitignored). Frozen workflow baseline: `v2.0`.
