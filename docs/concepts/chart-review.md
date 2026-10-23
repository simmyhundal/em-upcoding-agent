# Chart review (hybrid_review)

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
The tool that reads the charts returned for a provider and decides whether they support the billing. It applies the code's **chart test** first (how many 99214 and 99215 charts document a lower level than the one billed), then the summary rules, and a model only where both are silent. The code name is `hybrid_review`.

## Why it exists
It is the point where evidence becomes a conclusion: pattern consistent with upcoding, inconclusive, or normal. Putting rules first keeps the conclusion checkable.

## Example
Provider X returned 30 charts; 9 of the 99214 and 99215 charts document lower complexity than billed (30%). The chart test for workflow v4.1 asks for at least 5 such charts, an unsupported share of at least 10% and p-value under 0.20, so the review calls the pattern consistent with upcoding and attaches a [demand check](demand-check.md).

## Where to find it
`hybrid_review` in `src/agent_tools.py`; the rules in `src/summary_rules.py` and `src/records.py`.
