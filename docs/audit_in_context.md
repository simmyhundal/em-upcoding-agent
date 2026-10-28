# The postpay audit in context

[Back to the README](../README.md) · [diagram and outcomes](audit_postpay_zoom.md) · [actors, KPIs and timeline (research)](audit_actors_research.md) · [money flow (research)](audit_money_flow_research.md)

A health plan pays a claim first and checks it later. This page summarizes how that later check works and how much money it moves. Almost no commercial figures are published, so most numbers are Medicare or Medicaid analogs, marked as such.

## The seven stages
1. The patient has symptoms and seeks care.
2. The provider sees the patient and documents the visit.
3. The provider submits the claim (837P).
4. The plan adjudicates, applying prepay edits, and pays with a remittance (835).
5. The plan audits paid claims.
6. The plan recovers incorrect payments.
7. Collections, appeals and vendor fees.

PI Agent covers stages 5 to 7, the postpay audit.

## Who takes part
| Actor | Role in the audit |
|---|---|
| Payment integrity analyst | Picks providers to audit from claims history, peers and tips |
| Coder, nurse, clinician | Reads charts and sets the correct level |
| SIU | Takes suspected fraud cases and refers them out |
| Legal, medical director | Hears provider disputes (30 days to answer) |
| Finance and recovery | Sends the overpayment notice and offsets later payments |
| Vendor (optional) | Finds or recovers for a contingency fee, 15% to 30% |
| Provider | Answers the records request (30 to 45 days), repays or disputes |

From records request to written finding takes about 2.5 to 4.5 months; a dispute adds two to four more. State look-back limits run from 180 days (Texas) to 24 months (New York).

## Where $100 of E/M payments goes
The base is $100 a plan paid providers for E/M visits on 835s, after prepay edits. Each row is a share of the row above.

| # | Step | Value | Source status | Derivation |
|---|---|---|---|---|
| 0 | Paid by the plan for E/M visits | $100.00 | base | [definition](#derivation-notes "the 835 payment") |
| 1 | Upcoded (paid at too high a level) | $4.50 | analog | [$100 x 4.5%](#derivation-notes "Medicare CERT 2025: $1.47B upcoded of $32.3B E/M dollars paid; a Medicare rate applied to commercial dollars") |
| 2 | Found by a postpay audit | $0.104 | derived | [row 3 / 60%](#derivation-notes "backed out: if about 60% of what is found is collected, collected / 0.60 is what was found") |
| 3 | Collected | $0.062 | analog | [row 1 x 1.4%](#derivation-notes "Medicare Recovery Auditors collected $346M in FY2021 against $25.03B of improper payments measured for FY2021") |
| 4 | Kept after vendor fees | $0.050 | sourced (point in a range) | [row 3 x (1 - 20%)](#derivation-notes "commercial vendors take 15% to 30%; 20% is a point in that range") |
| 4A | Alternative: every upcoded dollar found | $2.16 | derived | [row 1 x 60% x 80%](#derivation-notes "before the cost of review and provider abrasion") |

### Derivation notes
- **Base.** The 835 payment is the allowed amount minus the patient's cost-sharing, which is outside the base. Medicare's error rate is measured on dollars paid, so it applies directly.
- **Upcoded.** Medicare's yearly record-review sample found 4.5% of E/M dollars paid at too high a level.
- **Collected.** Recovery Auditors collected $345.8M in FY2021; CMS measured $25.03B of improper payments for FY2021 (claims paid July 2019 to June 2020). That is 1.4%, for all error types, one contractor type, and a pandemic year.
- **Found.** Collected divided by 0.60, the share of identified overpayments Medicaid plans collected (68%, net of appeals).
- **Fees.** Commercial vendors take 15% to 30%.

### Why not recover the whole 4.5%?
The 4.5% is a national estimate and names no provider. Recovery means choosing providers, drawing a valid sample of each provider's claims, reading the charts, extrapolating the findings to all the provider's claims, and defending the demand on appeal. Each provider's sample must pay for itself (about $158 per chart review at Medicare's Recovery Auditors), records requests are capped at 0.5% of a provider's claims a year, look-back periods are limited, and about 42% of first-level Part B appeals favored the provider.

## Who keeps the recovered dollar
- **Self-funded plan** (two-thirds of covered workers): the employer's plan, less any vendor fee.
- **Fully insured plan:** the insurer, unless its loss ratio is below the floor (80% or 85%), in which case enrollees get a rebate.
- **Medicare:** the trust funds, less fees.

## Not modelled
Timing against state limits, patient cost-sharing refunds, network effects of audits, vendor incentives, and how a plan books recoveries under the loss-ratio rule.
