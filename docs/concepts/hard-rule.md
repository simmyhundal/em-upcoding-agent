# Hard rule on rule-supported upcoding calls (binding rule)

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
When the code's rules and its chart test both say a provider is upcoding, the agent cannot write a different conclusion without an `override_reason` that names a fact the rules cannot see (for example a data-quality flag or a specific claim). Code and older notes call this the *binding rule* (agent v3.5, narrowed).

## Why it exists
A model can talk itself out of a finding that the evidence supports, or into one it does not. The rule keeps the model's judgment where the rules are silent and binds it where they speak. In the fresh test of release 5 the agent overrode a binding call twice and was right both times, which is why the override path stays open.

## Example
The rules say upcoding, the chart test agrees, the agent writes inconclusive with no reason: `submit_findings` refuses it.

## Where to find it
`submit_findings` in `src/agent_tools.py`; [what the rule would have refused](../release5_binding_replay.md).
