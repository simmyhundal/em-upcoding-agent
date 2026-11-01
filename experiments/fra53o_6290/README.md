# fra53o_6290

The investigator agent v5.3 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `d43_6290`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 22 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "fra53o_6290",
 "version": "5.3",
 "screen_run": "d43_6290",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 6,
 "estimated_usd": 0.1002,
 "providers_with_findings": 2,
 "providers_called_upcoding": 0,
 "upcoders_found": 0,
 "honest_called_upcoding": 0,
 "upcoders_total": 0,
 "records_requests_to_honest": 2,
 "records_requests_total": 2,
 "rounds_on_honest": 3,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_d43_6290.json` (gitignored). Frozen workflow baseline: `v2.0`.
