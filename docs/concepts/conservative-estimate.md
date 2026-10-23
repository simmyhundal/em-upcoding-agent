# Conservative recovery estimate (90% lower bound)

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
The overpayment we claim from a provider is not our best guess; it is the amount we are 90% confident is **at least** owed, computed from a random sample of that provider's charts. Statisticians call this the 90% lower bound (a one-sided lower confidence limit).

## Why it exists
This is how government contractors extrapolate overpayments: the CMS Program Integrity Manual (chapter 8, section 8.4.5) asks for the lower limit of a one-sided 90% confidence interval. Claiming the lower bound protects against demanding more than a sample supports, at the price of recovering less, and it is why a case with few charts recovers little.

## Example
If a provider's 30 sampled charts suggest $9,000 was overpaid but the sample is noisy, the lower bound might be $3,200, and $3,200 is what the score credits and the demand claims.

## Where to find it
`src/recovery_40.py`, [score 4.0, recovery](../score_40.md#recovery).
