# Agentic E/M upcoding detection

An investigator agent for payment integrity (PI) teams. It screens providers for **E/M (Evaluation and Management) upcoding**, billing an office visit at a higher level than the visit supported, on synthetic Medicare-style claims; decides which providers to ask for charts and how; checks the charts against the claims; and hands drafts to PI teams to review. The providers are simulated too.

**TL;DR:** <!-- tldr:start -->
A fixed workflow and an AI agent both screen providers, request charts and draft cases for PI teams. On ten fresh seeds (79 planted upcoders), the latest agent (v3.5) and workflow (v2.5) each earn about $32k net per seed and are not reliably different; the release 3 workflow earned $24k on the same seeds. The gain is lower cost (fewer requests and fewer false accusations), not more catches: each still finds under half of the upcoders (37 and 36 of 79), far from the 12.5% miss-rate target.
<!-- tldr:end -->

Two designs are built side by side on the same data: a **workflow**, where code fixes the steps and a model writes only where rules are silent, and an **agent**, where a model chooses its own steps within caps. Since release 5 both are scored in **net dollars**: the overpayment a records sample supports, minus what the requests and any false accusation cost.

## How it works
![The agent and the actions it chooses from: screen, look closer, request charts, follow up, check notes, estimate, review, submit findings; simulated providers answer, checks gate the findings, PI teams review](docs/images/agent.svg)

The agent starts from the full claims book, with no pre-screened list. It picks each action itself, within caps on tool calls, dollars and charts requested; code refuses findings the evidence does not support, and PI teams review the drafts. [Eight-step walkthrough](docs/how-it-works.md) · [tools and guardrails](docs/agent_tools.md) · [the simulated providers](docs/provider_sim.md)

## How it has changed
![v1.x and v2.x are fixed workflows, v3.x is the agent: claims, screen, charts, who writes the summary, who decides, headline results](docs/images/progression.svg)

v1.x and v2.x are workflows; v3.x is the agent. Each release changes both: note checks (v2.1, v3.1), harder data (v2.2, v3.2), rules for providers that clone notes (v2.3, v3.3), a learned rule for when to stop asking (v2.4, v3.4), and learned choices of whom to ask, trained on net dollars (v2.5, v3.5). [Version history](docs/versioning.md) · [releases](https://github.com/simmyhundal/em-upcoding-agent/releases) · [roadmap](docs/roadmap.md)

## Results
<!-- release23:start -->
| Version | Seeds | Upcoders found | Honest providers accused | Requests sent to providers | Net $ per seed |
|---|---|---|---|---|---|
| Workflow v2.0 | release 1 seeds | 19 of 80 (24%) | 3 | 162 | $988 |
| Workflow v2.1 | release 1 seeds | 32 of 80 (40%) | 0 | 379 | $14,984 |
| Agent v3.0 | release 1 seeds | 18 of 80 (22%) | 0 | 153 | $2,299 |
| Agent v3.1 | release 1 seeds | 27 of 80 (34%) | 0 | 204 | $13,931 |
| Workflow v2.2 | release 2 seeds | 21 of 78 (27%) | 2 | 327 | $368 |
| Agent v3.2 | release 2 seeds | 12 of 78 (15%) | 1 | 124 | $1,325 |
| Workflow v2.2 | release 3 seeds | 24 of 79 (30%) | 2 | 326 | $4,362 |
| Workflow v2.3 | release 3 seeds | 37 of 79 (47%) | 1 | 583 | $4,923 |
| Agent v3.3 | release 3 seeds | 34 of 79 (43%) | 1 | 177 | $12,666 |
| Workflow v2.4 | release 4 seeds | 49 of 80 (61%) | 2 | 449 | $32,245 |
| Agent v3.4 | release 4 seeds | 40 of 80 (50%) | 3 | 181 | $26,505 |
| Workflow v2.5 | release 5 seeds | 37 of 79 (47%) | 3 | 462 | $31,888 |
| Agent v3.5 | release 5 seeds | 36 of 79 (46%) | 1 | 166 | $32,159 |

Ten seeds per set, 8 planted upcoders each; releases 2 to 5 use harder data. **Net $** is the overpayment a records sample supports for the upcoders found (90% lower bound) minus request and false-accusation costs: compare rows within a seed set only. Details: [release 1](docs/eval61.md), [2](docs/release2_results.md), [3](docs/release3_results.md), [4](docs/release4_results.md), [5](docs/release5_results.md); [every run](docs/results.md).
<!-- release23:end -->

- **What helped:** note checks. Cloned-note upcoders found went from 3 to 10 of 40 (workflow) and 1 to 8 of 40 (agent); the generator plants the clone signs, so real notes are harder.
- **What has not moved:** recall. No version meets the 12.5% miss-rate target; workflow and agent are not reliably different.
- **Read with care:** all synthetic, ten seeds per release, 8 upcoders each. Dollars rank versions at simulated scale and assume $2,000 per honest provider accused. Claims are Medicare-style; E/M level rules are the same for Medicare Advantage and commercial plans, but patient mix and record and recovery rules differ ([limitations](docs/limitations.md)).

## Next (release 6)
Fix the agent's written summaries ([#116](https://github.com/simmyhundal/em-upcoding-agent/issues/116)); size the dollars in missed upcoders, then retry providers that never answer ([#117](https://github.com/simmyhundal/em-upcoding-agent/issues/117)); test whether the agent should obey the policy's stop advice ([#118](https://github.com/simmyhundal/em-upcoding-agent/issues/118)).

## Explore
[Results and evaluation](docs/results-and-evaluation.md) · [limitations](docs/limitations.md) · [E/M background](docs/background.md) · [glossary](docs/glossary.md) · [design](docs/design.md) · [version 1, archived](docs/archive-version-1.md) · [about](docs/about.md) · [for contributors](CLAUDE.md)
