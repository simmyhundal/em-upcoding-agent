# The release process

[Back to the README](../README.md) · [decision log](decision_log.md) · [seed roles](seeds.md) · [versions](versioning.md)

How a release of this project is run, so it can continue with little input from Simmy. Written 2026-10-22 from the v4.0 to v5.1 cycle. To run the whole cycle in a new session, use the command **`/run-release`** (the skill in `.claude/skills/run-release/SKILL.md` reads this page and CLAUDE.md and follows it).

A release Y pairs data 4.Y, workflow v4.Y, agent v5.Y and a score version S4.Y that is fixed before the work starts. Short names: S4.x score, D4.x data, W4.x workflow, A5.x agent (see the [glossary](glossary.md)).

## The steps

**1. Core stories.** File issues in the new release's milestone that fix the shortcomings of the last release, from what its test showed and hypotheses about the causes. Before any work, write down:
- *The yardsticks.* The last release's workflow on the same new test seeds (free to run), the do-nothing baseline (zero), and the **oracle**: the best conceivable score under the same score version, with the same costs a tuned arm pays, **triage included** (it lists, and so triages, the providers it pursues). Report "score divided by oracle score" with the oracle's definition and seeds (see [ceiling benchmarks](ceiling_benchmarks_w41.md)). The oracle uses the answer key, so it is an upper bound.
- *The seed plan.* Allocate a development pool, a confirm pool and a **new, unrun test pool**, keep one reserved pool untouched, and record their roles in the [seed registry](seeds.md). Do not reuse a test pool unless it is declared a second look.
- *The power plan.* Estimate how many seeds a plausible effect needs (paired per-seed differences have a spread of about $800 to $1,300 under S4.0, so 20 to 60 seeds detect only large effects; about 100 seeds are needed for an effect of about $300 per seed) and size the pools for it. A single pre-declared confirmatory test on unused seeds avoids most of the multiple-comparison penalty.

**2. Setting (optional).** Decide the score and data versions for the release before the hypothesis work, when the last release exposed a deficiency in them. Re-score the frozen references (the last workflow and agent) on the new score and data and publish that table first, so the new numbers have something to compare with. Keep the old score and data versions frozen: a new version is a new module. An assumptions track runs beside the loop: each cycle, source at least one unverified parameter (the copy fee, minutes per task, dollars per provider), and the market research track (milestone "Payer stock-price drivers") feeds this step.

**3. Work the core stories.** Develop hypotheses on the workflow arm (free), one change each against the current best, on the development pool. Rules:
- Choose any parameter on the *select* batches; test once on a *confirm* batch declared in advance; never adjust after looking.
- Count every hypothesis tried and use the Bonferroni bar (0.05 divided by the number tried); report a result below the bar as a result and anything else as a lead.
- **Run the control for any mechanical gain.** A shorter list, fewer charts or no asks are acceptable ways to raise the score, but the same saving applied to the baseline (for example H8 with a 4-provider list) must be run, so the gain is split into what is mechanical and what is better asking.
- Write the result of each hypothesis in `docs/w_loop_v4*.md`, comment on the issue, and merge docs and result files.

**4. Freeze and test.** Write a freeze declaration (`docs/w41_freeze.md` is the template) before any run on the test seeds: what is frozen, the seeds, the arms, the comparisons and the pass criterion ("marked improvement": a stated dollar gain per seed and a p-value). Run the frozen workflow once on the new test seeds, against the **stored** result of the previous workflow (never re-run an earlier arm) and its same-list control. If it misses the criterion, reopen the core stories; **a reopen spends test seeds**, so decide in advance how many attempts are allowed and allocate new test seeds for each.

**5. Agent at parity.** Build the agent arm to mirror the frozen workflow in its tools. Report parity from a scripted agent that follows the advice, on development seeds only (same asks, same calls, same score, as match rates), and a cost estimate for the paid run from the previous agent's recorded usage.

**6. Run the agent on the test seeds.** The only step that costs money: show the estimate and the cap, get Simmy's approval, then run once. Compare it with the workflow and with the stored results of the other arms. The previous agent is compared indirectly, through the previous workflow that was run on the same seeds for free (the project is price sensitive); the previous agent's own stored result is used if its seeds are the same, and it is never re-run.

**7. Close out.** Update the README table and summary, the figures (progression slide, workflow and agent figures, waterfall), `docs/versioning.md`, the results pages and the seed registry; write the release notes; **tag and publish the GitHub releases**; clean up the milestone and issues; record in the decision log; note what each hypothesis taught so the next cycle starts from it. Step 7 of one cycle is the start of the next.

## Who decides what

Decided 2026-10-22 so work can continue when Simmy is busy.

**Autonomous (do it, then log it in [decision_log.md](decision_log.md)):** free runs and analysis; docs, notes and issues; opening and merging pull requests when the tests pass; **merging edits that touch frozen-version code paths** (refactors and new options, as long as the frozen version still reproduces: its tests and a replay pass); **tagging and publishing GitHub releases**; milestone and issue cleanup; building the next arm.

**Ask first:** a **paid run** (state the estimate and the cap first); deleting a repository or a branch other than a merged branch; anything Simmy has asked to hold.

**Never:** changing a tagged version's results (a frozen version is reproduced by hash and by replay; behaviour changes go behind a new version flag, as CLAUDE.md says), reading the answer key in an arm or its tools, tuning on a test seed and calling it held out, generating or running the reserved pool before the freeze, printing or committing the key in `.env`.

A spend cap applies per release (the agent run's batch cap is the guide; the v5.1 run cost $1.24). If a decision is not covered here, take the cautious option and put it in the log for review.

## What each step produces
Core stories: issues, the yardstick table, the seed and power plans. Setting: re-scored references. Loop: per-hypothesis docs and result files. Freeze: the declaration and the result page. Parity: the parity numbers and the estimate. Paid run: the result page and the cost. Close-out: the README, figures, release notes, tags, the registry and the log.
