# Agentic E/M upcoding detection

A postpay upcoding investigator for payment integrity (PI) teams. It audits synthetic Medicare-style paid claims to recover overpayments:

- 📄 **Claims:** find E/M (Evaluation and Management) upcoding, an office visit billed above its supported level, and visits billed that never happened;
- 🔽 **Screen:** rank providers by billing against what their patients predict, and count visits billed per day;
- 📁 **Charts:** request charts from the providers it picks and follow up on what comes back;
- ✏️ **Summaries:** check charts against claims, set a leaning (upcoding, unclear, normal) and write case summaries;
- 🧭 **Who decides:** choose next steps within caps, then hand drafts to PI teams to review;
- 📊 **Results:** score in net dollars against the answer key.

Two designs run on the same data: a **[workflow](docs/concepts/workflow-and-agent.md)** (code fixes the steps; a learned formula picks whom to ask) and an **[agent](docs/concepts/workflow-and-agent.md)** (a model picks its own steps within caps, with the same formula as advice).

Both are scored by the **RL score** ([score 4.2](docs/score_42.md)), net dollars per seed, the reward the policies are trained on:

```
RL score = Recovery - Staff cost - Abrasion

Recovery   = 90% lower bound of the overpayment a random chart sample supports, per provider sent a demand
Staff cost = hours x wage for triage, requests, chart review, demands; model dollars
Abrasion   = $43.84 per request round + $2,000 per demand, weighted by how honest the provider is
```

![Score 4.2 for agent v5.2 on ten test seeds: recovery, staff cost and abrasion down to the net score](docs/images/score_waterfall.svg)

<!-- score:start -->
- **Recovery +$391,910:** $370,474 from the visits-per-day check, the rest from reviewing billing levels.
- **Staff cost -$16,744:** charts $4,079, requests $1,546, demands $9,924, triage and model $1,196.
- **Abrasion -$3,051:** the cost to providers of requests and demands.
- **Net $372,114** for agent v5.2 over ten test seeds.
<!-- score:end -->

## Results
<!-- tldr:start -->
Every row uses score 4.2 (data 4.0 rows are re-scored from stored runs) beside the oracle of its data. Workflow v4.2 and agent v5.2 reach 60% and 59% of it on data 4.2, 94% of their recovery from a visits-per-day check on a signal the synthetic data makes clean; workflow v4.1 reaches 25% on data 4.0.
<!-- tldr:end -->

<!-- release23:start -->
| Version | [Data](docs/glossary.md#results-columns "Data version; ten test seeds each. Rows on different data are not directly comparable.") | [Score 4.2](docs/glossary.md#results-columns "Recovery minus staff cost minus abrasion (docs/score_42.md), summed over ten seeds. Same formula on every row.") | [Oracle](docs/glossary.md#results-columns "Best conceivable score on the same ten datasets under the same rules, using the answer key; pays triage, staff cost and abrasion; every office answers (docs/score_42.md).") | [% of oracle](docs/glossary.md#results-columns "Score divided by oracle.") |
|---|---|---|---|---|
| Workflow v4.0 | 4.0, test | -$6,212 | $62,662 | -10% |
| Agent v5.0 | 4.0, test | -$3,762 | $62,662 | -6% |
| Workflow v4.1 | 4.0, test | $15,791 | $62,662 | 25% |
| Agent v5.1 | 4.0, test | $11,206 | $62,662 | 18% |
| Workflow v4.1 | 4.2, test | $17,713 | $627,805 | 3% |
| Workflow v4.2 | 4.2, test | $375,031 | $627,805 | 60% |
| Agent v5.2 | 4.2, test | $372,114 | $627,805 | 59% |

[All results](docs/results.md) · [v4.0 and v5.0](docs/v4_v5_results.md) · [v4.1](docs/w41_fresh_result.md) · [v5.1](docs/a51_fresh_result.md) · [v4.2 and v5.2](docs/v42_test_result.md) · [releases 1 to 5](docs/release5_results.md)
<!-- release23:end -->

## How it works
![The agent and its actions: screen, look closer, request charts, follow up, check notes, estimate, review, submit findings](docs/images/agent.svg)

![Workflow v4.2: screen, request recommendation, request charts, stop, chart rules, break-even rule, checks, PI review; plus a visits-per-day lane](docs/images/workflow.svg)

The agent starts from the full claims book; code refuses findings the evidence does not support. [Operating model](docs/operating_model.md) · [walkthrough](docs/how-it-works.md) · [tools](docs/agent_tools.md) · [simulated providers](docs/provider_sim.md)

v1.x, v2.x and v4.x are workflows; v3.x and v5.x are agents. See the [progression slide](docs/images/progression.svg), [versions](docs/versioning.md), [releases](https://github.com/simmyhundal/em-upcoding-agent/releases) and [roadmap](docs/roadmap.md). Everything is synthetic ([limitations](docs/limitations.md)).

## Next (v4.3 and v5.3)
[Messier volume signal](https://github.com/simmyhundal/em-upcoding-agent/issues/197) · [chart realism](https://github.com/simmyhundal/em-upcoding-agent/issues/220) · [reach level upcoding](https://github.com/simmyhundal/em-upcoding-agent/issues/198) · [sourced score 4.3](https://github.com/simmyhundal/em-upcoding-agent/issues/200) · [Opus vs Sonnet agent](https://github.com/simmyhundal/em-upcoding-agent/issues/214)

## Explore
[Results](docs/results-and-evaluation.md) · [limitations](docs/limitations.md) · [E/M background](docs/background.md) · [glossary](docs/glossary.md) · [concepts](docs/concepts/README.md) · [design](docs/design.md) · [about](docs/about.md) · [contributors](CLAUDE.md) · [MIT license](LICENSE)
