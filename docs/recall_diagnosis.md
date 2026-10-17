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
