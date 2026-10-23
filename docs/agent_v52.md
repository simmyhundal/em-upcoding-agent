# Agent v5.2 (A5.2): the model-driven reviewer with the claims-data lane

[Back to the README](../README.md) · [workflow v4.2 freeze](w42_freeze.md) · [confirm result](w42_confirm_result.md) · [score 4.2](score_42.md) · [agent tools](agent_tools.md) · [concepts](concepts/README.md)

**What this page is.** The project builds two reviewers of suspected billing problems on synthetic claims: a [workflow](concepts/workflow-and-agent.md "Code fixes the order of the steps") and an [agent](concepts/workflow-and-agent.md "A model chooses its own steps within caps"). Workflow v4.2 was frozen and confirmed first; this page describes agent v5.2, which gets the same new capability through its tools so the two can be compared fairly. It is the agent of release 4.2 and 5.2: agent v5.1 plus the claims-data lane, scored by [score 4.2](score_42.md) on data 4.2.

## What changed from agent v5.1
`Environment(version="5.2")`, prompt `SYSTEM_52`, office version 4.2 (a claim for a visit that never happened gets no chart and the office reports no record of it), `eval/run_agent.py --version 5.2`. Agent v5.0, v5.1 and v3.x are unchanged (their tests pass). Three new tools mirror the workflow's [claims-data lane](concepts/volume-screen.md "Providers who billed 30 or more visits on one day"):
1. `volume_screen` (free, read-only): the providers who billed 30 or more visits on one service date, with the number of claims on those dates. Capped at 10 providers.
2. `request_stratum`: for a provider on that table, draws a [random sample](concepts/stratified-sample.md "A random sample within one slice of a provider's claims") of 30 of its claims on those dates, asks the office for the charts (with up to four follow-ups while the office gives nothing usable), and returns the [conservative estimate](concepts/conservative-estimate.md "The 90% lower bound") of the overpayment for those dates. A visit the office has [no record of](concepts/records-not-provided.md "A sampled claim the office has no record of counts as overpaid") counts as overpaid at its paid amount. Once per provider.
3. `send_demand`: sends the demand for a provider taken through `request_stratum`; refused when the conservative estimate does not cover the cost of a demand (the [break-even rule](concepts/break-even-rule.md "No demand when the conservative recovery is below the cost of a demand")).

The prompt also states score 4.2's prices (records are copied at no charge; a visit with no record counts as overpaid). Everything the agent sees is payer-visible: claims, what the office returns, and the payer's own estimate. Tests check that no answer-key field reaches a tool result (`tests/test_agent_52.py`). The lane shares its code with the workflow (`src/fwa_lane.py`), so the two cannot drift.

## Does the agent match workflow v4.2? (free, development seeds only)
`eval/agent52_parity.py` runs a *scripted agent* (a stand-in whose steps are written in code to follow the advice exactly, so the tools can be checked without paying for a model) on the first 20 development seeds of data 4.2 and compares it with the stored workflow v4.2 runs. No model is called.

| Check | Same on |
|---|---|
| Providers asked for a level sample | 20 of 20 seeds |
| Providers called upcoding | 20 of 20 seeds |
| Providers taken through the lane | 20 of 20 seeds |
| Providers sent a lane demand | 20 of 20 seeds |
| Score 4.2 within 1% (or $100) | 18 of 20 seeds |

Mean score 4.2 per seed: workflow v4.2 +$32,662; scripted agent +$32,633. The two seeds that differ by more (up to $585) are explained by one design difference, not judgment: the workflow's lane uses its own office, so a provider asked in both the level review and the lane is charged for both sets of charts, while the agent's single office counts overlapping charts once.

## Cost estimate for one run on the ten test seeds (not run yet)
Basis: agent v5.1's recorded usage on ten seeds, $1.242 in all ($0.09 to $0.16 per run, 5 to 11 tool calls; Opus 5.5, low effort). Agent v5.2 adds one `volume_screen`, about three `request_stratum` and about two `send_demand` calls per run (the development seeds average 3 impossible-day providers per dataset and 2 demands), each result about 300 tokens, and each extra turn re-reads the cached context. Expected: **about $0.25 per run, $2.5 for ten**; plausible range $1.8 to $3.5. Caps: $1 per run, $4 for the batch. The run is paid; it needs the standing approval of `/run-release paid cap=4` or an explicit OK.

## What is not done
- No paid run yet: `eval/run_v42_test.py agent --approved` runs it once on the test pool.
- The parity check uses a scripted agent. A real model may ignore the advice (agent v5.0 and v5.1 stayed close to their workflows; their gaps were within what the workflow-versus-agent differences in triage explain).
- The lane's signal is clean by construction; see [the volume screen](concepts/volume-screen.md).
