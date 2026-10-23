# Break-even rule (demand floor)

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
A case is not pursued with a demand if the [conservative recovery estimate](conservative-estimate.md) is below what the demand costs the payer ($276 in staff time). The call is withdrawn and the provider is left as inconclusive. In the code and older notes: the *demand floor*.

## Why it exists
A demand that costs more than it can recover loses money and annoys a provider. The rule enforces that in code, in both the workflow and the agent (`submit_findings` refuses the finding).

## Example
A provider is called upcoding, but the lower bound of the recovery is $180. The demand would cost $276 in staff time, so the call is turned into inconclusive.

## Where to find it
`submit_findings` in `src/agent_tools.py`; the workflow's equivalent in `eval/w_loop.py`. [Score 4.0](../score_40.md).
