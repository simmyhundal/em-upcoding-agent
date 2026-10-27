# Appeal reduction

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
The share of a demanded amount a payer expects to lose when providers dispute it and win, fully or in part. Score 4.3 sets it at **15%** of an ordinary demand's estimate, applied before the [collection rate](collection-rate.md). It is not applied to a [fraud referral](fraud-referral.md), whose collection rate is already net of appeals.

## Why it exists
Demands based on extrapolation are easy to challenge (the sample, the pricing, a chart that supports the billed level). The only sourced dollar figure is Medicare's: in fiscal year 2021, $52.7 million of $345.8 million collected by recovery audit contractors was overturned at the first appeal level, 15.2%. Provider-side commentators put the figure for extrapolated demands much higher (40% to 60%) without a measured source, and the federal inspector general's own examples include a demand cut by 69%, so 15% may be low; higher values are kept as sensitivity.

## Example
An estimate of $10,000 becomes $8,500 after a 15% reduction; with a collection rate of 68% the payer expects $5,780.

## Where to find it
`APPEAL_REDUCTION` in `src/recovery_43.py`; sources in [score 4.3 sources, section 3](../score_43_sources.md).
