# Investigator agent: tools, loop and guardrails

The agent (`src/agent.py`) is a model in a tool-use loop. Code supplies tools, limits and logging; the model decides what to do. This is the design Milestone 6 compares with the frozen v2.0 workflow, where code fixes the order of steps. Tools live in `src/agent_tools.py`.

## Tools
| Tool | What it does | Runs as | Notes |
|---|---|---|---|
| `screen_providers` | Ranks every provider (plain z, risk-adjusted z or combined rank) and picks a cutoff (top N or minimum score, optional cap and minimum claims). Returns a ranked table, the score distribution and how many providers sit at each cutoff. | Code | Deterministic and free. The agent chooses the screening instead of receiving a list (#39, #48). |
| `list_providers` | Claims, 99215 share and 99214-or-99215 share per provider, 40 per page. No scores. | Code | Replaces `screen_providers` in the no-screen ablation (#43). |
| `provider_profile`, `peer_comparison` | Evidence card (mix, complexity table, sample claims, any charts already received); provider against all providers. | Code | |
| `request_records`, `follow_up_records`, `close_records` | The multi-round exchange with the simulated provider office (`docs/provider_sim.md`). | Code (simulated office: seeded rules and templated text) | Budgeted per provider: each request burdens a practice. |
| `hybrid_review` (#49) | Per provider: the chart rule first, then the summary rules, and the model only where both say nothing. Reports the decision and which step made it. | Code, then a model fallback only with `--model-in-tools` | Up to 20 providers per call. |
| `draft_summary` | Draft case summary with the citation check. | Code (reuses `hybrid_review`'s decision, so a model only through that fallback) | Drafts for human review. |
| `estimate_overpayment` | Extrapolated overpayment from a random sample. | Code | Refuses targeted samples. |
| `submit_findings` | The final list of providers and leanings; ends the run. | Code (the leaning, headline and interpretation it stores are written by the agent model) | Stored as drafts. |
| `note_checks` (v3.1 only) | Claim-versus-note signals on the notes already received: notes that address fewer problems than the billed level implies, data review the claim cannot back, unsigned or late-signed notes, and (with an audit trail) bulk-created or paste-heavy notes. | Code | Rates, not proof; lists example claims. Fewer than 8 notes gives no pattern signal. |
| `request_audit_trail` (v3.1 only) | Second-tier request to the simulated office for the EHR audit trail of charts already received (created and edited times, paste events). | Code (simulated office) | Costs a round; the office may refuse. |

"Code" means deterministic Python with no model call. The agent model itself decides every step and writes the text passed to `submit_findings`. In the v3.0 runs so far `--model-in-tools` was off, so no tool called a model (`model_spend_in_tools_usd` is 0 in each `agent_run.json`).

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
- Live runs: a pilot on the development seed (`261013_3_api`) and the v3.0 evaluation on seeds 202 and 303 (`261013_8_api` to `261013_11_api`, `261013_16_api` to `261013_19_api`); results are in `docs/results.md`. The tests use a scripted client (`tests/test_agent.py`).
