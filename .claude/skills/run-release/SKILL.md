---
name: run-release
description: Run the full release process of this project (core stories, setting, hypothesis loop, freeze and test, agent parity, paid agent run, close-out). Use when the user types /run-release or asks to run the full release process.
---

Run one full release cycle of this project by following `docs/process.md` and `CLAUDE.md`, in order. Start by reading both, the open milestone (`gh issue list`), `docs/seeds.md`, `docs/decision_log.md` and the latest `docs/releases/` notes, then say which step the project is at and what you will do next.

Rules that hold throughout:
- The step list, the yardsticks (previous workflow on the same test seeds, zero, the oracle with triage), the seed plan, the control for mechanical gains and the freeze declaration are in `docs/process.md`. Declare before you run; never tune on a test seed; never re-run an earlier arm (use its stored result).
- Work autonomously on everything the process lists as autonomous, using subagents for long runs, and log each important event in `docs/decision_log.md`.
- Stop and ask Simmy only at the paid run: state the estimate and the cap first. Report progress in short messages that lead with the result.
- Finish with the close-out (README, figures, notes, tags and releases, registry, log) and a short summary of what changed and what is next.

If the argument names a step or an issue (for example `/run-release step 3`), start there.
