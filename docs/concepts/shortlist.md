# Shortlisted providers

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
The **screen** ranks every provider by how much its billing exceeds what its patients' conditions predict. The **shortlist** is the few providers at the top of that ranking that the system takes further. Workflow v4.1 and agent v5.1 shortlist 4. Older notes and code call these providers *listed*.

## Why it exists
Reviewing a provider costs money even before charts are requested ([triage](triage.md)). A short list keeps that cost small; a long list finds more upcoders but spends more on the ones who are not.

## Example
The screen is `eb_upper_t`, an empirical-Bayes score: a provider's share of 99214 and 99215 visits, shrunk toward its peers so that a provider with few visits does not rank high by luck. The agent still sees the top 10% of the screen, but is advised on the first 4 rows only.

## Where to find it
`src/screen_methods_v4.py` (`eb_upper_t`), [screens](../screens_v4.md), `list_note` in the `screen_providers` tool result.
