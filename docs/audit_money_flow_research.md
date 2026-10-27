# Where the dollars go: a per-$100 funnel for commercial postpay audits (research notes)

[Back to the README](../README.md) · Research notes (2026-10-27, sub-agent). Summary page: [the audit in context](audit_in_context.md).

Research done 2026-10-27 for simmyhundal/em-upcoding-agent, read-only (web search and primary documents; PDFs were converted to text and read where they loaded). This page builds on `docs/score_43_sources.md`, `docs/score_43_sources_addendum.md`, `docs/market_tam_mlr_headroom.md` and `docs/market_research_earnings.md`, and does not repeat their tables; it cites them where a figure comes from there. **Fit** grades how well a source stands in for a commercial payer: **A** commercial and the same measure, **B** a public payer measuring the same thing (an analog), **C** context only. "Snippet" means the figure was seen only in search-result text, not on a page I read, and is unverified.

## Summary

Out of $100 that a commercial plan pays on claims, about $3 to $10 is paid in error. The only rigorous measurement, Medicare fee-for-service CERT, gives $6.55 in FY2025, and about two-thirds of that is missing or insufficient documentation, not proven wrong care. E/M visits are roughly $7 to $11 of the $100. At Medicare's measured rates, the upcoded part of E/M is about **$0.20 to $1.10, central $0.40** (gross; about $0.05 less net of downcoding). Most payment-integrity value is created before payment: commercial SIUs in New York reported about $87 of prepayment "savings" for every $1 recovered after payment. After payment, records are requested on well under 1% of claims (Medicare: claim counts). Payer-side sources say about 55% to 70% of identified ordinary overpayments, and 16% to 24% of fraud-type ones, turn into cash, net of appeals. Vendor contingency fees take 15% to 30% of what is collected, and other collection costs run from about 6% (in-house, a vendor's assumption) to 25% (Medicare RAC fee plus CMS administration). Put together, a postpay E/M upcoding program recovers **cents per $100 of claims: about $0.01 at the central assumption (range $0.001 to $0.18), and about $0.17 even if every upcoded dollar were found (up to about $0.50 at the high values)**. Who keeps the money depends on funding. For about two-thirds of covered workers (self-funded plans; KFF 2025), it goes to the employer's plan, less the administrator's or vendor's fee. Fully insured plans keep it unless their medical loss ratio is below the floor, in which case it flows to enrollees as a rebate, and it is passed through to next year's premiums. Almost every number is Medicare or Medicaid; commercial sources are vendor marketing, one state regulator's totals, and policy text. The steps with no source at all are the share of upcoded dollars a postpay audit reaches, and the E/M share of commercial postpay findings. Those are assumptions below.

## The funnel: per $100 of commercial claims paid

The base is **dollars paid**. Prepayment edits and denials stop dollars before they are paid, so they are not part of the $100; they are shown in the box after the table. Each row is a share of the row it names; arithmetic is shown. Columns are scenarios ordered by net value to the payer, so in row 10 Low is the highest cost. Status uses three words: **sourced** (a commercial figure), **analog** (Medicare, Medicaid or all-payer), **assumption**. A chained row takes the weakest status of its inputs.

| # | Step | Low | Central | High | Status | Source (details in the sections below) |
|---|---|---|---|---|---|---|
| 0 | Commercial claims paid | $100 | $100 | $100 | base (definition) | |
| 1 | Paid in error, all causes (overpayments) | $3.00 | $6.50 | $10.00 | analog (central and ends; the ends are NHCAA fraud estimates without a published method) | Central: CERT FY2025 overpayment rate 6.5% (Medicare FFS). Low: NHCAA "conservative" 3% (fraud only, all payers). High: NHCAA's "as high as 10%" |
| 1a | ... of which no or insufficient documentation | $2.00 | $4.20 | $6.50 | analog | CERT FY2025: 12.0% + 53.0% = 65% of improper dollars |
| 1b | ... of which fraud and abuse | $1.50 | $2.20 | $3.00 | analog (all-payer estimates) | Shrank et al., JAMA 2019: $58.5B to $83.9B, about 1.5% to 2.2% of national spending; NHCAA 3% (conservative) |
| 2 | E/M visits paid (all E/M) | $7.00 | $9.00 | $11.00 | analog, derived | Medicare FFS 2025: E/M about $32.3B of $439.9B = 7.3% (derived from CERT K1). Commercial: professional services 33.6% of spend (HCCI 2017) x E/M "over one-third" of professional (PCC, snippet) = about 11% |
| 2a | ... of which office and outpatient visits (99202 to 99215) | $4.00 | $5.50 | $7.00 | analog, derived | Medicare 2025: established $16.1B + new $3.0B = $19.1B, 4.3% of FFS paid (improper dollars / rate, CERT G1). Commercial share not found |
| 3 | E/M overpaid by upcoding (gross) | $0.22 | $0.41 | $1.10 | analog (low, central), assumption (high) | Low: $7.00 x 3.1% (CERT 2025 established office visit upcoding rate). Central: $9.00 x 4.5% (CERT 2025 upcoding across E/M service types, $1.47B / $32.3B). High: $11.00 x 10% (assumption between CERT 2025 and OIG 2010, when 26% of E/M claims were upcoded and 21% of E/M dollars were improper) |
| 3a | E/M upcoding net of downcoding | $0.19 | $0.36 | $1.00 | analog, assumption | CERT 2025 downcoding: 0.4% (established) and 0.8% (new office visits) |
| 3b | E/M no-documentation dollars (nearest analog for "not rendered" or no response) | $0.07 | $0.11 | $0.30 | analog (low, central), assumption (high) | Low: $7.00 x 1.0% (established office visits, CERT F1). Central: $9.00 x 1.27% (no documentation is 12.6% of E/M improper dollars, which are 10.1% of E/M; K1). High: assumption. **Not proof that a visit did not happen** |
| 4 | Dollars put through postpay record review (all claim types) | $0.10 | $0.50 | $1.00 | assumption (anchored to claim counts) | Medicare: contractors reviewed "less than 1 percent" of more than 1B claims (GAO-13-522, snippet); RAC request cap 0.5% of a provider's paid claims (CMS, snippet). Both are **claim counts**. No commercial source |
| 5 | Overpayments identified postpay, all types | $0.10 | $0.25 | $1.20 | analog (low), assumption (central and high, from vendor marketing) | Low: Medicare RAC FY2021, $345.8M collected (+$52.7M overturned) against about $440B paid, about $0.09 (years differ). Central: one Cotiviti client, 0.2% postpay net savings (snippet). High: vendor programs claiming 1% to 3% of medical spend in total, about 40% of it postpay (ClarisHealth "over 60% prepay", snippet) |
| 6 | Share of upcoded E/M dollars a postpay program reaches | 1% | 5% | 25% | **assumption, no source** | Targeting helps: OIG 2010 found 56.4% of claims miscoded in its high-coding stratum against 42.3% for everyone else |
| 7 | E/M upcoding identified postpay = row 3 x row 6 | $0.002 | $0.021 | $0.28 | assumption (from rows 3 and 6) | $0.22 x 1%; $0.41 x 5%; $1.10 x 25% |
| 8 | Collected, net of appeals and time | 55% | 60% | 70% | analog | Ordinary overpayments: Medicaid plans recovered 68% of non-fraud overpayments (OIG 2018); CMS collected 55% of sustained OIG audit findings (OIG 2022). **Already net of appeals; do not also apply the 15% appeal cut.** Fraud-type cases: 16% to 24% (addendum) |
| 9 | E/M upcoding cash collected = row 7 x row 8 | $0.001 | $0.012 | $0.20 | assumption (from rows 7 and 8) | |
| 10 | Fees and own cost, as a share of collected | 25% | 20% | 6% | analog (25%, Medicare RAC), assumption (20%, 6%; vendor material) | Vendor contingency: 15% to 30% commercial. In-house: 6% (vendor assumption). RAC: 16.4% fee + 8.7% CMS administration = 25% |
| 11 | Net to the party that bears the claims risk = row 9 x (1 - row 10) | $0.001 | $0.010 | $0.18 | assumption (from rows 9 and 10) | |
| 12 | Ceiling: every upcoded dollar found (row 3a x 60% x 80%) | $0.09 | $0.17 | $0.48 | analog (rows 3a and 8; 20% cost) | Before the cost of review and provider abrasion |

**Prepayment box, outside the $100.** These dollars are never paid, so they never reach the funnel:

- New York health insurers' SIUs reported about **$3.5B in savings against $40.3M in recoveries** (2024 data), about 87 to 1 (NY DFS 2025 report; the same report also gives $3B and $30.6M for "2024" in another paragraph). Recoveries were about 1% of reported SIU value.
- Aetna has said about 95% of its SIU savings and recoveries were denied or reduced dollars (undated).
- Vendor figures: more than 60% of payment-integrity savings are prepay (ClarisHealth, snippet); one plan reached 1.1% prepay against 0.2% postpay (Cotiviti, snippet).
- Initial denial rates: HealthCare.gov insurers denied 19% of in-network claims in 2024 (KFF). That is a claim count, and the denials are mostly administrative or "other"; it is not a measure of improper billing.

**How to read it.** Rows 1 to 3 describe the problem. Rows 4 to 11 describe what a postpay program turns into cash. The gap between row 3 ($0.41) and row 11 ($0.01) is the product's opportunity and its difficulty: almost nothing upcoded is reached after payment. Row 6 is the lever, and it has no source. One internal check: row 7 over row 5 puts E/M at about 2%, 8% and 23% of all postpay findings. Since E/M is about 9% of claims dollars, the central 8% is plausible; the high case needs E/M to be found far more often than its share of dollars. Row 12 shows that even perfect reach yields under $0.50 per $100, which is about 50 basis points of claims at the high end and 17 at the central value.

---

## 1. What share of claims dollars is improper or wasteful

| Figure | Source and URL | Year | Setting | What it measures | Fit |
|---|---|---|---|---|---|
| Overall improper rate 6.55% ($28.83B); overpayments 6.5% ($28.75B); underpayments 0.2% ($0.96B); Part B 8.4% ($9.6B of $114.1B) | CMS, *2025 Medicare FFS Supplemental Improper Payment Data*, Tables A1, A4, L5, M5, https://www.cms.gov/files/document/nov-2025-medicare-ffs-supplemental-improper-payment-data-2025922.pdf ; CMS FY2025 fact sheet, https://cms.gov/newsroom/fact-sheets/fiscal-year-2025-improper-payments-fact-sheet | 2025 (FY2025) | Medicare FFS | Random sample of claims, records reviewed; dollars paid in error | **B.** The only rigorous claims-level rate; it measures payments to providers, the same unit as a commercial postpay audit |
| By error category (share of improper dollars): no documentation 12.0%, insufficient documentation 53.0%, medical necessity 15.3%, **incorrect coding 11.1%**, other 8.5% | Same, Table A3 | 2025 | Medicare FFS | Cause | B. Most "improper" dollars are paperwork. CMS: improper payment "is not a measure of fraud" |
| **E/M overall: $3.27B improper, 10.1%** (95% CI 9.0% to 11.1%); within E/M, incorrect coding 50.0%, insufficient documentation 31.1%, no documentation 12.6%, other 6.3% | Same, Table K1 | 2025 | Medicare Part B E/M | E/M error rate and causes | B |
| **Office visits, established: 5.3% improper ($853.7M)**; upcoding 3.1% ($489.7M, CI 2.4% to 3.8%); downcoding 0.4% ($66.8M); incorrect coding in total 3.5%; no documentation 1.0%; insufficient documentation 0.9% | Same, Tables G1, K3, F5, F4, F1, F2 | 2025 | Medicare | Rate by error type | **B, the best single analog for this product** |
| Office visits, new: 7.6% improper; upcoding 5.1%; downcoding 0.8% | Same, Tables G1, K3, F5 | 2025 | Medicare | Same | B |
| By code: 99214 5.0%, **99215 14.8%**, 99213 2.1%, 99204 5.4%, 99205 11.1%; one-level coding errors: 99215 8.7%, 99214 2.6% | Same, Tables K1, K2 | 2025 | Medicare | Per-code rates | B. Errors concentrate at level 5 |
| Upcoding across Part B: $1.55B, 1.4% of Part B; E/M service types $1.47B (my sum of the eight E/M rows) | Same, Table K3 | 2025 | Medicare | Upcoding dollars | B. Upcoding is about 4.5% of E/M dollars ($1.47B / $32.3B, where E/M paid = $3.27B / 10.1%) |
| Established office visits: "documentation supports lower level than billed" in 120 sampled claims; "higher level" in 7; no response in 12 | Same, Table 7 | 2025 | Medicare | Root causes (claim counts) | B. Upcoding outnumbers downcoding about 17 to 1 in claims with errors |
| Lines in error, established office visits: 182 of 1,040 (17.5%) | Same, Table N1 | 2025 | Medicare | Line count in error (any error) | B. A count, not dollars |
| 2010: **21% of E/M payments improper ($6.7B of $32.3B)**; 42% of claims incorrectly coded (**26% upcoded, 15% downcoded**); 19% lacking documentation; 79% of miscoded claims off by one level | HHS-OIG, *Improper Payments for E/M Services Cost Medicare Billions in 2010*, OEI-04-10-00181, https://oig.hhs.gov/reports/all/2014/improper-payments-for-evaluation-and-management-services-cost-medicare-billions-in-2010/ (PDF read) | 2014 (data 2010) | Medicare | OIG record review; claim counts and dollars | B. The high end; it predates the 2021 E/M guideline change, which made levels easier to support |
| Medicare Part C 6.09% ($23.67B) | CMS FY2025 fact sheet | 2025 | Medicare Advantage | **Risk-adjustment diagnoses** submitted by plans | **C. Not plan-to-provider claims; left out of the funnel** |
| Medicaid 6.12% ($37.39B), 77% of it insufficient documentation; managed care component about 0% | CMS FY2025 fact sheet; KFF on PERM, https://www.kff.org/medicaid/a-look-at-the-medicaid-payment-error-rate-measurement-perm-program-and-upcoming-changes-and-impacts/ | 2025 | Medicaid | PERM: fee-for-service claims and eligibility; the managed care component measures **capitation payments only**, not plan payments to providers | **C for the funnel.** No measured rate exists for plan payments to providers in Medicaid managed care |
| Fraud "a conservative estimate is 3%" of spending; some agencies put it "as high as 10%" | NHCAA, https://www.nhcaa.org/tools-insights/about-health-care-fraud/the-challenge-of-health-care-fraud/ | undated (2018 spending base) | All payers | Fraud losses, an estimate without a published method | B to C. The figure most often cited for commercial fraud, but not a measurement |
| Waste $760B to $935B (about 25% of spending); **fraud and abuse $58.5B to $83.9B**; pricing failure $230.7B to $240.5B | Shrank, Rogstad, Parekh, *JAMA* 2019;322(15):1501-1509, doi:10.1001/jama.2019.13978 (via secondary summaries; abstract not opened) | 2019 | All payers | Review of 71 estimates | C. Waste is mostly not recoverable by audit. The fraud-and-abuse line is about 1.5% to 2.2% of national spending, using about $3.8T as the base (my assumption) |
| 3% to 7% of paid claims dollars "at risk" for errors | Healthcare Finance News blog and an Optum paper (snippet; the page returned 403) | n.d. | Commercial | Vendor framing | C, vendor |
| Commercial claims-processing error rate 19.3% (2011) | AMA *National Health Insurer Report Card* 2011, via Fierce Healthcare, https://www.fiercehealthcare.com/healthcare/new-ama-health-insurer-report-card-finds-increasing-inaccuracy-claims-payment | 2011 | Commercial | Payer processing errors, as seen by physicians (mostly underpayment and denial) | C. Wrong direction (payer errors against providers) |

**Shares by cause, for the funnel.** Using CERT 2025 for E/M:

- **Incorrect coding** is half of E/M improper dollars. Upcoding is about 4.5% of E/M dollars; downcoding is about 0.4% to 0.8% for office visits.
- **No documentation** (nonresponse) is 12.6% of E/M improper dollars; insufficient documentation is 31.1%.
- **Services not rendered** are not measured separately anywhere. Non-response is the nearest analog, and it is not evidence of fraud.
- **Other fraud, waste and abuse** is not split out by CERT.

**No commercial measured improper-payment rate was found.**

**Searched, nothing usable:**

- Milliman, Mathematica and the Commonwealth Fund: one combined search on commercial improper or overpayment rates returned nothing from them.
- Vendor sites (Cotiviti, Optum, ClarisHealth, Chartis) give savings claims, not error rates.
- The AMA report card measures payer errors, not provider overpayments.

## 2. What share of claims dollars is audited, by method

| Figure | Source and URL | Year | Setting | What it measures | Fit |
|---|---|---|---|---|---|
| Medicare contractors reviewed "less than 1 percent" of the more than 1 billion FFS claims (2.3M reviews) | GAO-13-522, https://gao.gov/products/gao-13-522 (figure from a search summary, **snippet**) | 2013 (data 2012) | Medicare FFS | Claims reviewed, all review types, **count** | B |
| MAC reviews 98% prepayment; RAC reviews 85% postpayment; SMRC 100% postpayment. RAC cost $158 per review, identifying $14 of improper payments per $1 paid; SMRC $256 and $7 | GAO-16-394, https://www.gao.gov/products/GAO-16-394 | 2016 (data 2013 to 2014) | Medicare | Review mix, cost and yield | B. The yield per dollar of review cost is about 7 to 14 |
| RAC records-request cap: 0.5% of a provider's paid claims in the prior 12 months (non-SNF, non-IRF); adjusted up or down by the provider's denial rate | CMS RAC slide via search; Fierce Healthcare, https://www.fiercehealthcare.com/healthcare/cms-lowers-rac-medical-record-request-limits (**snippet**) | about 2016 onward | Medicare | Cap on record requests, **count** | B. A ceiling on postpay record review per provider |
| RAC FY2021: $345.76M collected on 209,711 claims; $52.72M overturned at Level 1; $56.71M fees; $29.95M administration; $180.67M (52%) to the Trust Fund | CMS FY2021 RAC Report to Congress, Appendices (already in the addendum) | about 2023 | Medicare | Postpay output | B. Against about $440B of FFS payments (CERT 2025, a different year), collections are about **$0.08 per $100** |
| **Targeted against random hit rate:** high-coding physicians' stratum 56.4% of claims miscoded, 99.4% of those upcoded (about 56% of claims upcoded); all others 42.3% miscoded, 64.1% upcoded (about 27% upcoded) | OIG OEI-04-10-00181, Appendix E, Tables E-1 and E-3 (PDF read) | 2014 (data 2010) | Medicare | Hit rate by selection | **B, the only targeted-against-random contrast found.** Targeting on billing pattern roughly doubles the upcoding hit rate per claim |
| Random hit rate: 17.5% of established office-visit lines in error (any error) | CERT 2025, Table N1 | 2025 | Medicare | Random sample | B |
| Cigna R49: about **3% of eligible claims** affected (Cigna's own estimate in its first notice); later "more than 97% of providers" unaffected; bypass when appeals show correct billing at least 80% of the time | Texas Medical Association, https://www.texmed.org/Template.aspx?id=66748 | 2025 | **Commercial** | Share of level 4 and 5 claims an automatic rule adjusts, **count** | A for setting; it is an edit, not a record review |
| NY insurers' SIUs: savings $3.5B, recoveries $40.3M; 59 SIUs | NY DFS, *2025 Annual Health Insurance Fraud Report*, March 2026, https://www.dfs.ny.gov/system/files/documents/2026/03/2025-Annual-Health-Insurance-Fraud-Report_0.pdf (PDF read) | 2026 (data 2024) | **Commercial** (and Medicaid HMOs, dental, disability) | Prepay against postpay value | A to C. The ratio is the finding; the lines of business are mixed |
| Payment-integrity savings: Cotiviti "up to 3% or more" (1% to 3%); Optum top performers 8% to 10% "roughly double the average" (illustrative); ClarisHealth benchmark 5.6% of medical spend from more than 25 plans; Chartis client recovery 1.25% of spend | Cotiviti, https://www.cotiviti.com/solutions/payment-accuracy/billing-accuracy ; Optum white paper, https://www.optum.com/content/dam/o4-dam/resources/pdfs/white-papers/best-practices-in-payment-integrity.pdf (PDF read); ClarisHealth press release 22 Apr 2025, https://www.clarishealth.com/press-release/clarishealth-reveals-key-operational-performance-benchmarks-payment-integrity/ ; Chartis case study (snippet) | 2021 to 2025 | Commercial | All payment integrity, prepay and postpay combined | C, vendor marketing. Totals include coordination of benefits, subrogation and prepay edits |
| Prepay share of savings more than 60%; one plan 1.1% prepay and 0.2% postpay net savings rate (2020) | ClarisHealth white paper; Cotiviti case study (**both snippets**; the Cotiviti page did not show the figures) | 2020 to 2025 | Commercial | Split | C, unverified |

**Reading.** No commercial payer publishes the share of claims or dollars that goes through a postpay record review. Medicare's figures are claim counts (under 1% reviewed; a 0.5% per-provider cap). Funnel row 4 converts them to dollars as an assumption, $0.10 to $1.00 per $100. On targeting, one source shows that choosing providers by billing pattern doubles the upcoding hit rate (56% against 27% of claims); that supports this product's premise. "Large share screened, few reviewed" is true by construction: every claim passes prepay edits and data mining, while records are pulled for a fraction of 1%.

## 3. From identified overpayments to cash

From earlier research (sources in `docs/score_43_sources.md` and `docs/score_43_sources_addendum.md`):

- **Collected out of identified, net of appeals:**
  - Medicaid managed-care plans: 68% of non-fraud and 22% of fraud-and-abuse overpayments (OIG OEI-02-15-00260, 2018).
  - Medicare program-integrity contractor referrals: 20% overall and 20% for Part B (OIG OEI-03-13-00630, 2017).
  - Medicare benefit-integrity contractors: 24% (OIG OEI-03-13-00620).
  - Sustained OIG audit findings: 55% (OIG A-04-18-03085).
  - Fraud Prevention System: 16% expected (OIG A-01-15-00510).
  - Vermont Medicaid SIU: 91% where findings stood.
- **Appeals:** Medicare RAC FY2021 Level 1 overturned 15.2% of collected dollars. Part B Level 1 decisions were 41.7% fully favorable to the provider. Do not stack this cut on the collection rates above, which are already net of appeals.
- **Contingency fees:**
  - Commercial: 15% to 30% (BCBS North Dakota 30%; Everett WA 15% to 17%, snippet; Withum 20% to 30%; ClarisHealth executive 12% to 16%).
  - Medicare RAC: 9% to 12.5% at first and 16.4% effective in FY2021.
  - Medicaid RAC: 9.3% to 17%.
- **Staff and legal cost:**
  - In-house cost of recovery about 6% of recoveries (vendor assumption).
  - RAC fee plus CMS administration: 25% of gross collections.
  - Per SIU case about $3,459 (NHCAA 2013) to $4,251 (bottom-up).

New in this pass:

| Figure | Source and URL | Year | Setting | What it measures | Fit |
|---|---|---|---|---|---|
| NY SIU recoveries about 1.2% of reported SIU value ($40.3M / $3.5B) | NY DFS 2026 (above) | data 2024 | Commercial | Prevention against recovery | A for setting; "savings" is self-reported and undefined |
| Aetna: about 95% of SIU savings and recoveries were denied or reduced dollars | UN insurance page quoting Aetna, https://www.un.org/insurance/sites/www.un.org.insurance/files/aetna_fraud.pdf (snippet) | undated | Commercial | Prevention share | C |
| NHCAA ROI: 10.2 to 1 (recoveries plus savings over SIU budget); later surveys say prepayment tools make impact "hard to calculate" | NHCAA ROI white paper, https://www.nhcaa.org/wp-content/uploads/2021/02/roi_nhcaa_whitepaper.pdf (snippet) | 2013 survey | Commercial | Return on SIU spend | C |
| RAC yield $14 of improper payments identified per $1 of RAC cost | GAO-16-394 | 2016 | Medicare | Identified per cost dollar | B. Identified, not collected |
| HFPP: deterrence can far exceed recovery; no rate | HFPP 2024 (already in the addendum) | 2024 | Public-private | Sentinel effect | C. Unquantified |
| Cigna and Aetna automatic E/M review (from 1 Oct 2025); Maryland fine of $80,000 and order to stop, 13 Mar 2026 | Earnings note; Maryland order via a search summary (**snippet**; the page returned 403) | 2025 to 2026 | Commercial | Prevention by policy, and its legal risk | A for setting |

**Cost avoidance.** Every commercial source that splits prevention from recovery puts most value in prevention: NY's 87 to 1, Aetna's 95%, vendors' "over 60%". These are not comparable measures, and none publishes a method. For the funnel, prevention is outside the $100. A postpay E/M program creates prevention only through a sentinel effect on the providers it audits, which is unmeasured (open question 3 below).

**Share demanded.** No commercial source gives identified against demanded. Closest analogs:

- Medicare: OIG recommended $647M in 148 audits and CMS sustained $498M (77%) (A-04-18-03085, first-pass sources).
- In the Fraud Prevention System example, an extrapolated E/M estimate of $630K became about $4K once worked into overpayment determinations (A-01-15-00510, addendum).

Both suggest that a meaningful share of identified dollars, especially extrapolated E/M dollars, is never demanded.

**Summary of how identified dollars divide (central, ordinary demands):**

| Out of $1.00 identified | Central | Range |
|---|---|---|
| Lost to appeals, write-offs, exits and time (not collected) | $0.40 | $0.30 to $0.45 (ordinary); $0.76 to $0.84 (fraud-type) |
| Collected | $0.60 | $0.55 to $0.70 (ordinary); $0.16 to $0.24 (fraud-type) |
| Of collected: contingency fee or in-house cost | $0.12 | $0.03 to $0.21 (6% to 30% of collected) |
| Net to the party that bears the claims | $0.48 | $0.38 to $0.66 |

## 4. Who keeps recovered dollars

**The MLR regulation (45 CFR 158; read on Cornell LII):**

- §158.140(b)(1)(ii) **deducts** "Overpayment recoveries received from providers" from incurred claims.
- §158.140(b)(2)(iv) **includes** in incurred claims "The amount of claims payments recovered through fraud reduction efforts not to exceed the amount of fraud reduction expenses." In effect, fraud-related recoveries do not lower the MLR numerator up to the amount spent on fraud reduction. That is the only credit the commercial rule gives to fraud spending.
- §158.150(c)(8) excludes "Fraud prevention activities" from quality improvement; (c)(7) excludes "All retrospective and concurrent utilization review"; (c)(5) excludes claims adjudication systems.
- **So for a commercial fully insured plan, payment-integrity spending is administrative cost, not quality improvement.** The Medicaid managed-care MLR rule follows the commercial rule on this point, per New York and Wisconsin MLR instructions.
- **Medicare Advantage is different.** 42 CFR 422.2430(a)(4)(ii) counts "Fraud reduction activities, including fraud prevention, fraud detection, and fraud recovery" as quality-improving activity (CMS-4182-F, April 2018, from contract year 2019). §422.2420(b)(3)(i) still deducts overpayment recoveries from incurred claims.

| Funding arrangement | Who keeps a recovered dollar | Mechanism and source | Notes |
|---|---|---|---|
| **Self-funded employer plan (ASO)**, 67% of covered workers (KFF EHBS 2025, https://www.kff.org/health-costs/report/2025-employer-health-benefits-survey/) | **The plan** (the employer's plan assets), less the administrator's or vendor's fee | Sixth Circuit, *Tiara Yachts v. BCBSM* (2025): plausibly fiduciary; recovery "must flow to the Plan" (quote from a search summary of the Holland & Knight note, **snippet**; https://www.hklaw.com/en/insights/publications/2025/06/sixth-circuit-reverses-dismissal-of-erisa-healthcare-fee-suit-against). Fees: BCBS ND keeps 30%; BCBS Michigan up to 30% (litigation; Becker's, secondary) | No MLR. The administrator earns the fee, so it profits from recovery without bearing claims risk. State recoupment look-back limits do not apply (addendum). Cross-plan offsetting is contested (DOL amicus) |
| **Level-funded small employer** (37% of covered workers at firms with 10 to 199 workers; KFF 2025) | Mostly the employer's claims fund, to the stop-loss attachment point | KFF 2025 | Not found: how stop-loss contracts treat recoveries |
| **Fully insured, individual and small group (80% floor) and large group (85%)** | **The insurer**, if its three-year MLR stays above the floor; **enrollees**, through a larger rebate, if it is below | 45 CFR 158.140(b)(1)(ii); rebate under 45 CFR 158 subpart B. MLR headroom note: $37.1B of headroom across all insurers in 2024, $2.4B shortfall | Most large insurers sit above the floors (headroom note), so they keep it in-year. Premium setting passes recoveries into the next year's rates (not quantified) |
| **Medicare Advantage** | **The MA organization**, subject to the 85% MLR and remittance to CMS when below (42 CFR 422.2410, not opened) | 42 CFR 422.2420(b)(3)(i); fraud-reduction spending counts in the numerator under 422.2430(a)(4)(ii) | MA plans keep provider recoveries; CMS's own Part C recovery is risk adjustment (RADV), a different stream |
| **Medicaid managed care** | **Set by the state contract.** "Finders keepers" (the plan keeps what it finds; no federal share due), or the state takes the recovery and refunds the federal share at the FMAP under 42 CFR 433.312. Reported recoveries must be used in rate setting (438.608(d)(4)). California: plans keep recoveries under $25M (DHCS APL 23-011, **snippet**; not opened). Texas: the plan keeps one-half of certain recoveries | CMS, *Medicaid and CHIP Managed Care Program Integrity Toolkit: Treatment of Recoveries and Overpayments*, updated 17 Jan 2025, https://www.medicaid.gov/medicaid/program-integrity/download/managed-care-overpay-rec-toolkit.pdf (PDF read); DHCS APL 23-011; Tex. Gov't Code 544.0502 (not verified) | Keeping it is temporary: recoveries lower future capitation rates. Plans report all overpayments within 30 days (from July 2025) |
| **Medicaid fee-for-service** | The state, which refunds the federal share | 42 CFR 433.312 (toolkit) | |
| **Medicare FFS** | **The Trust Funds**, less contingency fees and administration: 52% of RAC FY2021 gross collections were returned | CMS FY2021 RAC Report to Congress, App. B | |

## 5. E/M specifically: share at risk from upcoding, and what downcoding policies recover

| Figure | Source and URL | Year | Setting | What it measures | Fit |
|---|---|---|---|---|---|
| Established office visits at level 4: 39.3% (Jan 2017), 47.0% (Dec 2020), **50.3% (Jun 2023)**; level 5: 3.7%, 4.1%, **6.1%**; level 3 fell from 48.3% to 39.7%. New patients at level 4: 30.9% to 45.1% | Epic Research, *More New and Existing Patient Visits Coded at Level-of-Service Four After Billing Code Changes Took Effect in 2021*, 24 Oct 2023, https://media.epic.com/epicresearch/wordpressmedia/pdfs/more-new-and-existing-patient-visits-coded-at-level-of-service-four-after-billing-code-changes-took-effect-in-2021.pdf (PDF read; 368M visits, 219 organizations) | 2023 | **All payers, including commercial** | Level mix | A to B. The mix shift is real across payers; it is not proof of upcoding (the 2021 rules lowered the bar) |
| Level 4 or 5 share of outpatient E/M visits: 25% (2006) to 38% (2022); "more research is needed" | Elevance Health Public Policy Institute, Aug 2023, https://www.elevancehealth.com/public-policy-institute/coding-for-high-complexity-office-visits-on-the-rise | 2023 | Mostly commercial (about 14.8M members per a search summary; not on the page) | Level mix | A for setting; no dollar figure on the page |
| Physician office 99214 share: 38.5% (2018) to 45.0% (2023); ED 99284 32.5% to 39.6% | Trilliant Health, 14 May 2025, https://www.trillianthealth.com/market-research/studies/changes-in-coding-intensity-suggest-upcoding | 2025 | All payers | Level mix | B |
| Hospital upcoding (5 states): $14.6B extra in 2019, **$5.8B commercial**, $4.6B Medicare, $1.8B Medicaid | Cited by Trilliant (above); underlying study not opened | 2011 to 2019 | Hospitals | Dollar estimate | C. Hospital, not E/M |
| BCBS Vermont: since 2019, coding intensity added 5% per visit (unit cost 52%) | Vermont legislature workgroup slides, 19 Mar 2025 (search summary; the link returned 404) | 2025 | Commercial, one insurer | Per-visit cost decomposition | A for setting, **unverified** |
| UnitedHealth: provider coding intensity in office visits and EDs is "contributing incremental trend" (not quantified) | Earnings note (Q2 2026 transcript) | 2026 | Commercial | Qualitative | A, unquantified |
| CERT 2025: upcoding is 3.1% of established and 5.1% of new office-visit dollars; 99215 one-level errors 8.7% of 99215 dollars | CERT 2025 (above) | 2025 | Medicare | Dollars at risk | B, the central value for the funnel |
| OIG: upcoding by 1,669 physicians who consistently billed the top two levels; 56% of their claims upcoded | OIG OEI-04-10-00181 | 2014 | Medicare | Concentration | B. Upcoding concentrates in a few providers, which favors targeting |
| Cigna R49: about 3% of eligible claims (a claim count), adjusted one level (99204, 99205, 99214, 99215, 99244, 99245) | TMA (above) | 2025 | Commercial | Share of claims adjusted | A. **Dollars recovered not published** |
| Critics' figure: Medicare FFS overcoding of 99214 and 99215 equal to 0.13% of paid claims (2024) | Search summary only (**snippet**) | 2024 | Medicare | Rebuttal of Cigna's 3% | unverified; source not identified |
| Aetna Claim and Code Review Program; Anthem paused | Earnings note | 2025 to 2026 | Commercial | Policy | A, no dollars |

**What automatic downcoding recovers: no source found.** Cigna, Aetna and Anthem publish no savings figures, and no regulator order reviewed gives dollars. An order-of-magnitude estimate, with every input stated:

- 3% of eligible level 4 and 5 claims, adjusted one level. Cigna's share is of eligible claims, a count; applying it to dollars is my assumption.
- A one-level difference worth about 25% to 30% of the billed level's price. Assumption from the fee schedule's relative values; not checked here.
- Level 4 and 5 visits making up about 60% to 70% of office-visit dollars. Assumption from the Epic mix weighted by price.

On $5.50 of office-visit dollars per $100, that gives about $5.50 x 0.65 x 3% x 27% ≈ **$0.03 per $100**, all of it prevented before payment (outside the funnel) and some of it reversed on appeal. **Assumption-built, not sourced.** It lands in the same few-cents range as the postpay estimate. Cigna's 80% bypass rule means the policy, too, targets providers by pattern.

**The share of E/M dollars at risk from upcoding:** central 4.5% (CERT 2025, all E/M), range 3.1% (established office visits) to about 10% (assumption toward OIG 2010). Per $100 of commercial claims, $0.22 to $1.10, central $0.41. **No commercial measurement of the upcoded share exists.** The level-mix series show a shift in commercial and all-payer data, which is consistent with upcoding but not proof.

## What is not known, and how it could be found

1. **A commercial improper-payment rate, for E/M or overall.** No payer publishes one. Routes:
   - NHCAA's members-only Anti-Fraud Management Survey.
   - A state all-payer claims database with a records sample (no such study found).
   - A buyer pilot: a random sample of 100 E/M claims from one plan.
2. **The share of commercial claims dollars put through postpay record review** (funnel row 4). Routes:
   - NY DFS Section 409 fraud prevention plan filings (cost and caseload, not published; a public-records request).
   - Payment-integrity RFPs from state employee plans, which sometimes state audit volumes.
   - Interviews with SIU and payment-integrity leads.
3. **The share of upcoded dollars a postpay program reaches** (row 6, the largest lever): no source. The project's own simulation, which measures recovered over available dollars (`eval/metrics_d42.py`), is the only estimate available, and it is synthetic.
4. **The E/M share of commercial postpay findings and recoveries.** Vendors' case studies are mostly DRG, coordination of benefits and facility bills. Route: ask vendors (Cotiviti's "conversion rate" metric exists but is unpublished).
5. **Dollars recovered or avoided by Cigna R49 and Aetna's program.** Routes: Maryland Insurance Administration order (13 Mar 2026) and any market-conduct exam; California DMHC review of Anthem; physician-society appeal data.
6. **Commercial collection rate on ordinary E/M demands.** Still none; the 55% to 70% range is Medicare and Medicaid.
7. **How fully insured plans book E/M coding recoveries.** As "overpayment recoveries" (deducted from claims), or as fraud-reduction recoveries (added back up to fraud expense)? Route: NAIC Supplemental Health Care Exhibit instructions and one insurer's MLR filing.
8. **The commercial E/M share of claims dollars.** Inputs: HCCI 2017 (33.6% professional) and a PCC snippet (E/M over one-third of professional). Route: HCCI's latest Health Care Cost and Utilization Report appendix, or FAIR Health.
9. **Sentinel effect.** How much billing falls after an audit or a policy announcement. Route: before-and-after level mix for providers under Cigna R49, from all-payer claims (Epic Cosmos, Trilliant).
10. **Verify the snippet-only figures:**
    - GAO-13-522's "less than 1 percent"
    - the 0.5% records-request cap
    - Cotiviti's 1.1% prepay and 0.2% postpay
    - ClarisHealth's "over 60% prepay"
    - Everett's 15% and 17% fees
    - BCBSVT's 5% coding intensity
    - the 0.13% Medicare overcoding figure
    - the Maryland $80,000 fine
    - the NY DFS inconsistency ($3.5B and $40.3M against $3B and $30.6M, both labeled 2024)
    - Shrank's figures against the JAMA abstract
