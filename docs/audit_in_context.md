# The audit in context: who takes part, where the dollars go

[Back to the README](../README.md) · [actors, stages, KPIs and timeline (research notes)](audit_actors_research.md) · [dollar funnel (research notes)](audit_money_flow_research.md) · [diagram reference](audit_diagram_reference.md)

**What this page is.** A health plan pays a visit's claim first and checks it later. This page shows what that later check looks like in the real world (who does what, how long each hand-off takes, who keeps the money) so a reader can see which part of it this project simulates. It is a summary of two research notes written on 2026-10-27; every figure there carries a source and a fit grade (A commercial, B Medicare or Medicaid analog, C context). Almost no commercial figure is published, so most numbers are analogs, and the page says so where it matters.

![Swimlane of the commercial postpay audit, stages 1 to 7](images/audit_workflow.png)

(Vector version: [audit_workflow.svg](images/audit_workflow.svg).)

The diagram is hand-written SVG, shown here as a 2400-pixel PNG so it stays sharp on a tablet. An editable copy for diagrams.net or Miro is not drawn yet; the structure follows the reference in [audit_diagram_reference.md](audit_diagram_reference.md).

## The seven stages
1. The patient has symptoms and seeks care. 2. The provider sees the patient and documents the visit. 3. The provider submits the claim (an 837P). 4. The plan adjudicates (prepay edits, then payment and an 835 remittance): the provider's happy path. 5. The plan audits paid claims. 6. The plan recovers incorrect payments: the plan's happy path. 7. Collections, appeals and vendor fees. This project simulates 5 to 7; stage 4's edits are the contrast (the prepay line of work).

## Who is in stages 5 to 7, and how they are measured
- **Payment integrity team** picks providers from the paid-claims history (billing against peers, tips, complaints). Measured by savings and recoveries net of cost.
- **Coders and clinical reviewers** read the charts. Measured by accuracy and charts an hour; no published standard was found (10 to 15 an hour is from job ads).
- **SIU** (special investigations unit; state law requires one in New York and California) takes suspected fraud. New York plans reported about $3.5B in "savings" against $40.3M in recoveries: the value is mostly prevention.
- **Medical director and legal** hear disputes (30 days to dispute, 30 to answer in the one commercial policy read in full, Blue Cross VT).
- **Provider side:** practice administrator and compliance answer the records request (30 days, up to 45); the billing office repays, disputes or appeals.
- **Vendors** find or recover for a contingency fee: commercial 15% to 30%, government 8% to 17%.
- **Employer** (two-thirds of covered workers are in self-funded plans) owns the recovery; the administrator or vendor takes a fee, and courts have asked whether that is a fiduciary matter.
- **Regulators** set look-back limits (180 days in Texas to 24 months in New York) and watch recoupment practice.

## How long each hand-off takes (assumptions marked)
Records request to response 30 to 45 days; review 30 to 60 days (assumption); findings meeting and written notice 2 to 4 weeks (assumption); so about 2.5 to 4.5 months from request to written finding. Undisputed repayment adds one month; a disputed one adds two to four; an appeal or fraud referral takes one to two years or more. In Texas the plan must select the provider and send the request within roughly a quarter of payment. The simulation has no payment-to-demand clock yet, so these limits are not in the score.

## Where $100 of E/M payments goes
The base is $100 that the plan paid a provider for E/M visits on 835 remittances, after the claims passed prepay edits and checks. This repository's work starts there. Each row is a share of the row above. "Source status" says how well sourced the inputs are (sourced, analog = a Medicare or all-payer figure used as a stand-in, assumption); "Derivation" shows the arithmetic, with the reasoning on hover and in the notes below.

| # | Step | Value | Source status | Derivation |
|---|---|---|---|---|
| 0 | Paid by the plan to providers for E/M visits | $100.00 | base | [definition](#derivation-notes "the 835 payment; the starting point of this repository's work") |
| 1 | ...of which paid at too high a level (upcoded) | $4.50 | analog | [$100 x 4.5%](#derivation-notes "Medicare CERT 2025: $1.47B upcoded of $32.3B E/M dollars paid; a Medicare rate applied to commercial dollars") |
| 2 | Found by a postpay audit program | $0.23 | assumption, no source | [row 1 x 5%](#derivation-notes "the share of upcoded dollars a postpay program identifies; the largest unknown") |
| 3 | Collected (net of appeals and time) | $0.135 | analog | [row 2 x 60%](#derivation-notes "payers' sources: 55% to 70% of ordinary overpayments identified are collected, already net of appeals") |
| 4 | Kept after vendor fees and own cost | $0.108 | assumption | [row 3 x (1 - 20%)](#derivation-notes "commercial contingency fees run 15% to 30%; in-house about 6%") |
| 5 | Ceiling: every upcoded dollar found | $2.16 | derived | [row 1 x 60% x 80%](#derivation-notes "before the cost of review and provider abrasion") |

### Derivation notes
- **Base.** The plan's payment on the 835 is the allowed amount (the contract price) minus the patient's cost-sharing (copay, deductible, coinsurance). The patient's share is outside the base: a plan recovers its own overpayment, and refunding patients is a separate, unmodelled step. Medicare's error rate is measured on dollars Medicare paid, so it applies to this base directly.
- **Upcoded share.** Medicare's yearly record-review sample found 4.5% of E/M dollars paid at too high a level (3.1% for established office visits; a 2010 audit found 21% of E/M dollars improper).
- **Found.** The share of those upcoded dollars the audit program identifies. It is not a Medicare figure and not money recovered: recovery is row 3. Cross-check: Medicare's Recovery Auditors collected about $346M in FY2021 against roughly $29B of measured overpayments, about 1%, for all error types and counting collections rather than findings. Our 5% found and 60% collected give 3% collected, above that. Treat 5% as generous.
- **Collected.** Medicaid plans collected 68% of ordinary overpayments identified and 16% to 24% of fraud-type ones.
- **Fees.** 20% central.
- **Before the base (not shown).** The share of billed dollars stopped before payment (about 10%, mostly eligibility denials), the allowed-to-billed ratio (about 0.45, our assumption) and E/M's share of all payments (about 9%).

### Why not go after the full 4.5%?
Medicare does not review all of a provider's claims. It reads a random sample of that provider's charts and extrapolates the overpayment found to all of the provider's claims in the look-back period, usually at the lower bound of a 90% confidence interval (this repository does the same). So the limit is not reviewing every claim. The limit is that Medicare's 4.5% is a national estimate from a sample of claims, and it names no provider. Recovering money means choosing the providers worth pursuing, drawing a valid sample of each provider's claims, reading the charts, defending the extrapolation and issuing a demand. Each step costs money and meets limits:
- **Each provider's sample has to pay for itself.** Medicare's Recovery Auditors spent about $158 per chart review (GAO, 2016) and a sample needs dozens of charts, so a provider whose upcoding is small or whose claims are few is not worth a sample. Extrapolation is also contestable: the sample must be valid and the provider can appeal it. Score 4.3 builds this trade-off in.
- **Record requests are capped.** A Recovery Auditor may request records on at most 0.5% of a provider's paid claims a year, adjusted by the provider's error history.
- **Look-back and reopening limits** (three years for Recovery Auditors) and, commercially, state limits of 180 days to 24 months.
- **Appeals reverse many findings.** About 42% of Part B decisions at the first appeal level were fully favorable to the provider (FY2021).
- **Much of the error is documentation, not coding.** Two-thirds of Medicare's improper dollars are missing or insufficient documentation, which a reviewer must treat differently from a coding level.
- **Pursuit has costs beyond dollars:** provider relations and network adequacy.

The practical answer is that the recoverable amount is the part where expected recovery beats the cost of pursuing it, which is the problem this repository optimizes. The list above is partly sourced (review cost, request cap, appeal rate) and partly my inference (that most providers' extrapolated overpayment is too small to cover a sample's cost).

### What the Medicare numbers measure
Medicare's 4.5% (row 4) is an error rate, not money recovered. Its yearly sample (CERT) pulls claims Medicare has **already paid**, reads the records and counts the dollars paid at too high a level. It therefore measures what got through prepay review, so it has no prepay share. Recovery is a different, much smaller number: the Recovery Auditors collected $346M in FY2021 against tens of billions of measured overpayments. There is no published dollar split of Medicare E/M recoveries between prepay and postpay review; only counts (contractors do about 98% of their reviews before payment, the Recovery Auditors about 85% after). Medicare says prepay review prevented about $5B in FY2015, but its own auditors found the savings method inconsistent. For commercial plans nothing comparable is published. Prepay edits are assumed to catch almost no level-of-service upcoding, which is why the postpay program works on what is left.

Reading the table: of $100 the plan paid for E/M visits, $4.50 is upcoded. A postpay program keeps about **$0.11**; even finding every upcoded dollar would keep about $2.16.

## Who keeps the recovered dollar
Self-funded plan: the employer's plan, less the fee. Fully insured plan: the insurer, unless its medical loss ratio is below the floor (80% individual and small group, 85% large group), in which case enrollees get it as a rebate. Under the loss-ratio rule, recoveries from providers lower the ratio; fraud recoveries are added back up to the fraud work's cost. Medicare: the trust funds (52% of 2021 Recovery Audit collections). Medicaid managed care: set by the state contract.

## What else to think about (not modelled, or only partly)
1. **Which plan, which law.** Self-funded plans escape state recoupment limits (ERISA); fully insured plans do not. The simulation has one rule for everyone.
2. **Provider abrasion.** Automatic downcoding (Cigna's R49, Aetna's program) drew regulators and societies; a records-based sample is the defensible alternative, but abrasion is a modelled assumption (score weights), not a measurement. Network adequacy limits how hard a plan can push.
3. **Vendor incentives.** A contingency fee rewards finding and collecting, and the check is the appeal and the refund. A vendor can also pass cost to the employer.
4. **Payer incentives under the loss-ratio rule.** A plan above the floor keeps the recovery; one near it gives part back, so the same finding is worth less. Not in the score.
5. **Timing.** State clocks, payment-to-audit lag and appeal durations are research findings, not simulation inputs.
6. **Patient impact.** Members see an explanation of benefits and can report services not received; downcoding can change what they owe. Not modelled.
7. **Prepay versus postpay.** Most value is created before payment; the postpay product is the part left when prevention fails, and the dollar gap in the table is the opportunity and the difficulty.
8. **Data sources.** The payer holds claims history, not charts; charts come only by request, and only about a third of attachments move electronically. The project's data are synthetic and cover one year.
9. **Evidence quality.** No published commercial improper-payment rate, collection rate on E/M demands, reviewer productivity standard or share of dollars audited. The research notes list each gap and how it could be closed (interviews, state filings, a pilot sample).
10. **Who the customer is.** Budget owner (payment integrity, claims operations, network management) decides which of these matters; the prepay discovery note lists the questions for the people who know.
