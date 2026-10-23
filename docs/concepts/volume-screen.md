# Volume screen (impossible visits per day)

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
A check on claims alone: count the visits one provider billed for each service date. A provider who billed more visits in one day than any clinician can see (this project flags **30 or more**) is taken into the **claims-data lane**: the system requests charts for a random sample of that day's claims and demands what the sample supports. Older notes and code call this the *fwa lane* (fraud, waste and abuse).

## Why it exists
Level upcoding (billing a visit higher than it was) is only one way to overbill. Billing for visits that never took place is another, and a payer sees it in its own claims before it asks for a single chart. Counting visits per provider per day is a standard payer edit. It costs nothing to run, and the office's answer to a records request (no record of the visit) is itself the evidence.

## Example
A provider bills 48 visits on one Tuesday; its busiest ordinary day is 12. The lane flags the provider, draws 30 of that Tuesday's claims at random, and requests those charts. The office produces charts for 3 and reports no record of the other 27. Those 27 count as overpaid at the paid amount ([records not provided](records-not-provided.md)), and the [stratified sample](stratified-sample.md) is extrapolated to the whole day, with a [conservative estimate](conservative-estimate.md).

## Where to find it
`src/fwa_lane.py`; the score treatment in [score 4.2](../score_42.md). **This signal is clean by construction in the synthetic data** (the busiest honest day is at most 26 visits, an impossible-days provider's is at least 33), which real claims will not be; read the results with that in mind.
