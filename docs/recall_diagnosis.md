# Why recall is low on data 2.2 (diagnosis, free)

[Back to the README](../README.md)

Question from the seed 1515 smoke run: both arms found about 1 upcoder per seed on data 2.2, against about 4 per seed for workflow v2.1 on data 2.1. Checked on the development seed 42 (data 2.1 `261015_1_code` against data 2.2 `261016_1_code`), same screen (`eb_ratio`, top 5%), same office policy, same rules; no model calls, no cost.

## Result
The cause is data 2.2's honest coding noise acting on the chart rule, not the screen, the writer or the agent.

| On seed 42 | Data 2.1 | Data 2.2 |
|---|---|---|
| Upcoders in the top-5% list (of 8) | 7 | 6 |
| Honest providers' billed 99215 claims that were billed above the justified level (answer key) | 0.0% | **33.0%** |
| Peer "documented below billed" rate on 99215 charts (the control sample the rules compare against) | 10.3% | **53.6%** |
| Provider 1000000143: documented 99215 charts below billed | 7 of 10 (70%) | 6 of 9 (67%) |
| Rule outcome for 1000000143 | upcoding (70% is over 40% and over 3 times the peer rate) | inconclusive (67% is not over 3 times a 54% peer rate) |
| Workflow found | 3 of 8 (`261015_3_api`, v2.1) | 1 of 8 (`r2w_dev42`) |

Why: 99215 is only 4 to 6% of visits, so even a small honest up-slip rate from 99214 (about 2% of visits) makes a third of the billed 99215 claims wrong, and chart reading noise adds more. The chart rule in `src/summary_rules.py` (an upcoder needs at least 40% unsupported **and** at least 3 times the peer rate; `UP_RATE`, `UP_VS_PEER`) was set on clean data where the peer rate was about 10%. With a peer rate of 54% the second test cannot be met (it would need over 100%), so charts can no longer flag an upcoder, however clear they are. The agent reads the same peer rates in its evidence card and meets the same wall.

The evidence did not get worse: the upcoder's own chart rate is about the same (67% against 70%). The baseline moved. With 9 charts, 6 of 9 against a 54% peer rate is also statistically weak, so a threshold fix alone helps only so much: charts are genuinely less informative once honest providers make this many errors.

## What it means
- On data 2.2 the claims-side screen still ranks upcoders well (6 of 8 in the top 5%), but converting that into confirmed calls needs evidence the noisy charts mostly cannot give. The remaining signals are the note checks (found 1 of the 6 on seed 42) and the agent's judgment.
- A comparison of workflow and agent on this data compares two arms that both find about 1 upcoder per seed; the planned test would have little power.
- Whether 33% of honest 99215 claims being wrong is realistic is not established. The sources found ([data_v2_2.md](data_v2_2.md)) give a payment error rate of 6 to 7% of dollars for established office visits and a 42% incorrectly-coded rate (both directions) for all Medicare E/M claims in 2010; no source splits error by code level.

## Options (decision for Simmy)
1. **Make the chart rule noise-aware** (new rules version for workflow v2.2, tuned on development seeds only): replace "3 times the peer rate" with a test against the peer rate that accounts for the number of charts, for example a binomial or exact test at a stated level, and require a minimum excess. The frozen `rule_leaning` stays untouched. This is the right fix if the noise level is believed.
2. **Lower the default honest noise** (for example a miscode rate of 0.03 to 0.04) so the peer rate stays near 20 to 30% and the old rule can fire. Cheaper, but chosen to make the rule work, and the sources do not say what the right rate is; if used, say so.
3. **Keep both as they are** and report that on realistic noise neither arm finds many upcoders from charts; the evaluation then answers a different question (which arm does better when evidence is weak) and needs more seeds for any significance.

Free to try: 1 and 2 on the development seeds (42 and the defect twin), counting upcoders found by the workflow with no model calls. Not done yet.

## Result of option 1 (built, tested free on the development seed only)

**What changed (rules 2.2, `summary_rules.rule_leaning_22`; the frozen `rule_leaning` is untouched):** the peer unsupported rate is capped at 15% (the rule's own "documentation supports billing" line, `LOW_RATE`) before the rule runs. No new tuned number. The 54% peer rate comes from the control sample's 99215 claims, mostly from low-volume billers where a third are honest up-slips; a provider billing 99215 at several times its expected share is mostly billing true 99215s, so its charts should look cleaner than that. Below the cap (every release 1 run) nothing changes: regenerating the 26 stored #61 workflow summary files with rules 2.2 changes **0 leanings** (`docs/workflow_cost.md`; the text of 5 summaries gains a note that the baseline was capped). The v3.2 agent's `hybrid_review` uses the same rules.

**Development seed 42, data 2.2, workflow v2.2 with the eb_ratio top-5% list (11 providers, no model calls, $0):**

| Rules | Upcoders found (of 8) | Honest accused |
|---|---|---|
| Before (`r2w_dev42`) | 1 | 0 |
| Capped peer rate (`r2w_dev42b`) | **4** | 0 |

The four are the three honest-notes upcoders reached by charts (1000000143, 1000000215, 1000000088) and the one cloned-notes upcoder reached by the note rule (1000000095). The other two upcoders in the list are cloned-notes upcoders whose charts support the billed level (45 charts, 5% below) or never came back; no chart rule can reach them. That is the cloned-notes problem (#57), not this one. The sixth and eighth upcoders sit outside the top 5%.

**Honest limits.** The cap was chosen after seeing the failure on this one seed, but it reuses an existing constant instead of a new tuned number; one dataset and three chart-detected upcoders cannot prove it generalizes, and the fresh seeds are where that gets tested. The seed 1515 smoke result (`r2w_1515`, 1 found) was produced with the old rules and is superseded; it is not rerun with them, so no evaluation seed informed this change. Even so, the chart evidence is weak (6 of 9 against honest providers at 15%), so a false accusation among high-share honest doctors is possible; seed 42's list has none.

## First evaluation-style seed with the final rules (seed 1515; issue 98; run 2026-10-17)

Both arms on the final code (commit 3b38d9e), eb_ratio top 5%. Seed 1515 was not used to choose the cap.

| Arm | Cost | Upcoders found (of 7 counted) | Honest doctors called |
|---|---|---|---|
| Workflow v2.2 (`r2w_1515`) | $0.00 | 1 | 1 |
| Agent v3.2, Opus medium (`r2a_1515`) | $0.353 | 1 | 1 |

What limited recall: the top-5% list holds 3 of the 7 upcoders; of those, two (1000000135 and 1000000188) came back with too few records to judge, and the third (1000000138) was found through its notes. What limited precision: the one honest doctor both arms called (1000000213) has 4 of 6 documented 99215 charts below the billed level (67%), a chance cluster that the capped baseline (15%) cannot tell from an upcoder. The old baseline would not have called it. This is the price of the cap, seen on the first seed that did not help choose it: seed 42 gained three true calls and no false one; seed 1515 gained no true call and one false one. The honest summary of the rule so far is **real but unproven, with a false-accusation risk that is concentrated where few 99215 charts come back**. Raising the minimum number of documented 99215 charts above 6 would exclude this case, but choosing it now would be tuning on an evaluation seed; if wanted, it is a decision for before the next batch, taken on the development data only.
