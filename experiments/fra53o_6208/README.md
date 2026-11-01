# fra53o_6208

The investigator agent v5.3 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `d43_6208`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 22 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "fra53o_6208",
 "version": "5.3",
 "screen_run": "d43_6208",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 5,
 "estimated_usd": 0.0897,
 "providers_with_findings": 1,
 "providers_called_upcoding": 0,
 "upcoders_found": 0,
 "honest_called_upcoding": 0,
 "upcoders_total": 0,
 "records_requests_to_honest": 1,
 "records_requests_total": 1,
 "rounds_on_honest": 2,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_d43_6208.json` (gitignored). Frozen workflow baseline: `v2.0`.
