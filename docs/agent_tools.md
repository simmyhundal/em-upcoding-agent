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

## Version 3.2: data quality (issue 81)

`Environment(version="3.2")` is 3.1 plus a data-quality pre-flight that runs once when the environment loads (`src/data_quality.py`, graded in [data_quality.md](data_quality.md)) and two tools:

| Tool | What it does |
|---|---|
| `data_quality` | Read-only. The pre-flight's status, check sentences and global flags; with `provider_id`, that provider's flags and whether its findings are held. |
| `flag_data_issue` | Records a data concern (issue, detail, optional providers, `hold_findings` default true) for a person to raise with the plan. The agent cannot request data from the plan. |

`submit_findings` refuses a `pattern_consistent_with_upcoding` finding for a held provider (flagged by the pre-flight or by `flag_data_issue`) that has fewer than 8 charts received, and
appends the data caveat to every affected finding after the lint. The run folder gets `data_quality.json` and `data_issues.json`. Built and unit tested offline; no model run has used it.

## Version 5.1: mirrors workflow v4.1 (see [agent_v51.md](agent_v51.md))
`Environment(version="5.1")` is v5.0 plus three changes, all payer-visible. `screen_providers` (`eb_upper_t`) gives ASK or SKIP advice for the first 4 listed providers only and adds a `list_note`. `hybrid_review` uses the loosened rules 4.0 chart test
(5 charts, 10%, alpha 0.20) and, for a provider it calls upcoding, returns `demand_check` (point estimate, 90% lower bound, cost of a demand, `near_miss`, advice); `estimate_overpayment` returns it too. `request_records` accepts a second random
request (at most 30 charts; more is refused) once, and only for a provider called upcoding whose `demand_check` is a near-miss; any other second random request is refused, and the earlier review becomes stale so `hybrid_review` must be run again before `submit_findings`.
The demand floor, the binding rule of v3.5, the STOP advice and the style repair are as in v5.0.
