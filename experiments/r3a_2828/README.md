# r3a_2828

The investigator agent v3.3 (`src/agent.py`, model claude-opus-5-5) on the v2 data of `r3_2828`, with the statistical screen tool. Caps: $1.00, 60 tool calls, records for at most 22 providers. Office behavior is independent of upcoder status (correlation 0.0). Findings are drafts for human review.

```
{
 "run": "r3a_2828",
 "version": "3.3",
 "screen_run": "r3_2828",
 "screen_tool": true,
 "stop_reason": "submitted",
 "tool_calls": 22,
 "estimated_usd": 0.2012,
 "providers_with_findings": 11,
 "providers_called_upcoding": 1,
 "upcoders_found": 1,
 "honest_called_upcoding": 0,
 "upcoders_total": 7,
 "records_requests_to_honest": 6,
 "records_requests_total": 11,
 "rounds_on_honest": 9,
 "citation_accuracy": 1.0
}
```

Files: `audit.jsonl` (every tool call), `office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: `eval/answer_key/ground_truth_v2_r3_2828.json` (gitignored). Frozen workflow baseline: `v2.0`.
