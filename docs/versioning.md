# Versions and what is frozen

| Version | What it is | Tag |
|---|---|---|
| `v1.0` | Workflow with one LLM step on version-1 synthetic data (provider, patient, claim and documentation tables). Held-out run 261009_2_api. | `v1.0` (commit 25f5ade; also `heldout-freeze-261009`) |
| `v2.0` | Version-2 workflow: plan-shaped data (`docs/v2_schemas.md`), conditions derived from claims, records requests with limits, code-written summary parts, rule-decided clear cases, Batch API, cache, number check. Runs `261012_8_api` to `261012_18_api` and the code-only runs `261012_*_code`. | `v2.0` |
| `v3.0` | The investigator **agent** design (Milestone 6): a model that chooses its own tools and steps, with a simulated provider office, guardrails, audit log, the results table (`experiments/results.csv`) and the new metrics. Runs `261013_8_api` to `261013_11_api` and the repeats `261013_16_api` to `261013_19_api`. The workflow stays in the repository frozen as `v2.0` and is the comparison arm. | `v3.0` |

A major version marks a change in what the product is (v1 to v2: the data model; v2 to v3: who decides the next step), not a claim that it performs better; on the reserved seeds the agent found fewer upcoders than the workflow.

## Data, workflow and agent share the minor version
Three things carry version numbers: the **data** (generator, schemas and the simulated office), the **workflow** and the **agent**. The major number says what each one is (data 1: the version-1 tables; data 2: plan-shaped tables; workflow 2.x; agent 3.x). The **minor number is shared**: release Y pairs data 2.Y with workflow 2.Y and agent 3.Y, and they are evaluated together on the same fresh seeds. A release that changes only one of them still runs the others on the new data under the same number.

| Release | Data | Workflow | Agent | Status |
|---|---|---|---|---|
| 0 | 2.0 (`docs/v2_schemas.md`, office 2.0) | `v2.0` | `v3.0` | frozen and evaluated |
| 1 | 2.1 (adds the note package, `docs/data_v2_1.md`; office 2.1) | `v2.1` | `v3.1` | built; not yet evaluated (#61) |
| 2 | 2.2 | `v2.2` | `v3.2` | planned |

Data 1 pairs only with workflow `v1.0`. In `experiments/results.csv`, runs so far record the data version as `v1` or `v2` (meaning data 2.0); runs on data 2.1 and later should record the full number.

## What "frozen" means
- Code under `src/` and `eval/` that produces the v2 results does not change except through a `v2.x` patch: a commit that says what changed and re-runs the affected scoreboard rows.
- Thresholds (screen cutoff 5, rule cutoffs in `src/summary_rules.py` and `src/records.py`) are not re-tuned on seeds 42, 101 or 7. They were set by looking at seed 42 and have been seen on all three since.
- Results from `v1.0` cannot be reproduced on current code (the prompt, packet format and checks changed); their run folders hold the outputs.

## Reserved seeds
Seeds 202 and 303 were reserved and have now been used and seen (the Milestone 6 evaluation); they are retired. Seeds 404, 505 and 606 are the new reserved seeds: not generated or looked at, for the next version's evaluation. Generate them only for that evaluation, with the settings in `eval/make_v2_runs.py`.

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

## Two parallel streams from here
The product now develops on two lines at once, so we can keep learning from both designs:
- **v2.x: the workflow.** Code fixes the order of steps; the model only writes where rules are silent. Baseline `v2.0` (frozen).
- **v3.x: the agent.** A model chooses its tools and steps within caps. Baseline `v3.0` (frozen).

Features roughly mirror one another: a change lands in both streams, or is marked one-stream-only below with a reason. Shared pieces (the data generator, the provider office, the number check, the results table, the judge) change once and are re-run for both. Each stream's next release is `v2.1` and `v3.1`; the baselines are never edited. New results are compared with the frozen baselines on fresh seeds, using the decision rules fixed in advance in the multi-seed evaluation issue (#61). The reason for keeping the agent in development whatever the comparison shows: an agent should adapt to whatever data and situation it meets, which a fixed workflow cannot, and that has not yet been tested at low base rates or on new kinds of evidence.

| Feature (issue) | v2.1 workflow | v3.1 agent | Reason if one-sided |
|---|---|---|---|
| Richer claim-versus-note checks (#57) | built: note rule, office 2.1 policy (`eval/workflow_policy_v21.py`); not yet evaluated | built: `note_checks` and `request_audit_trail` tools, prompt; not yet evaluated | |
| Call the honest-notes upcoders we reach (#58) | planned | planned | |
| Low base rate safeguards (#59) | planned | planned | |
| Summary quality and judge calibration (#60) | planned | planned | |
| Second records request (#67) | built (office 2.1; policy sends a targeted second request) | built (office 2.1) | |
| Conditional next steps and the pre-submission lint (#63) | built (`case_summary.py --v21`: conditional steps, model-written summaries that fail a hard check are repaired by code) | built (`submit_findings` lints and refuses; steps conditional) | |
| Dispositions for screened candidates (#66) | partial: rule reason strings only; no disposition table yet | built (`set_aside`, refused without it) | agent-only for now; workflow mirror still to build |
| Estimate reliability gate (v3.1) | n/a (the workflow does not quote estimates) | built (`reliable`, `stratum_reviewed`; the lint refuses quoting an unreliable estimate) | agent-only by design |
| Screen table magnitude columns and `priority` ordering (#48) | planned: `priority` as the workflow's ordering | built (ratio, excess claims, low-complexity share, excess dollars; `method="priority"`) | mirrored by ordering |
| Hybrid review (#49) | planned | planned (tool exists) | |
| Screen cutoff choice (#48) | planned: budget-based rule | planned: agent chooses | mirrored by design |
| Multi-seed paired evaluation (#61) | planned | planned | shared |
