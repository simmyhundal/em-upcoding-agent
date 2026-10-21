# Agentic E/M upcoding detection

An upcoding investigator agent for payment integrity (PI) teams to reduce wasteful U.S. healthcare spending by:

- 📄 **Claims:** reviewing synthetic Medicare-style claims for E/M (Evaluation and Management) upcoding, billing an office visit at a higher level than the visit supported;
- 🔽 **Screen:** ranking providers whose billing is highest against what their patients' conditions predict;
- 📁 **Charts:** asking the providers it picks for charts and following up on what comes back (the providers are simulated too);
- ✏️ **Summaries:** checking the charts against the claims and drafting case summaries, with code writing the facts and a model only where the rules are silent;
- 🧭 **Who decides:** choosing its own next steps within caps, then handing drafts to PI teams to review;
- 📊 **Headline results:** scoring in net dollars (see the RL score formula below) against the answer key.

Two designs are built side by side on the same data:

- ⚙️ **Workflow:** code fixes the order of the steps, and a learned formula decides whom to ask for charts.
- 🤖 **Agent:** a model chooses its own steps within caps and gets the same formula as advice.

Both are scored by the **RL score** ([score 4.0](docs/score_40.md)), in net dollars per seed (the reinforcement learning (RL) reward the policies are trained on):

```
RL score = Recovery - Staff cost - Abrasion

Recovery   = 90% lower bound of the overpayment a random chart sample supports, per provider sent a demand
Staff cost = hours x wage for triage, requests, chart review and demands; $90 copy fee per request; model dollars
Abrasion   = $43.84 per request round + $2,000 per demand, weighted by how honest the provider is
```

![Score 4.0 for agent v5.0 on ten fresh seeds, dollars per seed: recovery, staff cost and abrasion down to the net score](docs/images/score_waterfall.svg)

<!-- score:start -->
- **Recovery +$385:** 3 of 80 upcoders found in all ten seeds, 3 demands, about $1,282 recovered per demand.
- **Staff cost -$1,144:** chart review $547, requests and copy fees $475, demand work $83, triage and model dollars $39.
- **Abrasion -$22:** the cost to providers of requests and demands, weighted down for providers that really upcode; no honest provider was demanded from.
<!-- score:end -->

## Results TL;DR
<!-- tldr:start -->
A fixed workflow and an AI agent both screen providers, request charts and draft cases for PI teams. On the old data (release 5), both earned about $32k net per seed and found under half of the upcoders. Data 4.0 and score 4.0 are harder and honest about staff time: on ten fresh seeds, the old workflow loses $11,185 per seed, while the new workflow (v4.0) loses $1,161 and the new agent (v5.0) $781. Each finds 3 of 80 upcoders and accuses no honest provider. Both are far better than before and still not above zero.
<!-- tldr:end -->

<!-- release23:start -->
| Version | [Data model](docs/glossary.md#results-columns "Easy: release 1, clean coding and planted clone signs. Hard: releases 2 to 5, adds coding noise, group billing, lagged claims and data defects. Data 4.0: every provider has a true upcoding rate and 8 have a habit.") | [Upcoders found (recall)](docs/glossary.md#results-columns "Upcoders found out of those planted.") | [Calls that were upcoders (precision)](docs/glossary.md#results-columns "Upcoders found out of all providers called upcoding.") | [Net $ per seed (RL score)](docs/glossary.md#results-columns "Overpayment a records sample supports (90% lower bound) minus costs. Compare rows within one seed set only. The last three rows use score 4.0, which also charges staff time.") |
|---|---|---|---|---|
| Workflow v2.0 | Easy | 24% | 86% | $988 |
| Workflow v2.1 | Easy | 40% | 100% | $14,984 |
| Agent v3.0 | Easy | 22% | 100% | $2,299 |
| Agent v3.1 | Easy | 34% | 100% | $13,931 |
| Workflow v2.2 (release 2) | Hard | 27% | 91% | $368 |
| Agent v3.2 | Hard | 15% | 92% | $1,325 |
| Workflow v2.2 (release 3) | Hard | 30% | 92% | $4,362 |
| Workflow v2.3 | Hard | 47% | 97% | $4,923 |
| Agent v3.3 | Hard | 43% | 97% | $12,666 |
| Workflow v2.4 | Hard | 61% | 96% | $32,245 |
| Agent v3.4 | Hard | 50% | 93% | $26,505 |
| Workflow v2.5 | Hard | 47% | 92% | $31,888 |
| Agent v3.5 | Hard | 46% | 97% | $32,159 |
| **Score 4.0 on data 4.0 (fresh seeds)** | | | | |
| Workflow v2.5 (frozen, for reference) | Data 4.0 | 1% | 25% | -$11,185 |
| Workflow v4.0 | Data 4.0 | 4% | 100% | -$1,161 |
| Agent v5.0 | Data 4.0 | 4% | 100% | -$781 |

Hover over a column title for its definition ([glossary](docs/glossary.md#results-columns)). Compare rows within one seed set only: releases [1](docs/eval61.md), [2](docs/release2_results.md), [3](docs/release3_results.md), [4](docs/release4_results.md), [5](docs/release5_results.md), [v4.0 and v5.0](docs/v4_v5_results.md); [every run](docs/results.md).
<!-- release23:end -->

## How it works
![The agent and the actions it chooses from: screen, look closer, request charts, follow up, check notes, estimate, review, submit findings; simulated providers answer, checks gate the findings, PI teams review](docs/images/agent.svg)

![The fixed workflow v4.0: screen with eb_upper_t, learned ask-or-skip, request charts, stop after the first sample, rules decide, demand floor, checks, PI teams review](docs/images/workflow.svg)

The agent starts from the full claims book with no pre-screened list; code refuses findings the evidence does not support. [Eight-step walkthrough](docs/how-it-works.md) · [tools and guardrails](docs/agent_tools.md) · [the simulated providers](docs/provider_sim.md)

v1.x, v2.x and v4.x are workflows; v3.x and v5.x are agents. Every release changed both; the [progression slide](docs/images/progression.svg), [version history](docs/versioning.md), [releases](https://github.com/simmyhundal/em-upcoding-agent/releases) and [roadmap](docs/roadmap.md) show how. Both lose money on data 4.0 (3 of 80 upcoders found); everything is synthetic ([limitations](docs/limitations.md)).

## Next (v4.1 and v5.1)
The development-to-fresh gap on a second fresh set ([#132](https://github.com/simmyhundal/em-upcoding-agent/issues/132)); recovery per demand ([#133](https://github.com/simmyhundal/em-upcoding-agent/issues/133)); the opportunistic habit ([#134](https://github.com/simmyhundal/em-upcoding-agent/issues/134)); agent v5.1 ([#135](https://github.com/simmyhundal/em-upcoding-agent/issues/135)); score 4.1 ([#136](https://github.com/simmyhundal/em-upcoding-agent/issues/136)); data 4.1 ([#137](https://github.com/simmyhundal/em-upcoding-agent/issues/137)).

## Explore
[Results and evaluation](docs/results-and-evaluation.md) · [limitations](docs/limitations.md) · [E/M background](docs/background.md) · [glossary](docs/glossary.md) · [design](docs/design.md) · [version 1, archived](docs/archive-version-1.md) · [about](docs/about.md) · [for contributors](CLAUDE.md)
