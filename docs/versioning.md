# Versions and what is frozen

| Version | What it is | Tag |
|---|---|---|
| `v1.0` | Workflow with one LLM step on version-1 synthetic data (provider, patient, claim and documentation tables). Held-out run 261009_2_api. | `v1.0` (commit 25f5ade; also `heldout-freeze-261009`) |
| `v2.0` | Version-2 workflow: plan-shaped data (`docs/v2_schemas.md`), conditions derived from claims, records requests with limits, code-written summary parts, rule-decided clear cases, Batch API, cache, number check. Runs `261012_8_api` to `261012_18_api` and the code-only runs `261012_*_code`. | `v2.0` |
| `v3.0` | The investigator **agent** design (Milestone 6): a model that chooses its own tools and steps, with a simulated provider office, guardrails, audit log, the results table (`experiments/results.csv`) and the new metrics. Runs `261013_8_api` to `261013_11_api` and the repeats `261013_16_api` to `261013_19_api`. The workflow stays in the repository frozen as `v2.0` and is the comparison arm. | `v3.0` |
| `v2.1` | Workflow on data 2.1: office 2.1 (second records request, note package, audit-trail request), the note rule and fixed v2.1 office policy (`eval/workflow_policy_v21.py`), conditional next steps and the summary lint (`case_summary.py --v21`). Evaluated in #61 (runs `261015_*`, arm W2.1). | `v2.1` |
| `v3.1` | Agent on data 2.1: `note_checks`, `request_audit_trail`, `set_aside`, the `submit_findings` lint, estimate reliability, screen magnitude columns and `priority` ordering. Evaluated in #61 (arm A3.1). | `v3.1` |

A major version marks a change in what the product is (v1 to v2: the data model; v2 to v3: who decides the next step), not a claim that it performs better; on the reserved seeds the agent found fewer upcoders than the workflow.

## Data, workflow and agent share the minor version
Three things carry version numbers: the **data** (generator, schemas and the simulated office), the **workflow** and the **agent**. The major number says what each one is (data 1: the version-1 tables; data 2: plan-shaped tables; workflow 2.x; agent 3.x). The **minor number is shared**: release Y pairs data 2.Y with workflow 2.Y and agent 3.Y, and they are evaluated together on the same fresh seeds. A release that changes only one of them still runs the others on the new data under the same number.

| Release | Data | Workflow | Agent | Status |
|---|---|---|---|---|
| 0 | 2.0 (`docs/v2_schemas.md`, office 2.0) | `v2.0` | `v3.0` | frozen and evaluated |
| 1 | 2.1 (adds the note package, `docs/data_v2_1.md`; office 2.1) | `v2.1` | `v3.1` | frozen and evaluated on ten fresh seeds (#61, [eval61.md](eval61.md)) |
| 2 | 2.2 (realism and data defects, issues #74 to #80; [data_v2_2.md](data_v2_2.md)) | `v2.2` | `v3.2` | frozen once its evaluation is posted: ten fresh seeds, workflow ahead of agent ([eval61.md](eval61.md), [release2_results.md](release2_results.md)) |
| 3 | **2.2 again** (data stays; Simmy's decision, so release 3 compares with release 2 on the same data) | `v2.3` | `v3.3` | built and tested once on ten fresh seeds ([release3_results.md](release3_results.md)): cloned-notes detection first ([#99](https://github.com/simmyhundal/em-upcoding-agent/issues/99), [replay_rules_23.md](replay_rules_23.md)) |
| 4 | 2.2 again | `v2.4` | `v3.4` | tested once on ten fresh seeds ([release4_results.md](release4_results.md)) |
| 5 | 2.2 again | `v2.5` | `v3.5` | tested once on ten fresh seeds ([release5_results.md](release5_results.md)); dollars are the primary score |
| 6 (v4/v5 line) | **4.0** (provider upcoding rates and habits; see below) | `v4.0` | `v5.0` | built, frozen and tested once on ten fresh seeds ([v4_v5_results.md](v4_v5_results.md)); not above zero |

Exception, release 3: the data version stays 2.2, so the workflow and agent number moves (2.3, 3.3) and the data number does not; the shared-minor rule applies again when the data next changes. Data 1 pairs only with workflow `v1.0`. In `experiments/results.csv`, runs so far record the data version as `v1` or `v2` (meaning data 2.0); runs on data 2.1 and later should record the full number.

What a visit's level rests on, by data version: data 1 gives a documented MDM level plus minutes; data 2.0 gives the three MDM elements (the second-highest sets the level, as in real coding) or minutes; data 2.1 and later add a templated note.

## Judge versions
Judges are named after the release they belong to, like the other pieces. `j1`: LLM judge on the evidence card. `j2`: LLM judge plus the tool outputs the author saw. `j2.1` to `j2.3`: the deterministic rule judge (`eval/judge_rules.py`), release 1. **`j3.2`: the rule judge of release 2** (data 2.2, workflow v2.2, agent v3.2), built in [#93](https://github.com/simmyhundal/em-upcoding-agent/issues/93) as `eval/judge_rules_32.py` (`judge_rules.py` stays j2.3, unchanged): its own evidence tiers instead of the writer's rule, citation support, dollar honesty, the note package in the packet, and a reviewer checklist beside the score ([rule_judge_32.md](rule_judge_32.md)); the release 2 evaluation uses it as its only usefulness judge. Not yet checked against a person ([human_spot_check.md](human_spot_check.md)). **`j3.3`: the rule judge of release 3** (`eval/judge_rules_33.py`, built on j3.2 and leaving it unchanged): j3.2 deducted 1.5 from every upcoding call resting on cloned-notes signs with supportive charts, the case release 3 added, so j3.3 adds a "cloning signs" evidence tier ([judge_release3.md](judge_release3.md)). A judge version never changes after it is used: a change ships as a new version, and `experiments/results.csv` records the version beside each score.

## What "frozen" means
- A frozen version's behavior lives behind its version flag (`Office(version="2.1")`, `Environment(version="3.1")`, `case_summary.py --v21`, data `--data-version 2.1`). Release 2 work adds new flags (`2.2`, `3.2`) and leaves the frozen paths alone, so `eval/run_eval61.py` reproduces the #61 runs from their response caches.
- Code under `src/` and `eval/` that produces the v2 results does not change except through a `v2.x` patch: a commit that says what changed and re-runs the affected scoreboard rows.
- Thresholds (screen cutoff 5, rule cutoffs in `src/summary_rules.py` and `src/records.py`) are not re-tuned on seeds 42, 101 or 7. They were set by looking at seed 42 and have been seen on all three since.
- Results from `v1.0` cannot be reproduced on current code (the prompt, packet format and checks changed); their run folders hold the outputs.

## Reserved seeds
Used and retired: 202 and 303 (the Milestone 6 evaluation), 404 to 1313 and 1414 (the release 1 evaluation, #61). Seed 42 stays the development seed. Releases 2 to 5 each named ten fresh seeds on their evaluation issue before generating them (1515 to 5454, in steps of 101); all are development data now. The next fresh seeds start at 5555. From the v4/v5 line on, fresh seeds no longer have to be named on an issue before they are generated (Simmy, 2026-10-20); each run records the seeds it used, nothing is tuned on a fresh seed, and a seed that anything was tuned on is never reported as held out.

## Known limits carried into v2.0
- Synthetic data from one generator family; 8 upcoders per run.
- The v2 schemas (`docs/v2_schemas.md`) were written from general knowledge and have not been reviewed by someone who works with 837, 834 and 835 data (issue 32, backlog).
- The justified level is still drawn first and the MDM elements are built to fit it (issue 45 notes this).
- The AI step makes false accusations at low base rates; the screen sends only part of the upcoders on; usefulness is 3.3 to 3.7 against a target of 4.

## Reproduction
`python eval/make_v2_runs.py` rebuilds the code-only runs (checked: rebuilding run 261012_1_code reproduced the committed files exactly). `python eval/make_v2_ai_runs.py` reruns the AI step; the response caches in each run folder make unchanged runs free.

## Patches since v2.0 (no results changed)
- `summary_rules._rule_headline` crashed or mis-worded when the pooled 99214/99215 rule decided; it now states the pooled counts. Four stored headlines (runs 261012_9_api and 261012_10_api) kept their older wording; no leaning, citation or score changed (regenerated from the response cache and compared).
- `summary_rules.pick_citations` always cites something from the packet's own samples, so a rule-decided summary can no longer be rejected for citing nothing.
- `records.read_chart` was split out of `request_records` so the provider simulator reads charts the same way (outputs verified identical).

## Patches since v3.0 (no results changed)
- `agent_tools.Environment.call` returns `bad arguments` for an `AttributeError` too (issue 85). A live run (`261015_64_api`) crashed when the model passed `submit_findings` a list of strings; the old code could only crash on that path, so no recorded run changes.
- Office 2.1 no longer draws a sample from an empty list when a follow-up has nothing left to send (issue 84). Office 2.0 never reached that branch with an empty list, so frozen results are unchanged.

## Two parallel streams from here
The product now develops on two lines at once, so we can keep learning from both designs:
- **v2.x: the workflow.** Code fixes the order of steps; the model only writes where rules are silent. Baseline `v2.0` (frozen).
- **v3.x: the agent.** A model chooses its tools and steps within caps. Baseline `v3.0` (frozen).

Features roughly mirror one another: a change lands in both streams, or is marked one-stream-only below with a reason. Shared pieces (the data generator, the provider office, the number check, the results table, the judge) change once and are re-run for both. Frozen so far: `v2.0` and `v2.1` (workflow), `v3.0` and `v3.1` (agent); the next releases are `v2.2` and `v3.2`, and the baselines are never edited. New results are compared with the frozen baselines on fresh seeds, using the decision rules fixed in advance in the multi-seed evaluation issue (#61). The reason for keeping the agent in development whatever the comparison shows: an agent should adapt to whatever data and situation it meets, which a fixed workflow cannot, and that has not yet been tested at low base rates or on new kinds of evidence.

Release 2 (merged to main, frozen once its evaluation is posted; was branch `release2-overnight`). Data 2.2 is behind `--data-version 2.2` ([data_v2_2.md](data_v2_2.md)); the frozen paths are unchanged and were checked by regenerating `261015_66_code`, `261015_1_code` and `261012_1_code` and diffing every file, and by replaying the recorded agent run `261015_70_api` through `Environment(version="3.1")` (all 14 findings identical).

| Feature (issue) | v2.2 workflow | v3.2 agent | Reason if one-sided |
|---|---|---|---|
| Screen ranking metrics (#83) | built: columns of `results.csv`, [screen_metrics.md](screen_metrics.md) | same (evaluation only) | shared |
| Screen methods (#88) | `eb_ratio` and `priority` are the release 2 candidates ([screen_methods.md](screen_methods.md)): `flagging.py --method`, v2.2 workflow arms; `riskadj` stays frozen | `screen_providers` with method `eb_ratio` or `priority` in v3.2 | confirmed or rejected on the fresh seeds ([release2_plan.md](release2_plan.md)) |
| Data-quality pre-flight (#81) | built: `flagging.py --preflight` ([data_quality.md](data_quality.md)); the case-summary step does not consume the column yet | built: `data_quality` and `flag_data_issue` tools, hold in `submit_findings`; offline tests only | |
| Fewer model calls in the writer (#91) | built: rules 2.2 (`case_summary.py --v22`, `summary_rules.rule_leaning_22`) decide inconclusive the ambiguous cases where the v2.1 model always said inconclusive; 115 to 11 model calls on the release 1 runs, no leaning changed ([workflow_cost.md](workflow_cost.md)) | n/a: the agent writes its own findings (its cost is #92) | the agent has no rule-then-model writer |
| No LLM usefulness judge in the evaluation (#91, #93) | built: the 2.2 workflow path skips `judge_usefulness.py`; the rule judge runs | #92 | |
| Agent cost (#92) | n/a: the workflow has no agent loop (its cost is #91) | built: $1 cap for 3.2 (`run_agent.EVAL_MAX_USD_32`), no LLM judge (`judge_agent_runs.main(..., "3.2")` rebuilds the view only, replaying office 2.1), usage per turn (`turn_usage.jsonl`), `run_agent.py --model` and `--effort`; measured in [agent_cost.md](agent_cost.md) | agent loop only |

Release 3 (in development, branch `release3-dev`; data stays 2.2, [#99](https://github.com/simmyhundal/em-upcoding-agent/issues/99), [dev_release3.md](dev_release3.md)). Workflow v2.3 and agent v3.3 are built behind flags (`Environment(version="3.3")`, `run_agent.py --version 3.3`).

| Feature (#99) | v2.3 workflow | v3.3 agent | Reason if one-sided |
|---|---|---|---|
| Rules 2.3: cloned-notes signs decide by rule | built: `summary_rules.rule_leaning_23` (late signatures, audit-trail signs, far-above-expected share; chart calls must beat the real peer rate) with `case_summary.py --v23` | built: `hybrid_review` uses rules 2.3, the lint accepts such calls, `SYSTEM_33` explains cloned notes and the chart test | mirrored |
| Screen `eb_ratio_t` (test-line covariate) | built: `screen_methods.score_t`, `flagging.py --method eb_ratio_t` | built: `screen_providers` method `eb_ratio_t` | mirrored |
| Wider list with a light tier | built, **the W2.3 default** (Simmy's decision: more upcoders found, about 94 more honest practices asked on the development seeds): top 10%, ranks 12 to 22 get one request unless the notes show cloning (`eval/workflow_policy_23.py`) | built: the prompt suggests the top 10% and a light touch beyond the first 5%; records budget 22 (v3.0 to v3.2: 15); the agent chooses | mirrored by design (the agent chooses) |
| Audit-trail request on late signatures | built (adds nothing on the development seeds) | the existing `request_audit_trail` tool, prompted | mirrored |

Release 4 (in development; issues #102 to #104, #108). Workflow v2.4 is built behind flags; agent v3.4 has the read-only advisor tool and nothing else new yet.

| Feature | v2.4 workflow | v3.4 agent | Reason if one-sided |
|---|---|---|---|
| Learned stop-or-escalate formula (#108) | built: `eval/workflow_policy_24.py` with `learned`, `src/escalation_policy.py`, `src/policy_24.json`; variants G, L, GL ([learned_policy_plain.md](learned_policy_plain.md)); fresh test on ten seeds: **GL is the v2.4 default** by the pre-registered rule ([release4_results.md](release4_results.md)) | built as **advice only**: tool `advise_next_step` (`Environment(version="3.4")`, `SYSTEM_34`) answers after a first sample; the agent decides (**in the ten-seed test it never called the tool**: [release4_agent_results.md](release4_agent_results.md)) | different mechanism by design: the workflow obeys the formula, the agent is advised |
| Ratio gate on the light tier (#102) | built (variant G, 2.5) | built as **advice only**: `advise_next_step` before any request says ASK or SKIP by the same gate (ratio 2.5 beyond the first 5%), plus the agent's own habit of asking at about 3x expected | the workflow obeys the gate, the agent is advised and chooses |
| Rules first, then spend rounds only where the sample leaves a question (#102) | built (rules 2.3 decide every provider asked; learned stop-or-escalate) | built: **enforced in code** (`submit_findings` refuses until `hybrid_review` has been run on every provider whose records arrived); follow-up only where the first sample leaves a question is a prompt rule in `SYSTEM_34`, measured from the audit log | the rule-application invariant is code; the escalation judgment stays with the agent |
| Silent offices (#103) | moved to release 5 (#109) | moved to release 5 | depends on how non-response is modeled (#68) |
| High-acuity override (#104) | **do not build** (checked: one upcoder and one honest doctor on 20 development seeds) | do not build | evidence too thin to justify a rule in either stream |

Known gaps in the mirror rule (checked 2026-10-18): dispositions for screened candidates (#66) are a refusal gate only in the agent (`set_aside`); the workflow has a post-hoc table (`eval/dispositions_w.py`). The "hybrid review (#49)" and "data-quality pre-flight (#81)" rows above are out of date: both streams now decide with rules first and a model only where the rules are silent, and the workflow's case-summary step applies the pre-flight holds. The agent alone flags data issues (`flag_data_issue`), reads its own estimate reliability, and chooses its own list size. The agent writes its own findings while the workflow's summaries are code-written; judges j3.2 and j3.3 score both.

Release 1 (frozen). Items still planned carry over to `v2.2` and `v3.2`.

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

Release 4 (in development; workflow v2.4 is still a fixed workflow, with one decision made by a learned scoring formula: [learned_policy_plain.md](learned_policy_plain.md); milestone "v2.4 and v3.4"): narrow the wide list for both arms, taking the agent's habits into the fixed workflow ([release4_agent_narrowing.md](release4_agent_narrowing.md)); silent offices; high-acuity override. Fresh seeds only: 1515 to 3434 are development data.

Release 5 (started on branch `release5-dev`; dollars are the primary score from the start, baseline in [release5_dollar_baseline.md](release5_dollar_baseline.md); milestone "v2.5 and v3.5", [#109](https://github.com/simmyhundal/em-upcoding-agent/issues/109)): a recovery model of cloned claims and the dollar reward on the 90% lower bound of the extrapolated estimate; the release 4 dollar documents (`dev_arm_dollars.md`, `rl_escalate_dollars.md`, `rl_ask_dollars.md`) are its groundwork.

| Feature | v2.5 workflow | v3.5 agent | Reason if one-sided |
|---|---|---|---|
| Learned ask-or-skip and stop-or-escalate fitted on net dollars (#109) | built: `eval/workflow_policy_25.py`, `src/policy_25.py`, `src/policy_25.json` (fitted by `eval/export_policy_25.py` on 30 development seeds); chosen start by Simmy after [release5_train.md](release5_train.md) | built (`Environment(version="3.5")`, `SYSTEM_35`; not yet run on the model): the same `src/policy_25.json` as **advice inside the results** of `request_records`, `follow_up_records` and `request_audit_trail` plus an `ask_advice` column in the screen (#111); an upcoding call from the rules that the chart rule also supports is **binding** unless `override_reason` names a claim id, data-quality flag or note sign (#112); practice status and rounds sent shown every turn (#113); advice use and overrides logged in `advice_log.json` | the workflow obeys the formulas; the agent is advised and, where code can enforce an invariant, bound |

## The v4/v5 line: data 4.0, workflow v4.x, agent v5.x
Decided 2026-10-20 (Simmy): a significant shift in the data model and the score, so the majors move. Release Y on this line pairs **data 4.Y, workflow v4.Y and agent v5.Y** (the same shared-minor rule as data 2.Y, v2.Y and v3.Y). Milestone 15 was renamed from "v2.6 and v3.6" (never built) to "v4.0 and v5.0", and its issues #116, #117 and #118 moved with it.

- **Data 4.0** (built, [data_v4_0.md](data_v4_0.md); `src/generate_v4.py`, development seeds `d4_*`, [statistics](data_v4_0_stats.md)). Every provider has an upcoding rate. Exactly 8 upcoders per dataset, each with a rate from 15% to 40% and one habit: systematic (always bills 99214 for 99213-level visits), opportunistic (inflates only borderline visits) or template-driven (an EHR default to a higher level, no intent; still a target, and lighter actions for it are #123). Non-upcoders' rate is centred between -15% and +15%. The answer-key `role` stays binary (the planted 8) with the rate beside it. Opportunistic upcoding needs a continuous per-visit complexity from which the justified level is derived, reversing the order noted in issue 45. Data 2.x stays reproducible behind `--data-version`.
- **Score 4.0** (built, [score_40.md](score_40.md); `eval/score_40.py`; free check on releases 2 to 5: [score_40_check.md](score_40_check.md)): dollars recovered (the estimate from any provider sent a demand, not capped at the true overpayment, since a payer has no answer key) minus staff-hours cost minus provider abrasion (weighted by the true net rate). Later score versions add an SIU hours cap, appeals and a recovery tool. Full specification and the order of issues: [v4_v5_plan.md](v4_v5_plan.md).
- **Screen (#127, [screens_v4.md](screens_v4.md), [downstream check](screens_v4_pipeline.md)):** `eb_upper_t` (the shrunk share billed 99214 or 99215, with the test line) is the chosen default: workflow built (`flagging.py --method eb_upper_t`, `src/screen_methods_v4.py`); agent: wired when agent v5.0 is built in #128 (one-sided until then: the agent version does not exist yet).
- **Workflow v4.0 (built and frozen, [w_loop_v4.md](w_loop_v4.md), issue #131):** the `eb_upper_t` list, rules 4.0 (the chart test pooled over 99214 and 99215), a first sample of 30 random charts, the ask-or-skip refitted on score 4.0 (`src/policy_40_ask.json`, fitted on development batches 1 to 4), no escalation, and a demand only when the payer's estimate of the recovery covers the staff cost of a demand (`eval/workflow_policy_40.py`, `FROZEN_V40`; API-free). On 100 development seeds: score 4.0 per seed +\$549 against -\$10,820 for the frozen v2.5 (100 of 100 seeds better); out of sample (batches 5 to 10) +\$426 against -\$236 for the version before its ask model. Agent v5.0 mirrors it in its tools (built: `Environment(version="5.0")`; the eb_upper_t screen, rules 4.0, ask advice refitted on score 4.0, advice STOP after the first sample, the demand floor and the style repair of [agent_text_replay.md](agent_text_replay.md); near parity, not parity: a scripted agent that follows the advice asks the same providers as the workflow on 8 of 8 development seeds and calls the same providers on 6 of 8 (`eval/agent50_parity.py`); run once on the ten fresh seeds, issue #128). On the ten fresh seeds workflow v4.0 scored -\$1,161 per seed against -\$11,185 for the frozen v2.5, and agent v5.0 -\$781 (not above zero, as on the development pool for the workflow: [w_loop_v4.md](w_loop_v4.md)).
- **Agent v5.1 (built, not run; [agent_v51.md](agent_v51.md)):** mirrors workflow v4.1 (H23, N = 4; [w41_freeze.md](w41_freeze.md), [w41_fresh_result.md](w41_fresh_result.md)) in `Environment(version="5.1")`: ASK advice for the first 4 listed providers only, the loosened rules 4.0 chart test, and a once-only near-miss extension of 30 random charts (`demand_check` in `hybrid_review`; the extension gate in `request_records`), with the demand floor and binding rule kept. A scripted agent that follows the advice matches workflow v4.1 on 20 development seeds (asked 20 of 20, extended and called 19 of 20). The paid run on the ten test seeds waits for an estimate and an OK.
- **Reference arms:** frozen v2.5 and v3.5 run unchanged on data 4.0 and are scored with the new score, which separates the data change from the method change; so v4.0 and v5.0 may already carry new features.
