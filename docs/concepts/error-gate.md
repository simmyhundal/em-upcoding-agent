# Error gate (extrapolation threshold, measured in dollars)

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
Before a payer extends what it found in a small sample to a provider's whole book of claims, it checks that the sample shows enough error. In score 4.3 the check is the sample's **net overpayment as a share of the paid dollars of the reviewed claims**; the project calls it the *dollar gate*. The sample is extrapolated only when that share is **5% or more**; below it, the payer recovers only the overpayment on the sampled claims themselves. Score 4.2 and earlier used a different measure, the share of sampled claims found overpaid (15%).

## Why it exists
A sample of 30 charts can mislead: one bad claim in a thin sample, multiplied across a thousand claims, would make a demand the payer could not defend. Medicare law and manual require a "sustained or high level of payment error" before extrapolating, with no number given. The only numeric gate found in public sources is the 5% net dollar error rate that Office of Inspector General integrity agreements used to trigger a larger sample; no commercial payer publishes one. Measuring in dollars, net of underpayments, matches how those agreements measure error.

## Example
A provider's 30 reviewed claims were paid $4,000 in all, and the review found $320 of net overpayment: 8%, above 5%, so the payer extrapolates to the provider's other claims and takes the conservative estimate. If the review found $120 (3%), the payer recovers only the $120.

## Where to find it
`GATE_UNIT` and `GATE_DOLLAR_RATE` in `src/recovery_43.py`; sources in [score 4.3 sources, section 5](../score_43_sources.md). In the results so far the gate does not change any row.
