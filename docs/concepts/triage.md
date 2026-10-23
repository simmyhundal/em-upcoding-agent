# Triage

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
The first look an analyst takes at a shortlisted provider before deciding whether to pursue it: reading the screen row and the provider's billing pattern. In this project it is a priced step: 15 minutes of an analyst's time, about **$13** per shortlisted provider.

## Why it exists
Triage is a standard term in payment integrity for sorting cases by priority before investing in them. We price it because the number of providers reviewed is a lever: in workflow v4.1 about half of the gain over v4.0 came from shortlisting fewer providers, which saves triage cost, not from asking better.

## Example
A shortlist of 4 costs about $52 in triage per dataset; a list of 22 costs about $289 whether or not any provider is pursued. See the [mechanical gains rule](../../CLAUDE.md).

## Where to find it
`MINUTES["triage_per_listed"]` in `src/recovery_40.py`; wages and minutes in [score 4.0](../score_40.md#staff-hours-cost).
