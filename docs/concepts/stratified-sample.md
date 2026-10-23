# Stratified sample

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
A random sample drawn from one slice of a provider's claims (a *stratum*), such as the claims dated on the days a volume screen flagged. Because the draw is random within the slice, it supports extrapolating to that slice, and only that slice. It does not support a claim about the provider's other claims.

## Why it exists
Extrapolating a random sample of all of a provider's claims to a problem confined to a few days would waste most of the sample on claims that have nothing to do with it. Sampling the problem days directly uses the same 30 charts where they matter. Stratified random sampling is a standard way to build a statistically valid sample in overpayment audits.

## Example
A provider billed 238 claims on its flagged days. 30 are drawn at random and requested. The estimate is for those 238 claims (238 times the sample mean, minus the 90% margin), not for the provider's other 800 claims.

## Where to find it
`recovery_stratified` in `src/recovery_42.py`; the draw is in `src/fwa_lane.py`.
