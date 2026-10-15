# Roadmap

[Back to the README](../README.md)

<!-- roadmap:start -->
Live from this repository's [milestones](https://github.com/simmyhundal/em-upcoding-agent/milestones); each badge shows the milestone's current title and closed/total issues.

- ![PoC (Path B): statistics select, AI explains and advises](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/1) Statistics choose who gets a close look; an AI reads each flagged provider's evidence, writes a cited summary and gives an advisory leaning (upcoding, high-acuity panel, inconclusive); code checks the citations; people decide.
- ![Path A (parked): LLM judges from clinical notes](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/2) An LLM judges from synthetic free-text clinical notes instead of structured evidence.
- ![M3: Enhancements to Path B](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/3) Follow-on features once the Path B PoC (Milestone 1) is evaluated: evidence visuals for reviewers and a downstream artifact for the Payment Integrity team.
- ![M4: Reduce API cost](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/4) Cut the cost per run (about $2.14 for the first full run: $1.49 Claude Opus 5.5 writer, $0.65 Claude Sonnet 5.5 judge) without losing quality.
- ![M5: Realistic plan inputs (v2 data model)](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/5) A new version of the tool whose inputs look like what a health plan actually holds, in the shapes plans store them, instead of the simplified CSVs used so far.
- ![M6: Autonomous investigator agent](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/6) Turn the workflow (code fixes the order, one LLM step) into an agent that chooses which tools to use to find upcoders.
- ![Backlog (v2.1)](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/7) Work deferred past the v2.0 freeze.
- ![M7: Recovery and downstream actions](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/8) Simulate what happens after a provider is finally flagged (recovery sampling, deficient responses, extrapolated overpayment, notices) so results cover recovery and other downstream uses, not only advising which providers to look at.
- ![Housekeeping: docs, visuals and releases](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/9) Keep the README, visuals and GitHub releases current and consistent with each tagged version.
- ![v2.1 and v3.1: parallel workflow and agent builds](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/10) Two streams built side by side: v2.1 improves the fixed workflow, v3.1 improves the agent.
- ![v2.2 and v3.2: data 2.2 realism and data quality](https://img.shields.io/github/milestones/progress/simmyhundal/em-upcoding-agent/11) Release 2: data 2.2, workflow v2.2 and agent v3.2.
<!-- roadmap:end -->
