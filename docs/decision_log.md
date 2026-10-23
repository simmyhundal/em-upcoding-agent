# Decision log

[Back to the README](../README.md) · [process](process.md)

Important events for Simmy to review: releases and tags, merges that touch frozen-version code paths, paid runs, freezes, seed pools burned, and decisions on score or data versions. Newest first. Autonomy rules are in [process.md](process.md).

| Date | Event | Detail |
|---|---|---|
| 2026-10-23 | New public repository: em-prepay-agent (prepay, pend and request records, starts on data 4.2) | After Maxine's note asking for a prepay (upstream, less abrasive) product, Simmy chose prepay point 4 and a new public repository (MIT, same copyright), created at https://github.com/simmyhundal/em-prepay-agent. It depends on this repository's generators at a pinned commit (`GENERATOR_PIN`); it does not fork them. Plan, score P1.0 and first reference arms are there; discovery note and copy-list are `docs/prepay_discovery.md` and `docs/prepay_copylist.md` here (PR 193). |
| 2026-10-23 | Data 4.2 merged (PR 192) | Generator, office 4.2, answer key without a role, metrics and adapter, reference arms on 20 development seeds; calibration of habit shares, the lab-line and date range (issues 137, 144) and the seed plan (issue 185) are still open. |
| 2026-10-23 | Prepay repository proposed: pend and request records, starts on data 4.2 | After Maxine's note asking for a prepay (upstream, less abrasive) product. Simmy chose prepay point 4 (pend and request records) and a new public repository built on this one. Draft discovery note and copy-list in `docs/prepay_discovery.md` and `docs/prepay_copylist.md`; the repository is not yet created. |
| 2026-10-23 | True test of v4.1 and v5.1 deferred; paid agent step not approved | Simmy did not approve the paid agent run on the reserved pool (6565 to 7474) to save money. The pool stays unrun so it can be used once for the workflow and the agent together. The README and notes describe v4.1 and v5.1 as second-use results on the W4.0 test seeds. |
| 2026-10-22 | Releases v4.1 and v5.1 tagged and published | Workflow v4.1 (+$1,003 per seed on the test seeds, found 9 of 80) and agent v5.1 (+$743 per seed, found 10 of 80); notes in `docs/releases/`. Both are not distinguishable from zero; one seed carries each total. |
| 2026-10-22 | Paid run: agent v5.1 on seeds 5555 to 6464 | $1.242 for ten runs (estimate $1.7, cap $4), approved by Simmy; `docs/a51_fresh_result.md`; recorded as a second use in the seed registry. |
| 2026-10-22 | Merge touching agent code paths: PRs 171 and 179 | 171 keeps the answer key's roles out of `Environment` (behaviour-preserving, replays identical); 179 builds agent v5.1 behind its own version flag. Agent v5.0 and v3.x unchanged. |
| 2026-10-22 | W4.1 frozen and tested | H23 at N = 4, declared in `docs/w41_freeze.md` before the run; test seeds 5555 to 6464 (second use). Criterion (+$500 per seed over W4.0 and p < 0.05) met. |
| 2026-10-22 | Seed registry merged (PR 180) | `experiments/seed_registry.json` and `docs/seeds.md`; the development loop and fresh-run scripts now check seed roles. |
| 2026-10-22 | Releases v4.0 and v5.0 tagged and published | Notes in `docs/releases/`; the v4/v5 line merged earlier (PR 138). |
| 2026-10-21 | Paid run: agent v5.0 on seeds 5555 to 6464 | $1.14 for ten runs, approved by Simmy (issue 128); first use of the test seeds. |
