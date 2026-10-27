# Oracle (the best conceivable score)

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
A ceiling computed with the answer key: the score a reviewer would get with perfect knowledge of which providers and claims are overbilled, inside the same scoring rules and paying the same costs. It is an **upper bound, not a target**, and no arm can see what it uses. The README shows each version's score as a share of it.

## Why it exists
A dollar score alone cannot say whether $375,000 is good. The oracle says what the data allowed: on the ten data 4.2 test seeds it was $627,805 under score 4.2, so workflow v4.2 reached 60% of it. It also keeps a ceiling honest about what an arm cannot reach, such as fraud with no signal in the claims.

## Example
For each provider the oracle chooses the best chart sample size, or a sample drawn only from the claims it knows are for visits that never happened; it pursues the provider only if the expected recovery beats the staff cost, the triage and the abrasion, honest provider or not. It assumes every office answers.

## Where to find it
`eval/oracle_s42.py` and `eval/oracle_s43.py`; how it is built and what it excludes: [score 4.2](../score_42.md) and [score 4.3](../score_43.md).
