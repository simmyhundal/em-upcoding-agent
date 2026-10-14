# Agentic E/M upcoding detection

An investigator agent for payment integrity: it screens primary care providers for E/M (Evaluation and Management) upcoding on synthetic Medicare-style claims, decides which practices to ask for charts and how, checks the notes against the claims, and hands drafts to people to review. The practices are simulated too. **TL;DR:** <!-- tldr:start -->
On two reserved test seeds (16 planted upcoders), the fixed workflow found 6 and the agent 4; neither accused an honest practice, and the agent asked 9 honest practices for charts to the workflow's 17.
<!-- tldr:end --> Neither design is close to the 12.5% miss-rate target: cloned notes and low upcoder rates are the weak spots. **Next:** parallel builds of the workflow (v2.x) and the agent (v3.x) that check notes against claims, then a multi-seed evaluation on fresh seeds before claiming either is better.

## How it works
![The agent and the actions it chooses from: screen, look closer, request charts, follow up, check notes, estimate, review, submit findings; simulated practices answer, checks gate the findings, people review the drafts](docs/images/agent.svg)

The agent starts from the full claims book, with no pre-screened list. It picks each action itself, within caps on tool calls, dollars and charts requested; code refuses findings the evidence does not support, and people review the drafts. [Eight-step walkthrough](docs/how-it-works.md) · [tools and guardrails](docs/agent_tools.md) · [the simulated practices](docs/provider_sim.md)

## How it has changed
![v1.x and v2.x are fixed workflows, v3.x is the agent: claims, screen, charts, who writes the summary, who decides, headline results](docs/images/progression.svg)

v1.x and v2.x are fixed workflows: code picks the steps and a model writes only where rules are silent. v3.x is the agent. The next builds, v2.x and v3.x in parallel, add note-level checks. [Version history](docs/versioning.md) · [releases](https://github.com/simmyhundal/em-upcoding-agent/releases) · [roadmap](docs/roadmap.md)

## Results
<!-- scoreboard:start -->
| Arm | Upcoders found | Honest practices accused | Honest practices asked for charts | Request rounds | Summary usefulness (1-5, LLM judge) |
|---|---|---|---|---|---|
| Workflow v2.x, screen at suspicion 5 | 6 of 16 | 0 | 17 | 41 | 3.4 |
| Workflow v2.x, screen at top 25 | 6 of 16 | 0 | 35 | 71 | 3.5 |
| Agent v3.x, with the screen tool | 4 of 16 | 0 | 9 | 26 | 2.9 |
| Agent v3.x, without the screen tool | 4 of 16 | 0 | 12 | 28 | 2.3 |

Two reserved test seeds, 8 planted upcoders each (more in [the full results](docs/results.md)).
<!-- scoreboard:end -->

- No arm meets the 12.5% miss-rate threshold. The agent reaches fewer upcoders than the workflow but asks far fewer honest practices for charts.
- Upcoders who clone their notes are almost never found, and at low upcoder rates the model step over-accuses.
- Everything is synthetic, simulated and on a few seeds with 8 upcoders each: read the gaps as directional.

[Results and evaluation](docs/results-and-evaluation.md) · [every run](docs/results.md) · [limitations](docs/limitations.md)

## Explore
[Background on E/M levels](docs/background.md) · [glossary](docs/glossary.md) · [design notes](docs/design.md) · [version 1, archived](docs/archive-version-1.md) · [about this project](docs/about.md) · [for agents and contributors](CLAUDE.md) (commands, file map, rules)
