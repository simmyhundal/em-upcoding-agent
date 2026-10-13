# Investigator agent: tools, loop and guardrails

The agent (`src/agent.py`) is a model in a tool-use loop. Code supplies tools, limits and logging; the model decides what to do. This is the design Milestone 6 compares with the frozen v2.0 workflow, where code fixes the order of steps. Tools live in `src/agent_tools.py`.

## Tools
| Tool | What it does | Notes |
|---|---|---|
| `screen_providers` | Ranks every provider (plain z, risk-adjusted z or combined rank) and picks a cutoff (top N or minimum score, optional cap and minimum claims). Returns a ranked table, the score distribution and how many providers sit at each cutoff. | Deterministic and free. The agent chooses the screening instead of receiving a list (#39, #48). |
| `list_providers` | Claims, 99215 share and 99214-or-99215 share per provider, 40 per page. No scores. | Replaces `screen_providers` in the no-screen ablation (#43). |
| `provider_profile`, `peer_comparison` | Evidence card (mix, complexity table, sample claims, any charts already received); provider against all providers. | |
| `request_records`, `follow_up_records`, `close_records` | The multi-round exchange with the simulated provider office (`docs/provider_sim.md`). | Budgeted per provider: each request burdens a practice. |
| `hybrid_review` (#49) | Per provider: the chart rule first, then the summary rules, and the model only where both say nothing. Reports the decision and which step made it. | Up to 20 providers per call. |
| `draft_summary` | Draft case summary with the citation check. | Drafts for human review. |
| `estimate_overpayment` | Extrapolated overpayment from a random sample. | Refuses targeted samples. |
| `submit_findings` | The final list of providers and leanings; ends the run. | Stored as drafts. |

## What the agent can and cannot see
It reads payer-visible data only: claims, patients and providers derived from claims, documentation from a control sample of earlier reviews (the peer baseline), and whatever the office returns. It never sees roles, justified levels, the records universe, the office's hidden behavior or the answer key. A test runs a full scripted agent with `open` instrumented and checks no answer-key path is touched, and that tool results and the audit log contain no truth words.

## Limits
Hard caps on tool calls (60), turns (80) and dollars (3.00 per run), with a budget notice at 80%; a records budget (providers asked, 15); the office's own caps (3 rounds, 120 days per provider). The run ends at a cap, and anything already submitted is kept.

## Logging and review
Every tool call and result goes to `audit.jsonl` (arguments, result, running cost); the office keeps a transcript. Findings are written in the same shape as the workflow's case summaries, so the citation check and the judge apply unchanged. Nothing is sent or decided automatically.

## Choices to know about
- The model sees tool results as JSON; tables are `{cols, rows}`. Results over 14,000 characters are cut and marked.
- Forced tool choice is not used (the model chooses); thinking blocks are passed back unchanged.
- The agent's own spend is estimated from usage (list prices; cache reads and writes included). `hybrid_review` and `draft_summary` can call a model inside a tool (`--model-in-tools`); that spend is tracked separately.
- The first live run has not happened yet; everything here is tested with a scripted client (`tests/test_agent.py`).
