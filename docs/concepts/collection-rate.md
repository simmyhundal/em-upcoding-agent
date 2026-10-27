# Collection rate

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
The share of an overpayment a payer has identified or demanded that ends up as cash. Score 4.3 uses two rates. An **ordinary demand** is collected at **68%** after the [appeal reduction](appeal-reduction.md); a **fraud referral** is collected at **25%**, a figure that already counts appealed and overturned dollars as uncollected.

## Why it exists
A demand is not money in the bank. Providers dispute, stop billing, close or are handed to law enforcement. Counting the whole estimate as recovered made every earlier score too generous. The rates come from audits of public programs, because no commercial payer or vendor publishes identified-against-collected figures: Medicaid managed-care plans' own SIUs collected 22% of fraud-related overpayments and 68% of other overpayments in the same year; Medicare program-integrity referrals collected about 20%.

## Example
A payer's conservative estimate for an ordinary demand is $10,000: after a 15% appeal reduction it is $8,500, and at 68% the payer expects $5,780. For a referral with the same $10,000 estimate it expects $2,500.

## Where to find it
`COLLECTION_DEMAND`, `COLLECTION_REFERRAL` and `collected()` in `src/recovery_43.py`; sources in the [addendum](../score_43_sources_addendum.md).
