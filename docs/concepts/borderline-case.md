# Borderline case (near-miss)

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
A provider called upcoding whose **best estimate** of the recovery is at least twice the cost of a demand ($276), but whose [conservative estimate](conservative-estimate.md) is still below that cost, so the [break-even rule](break-even-rule.md) would withdraw the demand. Code and older notes call this a *near-miss*.

## Why it exists
More charts narrow the interval. For these providers one more sample of 30 random charts can lift the conservative estimate over the cost of a demand, so workflow v4.1 and agent v5.1 request it, once. For everyone else a second sample is refused.

## Example
A provider's estimate is $1,400 and its lower bound is $150. A demand costs $276. The first sample leaves the case unpursued; a second sample of 30 may raise the lower bound above $276.

## Where to find it
`near_miss` in the `demand_check` of [chart review](chart-review.md); [workflow v4.1 freeze](../w41_freeze.md).
