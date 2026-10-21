# What commercial health plans say about coding and cost: earnings and analyst layer

[Back to the README](../README.md)

Research note, 2026-10-21. Layer 1 of three (earnings and analysts; buyers and budgets; sizing). Everything below is from public web pages read on 2026-10-21; where a page was a third-party transcript or summary, it is marked. Nothing here is a finding about willingness to pay: layer 1 does not reach that.

## Bottom line

1. **The hypothesis holds in a narrow form.** Stock moves of the large plans follow the medical care ratio (medical costs over premiums), medical cost trend and guidance, not E/M coding as such. Provider coding intensity is named by management as one contributor to trend and is not quantified.
2. **Coding intensity is on the record at the biggest plans**, in office visits and emergency departments (UnitedHealth), hospital acuity (Elevance, Centene) and inpatient secondary diagnoses (the Blue Cross Blue Shield Association study).
3. **Plans are already acting on E/M levels with automated policies**, not only investigations: Cigna and Aetna started level 4 and 5 review programs on 2025-10-01; Anthem's was paused after California regulators and physician groups objected. This is the competing approach our product meets, and it shows the provider and regulator backlash that our abrasion term stands for.

## Evidence

### What moves the stock

| Item | What the source says | Source type |
|---|---|---|
| UnitedHealth Q3 2026 (2026-10-13) | Medical care ratio 88.4% against 89.9% a year earlier; adjusted EPS $4.69 against a consensus around $4.12 to $4.15; full-year guidance raised to at least $20.50; shares up about 3% to 4% that day | [SEC 8-K via search](https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm), [XTB](https://www.xtb.com/en/market-analysis/news-and-research/unitedhealth-group-shares-gain-3-after-stronger-than-expected-earnings-and-guidance), [247 Wall St](https://247wallst.com/investing/2026/10/13/unitedhealth-rises-4-on-earnings-beat-and-raised-full-year-outlook-humana-advances-2/) (search summaries; I did not open the 8-K) |
| UnitedHealth Q1 2026 | Medical loss ratio 83.9% against 85.5% expected; guidance raised | [Healthcare Uncovered roundup](https://healthcareuncovered.substack.com/p/big-insurance-q1-2026-earnings-round) (fetched) |
| UnitedHealth 2025 reset | After the 2025 guidance cut, analysts treated the ratio as the key metric; shares closed more than 7% lower when the outlook was reissued in July 2025 | [NBC/CNBC via search](https://www.nbcchicago.com/news/business/money-report/unitedhealth-says-2025-earnings-will-be-worse-than-expected-as-high-medical-costs-dog-insurers/3799928/) (search summary only; the one-day moves differ across sources) |

Reading: the stock reacts to the ratio against consensus and to the guidance, so a vendor's value to a plan reaches the stock only through basis points of medical cost. Not tested here: whether any analyst models E/M coding specifically.

### What plans say about coding

- **UnitedHealth, Q2 2026 call (2026-07-16)**, from a third-party transcript ([Webull](https://www.webull.com/news/15237979893818368); speaker names are garbled in the transcript, so check against the webcast): commercial medical cost trend "modestly above the 11% level we previously saw"; "provider coding intensity with office visits, emergency departments" is "also contributing incremental trend", with no basis-point figure for coding; "more aggressive billing practices among providers, especially higher service encoding intensity". The No Surprises Act arbitration process is quantified separately: about 50 basis points of incremental trend in 2026, totaling at least 100 basis points. Management also lists "AI-enhanced fraud, waste and abuse efforts" as part of commercial margin recovery and targets a commercial group margin of 7% or more.
- **Correction of a secondary source.** A [Yahoo Finance piece](https://finance.yahoo.com/healthcare/articles/unitedhealth-inside-942-million-industry-113644250.html) ties "roughly 100 basis points" to arbitration abuse and coding intensity together. In the transcript the 100 basis points is the arbitration figure; coding has none. Do not quote 100 basis points for coding.
- **UnitedHealth, Q2 2025, Elevance, Centene** (from [HFMA, 2025-07-29](https://www.hfma.org/revenue-cycle/reeling-payers-plan-to-increase-scrutiny-of-providers-coding-practices/), fetched): UnitedHealth's CEO cited "more aggressive care provider coding and billing technologies"; Elevance's CEO said AI-enabled coding tools let hospitals increase documented acuity, that outlier claims go through payment integrity, and called it "a bit of a catch-up game"; Centene's CEO reported "a step-up in coding intensity" and plans to put AI into its own payment integrity work. E/M levels are not named in that article.
- **Blue Cross Blue Shield Association study** (September 2026): about $942 million more cost for member plans against 2023 over two years, $653 million of it from secondary diagnoses; diagnoses rose without a matching rise in treatment; inpatient claims; hospitals reportedly dispute the reading. Sources disagree on the release date (17 or 24 September) and the window, so check the [Fierce Healthcare piece](https://fiercehealthcare.com/finance/hospitals-use-ai-coding-tools-cost-bcbsa-plans-942m-more-similar-care-analysis) (not fetched: 403) or the association's release. It is inpatient, not E/M.
- **Moody's** lists higher provider coding intensity among 2026 cost drivers in its [negative sector outlook](https://www.fiercehealthcare.com/payers/moodys-insurers-2026-outlook-negative-cost-pressures-continue-batter-industry) (search summary only; the page returned 403).
- **No coding commentary found** in the Q1 2026 roundup for Cigna, CVS/Aetna, Centene, Humana or Molina. That is silence in one roundup, not proof they say nothing.

### What plans are doing about E/M levels

- **Cigna policy R49**, effective 2025-10-01: automated review of 99204, 99205, 99214, 99215, 99244 and 99245, adjusting by one level where documentation is judged not to support the billed level; the higher level is paid if records later support it ([Peregrine Healthcare](https://peregrinehealthcare.com/cigna-aetna-downcoding-policy/), a vendor summary; read Cigna's own policy). One search summary says it applies to providers with a consistent pattern of higher coding against peers, and that Maryland's insurance regulator fined Cigna and ordered it to stop automatic downcoding; I could not confirm either from a primary source.
- **Aetna Claim and Code Review Program**, 2025-10-01: level 4 and 5 visits reviewed by certified coders against CMS and AMA guidelines; providers can send records for reconsideration (same vendor summary).
- **Anthem** E/M downcoding, planned for 2026-02-15, paused while California's Department of Managed Health Care reviews it; physician groups cite lack of transparency and possible conflict with prompt-pay and disclosure law ([California Medical Association](https://www.cmadocs.org/newsroom/news/view/anthem-extends-pause-on-e-m-downcoding-policy-until-april-1)). The pause end date differs across CMA updates (April 1, May 1).
- Specialty societies and the AMA oppose these programs; one search result dates an otolaryngology society's letters to September 2026.

## What this means for the product (inference, not finding)

- **The pain is real and named in E/M and ED visits at the largest commercial plan**, but unquantified in the public record, so the sizing in layer 3 cannot come from earnings calls.
- **The incumbent response is policy-based and automatic.** A claim-level downcoding rule is cheap and is being contested by regulators and providers. A tool that targets providers, requests charts, and recovers only what a sample supports sits at the other end: more labor, less provider friction, defensible under review. Our score 4.0 prices that trade (staff cost and abrasion), and these programs are the comparison a buyer will make. Whether buyers value defensibility enough to pay for it is a layer 2 question.
- **AI documentation tools** are named as a driver (Elevance, Centene, the association study). That bears on the data model: templated or ambient-scribe notes make chart-based checks weaker and note signs less reliable ([#144](https://github.com/simmyhundal/em-upcoding-agent/issues/144) and the note-realism items).
- **The abrasion term has a public analogue.** Regulator and physician-group action against automatic downcoding is the real-world counterpart of provider abrasion in score 4.0.

## Gaps and next steps

- Primary sources not yet read: UnitedHealth's 8-Ks and the full Q2 and Q3 2026 webcasts, Cigna's R49 policy text, the Maryland and California regulator documents, the Moody's report, Elevance's and Centene's 2026 transcripts.
- Not covered: Cigna, CVS/Aetna, Humana, Molina and Centene transcripts for coding language; analyst notes themselves (only news summaries of them); any dollar estimate of E/M upcoding for a commercial plan.
- Next: layer 2 (how payment integrity is bought: vendor models, contingency fees, RFPs, job postings, interviews) and layer 3 (sizing against our recovery per demand, issue [#145](https://github.com/simmyhundal/em-upcoding-agent/issues/145)).
