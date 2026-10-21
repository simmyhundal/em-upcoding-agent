# Prior authorization as an adjacent use case: what we can and cannot size

[Back to the README](../README.md)

Research note, 2026-10-21. Question: could an agentic system that replaces human-led prior authorization (PA) work, with better accuracy, faster answers and lower administrative cost, be a second use case beside E/M upcoding detection? Sources are public web pages read today, the Elion briefing of 2026-09-15 that Simmy shared, and UnitedHealth's FY2025 10-K that Simmy shared. Where a figure came through a search summary it is marked. This note sizes nothing: the inputs that would size it are mostly not public, and it says which.

## Verdict

Worth keeping on the list; not yet sizable from public data, and different in kind from the upcoding product.
- **Management intent is public and strong**: UnitedHealth and Elevance both put AI on PA, and the industry pledge sets a real-time target for 2027.
- **The volume is falling and the part an agent may do is the cheap part**: the pledge cuts PA scope and keeps denials with clinicians, so the automatable work is triage and approvals, which cost the plan administration but do not lower medical cost.
- **The buyers are also the builders** at the two largest plans.

## What the Elion briefing says (drug PA, mostly the provider and pharmacy side)

- The sequence is the same everywhere: learn that PA is needed, open the case, answer the plan's question set from the chart, read the determination, work the denial. Steps with a published standard (NCPDP SCRIPT electronic PA transactions for drugs, X12 278 for medical-benefit drugs) keep getting faster; the steps without one are where the work stays: who answers the question set, who owns renewals.
- Newer tools read the chart against the plan's published criteria with a person reviewing; a confidence threshold decides whether a request goes out unattended; an incomplete request "comes back denied about as fast as a complete one comes back approved".
- The slowest work is appeals, where the prescriber writes a letter of medical necessity; statutory clocks run from 72 hours (Part D coverage determination, 24 if expedited) to four months (ACA external review).
- It does not mention Elevance. Market signals in it: Forus (drug PA and medication access) raised $150M at a $3B valuation; Inova partnered with Anomaly to flag wrongful denials and downcoding across its payer contracts; Abridge launched Pre-Bill Review. Providers are automating *their* side, which is the counterpart of what a plan would automate.

## What plans and regulators say

- **UnitedHealth, Q2 2026 call** (third-party transcript, [Webull](https://www.webull.com/news/15237979893818368)): a UnitedHealth executive said "process 80% of our prior authorizations in real-time by the end of 2027"; another cited digital PA producing "96% first passed approval" and AI making a nurse care manager "40% faster"; the CFO listed "AI-enhanced fraud, waste and abuse efforts" within commercial margin recovery. UnitedHealth's FY2025 operating cost ratio was 13.3% (13.2% in 2024, 14.7% in 2023), the line where administrative savings land.
- **Elevance** (search summaries of the April 2026 call, [Becker's](https://www.beckerspayer.com/payer-issues/inside-elevances-1b-ai-investment.html)): about $1B across digital and AI capabilities; the CEO says its Health OS platform and AI tools cut PA denials by nearly 70% (company-reported; one secondary source gives 61% for denials citing insufficient clinical information, so the metric is unclear).
- **Industry pledge** (June 2025; [Medical Economics](https://www.medicaleconomics.com/insurance-companies-vow-to-fix-prior-authorization-process-again), [Healio](https://www.healio.com/news/primary-care/20250623/hhs-announces-industry-pledge-to-reduce-and-simplify-prior-authorization) via search summaries): reduce the scope of medical PA by 2026, standardize electronic PA on FHIR APIs by 1 January 2027, answer at least 80% of electronic approvals with full documentation in real time in 2027, keep clinical review by medical professionals for every non-approval on clinical grounds. Voluntary, no enforcement; AHIP reports PA volume down 11% in a year (its own figure).
- **Federal rule** (CMS-0057-F, [CMS](https://www.cms.gov/newsroom/press-releases/cms-finalizes-rule-expand-access-health-information-and-improve-prior-authorization-process), search summary): decisions in 72 hours (expedited) and 7 calendar days (standard) from 2026, with a specific denial reason, and public PA metrics. It covers Medicare Advantage, Medicaid and CHIP; CMS's own release excludes federal-exchange plans, and employer commercial plans are not covered, so for our target (commercial) the clocks come from state law and contracts.
- **Accuracy is a real cost today**: in Medicare Advantage, [KFF](https://www.kff.org/medicare/medicare-advantage-insurers-made-nearly-53-million-prior-authorization-determinations-in-2024/) reports about 52.8M determinations in 2024, 7.7% denied in full or part, 11.5% of denials appealed, 80.7% of appeals overturned. By insurer: UnitedHealthcare 12.8% denied, Centene 12.3% denied with 95.5% of its appeals overturned, Elevance 4.2% denied. A high overturn rate means avoidable administrative rework and provider friction, the same abrasion our score 4.0 prices. Commercial equivalents are not public in this source.

## Why it is adjacent, and where it is not

Fits our assets: reading a chart against written criteria is the same capability as our review step; our evaluation harness (a simulated office, an answer key, a score in net dollars with a provider-friction term) transfers; an appeal-overturn rate is a natural ground-truth proxy for a wrong denial.

Does not fit, or fits less:
1. **Different economics.** An upcoding tool lowers medical cost (and the plan's medical loss ratio). A PA agent lowers administrative cost (operating cost ratio) and can raise medical cost if it approves faster; PA exists to contain spend.
2. **Denials are regulated.** The pledge keeps denials with clinicians, and the briefing notes states barring non-human clinical decisions. An agent can assemble, triage and approve; a clinician still decides a denial.
3. **Shrinking and built in-house at the top.** Volume is being cut by the plans themselves, and the two largest plans are building. The addressable buyer is more likely a mid-size plan, a delegated utilization-management vendor, or a provider-side access team.
4. **New data model.** We would need PA requests, criteria, approvals, denials and appeal outcomes as ground truth; nothing in the repository covers it.

## Sizing frame (inputs, with what we have)

PA agent value per year ~ (determinations per year) x (share the agent can complete or triage) x (plan cost per human-handled determination) + (appeals avoided) x (cost per appeal) - (agent and review cost).

| Input | Have | Missing |
|---|---|---|
| Determinations per year | Medicare Advantage: about 52.8M in 2024 (KFF); the briefing gives no counts | Commercial counts by plan; drugs versus medical |
| Share automatable | UnitedHealth target 80% real-time by end of 2027; pledge: 80% of electronic approvals in real time | What share of *all* requests, and how many are approvals the agent can finish |
| Plan cost per determination | Nothing sourced. A 2020 provider-side figure is $13.40 manual against $3.76 electronic ([CAQH via search summary](https://www.caqh.org/sites/default/files/core/CAQH%20CORE%20CCF-PAN%20PA%20Pilot%20Case%20Study%20Webinar%20Part%202%20Slides%20.pdf)); the payer-side figure was not found | Payer-side cost, current edition |
| Appeals | MA: 11.5% of denials appealed, 80.7% overturned (2024) | Cost per appeal; commercial rates |
| Competing spend | Elevance about $1B and UnitedHealth about $1.5B AI budgets (secondary sources) | What share is PA |

I am not putting a dollar figure on it: every multiplier but the Medicare Advantage volume is missing or old, and the volume itself is for the wrong market (our target is commercial). Putting numbers into this grid before sourcing them would make a market size out of assumptions.

## Next

1. Source payer-side cost per PA determination and per appeal (current CAQH Index edition, plan and vendor disclosures).
2. Source commercial PA volume (state reports, employer-plan surveys, the first public PA metrics reports plans filed in 2026 for Medicare Advantage and Medicaid as a scale proxy).
3. Layer 2 interviews: who buys PA automation (plan UM leaders, delegated vendors), and on what terms.
4. Decide whether PA is a second product or only a source of design ideas (confidence thresholds, evidence gating, abrasion) for the upcoding line.
