# The postpay audit: today and with PI Agent

[Back to the README](../README.md) · [the audit in context](audit_in_context.md)

The diagram shows the postpay audit (stages 5 to 7) as it runs today and with PI Agent, and the table shows where $100 of E/M payments ends up for each party. PI Agent is simulated on synthetic claims. It takes over the screen, the records request, chart reading and the estimate; people still approve the list and sign the demand. It sends no letters and writes no findings.

![The postpay audit, today and with PI Agent](images/audit_postpay_zoom.png)

Vector version: [audit_postpay_zoom.svg](images/audit_postpay_zoom.svg).

## What changes
| Step | Today | With PI Agent |
|---|---|---|
| Choose providers | Analyst screens paid claims | Software screens; analyst approves the list |
| Records request | Analyst drafts it and picks the sample | Software chooses whom to ask and writes it |
| Read charts | Coder, then nurse and physician | Rules read; a model only where rules are silent; a person reviews undecided cases |
| Estimate | Analyst or vendor extrapolates | Software computes a lower bound and proposes a demand only if it covers its cost |
| Sign-off | Findings meeting, medical director | A person signs the demand |
| Demand onward | Finance, legal, provider, offset, vendor fee | Same |
| Human hand-offs, screen to demand | 6 | 3 |

## Where $100 of E/M payments goes
Of the $100, $4.50 is upcoded (see [the audit in context](audit_in_context.md)). Dollars per $100.

| | Today (Medicare-based) | With PI Agent (simulated) |
|---|---|---|
| Collected | $0.062 | $0.062 |
| Provider repays | $0.062 | $0.062 |
| Vendor fee, if outsourced | $0.012 | $0 in-house; $0.012 if outsourced |
| Payer cost of the audit | not published (Medicare: 25% of collected, $0.016) | $0.043 |
| Payer keeps | about $0.047 to $0.050, own staff cost not counted | $0.019 |

- **Same recovery.** On the data 4.0 test seeds workflow v4.1 collected $15,107 of $1,090,695 upcoded dollars, 1.4%, the same as Medicare's ratio.
- **Cost not proven lower.** The simulated arm spends 69% of what it collects at assumed prices; today's cost is unpublished. It still nets $4,603 over ten seeds, 52% of the oracle's $8,778, while earlier arms lose money.
- **Scaled.** The synthetic data hold upcoded dollars at 1.3% of payments, so the right column applies the simulation's ratios to the $4.50 base.
- **Step counts** come from the design, not from timing a payer's staff.

Sources: `experiments/yardstick_s43.json` and the answer keys for the simulated column; the research notes for the rest.
