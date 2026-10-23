# No-more-requests advice (STOP)

[Back to concepts](README.md) · [glossary](../glossary.md)

## What it means
After the first sample of charts and one follow-up on any deficiency, the advice is to ask for nothing more (no targeted request for 99215 charts, no audit trail), then run [chart review](chart-review.md). The code value is `STOP`; the only exception is the [borderline case](borderline-case.md).

## Why it exists
On score 4.0 the extra rounds of asking did not pay: they cost staff time and abrade providers more than they recovered. The advice is the result of testing escalation and finding it lost money.

## Example
The agent has received 30 charts and followed up on missing signatures. It does not send a targeted request for 15 charts of 99215; it runs chart review and finishes the case.

## Where to find it
`ask_advice` in `src/agent_tools.py`; why escalation was dropped: [workflow v4.0 loop](../w_loop_v4.md).
