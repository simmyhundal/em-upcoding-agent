# Agent v5.1 (A5.1): mirrors workflow v4.1 inside the agent's tools

[Back to the README](../README.md) · [workflow v4.1 freeze](w41_freeze.md) · [workflow v4.1 result](w41_fresh_result.md) · [agent tools](agent_tools.md) · [versioning](versioning.md)

Score 4.0, data 4.0. Built and tested for free. **Not run on any fresh seed.** The paid run needs Simmy's OK after the estimate below.

## What changed from agent v5.0
`Environment(version="5.1")`, prompt `SYSTEM_51`, `eval/run_agent.py --version 5.1`. Agent v5.0 and v3.x are unchanged (their tests pass). A5.1 copies the three things workflow v4.1 (H23, N = 4) added to workflow v4.0:
1. **A list of four.** `screen_providers` (method `eb_upper_t`) still shows the top 10%, but `ask_advice` is ASK or SKIP only for the first 4 rows. Every other row is SKIP, and the result carries a `list_note`. The ask model sees the same row as in the workflow (the rank is kept). Triage costs about $13 for each provider the agent submits a finding for; the workflow triages all four listed providers, the agent only those it asked.
2. **A looser chart test.** `hybrid_review` uses rules 4.0 with the options of H17 (at least 5 documented 99214 and 99215 charts, unsupported share at least 10%, alpha 0.20). The writing lint in `submit_findings` accepts the same test.
3. **A near-miss extension.** For a provider that `hybrid_review` calls upcoding, the result carries `demand_check`: the payer's point estimate of the recovery, its 90% lower bound, the cost of a demand ($276) and `near_miss`. Near-miss means the point estimate is at least twice that cost while the lower bound is below it. Then the advice is to request 30 more random charts, once, follow up on any deficiency, run `hybrid_review` again and stop. `request_records` enforces this: a second random request is refused unless the provider was called upcoding and is a near-miss, it is accepted once only, and a request of more than 30 charts is refused. After it, the earlier review is stale, so `submit_findings` demands a new `hybrid_review`. `estimate_overpayment` also returns `demand_check`.

Kept from v5.0: the demand floor in `submit_findings` (a call whose lower bound is below the cost of a demand is withdrawn to inconclusive), the narrow binding rule of v3.5, the STOP advice after the first sample (no targeted request, no audit trail), and the style repair. Everything the agent sees is payer-visible: the estimate uses only claims and the charts the office sent (`src/recovery_40.py`); tests check that no answer key file is opened and no role appears in a tool result.

## Parity with workflow v4.1 (free, development seeds only)
`eval/agent51_parity.py` runs a scripted agent that follows the advice (ask where ASK, 30 random charts and one follow-up, `hybrid_review`, a second request for each near-miss, `hybrid_review` again, submit the leanings). It runs on the 20 development seeds of batches 5 and 6 (3630 to 4029) and is compared with the stored workflow run `wlh23_n4_<seed>`. No model is called.

| Check | Same on |
|---|---|
| Providers asked | 20 of 20 seeds |
| Providers given the extension | 19 of 20 seeds |
| Providers called upcoding (after the demand floor) | 19 of 20 seeds |
| Score 4.0, agent scored with the workflow's four listed providers | 19 of 20 seeds (to the cent) |

Mean score per seed: workflow v4.1 +$1,381; scripted agent with the same four listed +$1,405; scripted agent with its natural triage (a finding only for providers asked) +$1,430. The gap in the natural column is the triage of listed providers that were not asked ($13 each); it favours the agent by construction.

The one seed that differs is 4029. The scripted agent extended provider 1000000056 and the workflow did not, and the workflow's final score there is $487 lower. What was observed: in the workflow's first pass this provider's summary read inconclusive (the chart test did not fire); after another provider's extension rewrote the view, the rebuilt summary read upcoding (6 of 27 documented charts below the billed level, p = 0.199, under alpha 0.20), and the demand floor then withdrew it. The workflow decides extensions from the first pass; the agent sees the second reading. I did not trace why the two passes differ (the first-pass p value and peer rate were not measured). It is a borderline case of the loosened test. This is near parity, not parity, as for v5.0.

## The paid path was checked on development seeds
Parity above was measured on the live environment. The paid runner scores a run another way: `run_agent.main` writes `audit.jsonl`, `judge_agent_runs.main` replays it against a fresh office to rebuild the charts, and `score_40.from_run` scores the rebuilt view. `eval/agent51_replay_check.py` feeds the scripted agent's recorded tool calls through the real loop with a stub client (no API call), including a refused second extension and a refused request of 80 charts, then scores the stored run. Result on seeds 3672 (one extension) and 4008 (two): the stored-path score equals the live score to the cent, with equal rounds, charts and demands. Two details made this work: the extension is refused when it asks for more than 30 charts (not cut, so the logged arguments are what the office received), and the replay skips `request_records` calls that the environment refused. The advice log records an extension as its own action, `EXT`, which counts as following the advice.

## Cost estimate for one run on the ten test seeds (not run)
Basis: A5.0's recorded usage on the same ten seeds, $1.135 in all (experiments `fra50_*`; $0.08 to $0.15 per run, 4 to 6 turns, 5 to 16 tool calls; Opus 5.5, low effort).
- Prompt and longer tool results: about +$0.05 for ten runs (about 450 more prompt tokens, a `demand_check` of about 150 tokens per call).
- Extensions: the scripted agent extended 13 providers in 20 development seeds, so about 6 or 7 in ten seeds. Each adds about three turns and about 3,500 tokens of charts to the cached context: about $0.085, so about $0.55.
- **Expected total: about $1.7.** Plausible range $1.3 (no extension) to $3 (two extensions on every seed). The runner stops at a $4 batch cap, and each run has a $1 cap.

## What is not done
- No paid run. `eval/run_v51_fresh_agent.py` refuses without `--approved`. It runs A5.1 once on 5555 to 6464 (second use of those seeds for the agent line, as for W4.1) and writes `experiments/v51_fresh_results.json`. The second fresh pool (6565 to 7474) is untouched.
- The parity check uses a scripted agent. A real model may ignore the advice, so the agent's score can differ from the workflow's (A5.0 was $380 per seed above W4.0 with equal found).
- The list of four and the extension are mirrored by advice and one hard rule (the extension gate). The agent can still ask a provider outside the list (the records budget is 22, as for A5.0); this costs it staff hours under score 4.0 and is logged.
