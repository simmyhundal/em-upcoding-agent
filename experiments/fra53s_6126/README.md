# fra53s_6126

The investigator agent v5.3 (`src/agent.py`, model claude-sonnet-5-5) on the v2 data of `d43_6126`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 22 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "fra53s_6126",
 "version": "5.3",
 "screen_run": "d43_6126",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 15,
 "estimated_usd": 0.0562,
 "providers_with_findings": 1,
 "providers_called_upcoding": 0,
 "upcoders_found": 0,
 "honest_called_upcoding": 0,
 "upcoders_total": 0,
 "records_requests_to_honest": 10,
 "records_requests_total": 10,
 "rounds_on_honest": 25,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_d43_6126.json` (gitignored). Frozen workflow baseline: `v2.0`.
