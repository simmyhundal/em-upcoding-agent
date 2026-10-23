# Request recommendation (ASK or SKIP)

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
Before any charts are requested, the system recommends, for each provider on the [shortlist](shortlist.md), whether asking for charts is expected to pay for itself: **ASK** or **SKIP**. In the code the field is `ask_advice` and the values are `ASK` and `SKIP`.

## Why it exists
Requesting charts costs staff time, copy fees, and goodwill with the provider. For some providers the expected recovery is lower than that cost, and the recommendation says so.

## Example
The recommendation comes from a small model (a ridge regression) fitted on development data. It takes the provider's row from the screen (how far its billing sits above what its patients predict, its rank, volume) and predicts the net dollars of asking under [score 4.0](../score_40.md). Positive means ASK. In the workflow the recommendation decides; in the agent it is advice the model may disregard (and pays for if it does).

## Where to find it
`src/policy_40.py`, `src/policy_40_ask.json`, `eval/fit_ask_41.py`. The workflow's rule: [workflow v4.1 freeze](../w41_freeze.md).
