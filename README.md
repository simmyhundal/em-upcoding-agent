# Agentic E/M upcoding detection

An investigator agent for payment integrity: it screens primary care providers for E/M (Evaluation and Management) upcoding on synthetic Medicare-style claims, decides which practices to ask for charts and how, checks the notes against the claims, and hands drafts to people to review. The practices are simulated too. **TL;DR:** <!-- tldr:start -->
On ten fresh test seeds (80 planted upcoders), workflow v2.1 found 32 and agent v3.1 27 (up from 19 and 18 for v2.0 and v3.0); neither accused an honest practice.
<!-- tldr:end --> Both upgrades helped, but the workflow and the agent are not reliably different, so the workflow stays the main line. Neither is close to the 12.5% miss-rate target: both still miss most upcoders. **Since then (harder data with honest coding noise, group billing and data defects):** a first ten-seed look favored the workflow, but it was not a planned test; on ten fresh seeds workflow v2.3 found 37 of 79 upcoders and agent v3.3 34, with no significant gap ([details](docs/release3_results.md)).

## How it works
![The agent and the actions it chooses from: screen, look closer, request charts, follow up, check notes, estimate, review, submit findings; simulated practices answer, checks gate the findings, people review the drafts](docs/images/agent.svg)

The agent starts from the full claims book, with no pre-screened list. It picks each action itself, within caps on tool calls, dollars and charts requested; code refuses findings the evidence does not support, and people review the drafts. [Eight-step walkthrough](docs/how-it-works.md) · [tools and guardrails](docs/agent_tools.md) · [the simulated practices](docs/provider_sim.md)

## How it has changed
![v1.x and v2.x are fixed workflows, v3.x is the agent: claims, screen, charts, who writes the summary, who decides, headline results](docs/images/progression.svg)

v1.x and v2.x are fixed workflows: code picks the steps and a model writes only where rules are silent. v3.x is the agent. v2.1 and v3.1, built in parallel, add note-level checks; v2.2 and v3.2 make the data harder. [Version history](docs/versioning.md) · [releases](https://github.com/simmyhundal/em-upcoding-agent/releases) · [roadmap](docs/roadmap.md)

## Results
<!-- scoreboard:start -->
| Arm | Upcoders found | Recall | Honest practices accused | Precision | Honest practices asked for charts | Requests and follow-ups sent to practices | Summary usefulness (1-5, LLM judge) |
|---|---|---|---|---|---|---|---|
| Workflow v2.0 (frozen) | 19 of 80 | 24% | 3 | 86% | 61 | 162 | 3.4 |
| Workflow v2.1 | 32 of 80 | 40% | 0 | 100% | 61 | 379 | 3.1 |
| Agent v3.0 (frozen) | 18 of 80 | 22% | 0 | 100% | 50 | 153 | 3.0 |
| Agent v3.1 | 27 of 80 | 34% | 0 | 100% | 63 | 204 | 3.3 |

Ten fresh test seeds, 8 planted upcoders each, all four arms on the same data. **Recall** is upcoders found out of those planted; **precision** is upcoders found out of all providers the arm called upcoding (found plus honest accused). "Requests and follow-ups sent" counts every chart request and follow-up message to a practice, a measure of the burden on practices. Paired comparisons and the decision rules: [the evaluation](docs/eval61.md); every run: [the full results](docs/results.md).
<!-- scoreboard:end -->

<!-- release23:start -->
| Arm | Seeds | Upcoders found | Recall | Honest practices accused | Precision | Honest practices asked for charts | Requests and follow-ups sent to practices |
|---|---|---|---|---|---|---|---|
| Workflow v2.2 | release 2 seeds | 21 of 78 | 27% | 2 | 91% | 66 | 327 |
| Agent v3.2 | release 2 seeds | 12 of 78 | 15% | 1 | 92% | 58 | 124 |
| Workflow v2.2 | release 3 seeds | 24 of 79 | 30% | 2 | 92% | 64 | 326 |
| Workflow v2.3 | release 3 seeds | 37 of 79 | 47% | 1 | 97% | 150 | 583 |
| Agent v3.3 | release 3 seeds | 34 of 79 | 43% | 1 | 97% | 79 | 177 |

Harder data (honest coding noise, group billing, data defects), ten seeds in each set, 8 planted upcoders each. The release 2 comparison was an unplanned ten-seed look, so it carries no significance claim; on the later pre-registered ten seeds workflow v2.3 and agent v3.3 are not significantly different. Details: [release 2](docs/release2_results.md), [release 3](docs/release3_results.md).
<!-- release23:end -->

- The note checks are what helped: upcoders who clone their notes went from 3 to 10 of 40 found (workflow) and 1 to 8 of 40 (agent). The clone signals are planted by the data generator, so this is easier than real notes.
- No arm meets the 12.5% miss-rate threshold. Workflow v2.1's extra requests (second samples, audit trails) more than double the requests and follow-ups sent; the agent v3.1 sends about half as many as workflow v2.1.
- Everything is synthetic, simulated and on a few seeds with 8 upcoders each: read the gaps as directional.

[Results and evaluation](docs/results-and-evaluation.md) · [every run](docs/results.md) · [limitations](docs/limitations.md)

## Explore
[Background on E/M levels](docs/background.md) · [glossary](docs/glossary.md) · [design notes](docs/design.md) · [version 1, archived](docs/archive-version-1.md) · [about this project](docs/about.md) · [for agents and contributors](CLAUDE.md) (commands, file map, rules)
