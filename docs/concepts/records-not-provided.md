# Records not provided

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
When a payer samples claims and asks the provider for the charts, a claim for which the provider produces no record of the visit counts as an overpayment of its whole paid amount, not as 'unknown'. In this project the rule applies only when the office **answers and reports** that it has no record of the visit. A provider that simply does not respond counts for nothing (silence is not evidence). The code name is `NO_RECORD`.

## Why it exists
The CMS Program Integrity Manual (chapter 8, section 8.4.5) treats sampling units whose records were not provided as overpayments. Without this rule, a claim for a service that never happened could never be recovered from a chart sample, because there is no chart to compare to the bill. Score 4.0 left the rule out; score 4.2 puts it in.

## Example
Of 30 sampled claims, the office sends charts for 3 and reports no record for 27. The 27 count at their paid amount (say $100 each), the 3 are compared with their bills, and the result goes through the usual estimate (netting, 15% error gate, 90% lower bound).

## Where to find it
`src/recovery_42.py`; [score 4.2](../score_42.md).
