# Prepay discovery note: pend and request records

[Back to the README](../README.md) · [copy-list](prepay_copylist.md) · [decision log](decision_log.md)

Draft, 2026-10-23, for Simmy's review. This note proposes a second repository for the **prepay** use case, built on this one. Nothing here is a finding; it is a plan and a list of questions.

## Why prepay

This repository is **postpay**: it audits claims after they are paid, asks providers for charts, and demands money back. A contact at a prospective customer (Maxine) wrote that they want to "sit as far upstream as possible (the industry term is prepay) instead of handling things via audit (postpay)... less abrasive". Postpay recovers money from providers who already have it, and the market notes ([earnings](market_research_earnings.md), [prior-auth sizing](market_prior_auth_sizing.md)) show plans moving toward automatic edits and real-time decisions. Our own results point the same way: on data 4.0 the cost of a postpay demand (staff time, copy fees, abrasion) is close to what it recovers, and most of the loss is in chasing providers who did nothing wrong.

## The prepay points

A claim passes several places where something can be done about E/M level. The further upstream, the less abrasion, and the less we know.

| Point | Where | What the system does | What it knows | Fit |
|---|---|---|---|---|
| 0 | At the point of care | Coding help for the clinician | Everything | Provider-side product, not payer |
| 1 | Pre-bill, in the provider's system | Flags documentation that does not support the level | The note | Provider-side product |
| 2 | Prior authorization | Not used for office visits | n/a | Does not apply to 99211 to 99215 |
| 3 | Claim edits at adjudication | Rules on the claim alone (frequency, level against diagnosis, provider history) | The claim and the provider's history | Baseline arm: cheap, automatic, no chart |
| **4** | **Pend the claim and request records** | **Choose which claims to hold, request the chart before paying, pay, adjust or deny on what comes back** | **The claim, history, and a chart for the pended claims** | **Chosen** |
| 5 | Provider-level prepay status (gold carding in reverse) | Put a provider on prepay review for a period, or relieve a clean one | A provider's record over time | Later layer on point 4 |
| 6 | Automatic level adjustment | Pay a lower level without records, appeal on request | The claim only | Competitor (Cigna R49, Aetna); the regulator and provider backlash is documented |

Point 4 was chosen because it keeps what this repository already does well (choose whom to ask, read the chart against the claim, decide by rule, count the cost of friction) and moves it before payment, where the payer holds the money and needs no demand. It also gives the plan a defensible position against point 6: pay the level the chart supports, with a record.

## What changes from postpay

| | Postpay (this repo) | Prepay point 4 |
|---|---|---|
| Unit of decision | A provider, from a screened list | A single claim, arriving in a stream |
| Money | Recovered later, from a random chart sample's lower bound, by demand | Never paid: the level difference on a pended claim |
| Records | Requested on a provider, 30 random charts | Requested on the claim; one chart per pend |
| Cost of being wrong | Abrasion, weighted by the provider's true rate | Wrongful pends and denials, delay against prompt-pay deadlines, appeals that overturn |
| Time | Months | Days: a clock runs from the claim's receipt |
| Evidence base | A sample extrapolated | The chart in hand, so no extrapolation |

## The design question

For each arriving claim, the system chooses: **pay, pend and request records, or pay at a lower level by rule**. A pended claim ends as paid as billed, paid at a lower level, or denied for missing records, once the office responds (or does not). The policy needs to know the claim, the provider's history to date, and the budget (staff time and a daily pend cap).

Arms to build, in order:
1. **Pay all**: floor, score zero by construction.
2. **Claim-edit rules** (point 3): the baseline a plan already runs.
3. **Workflow**: the screen's provider score as a prior, an ask-or-skip rule, rules on the returned chart. Reuses the learned ask-or-skip in `src/policy_40.py`.
4. **Agent**: a model chooses within caps, as in agent v5.x.
5. **Automatic level adjustment** (point 6) as a competitor with its own wrongful-adjustment cost.

## Score (draft)

```
Prepay score = Overpayment prevented - Staff cost - Abrasion
Overpayment prevented = level difference on pended claims the chart shows were upcoded
Staff cost = triage per claim, chart review per pend, request and copy fee
Abrasion = wrongful pends, wrongful adjustments or denials, days of delay past the prompt-pay deadline, appeals overturned
```

The postpay score's honest-provider penalty becomes a per-claim cost of pending a correct claim, plus a larger cost for adjusting one wrongly. Every parameter is an assumption with a sensitivity, as in [score 4.0](score_40.md). Prompt-pay deadlines vary by state and contract, so they are parameters, not facts.

## Data

Start on **data 4.2** ([data_v4_2.md](data_v4_2.md)): no binary upcoder label, a continuous true net rate per provider, fraud kinds independent of level rate, and an office that can return `NO_RECORD`. It is the right base because prepay decisions on a single claim need a per-claim truth (the justified level of the visit), which data 4.x already generates. What it lacks: a **claim stream with arrival dates**, claims lag already exist; the pend and release dates would be new. The generator should stay in this repository and the new one depend on it (pinned), per the earlier recommendation.

## Open questions for Maxine and Ric

1. Who owns the budget: payment integrity, claims operations, or network management?
2. Which claims are pended for records today, and what share of those pends are for E/M levels?
3. How long can a claim wait? What are the state and contract prompt-pay clocks for commercial lines?
4. What do appeals look like: how many pended E/M claims are appealed, and what share are overturned?
5. Is automatic level adjustment already in use or paused (Anthem paused, Cigna R49 contested)? What would they accept instead?
6. Would they accept a provider-level prepay status (point 5), or is that a contract issue?
7. What data would a pilot have: claims only, or charts for pended claims?

## Risks and honesty

- Everything here is synthetic. The simulated office responds the way we designed it.
- Prepay results will look better than postpay for a reason that is partly by construction: the chart is in hand before payment, so no extrapolation is needed. The comparison should hold the amount of review constant.
- Our postpay results are fragile (one seed carries each total). A new repository does not fix that; the same registry and test protocol must carry over.
- Wrongful-pend cost is the weakest-sourced term. It needs interview data before the score is trusted.

## Proposed first steps

1. Confirm the repository name (suggestion: `em-prepay-agent`), public, MIT, same copyright.
2. Copy the files in the [copy-list](prepay_copylist.md); record the source commit in `LINEAGE.md`.
3. Write prepay score 1.0 and the claim environment (new).
4. Reference arms on D4.2 development seeds; then the usual process: freeze, test once, close out.
