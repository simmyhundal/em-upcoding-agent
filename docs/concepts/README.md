# Concepts

[Back to the README](../../README.md) · [glossary](../glossary.md)

Plain-language pages for terms this project uses. Each says what the term means, why it exists, a small example, and where it is in the code. Terms from the code or older notes are shown in italics.

| Concept | In one line |
|---|---|
| [Workflow and agent](workflow-and-agent.md) | Two ways to build the same reviewer |
| [Request recommendation (ASK or SKIP)](request-recommendation.md) | Before any charts are requested, the system recommends, for each provider on the [shortlist](shortlist.md), whether asking for charts is exp... |
| [Shortlisted providers](shortlist.md) | The **screen** ranks every provider by how much its billing exceeds what its patients' conditions predict |
| [Triage](triage.md) | The first look an analyst takes at a shortlisted provider before deciding whether to pursue it: reading the screen row and the provider's bi... |
| [Conservative recovery estimate (90% lower bound)](conservative-estimate.md) | The overpayment we claim from a provider is not our best guess; it is the amount we are 90% confident is **at least** owed, computed from a... |
| [Borderline case (near-miss)](borderline-case.md) | A provider called upcoding whose **best estimate** of the recovery is at least twice the cost of a demand ($276), but whose [conservative es... |
| [Break-even rule (demand floor)](break-even-rule.md) | A case is not pursued with a demand if the [conservative recovery estimate](conservative-estimate.md) is below what the demand costs the pay... |
| [Hard rule on rule-supported upcoding calls (binding rule)](hard-rule.md) | When the code's rules and its chart test both say a provider is upcoding, the agent cannot write a different conclusion without an `override... |
| [No-more-requests advice (STOP)](no-more-requests.md) | After the first sample of charts and one follow-up on any deficiency, the advice is to ask for nothing more (no targeted request for 99215 c... |
| [Chart review (hybrid_review)](chart-review.md) | The tool that reads the charts returned for a provider and decides whether they support the billing |
| [Demand check (demand_check)](demand-check.md) | What chart review attaches to a provider called upcoding: the payer's best estimate of the recovery, its [conservative estimate](conservativ... |
| [Volume screen (impossible visits per day)](volume-screen.md) | A check on claims alone: count the visits one provider billed for each service date |
| [Records not provided](records-not-provided.md) | When a payer samples claims and asks the provider for the charts, a claim for which the provider produces no record of the visit counts as a... |
| [Stratified sample](stratified-sample.md) | A random sample drawn from one slice of a provider's claims (a *stratum*), such as the claims dated on the days a volume screen flagged |
