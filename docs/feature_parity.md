# Feature parity: what each workflow and agent version builds

[Back to the README](../README.md) · [versions](versioning.md) · [concepts](concepts/README.md)

**What this page is.** The workflow (code fixes the order of the steps) and the agent (a model chooses its own steps within caps) are developed side by side. The rule: a change lands in both, or is marked one-sided with a reason. This page lists, version by version, what each stream built, and `tests/test_parity_table.py` checks that every row has both cells and a reason when one is missing. Shared pieces (the data generator, the provider office, the number check, the results table) change once and are re-run for both. Which versions exist and what is frozen: [versions](versioning.md).

## Workflow v2.1 and agent v3.1 (data 2.1: the note package)

| Feature (issue) | v2.1 workflow | v3.1 agent | Reason if one-sided |
|---|---|---|---|
| Richer claim-versus-note checks (#57) | built and evaluated (#61): note rule, office 2.1 policy (`eval/workflow_policy_v21.py`) | built and evaluated (#61): `note_checks` and `request_audit_trail` tools, prompt | |
| Call the honest-notes upcoders we reach (#58) | planned | planned | |
| Low base rate safeguards (#59) | planned | planned | |
| Summary quality and judge calibration (#60) | planned | planned | |
| Second records request (#67) | built (office 2.1; policy sends a targeted second request) | built (office 2.1) | |
| Conditional next steps and the pre-submission lint (#63) | built (`case_summary.py --v21`: conditional steps, model-written summaries that fail a hard check are repaired by code) | built (`submit_findings` lints and refuses; steps conditional) | |
| Dispositions for screened candidates (#66) | built as a post-hoc table (`eval/dispositions_w.py`, [dispositions_w.md](dispositions_w.md)): a reason for every listed provider; it is a table written after the run, not a refusal gate | built (`set_aside`, refused without it) | the workflow cannot be refused: its code decides every provider, so the table only records why |
| Estimate reliability gate (v3.1) | n/a (the workflow does not quote estimates) | built (`reliable`, `stratum_reviewed`; the lint refuses quoting an unreliable estimate) | agent-only by design |
| Screen table magnitude columns and `priority` ordering (#48) | planned: `priority` as the workflow's ordering | built (ratio, excess claims, low-complexity share, excess dollars; `method="priority"`) | mirrored by ordering |
| Hybrid review (#49) | planned | planned (tool exists) | |
| Screen cutoff choice (#48) | planned: budget-based rule | planned: agent chooses | mirrored by design |
| Multi-seed paired evaluation (#61) | done ([eval61.md](eval61.md)) | done | shared |

## Workflow v2.2 and agent v3.2 (data 2.2: realism and data defects)

| Feature (issue) | v2.2 workflow | v3.2 agent | Reason if one-sided |
|---|---|---|---|
| Screen ranking metrics (#83) | built: columns of `results.csv`, [screen_metrics.md](screen_metrics.md) | same (evaluation only) | shared |
| Screen methods (#88) | `eb_ratio` and `priority` are the release 2 candidates ([screen_methods.md](screen_methods.md)): `flagging.py --method`, v2.2 workflow arms; `riskadj` stays frozen | `screen_providers` with method `eb_ratio` or `priority` in v3.2 | confirmed or rejected on the fresh seeds ([release2_plan.md](release2_plan.md)) |
| Data-quality pre-flight (#81) | built: `flagging.py --preflight` ([data_quality.md](data_quality.md)); the case-summary step does not consume the column yet | built: `data_quality` and `flag_data_issue` tools, hold in `submit_findings`; offline tests only | |
| Fewer model calls in the writer (#91) | built: rules 2.2 (`case_summary.py --v22`, `summary_rules.rule_leaning_22`) decide inconclusive the ambiguous cases where the v2.1 model always said inconclusive; 115 to 11 model calls on the release 1 runs, no leaning changed ([workflow_cost.md](workflow_cost.md)) | n/a: the agent writes its own findings (its cost is #92) | the agent has no rule-then-model writer |
| No LLM usefulness judge in the evaluation (#91, #93) | built: the 2.2 workflow path skips `judge_usefulness.py`; the rule judge runs | #92 | |
| Agent cost (#92) | n/a: the workflow has no agent loop (its cost is #91) | built: $1 cap for 3.2 (`run_agent.EVAL_MAX_USD_32`), no LLM judge (`judge_agent_runs.main(..., "3.2")` rebuilds the view only, replaying office 2.1), usage per turn (`turn_usage.jsonl`), `run_agent.py --model` and `--effort`; measured in [agent_cost.md](agent_cost.md) | agent loop only |

## Workflow v2.3 and agent v3.3 (cloned-notes detection)

| Feature (#99) | v2.3 workflow | v3.3 agent | Reason if one-sided |
|---|---|---|---|
| Rules 2.3: cloned-notes signs decide by rule | built: `summary_rules.rule_leaning_23` (late signatures, audit-trail signs, far-above-expected share; chart calls must beat the real peer rate) with `case_summary.py --v23` | built: `hybrid_review` uses rules 2.3, the lint accepts such calls, `SYSTEM_33` explains cloned notes and the chart test | mirrored |
| Screen `eb_ratio_t` (test-line covariate) | built: `screen_methods.score_t`, `flagging.py --method eb_ratio_t` | built: `screen_providers` method `eb_ratio_t` | mirrored |
| Wider list with a light tier | built, **the W2.3 default** (Simmy's decision: more upcoders found, about 94 more honest practices asked on the development seeds): top 10%, ranks 12 to 22 get one request unless the notes show cloning (`eval/workflow_policy_23.py`) | built: the prompt suggests the top 10% and a light touch beyond the first 5%; records budget 22 (v3.0 to v3.2: 15); the agent chooses | mirrored by design (the agent chooses) |
| Audit-trail request on late signatures | built (adds nothing on the development seeds) | the existing `request_audit_trail` tool, prompted | mirrored |

## Workflow v2.4 and agent v3.4 (a narrower list, a learned stop)

| Feature | v2.4 workflow | v3.4 agent | Reason if one-sided |
|---|---|---|---|
| Learned stop-or-escalate formula (#108) | built: `eval/workflow_policy_24.py` with `learned`, `src/escalation_policy.py`, `src/policy_24.json`; variants G, L, GL ([learned_policy_plain.md](learned_policy_plain.md)); fresh test on ten seeds: **GL is the v2.4 default** by the pre-registered rule ([release4_results.md](release4_results.md)) | built as **advice only**: tool `advise_next_step` (`Environment(version="3.4")`, `SYSTEM_34`) answers after a first sample; the agent decides (**in the ten-seed test it never called the tool**: [release4_agent_results.md](release4_agent_results.md)) | different mechanism by design: the workflow obeys the formula, the agent is advised |
| Ratio gate on the light tier (#102) | built (variant G, 2.5) | built as **advice only**: `advise_next_step` before any request says ASK or SKIP by the same gate (ratio 2.5 beyond the first 5%), plus the agent's own habit of asking at about 3x expected | the workflow obeys the gate, the agent is advised and chooses |
| Rules first, then spend rounds only where the sample leaves a question (#102) | built (rules 2.3 decide every provider asked; learned stop-or-escalate) | built: **enforced in code** (`submit_findings` refuses until `hybrid_review` has been run on every provider whose records arrived); follow-up only where the first sample leaves a question is a prompt rule in `SYSTEM_34`, measured from the audit log | the rule-application invariant is code; the escalation judgment stays with the agent |
| Silent offices (#103) | moved to release 5 (#109) | moved to release 5 | depends on how non-response is modeled (#68) |
| High-acuity override (#104) | **do not build** (checked: one upcoder and one honest doctor on 20 development seeds) | do not build | evidence too thin to justify a rule in either stream |

## Workflow v2.5 and agent v3.5 (dollars as the score)

| Feature | v2.5 workflow | v3.5 agent | Reason if one-sided |
|---|---|---|---|
| Learned ask-or-skip and stop-or-escalate fitted on net dollars (#109) | built: `eval/workflow_policy_25.py`, `src/policy_25.py`, `src/policy_25.json` (fitted by `eval/export_policy_25.py` on 30 development seeds); chosen start by Simmy after [release5_train.md](release5_train.md) | built (`Environment(version="3.5")`, `SYSTEM_35`; not yet run on the model): the same `src/policy_25.json` as **advice inside the results** of `request_records`, `follow_up_records` and `request_audit_trail` plus an `ask_advice` column in the screen (#111); an upcoding call from the rules that the chart rule also supports is **binding** unless `override_reason` names a claim id, data-quality flag or note sign (#112); practice status and rounds sent shown every turn (#113); advice use and overrides logged in `advice_log.json` | the workflow obeys the formulas; the agent is advised and, where code can enforce an invariant, bound |

## Workflow v4.0 to v4.2 and agent v5.0 to v5.2 (data 4.0 and 4.2, scores 4.0 to 4.2)

What the versions of the v4 and v5 line added, newest last (one bullet each); the table after them is the mirror check for v4.2 and v5.2.

- **Data 4.0** (built, [data_v4_0.md](data_v4_0.md); `src/generate_v4.py`, development seeds `d4_*`, [statistics](data_v4_0_stats.md)). Every provider has an upcoding rate. Exactly 8 upcoders per dataset, each with a rate from 15% to 40% and one habit: systematic (always bills 99214 for 99213-level visits), opportunistic (inflates only borderline visits) or template-driven (an EHR default to a higher level, no intent; still a target, and lighter actions for it are #123). Non-upcoders' rate is centred between -15% and +15%. The answer-key `role` stays binary (the planted 8) with the rate beside it. Opportunistic upcoding needs a continuous per-visit complexity from which the justified level is derived, reversing the order noted in issue 45. Data 2.x stays reproducible behind `--data-version`.
- **Score 4.0** (built, [score_40.md](score_40.md); `eval/score_40.py`; free check on releases 2 to 5: [score_40_check.md](score_40_check.md)): dollars recovered (the estimate from any provider sent a demand, not capped at the true overpayment, since a payer has no answer key) minus staff-hours cost minus provider abrasion (weighted by the true net rate). Later score versions add an SIU hours cap, appeals and a recovery tool. Full specification and the order of issues: [v4_v5_plan.md](v4_v5_plan.md).
- **Screen (#127, [screens_v4.md](screens_v4.md), [downstream check](screens_v4_pipeline.md)):** `eb_upper_t` (the shrunk share billed 99214 or 99215, with the test line) is the chosen default: workflow built (`flagging.py --method eb_upper_t`, `src/screen_methods_v4.py`); agent: wired when agent v5.0 is built in #128 (one-sided until then: the agent version does not exist yet).
- **Workflow v4.0 (built and frozen, [w_loop_v4.md](w_loop_v4.md), issue #131):** the `eb_upper_t` list, rules 4.0 (the chart test pooled over 99214 and 99215), a first sample of 30 random charts, the ask-or-skip refitted on score 4.0 (`src/policy_40_ask.json`, fitted on development batches 1 to 4), no escalation, and a demand only when the payer's estimate of the recovery covers the staff cost of a demand (`eval/workflow_policy_40.py`, `FROZEN_V40`; API-free). On 100 development seeds: score 4.0 per seed +\$549 against -\$10,820 for the frozen v2.5 (100 of 100 seeds better); out of sample (batches 5 to 10) +\$426 against -\$236 for the version before its ask model. Agent v5.0 mirrors it in its tools (built: `Environment(version="5.0")`; the eb_upper_t screen, rules 4.0, ask advice refitted on score 4.0, advice STOP after the first sample, the demand floor and the style repair of [agent_text_replay.md](agent_text_replay.md); near parity, not parity: a scripted agent that follows the advice asks the same providers as the workflow on 8 of 8 development seeds and calls the same providers on 6 of 8 (`eval/agent50_parity.py`); run once on the ten fresh seeds, issue #128). On the ten fresh seeds workflow v4.0 scored -\$1,161 per seed against -\$11,185 for the frozen v2.5, and agent v5.0 -\$781 (not above zero, as on the development pool for the workflow: [w_loop_v4.md](w_loop_v4.md)).
- **Agent v5.1 (built and run once on the ten test seeds: +$743 per seed, [a51_fresh_result.md](a51_fresh_result.md); [agent_v51.md](agent_v51.md)):** mirrors workflow v4.1 (H23, N = 4; [w41_freeze.md](w41_freeze.md), [w41_fresh_result.md](w41_fresh_result.md)) in `Environment(version="5.1")`: ASK advice for the first 4 listed providers only, the loosened rules 4.0 chart test, and a once-only near-miss extension of 30 random charts (`demand_check` in `hybrid_review`; the extension gate in `request_records`), with the demand floor and binding rule kept. A scripted agent that follows the advice matches workflow v4.1 on 20 development seeds (asked 20 of 20, extended and called 19 of 20). The paid run on the ten test seeds waits for an estimate and an OK.
- **Workflow v4.2 and agent v5.2 (release 2 of the line; [v42_test_result.md](v42_test_result.md)):** data 4.2 ([data_v4_2.md](data_v4_2.md)) has no planted upcoder and adds fraud. [Score 4.2](score_42.md) (copy fee $0; a visit the office has no record of counts as overpaid; abrasion by total true rate). Workflow v4.2 (`H28` in `eval/w_loop_42.py`) is workflow v4.1 plus the claims-data lane (`src/fwa_lane.py`): flag a provider with 30 or more visits on one service date, request a random sample of its claims on those dates, price it as a [stratified sample](concepts/stratified-sample.md), demand when the conservative estimate covers a demand; up to four follow-ups when the office gives nothing usable. Agent v5.2 (`Environment(version="5.2")`, office 4.2, tools `volume_screen`, `request_stratum`, `send_demand`; [agent_v52.md](agent_v52.md)) mirrors it by advice and by the shared lane code. Agent v5.0, v5.1 and v3.x are unchanged. The earlier ask-or-skip, list of 4 and borderline extension of v4.1 are unchanged.
- **Reference arms:** frozen v2.5 and v3.5 run unchanged on data 4.0 and are scored with the new score, which separates the data change from the method change; so v4.0 and v5.0 may already carry new features.

| Feature (v4.2 and v5.2) | v4.2 workflow | v5.2 agent | Reason if one-sided |
|---|---|---|---|
| Score 4.2, data 4.2, office 4.2 | scored on data 4.2 (`eval/score_42.py`) | `Environment(version="5.2")` on office 4.2 | |
| Volume screen and claims-data lane | built (`H28`, `src/fwa_lane.py`) | built (`volume_screen`, `request_stratum`, `send_demand`), same code | |
| Follow-up persistence (up to 4 follow-ups) | built (`persist` 3) | built (the tool calls the same function) | |
| Chart rules, list of 4, borderline second sample, break-even rule | as v4.1 | as v5.1 | |
| Ghost-member billing for visits never rendered | not built | not built | no volume signal separates it in data 4.2 (docs/score_42.md, known weaknesses) |

## Known gaps in the mirror rule

Checked 2026-10-18: dispositions for screened candidates (#66) are a refusal gate only in the agent (`set_aside`); the workflow has a post-hoc table (`eval/dispositions_w.py`). The "hybrid review (#49)" and "data-quality pre-flight (#81)" rows above are out of date: both streams now decide with rules first and a model only where the rules are silent, and the workflow's case-summary step applies the pre-flight holds. The agent alone flags data issues (`flag_data_issue`), reads its own estimate reliability, and chooses its own list size. The agent writes its own findings while the workflow's summaries are code-written; judges j3.2 and j3.3 score both.
