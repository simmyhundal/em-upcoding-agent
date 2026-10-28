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

## Where $100 billed goes (central case in the middle column)
The base is the $100 a provider asks for on the first professional claim (837P), not a payer's total spend. Each row is a share of the row it names. Low, Central and High are ordered by value to the payer, so Low has the highest prepay stop and lowest prices. "Source status" says how well sourced the inputs are; "Derivation" shows the arithmetic (hover for the reasoning, details under the table).

| # | Step | Low | Central | High | Source status | Derivation |
|---|---|---|---|---|---|---|
| 0 | Billed on the first professional claim (837P) | $100.00 | $100.00 | $100.00 | base | [base](#derivation-notes "the base of the table") |
| 1 | Stopped before payment (initial denials and prepay edits, net of later reversals) | $15.00 | $10.00 | $5.00 | analog; assumption in the ends | [$100 x 10%](#derivation-notes "initial denial 11.8% overall, 15 to 20% private; over half later paid") |
| 2 | Allowed (contract) amount on the claims that go on to payment | $29.75 | $40.50 | $57.00 | assumption on a sourced anchor | [$100 x (1 - 10%) x 0.45](#derivation-notes "HCCI: commercial about 110% to 122% of Medicare; charges 2.5 to 3 times Medicare is a guess") |
| 3 | ...of which E/M visits (all evaluation and management) | $2.08 | $3.65 | $6.27 | analog, derived | [row 2 x 9%](#derivation-notes "7.3% Medicare, about 11% commercial") |
| 4 | ...of which paid at too high a level (upcoded) | $0.06 | $0.16 | $0.63 | analog; assumption in the high case | [row 3 x 4.5%](#derivation-notes "CERT counts payments already made in error: what prepay did not stop") |
| 5 | Found by a postpay audit program | $0.0006 | $0.0082 | $0.16 | assumption, no source | [row 4 x 5%](#derivation-notes "the largest unknown") |
| 6 | Collected (net of appeals and time) | $0.0004 | $0.0049 | $0.11 | analog | [row 5 x 60%](#derivation-notes "already net of appeals; do not cut again") |
| 7 | Kept after vendor fees and own cost | $0.0003 | $0.0039 | $0.10 | assumption | [row 6 x (1 - 20%)](#derivation-notes "contingency fees 15 to 30%") |
| 8 | Ceiling: every upcoded dollar found | $0.03 | $0.08 | $0.41 | derived | [row 4 x 60% x 80%](#derivation-notes "if reach were 100%") |

### Derivation notes
- **Row 0.** Definition: the $100 the provider asked for.
- **Row 1.** 10% central: initial denials run 12% to 20% and more than half are later paid (Kodiak, Premier), so about 5% to 8% net; 10% is the upper-central choice. Mostly eligibility and administrative denials: prepay is assumed to catch almost no level-of-service upcoding.
- **Row 2.** = $100 x (1 - row 1 share) x allowed-to-billed ratio 0.45. Anchor: commercial professional prices average 122% of Medicare (HCCI 2017). The charge-to-Medicare multiple (about 2.5) is our guess; no published allowed-to-charges ratio was found. Allowed includes the patient's cost-sharing.
- **Row 3.** = row 2 x E/M share 9%. Medicare spends 7.3% of its dollars on E/M; commercial professional services are 33.6% of spend and E/M is over a third of those, about 11%; 9% sits between.
- **Row 4.** = row 3 x 4.5%. Medicare's CERT 2025 sample found $1.47B of $32.3B E/M dollars upcoded. Low 3.1% (established office visits); high 10% (our assumption toward a 2010 audit). A Medicare error rate applied to commercial dollars.
- **Row 5.** = row 4 x share reached: 1%, 5% or 25%. Targeting helps: a 2010 audit found 56% of claims upcoded among high-coding physicians against 27% for the rest.
- **Row 6.** = row 5 x 55%, 60% or 70%. Payers' sources: 68% of ordinary overpayments identified were collected; 16% to 24% for fraud-type cases. Already net of appeals.
- **Row 7.** = row 6 x (1 - fee). Fee 25%, 20% or 6%: commercial vendors take 15% to 30%; in-house is about 6% (a vendor's figure).
- **Row 8.** = row 4 x collected share x kept share. Before the cost of review and provider abrasion.

### What the Medicare numbers measure
Medicare's 4.5% (row 4) is an error rate, not money recovered. Its yearly sample (CERT) pulls claims Medicare has **already paid**, reads the records and counts the dollars paid at too high a level. It therefore measures what got through prepay review, so it has no prepay share. Recovery is a different, much smaller number: the Recovery Auditors collected $346M in FY2021 against tens of billions of measured overpayments. There is no published dollar split of Medicare E/M recoveries between prepay and postpay review; only counts (contractors do about 98% of their reviews before payment, the Recovery Auditors about 85% after). Medicare says prepay review prevented about $5B in FY2015, but its own auditors found the savings method inconsistent. For commercial plans nothing comparable is published. Prepay edits are assumed to catch almost no level-of-service upcoding, which is why the postpay program works on what is left.

Reading the central column: of $100 billed, about $40 is allowed, $3.65 of that is E/M, $0.16 is upcoded, and a postpay program keeps about **$0.004** (range $0.0003 to $0.10). Even finding every upcoded dollar would keep about $0.08. Prevention before payment is far larger (New York plans report about $87 of prepay savings per dollar recovered), which is the argument for the prepay repository. The reach share (row 5) has no source; this project's simulation is the only estimate available.

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
