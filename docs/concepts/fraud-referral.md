# Fraud referral

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
The way a payer pursues a provider whose billing looks like fraud, not like a coding disagreement: its special investigations unit (SIU) opens a case, reviews records, involves clinical and legal staff and may pass the case to law enforcement or the state. In score 4.3 a provider found by the [volume screen](volume-screen.md), or one whose chart sample turns out to include claims for visits that never happened, is a referral, not an ordinary demand: it costs **$4,000** of staff time in place of an ordinary demand's $276, and only **25%** of the estimated overpayment is collected.

## Why it exists
An ordinary demand for a billing level is a letter backed by a chart sample. A case for visits that never happened takes far more work, and the sources agree it collects far less: the provider often stops billing (so there is nothing to offset against) or the case goes to the state or law enforcement, which freezes collection. Pricing it as a demand made the volume screen look about ten times better than it is.

## Example
The volume screen flags a provider and the sample's conservative estimate is $12,000. The payer expects to collect $3,000 (25%) and has spent $4,000 on the case, so under score 4.3 pursuing this provider loses $1,000.

## Where to find it
`REFERRAL_COST` and `COLLECTION_REFERRAL` in `src/recovery_43.py`; the $4,000 is an assumption anchored to an industry survey of $3,459 per closed investigation (2013); see [score 4.3 sources](../score_43_sources.md) and the [addendum](../score_43_sources_addendum.md).
