# Release 4.2 and 5.2: step 1 (core stories, yardsticks, seed and power plan)

[Back to the README](../README.md) · [process](process.md) · [reflection after v4.1 and v5.1](reflection_v41_v51.md) · [seed roles](seeds.md)

Written 2026-10-23 from the reflection of the last cycle. Versions to be built: D4.2 (data), S4.2 (score), W4.2 (workflow), A5.2 (agent). Nothing here needs a paid run.

## Core stories (milestone "v4.2 and v5.2")
Ordered by what changes the answer most:
1. **[#173](https://github.com/simmyhundal/em-upcoding-agent/issues/173) D4.2: no binary upcoder label**, continuous truth for upcoding and fraud, waste and abuse, abrasion when the true level does not justify pursuit. Everything else is measured on it.
2. **[#178](https://github.com/simmyhundal/em-upcoding-agent/issues/178) S4.2: the commercial profile as the primary score**, with [#136](https://github.com/simmyhundal/em-upcoding-agent/issues/136), [#145](https://github.com/simmyhundal/em-upcoding-agent/issues/145) and [#146](https://github.com/simmyhundal/em-upcoding-agent/issues/146) (scale and look-back, dollars per provider, commercial profiles) as the parameters to source.
3. **[#137](https://github.com/simmyhundal/em-upcoding-agent/issues/137) and [#144](https://github.com/simmyhundal/em-upcoding-agent/issues/144): D4.2 calibration** (habit shares, noise, date range; the planted lab-line link).
4. **[#166](https://github.com/simmyhundal/em-upcoding-agent/issues/166): list sizes 2 and 3**, and the 4-provider-list control, on the new data.
5. **[#66](https://github.com/simmyhundal/em-upcoding-agent/issues/66) and [#100](https://github.com/simmyhundal/em-upcoding-agent/issues/100)**: leftovers of the last cycle (the workflow's disposition table is built; #100's roles refactor is merged).
6. **Measurement:** [#185](https://github.com/simmyhundal/em-upcoding-agent/issues/185) seed and power plan, [#186](https://github.com/simmyhundal/em-upcoding-agent/issues/186) score over oracle score, [#187](https://github.com/simmyhundal/em-upcoding-agent/issues/187) agent run-to-run variance (paid), [#188](https://github.com/simmyhundal/em-upcoding-agent/issues/188) independent replication. Customer track: [#189](https://github.com/simmyhundal/em-upcoding-agent/issues/189).

## Yardsticks for the release's test
- The previous release's workflow, **W4.1, re-run on the new test seeds** (free); W4.1 with the same list as the control for any mechanical gain.
- **Zero** (do nothing).
- **The oracle with triage** under S4.2 and D4.2, reported as score over oracle score ([#186](https://github.com/simmyhundal/em-upcoding-agent/issues/186)); the oracle uses the answer key and is an upper bound. For reference, under S4.0 and D4.0 the oracle was $2,775 to $4,461 per seed and W4.1 about $1,103 per seed on the development seeds ([ceiling_benchmarks_w41.md](ceiling_benchmarks_w41.md)).
- The previous agent (A5.1) is not re-run; the new agent is compared indirectly, through W4.1 on the same seeds.

## Seed plan (to be recorded in the registry when D4.2 is generated; [#185](https://github.com/simmyhundal/em-upcoding-agent/issues/185))
- **D4.2 pools:** a development pool of 100 seeds (select), a separate confirm pool of 60 to 100 read once per decision, a test pool of ten that nobody has run, and one reserved pool. Pool seeds are keyed by data version, so numbers may repeat across versions; the dev-loop guard becomes a registry check.
- **Carried over:** the D4.0 reserved pool (6565 to 7474) is unrun because the paid agent step of v4.1 and v5.1 was not approved (decision log, 2026-10-23). It stays reserved: use it once for the workflow and the agent together if that step is ever approved.
- **The v4.1 and v5.1 numbers** are second-use results on the W4.0 test seeds (final development run), not a true test.

## Power plan
Paired per-seed differences under S4.0 had a spread of $800 to $1,300; effects found were $160 to $400 per seed. Detecting $300 per seed at 80% power needs about 100 seeds at the 0.05 level and about 200 at the 0.005 bar. So the loop's hypotheses are tested on the 100-seed development pool and a 100-seed confirm pool; a single pre-declared confirmatory test per decision on unused seeds replaces repeated looks. The spread under S4.2 and D4.2 is re-measured on the first 20 seeds before fixing the sizes.
