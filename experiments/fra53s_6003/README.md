# fra53s_6003

The investigator agent v5.3 (`src/agent.py`, model claude-sonnet-5-5) on the v2 data of `d43_6003`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 22 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "fra53s_6003",
 "version": "5.3",
 "screen_run": "d43_6003",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 16,
 "estimated_usd": 0.0648,
 "providers_with_findings": 1,
 "providers_called_upcoding": 0,
 "upcoders_found": 0,
 "honest_called_upcoding": 0,
 "upcoders_total": 0,
 "records_requests_to_honest": 10,
 "records_requests_total": 10,
 "rounds_on_honest": 26,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_d43_6003.json` (gitignored). Frozen workflow baseline: `v2.0`.
