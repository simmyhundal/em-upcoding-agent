# Paid agent runs: what is kept so a reader can audit them

[Back to the README](../README.md) · [agent v5.2](agent_v52.md) · [v4.2 and v5.2 test result](v42_test_result.md)

**What this page is.** The three paid agent runs on fresh test seeds (agent v5.0, v5.1 and v5.2, one run per seed, ten seeds each) leave a trace; this page says what is committed under `experiments/` and what it shows. A score alone cannot prove the model followed the intended workflow, so the tool-by-tool record is kept.

| Version | Folders | Seeds | Spend |
|---|---|---|---|
| Agent v5.0 | `experiments/fra50_<seed>` | 5555 + 101j (data 4.0) | $1.14 |
| Agent v5.1 | `experiments/fra51_<seed>` | 5555 + 101j (data 4.0) | $1.242 |
| Agent v5.2 | `experiments/fra52_<seed>` | 4700 + 37j (data 4.2) | $1.781 |

In each folder: `audit.jsonl` (every tool call with arguments and result, in order), `office_transcript.jsonl` (every request, follow-up and answer from the simulated provider office), `agent_run.json` (stop reason, turns, tool calls, spend, model), `turn_usage.jsonl` (tokens and dollars per turn), `agent_notes.txt` (the model's own notes), `case_summaries_checked.jsonl` (its submitted findings after the checks), `set_aside.json`, `advice_log.json`, `fwa_lane.json` (agent v5.2: the lane as scored), `results.json`. Nothing in them is an answer-key file or a credential (`results.json` holds evaluation counts for the data 4.0 runs).

**Run settings.** Model `claude-opus-5-5`, effort low, one run per seed, $1 cap per run. System prompts, by SHA-256 of the text in `src/agent.py` (first 16 hex digits): `SYSTEM_50` a79f42ede9f03f4b, `SYSTEM_51` 21a115e9bbf8e1fd, `SYSTEM_52` ca1b32eef05f11b2.

**What is not here.** Repeat runs on the same seed (run-to-run variance is unmeasured, [#187](https://github.com/simmyhundal/em-upcoding-agent/issues/187)) and the raw model messages.
