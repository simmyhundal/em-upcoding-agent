# Workflow and agent

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
Two ways to build the same reviewer. In a **workflow**, our code fixes the order of the steps (screen, request charts, check, draft), and a learned formula decides whom to ask. In an **agent**, a language model chooses its own next step from a menu of tools, inside caps on rounds, charts and spend. Both are given the same data and scored the same way.

## Why it exists
Anthropic's own guide to building agents draws the same line: workflows follow predefined code paths, agents direct their own process. We keep both because the agent can adapt to situations the workflow's code did not anticipate, and the workflow is cheaper and easier to audit.

## Example
A workflow always runs the same four steps on the same four providers. An agent might look at the screen, decide a provider is not worth a request, and move on, or ask for more charts than the workflow would.

## Where to find it
`src/case_summary.py` and `eval/w_loop.py` (workflow); `src/agent.py` and `src/agent_tools.py` (agent). [Agent tools](../agent_tools.md), [how it works](../how-it-works.md).
