# Agentic E/M upcoding detection

A postpay upcoding investigator for payment integrity (PI) teams: it audits claims to recover wasteful U.S. healthcare spending by:

- 📄 **Claims:** reviewing synthetic Medicare-style paid claims for E/M (Evaluation and Management) upcoding, billing an office visit at a higher level than the visit supported;
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

![Score 4.0 for agent v5.1 on ten test seeds, dollars summed over ten seeds: recovery, staff cost and abrasion down to the net score](docs/images/score_waterfall.svg)

<!-- score:start -->
- **Recovery +$20,972:** 10 of 80 upcoders found, 10 demands, about $2,097 recovered per demand.
- **Staff cost -$13,470:** chart review $5,955 (692 charts), requests and copy fees $4,429 (42 rounds), demand work $2,757, triage and model dollars $329.
- **Abrasion -$76:** the cost to providers of requests and demands; no honest provider was demanded from.
- **Net score $7,426** over ten seeds.
<!-- score:end -->

## Results
<!-- tldr:start -->
A fixed workflow and an AI agent both screen providers, request charts and draft cases for PI teams. On the old data (release 5), both earned about $320k net over ten seeds under score 2.5 and found under half of the upcoders. Data 4.0 and score 4.0 are harder and charge for staff time. On ten test seeds the old workflow (v2.5) scores -$111,847 in total, workflow v4.0 -$11,612 and agent v5.0 -$7,812; the newest, workflow v4.1 ($10,031) and agent v5.1 ($7,426), find 9 and 10 of 80 upcoders and accuse no honest provider. They beat their predecessors on most seeds, but one seed carries each total and neither is distinguishable from zero.
<!-- tldr:end -->

<!-- release23:start -->
| Version | [Data, seeds](docs/glossary.md#results-columns "Data version and the ten seeds. Compare rows within one data and seed set.") | [Upcoders found (recall)](docs/glossary.md#results-columns "Planted upcoders found.") | [Calls that were upcoders (precision)](docs/glossary.md#results-columns "Calls that were upcoders.") | [Score 2.5](docs/glossary.md#results-columns "Release 5's score: the overpayment a sample supports (90% lower bound) minus request, review and false-accusation costs. Sum over ten seeds. Applied to release 1 after the fact.") | [Score 4.0](docs/glossary.md#results-columns "Recovery minus staff-hours cost minus provider abrasion (docs/score_40.md). Sum over ten seeds.") |
|---|---|---|---|---|---|
| Workflow v2.1 | 2.1, release 1 | 40% | 100% | $149,839 | n/a |
| Agent v3.1 | 2.1, release 1 | 34% | 100% | $139,308 | n/a |
| Workflow v2.5 | 2.2, release 5 | 47% | 92% | $318,882 | -$72,680 |
| Agent v3.5 | 2.2, release 5 | 46% | 97% | $321,585 | -$16,574 |
| Workflow v2.5 (frozen) | 4.0, test | 1% | 25% | n/a | -$111,847 |
| Workflow v4.0 | 4.0, test | 4% | 100% | n/a | -$11,612 |
| Agent v5.0 | 4.0, test | 4% | 100% | n/a | -$7,812 |
| Workflow v4.1 | 4.0, test | 11% | 100% | n/a | $10,031 |
| Agent v5.1 | 4.0, test | 12% | 100% | n/a | $7,426 |

Hover over a column title for its definition ([glossary](docs/glossary.md#results-columns)). Every run and release: [results](docs/results.md), [release 1](docs/eval61.md), [5](docs/release5_results.md), [v4.0 and v5.0](docs/v4_v5_results.md), [v4.1](docs/w41_fresh_result.md), [v5.1](docs/a51_fresh_result.md).
<!-- release23:end -->

## How it works
![The agent and the actions it chooses from: screen, look closer, request charts, follow up, check notes, estimate, review, submit findings; simulated providers answer, checks gate the findings, PI teams review](docs/images/agent.svg)

![The fixed workflow v4.1: a list of 4 from eb_upper_t, learned ask-or-skip, request charts and extend near-misses once, looser chart rules decide, demand floor, checks, PI teams review](docs/images/workflow.svg)

The agent starts from the full claims book with no pre-screened list; code refuses findings the evidence does not support. [Eight-step walkthrough](docs/how-it-works.md) · [tools and guardrails](docs/agent_tools.md) · [the simulated providers](docs/provider_sim.md)

v1.x, v2.x and v4.x are workflows; v3.x and v5.x are agents. Every release changed both; the [progression slide](docs/images/progression.svg), [version history](docs/versioning.md), [releases](https://github.com/simmyhundal/em-upcoding-agent/releases) and [roadmap](docs/roadmap.md) show how. On data 4.0 the first versions lost money (3 of 80 upcoders found); v4.1 and v5.1 find 9 and 10 and score above zero, though not reliably. Everything is synthetic ([limitations](docs/limitations.md)).

## Next (v4.2 and v5.2)
No binary upcoder label, with fraud, waste and abuse ([#173](https://github.com/simmyhundal/em-upcoding-agent/issues/173)); list sizes 2 and 3 ([#166](https://github.com/simmyhundal/em-upcoding-agent/issues/166)); score 4.2 with a sourced commercial profile ([#178](https://github.com/simmyhundal/em-upcoding-agent/issues/178)); data 4.2 ([#137](https://github.com/simmyhundal/em-upcoding-agent/issues/137), [#144](https://github.com/simmyhundal/em-upcoding-agent/issues/144)).

## Explore
[Results and evaluation](docs/results-and-evaluation.md) · [limitations](docs/limitations.md) · [E/M background](docs/background.md) · [glossary](docs/glossary.md) · [design](docs/design.md) · [version 1, archived](docs/archive-version-1.md) · [about](docs/about.md) · [for contributors](CLAUDE.md) · [MIT license](LICENSE)
