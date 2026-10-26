# Patches to frozen versions (no results changed)

[Back to the README](../README.md) · [versions](versioning.md)

**What this page is.** Small fixes made to code that frozen versions run, each checked to leave every recorded result unchanged. A tagged version is never edited; these are the exceptions, with the check that justified them.

## Since v2.0
- `summary_rules._rule_headline` crashed or mis-worded when the pooled 99214/99215 rule decided; it now states the pooled counts. Four stored headlines (runs 261012_9_api and 261012_10_api) kept their older wording; no leaning, citation or score changed (regenerated from the response cache and compared).
- `summary_rules.pick_citations` always cites something from the packet's own samples, so a rule-decided summary can no longer be rejected for citing nothing.
- `records.read_chart` was split out of `request_records` so the provider simulator reads charts the same way (outputs verified identical).

## Since v3.0
- `agent_tools.Environment.call` returns `bad arguments` for an `AttributeError` too (issue 85). A live run (`261015_64_api`) crashed when the model passed `submit_findings` a list of strings; the old code could only crash on that path, so no recorded run changes.
- Office 2.1 no longer draws a sample from an empty list when a follow-up has nothing left to send (issue 84). Office 2.0 never reached that branch with an empty list, so frozen results are unchanged.

