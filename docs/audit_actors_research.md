# The commercial postpay audit: actors, stages, KPIs and timeline (research notes)

[Back to the README](../README.md) · Research notes (2026-10-27, sub-agent). Summary page: [the audit in context](audit_in_context.md).

**What this page is.** Research notes for a newcomer: who takes part in a commercial health plan's post-payment audit of office-visit (E/M) coding and of fraud, waste and abuse, what each party does and cares about, how each is measured, and how long each hand-off takes. Done 2026-10-27 by a research sub-agent (web search and primary documents; no code; no repository files changed). It builds on [score 4.3 sources](score_43_sources.md) and [its addendum](score_43_sources_addendum.md) and does not repeat their research; where a figure is already there, this page points to it.

**How to read the grades.** As in the addendum, every figure carries a fit grade for *our* setting (a commercial plan, post-payment, physician E/M claims):
- **A**: commercial plan or state commercial law, close to our setting.
- **B**: partial. Medicare or Medicaid analog, one plan's policy, or a related unit (for example hospital rather than physician).
- **C**: context only. Vendor marketing, trade press, forum posts, or a different unit (for example initial claim denials rather than audit findings).

"Snippet" means the figure was read in search-result text or a secondary summary, and the primary page was not opened. "Assumption" means no source was found and the number is ours.

**The stages (Simmy's frame).** 1) patient has symptoms and seeks care; 2) provider sees the patient; 3) provider submits the claim (837P); 4) payer adjudicates, applies prepay edits and pays with a remittance (835): the provider's happy path; 5) payer audits paid claims; 6) payer recovers incorrect payments: the payer's happy path; 7) collections, appeals and vendor fees. The project zooms into stages 5 to 7.

**The one complete commercial process found.** Blue Cross and Blue Shield of Vermont's *Provider Audit, Sampling, Extrapolation and Re-Audit Process* policy (CPP_19, effective 2025-03-01, https://www.bluecrossvt.org/documents/cpp19-provider-audit-sampling-extrapolation-and-re-audit-process-policy; read in full) is the only commercial document found that lays out stages 5 to 7 end to end with days. It is **one plan's policy** (grade B). Its steps are cross-checked below against Blue Cross and Blue Shield of Rhode Island's *Post Payment Audits* policy (2022, https://www.bcbsri.com/providers/sites/providers/files/policies/2022/08/Post%20Payment%20Audits.pdf; read in full) and California's claims-payment regulation, 28 CCR §1300.71 (https://www.law.cornell.edu/regulations/california/28-CCR-1300.71; read).

---

## A. The actors and what each does at each stage

### A.1 Who is involved, stage by stage

| Stage | Payer side | Provider side | Others |
|---|---|---|---|
| 1. Patient seeks care | Eligibility and benefits on file (834 enrollment from the employer or exchange); provider directory | Front desk checks eligibility (270/271) | Patient; employer plan sponsor (self-funded plans) |
| 2. Service rendered | None | Physician documents the visit in the EHR; the EHR's templates and defaults shape the note | EHR vendor |
| 3. Claim submitted | Clearinghouse acknowledgement (277CA) | Billing and coding staff choose the level, submit the 837P | Clearinghouse |
| 4. Adjudication and payment | Claims adjudication applies benefits, contract fee schedule and prepay edits (NCCI-style and vendor libraries); pays by EFT with an 835 | Billing staff post the 835, work denials | Edit-library vendors; state prompt-pay rules |
| 5. Postpay audit | Payment integrity or analytics team screens paid claims; SIU takes suspected fraud; coders and clinical reviewers read records; provider relations is informed | Practice administrator and compliance answer the records request; billing staff assemble charts | Post-pay data-mining and audit vendors; for self-funded plans, the employer's contract governs vendor fees |
| 6. Recovery | Finance and recovery unit send the overpayment notice, offset future payments | Practice repays, disputes, or negotiates a settlement | Recovery vendors |
| 7. Collections, appeals, fees | Legal and the medical director hear disputes; SIU refers fraud; finance books vendor fees | Practice appeals, may hire counsel | State insurance department (complaints, recoupment limits); law enforcement (fraud); employer (shared-savings fees) |

### A.2 Payer-side actors

- **Claims adjudication.** Applies eligibility, benefits, contract pricing and edits before payment. Commercial plans adopt Medicare's NCCI edit logic voluntarily; Medicaid programs were required to by the ACA (CMS NCCI FAQ library, https://www.cms.gov/ncci-medicare/medicare-ncci-faq-library; snippet). A Vermont plan's payment policy runs claim lines through ClaimsXten-Select, then Cotiviti edits, with NCCI applied quarterly (Vermont legislature testimony, 2024, https://legislature.Vermont.gov/Documents/2024/WorkGroups/Senate%20Health%20and%20Welfare/Bills/H.766/Witness%20Testimony/H.766~Julie%20Lin~Corporate%20Payment%20Policy%2032%20Claims%20Editing%20Edits%20~4-3-2024.pdf; snippet). Grade B.
- **Payment integrity (PI) or analytics team.** Selects providers for audit. Blue Cross VT: audits are "typically" based on utilization and billing patterns relative to peers, FWA hotline information, customer complaints and internal or external referrals; most are post-payment; the plan may also put a provider on prepayment review (CPP_19, §II). Grade B.
- **Special Investigations Unit (SIU).** Required by state law in several states. New York Insurance Law §409 requires insurers writing at least 3,000 accident and health policies (and HMOs with at least 60,000 enrollees) to file a Fraud Prevention Plan with a full-time SIU, separate from claims and underwriting, with objective staffing criteria and investigator qualifications set in Regulation 95 (NY DFS, *2025 Annual Health Insurance Fraud Report*, March 2026, pp. 5 to 6, https://www.dfs.ny.gov/system/files/documents/2026/03/2025-Annual-Health-Insurance-Fraud-Report_0.pdf; read). California requires most licensed insurers to maintain SIUs and file an annual SIU compliance report (Cal. Ins. Code §§1875.20 to 1875.24; 10 CCR §§2698.30 to 2698.43; CDI, https://www.insurance.ca.gov/0300-fraud/0100-fraud-division-overview/12-siu/Review-Program.cfm; snippet). Grade A.
- **Certified coders and clinical reviewers.** Blue Cross VT: records "will be reviewed by an individual with the requisite level of clinical and coding experience", a plan employee or an external resource (CPP_19, §II). Medicare requires each medical-review contractor reviewer to have a credentials file holding at least a copy of an active professional license (CMS Program Integrity Manual ch. 3, §3.3.1.1, Transmittal 11529, 2022, https://hhs.gov/guidance/sites/default/files/hhs-guidance-documents/R11529PI.pdf; snippet). A Medicaid managed-care plan's "Program Integrity Medical Coding Reviewer" postings require a CPC, RHIT or RHIA credential (CareSource job ads; snippet; grade C). Nurses review medical necessity; coders review level; medical directors sign off disputes (see below).
- **Medical director and legal.** Blue Cross VT: a provider's written dispute of audit findings goes to the plan's Legal Department and Medical Director, who answer within 30 days (CPP_19, §VI.b.i). Grade B.
- **Provider relations.** Owns the contract and the relationship; at Blue Cross VT audit findings are delivered at a required face-to-face meeting with the provider (CPP_19, §VI.b.i). No source describes provider relations' formal role in audit decisions; the addendum notes the risk of a provider-relations or medical-director override (Vermont Medicaid lost 44% of identified dollars to internal reversals; addendum row 5).
- **Finance and recovery.** Sends overpayment notices and runs offsets. UnitedHealthcare's Bulk Recovery Process lets any UHC-administered plan recover its overpayment from UHC's aggregated payments to the same provider, after an initial letter and usually a second letter (UHC, *Bulk Recovery Process* notice, 2023, https://www.uhc.com/content/dam/uhcdotcom/en/Legal/PDF/Bulk-Recovery-Process.pdf; snippet). Grade A for mechanism.

### A.3 Provider-side actors

- **Physician.** Documents the visit; the level must be supported by medical decision-making or time (project page [how it works](how-it-works.md); CPT E/M guidelines). The AAFP, objecting to Cigna's R49 policy, notes CPT requires the medical record to determine the level, not the diagnosis alone (AAFP FPM blog, 2025, https://www.aafp.org/pubs/fpm/blogs/gettingpaid/entry/cigna-downcoding-em.html; snippet).
- **Billing and coding staff.** Submit the 837P, post the 835, work denials, assemble records for requests.
- **Compliance.** HHS-OIG's *General Compliance Program Guidance* (November 2023, https://oig.hhs.gov/compliance/general-compliance-program-guidance/; secondary summaries read) keeps the seven-element structure, including auditing and monitoring, for all health care entities. Grade B (federal guidance, voluntary for commercial business).
- **Practice administrator.** Owns revenue-cycle metrics (A/R days, denials) and the response to audits. MGMA's 2025 poll: 30% of medical groups audit payer payments against contracted rates monthly, 18% quarterly, 30% annually (MGMA Stat, 193 responses, https://www.mgma.com/mgma-stat/regular-auditing-of-payer-payments-crucial-to-ensure-accurate-reimbursement; snippet). Grade A for setting (practices), C for relevance (audits of payers, not by payers).
- **EHR vendor.** Templates and copy-forward can inflate documentation. HHS-OIG found only 3 of 18 Medicare contractors used EHR audit-log data in reviews and many could not tell whether a provider used copy-paste (*CMS and Its Contractors Have Adopted Few Program Integrity Practices to Address Vulnerabilities in EHRs*, OEI-01-11-00571, January 2014; via secondary summaries, https://www.healthcareitnews.com/news/cms-called-out-ehr-fraud-failings; snippet). Grade B.

### A.4 Others

- **Patient.** Seeks care, receives an explanation of benefits, and can report services not received; Blue Cross VT lists customer complaints and its FWA hotline among audit triggers (CPP_19, §II). NY DFS received 2,651 accident and health fraud reports in 2025, mostly from licensees required to report, with consumers and anonymous tips among the rest (NY DFS 2025 report, p. 4). Grade A.
- **Employer plan sponsor (self-funded).** 67% of covered workers are in self-funded plans (27% at firms with 10 to 199 workers, 80% at larger firms) (KFF, *2025 Employer Health Benefits Survey*, October 2025, https://www.kff.org/health-costs/press-release/2025-employer-health-benefits-survey/; snippet). The insurer acts as third-party administrator; the employer pays claims and often pays a share of recoveries as a fee (section C). Grade A.
- **Vendors.** Post-pay data mining, coding audit, credit-balance and COB recovery. Blue Cross VT uses vendors for COB, duplicates, administrative billing errors, payment-policy compliance, facility and drug claims, and credit balances, while its own audit team runs coding audits (CPP_19, §I). BCBS North Dakota offers self-funded clients Cotiviti-run "data mining for coding irregularities" for a 30% retained share (addendum, fees table). Grade A/B.
- **Regulators.** State insurance departments and managed-care regulators enforce prompt pay, recoupment limits and SIU rules (Texas order against UnitedHealthcare for 1,196 recovery requests sent after the 180-day limit; first pass, section 6). California's DMHC engaged Cigna over its E/M downcoding policy (section C). CMS governs Medicare Advantage and, with states, Medicaid managed care; HHS-OIG audits and refers. Grade A for states.
- **Law enforcement.** State fraud bureaus (NY's Insurance Frauds Bureau opened 73 healthcare fraud cases and made 40 arrests in 2025; NY DFS 2025 report, p. 5), Medicaid Fraud Control Units, HHS-OIG, FBI and DOJ. The 2025 National Health Care Fraud Takedown charged 324 defendants with $14.6B of alleged intended loss (DOJ, June 30, 2025, https://www.justice.gov/opa/pr/national-health-care-fraud-takedown-results-324-defendants-charged-connection-over-146; snippet). Few plan referrals are taken up: 23% of Medicaid MCO referrals to MFCUs, 6% of Texas MCO referrals to the state OIG (first pass, section 1; addendum row 8). Grade B.
- **Healthcare Fraud Prevention Partnership (HFPP).** A public-private data-sharing partnership: 94 data-sharing partners and 89.6 billion claim records in the cross-payer data set; 22 analytic studies; partners reported more than $62M in hard and soft savings in 2023 to 2024 (CMS, *HFPP Biennial Report to Congress CY2023 to 2024*, https://www.cms.gov/files/document/cy23-24-biennial-hfpp-report-congress.pdf; snippet). Grade B.

---

## B. KPIs by actor, with published values

### B.1 SIU

| KPI | Value | Source | Setting | Fit |
|---|---|---|---|---|
| Budget, staff, cases closed | Average budget $2.66M; median 10.5 FTE; average 769 investigations closed a year; half closed within 60 days, nearly a third took more than 9 months | NHCAA Anti-Fraud Management Survey 2013 via FierceHealthcare (first pass, section 1) | 52 private insurers | A setting, weak provenance (trade summary, members-only survey) |
| Cost per closed case | About $3,459 (budget over cases, blended); bottom-up provider case $4,251 (assumption) | First pass, section 1 | | Assumption anchored to A |
| Return on investment | SIUs "recover and save" 10.2 times their budget; savings plus recoveries, so not cash | NHCAA 2013 via Fierce; NHCAA ROI white paper, https://www.nhcaa.org/wp-content/uploads/2021/02/roi_nhcaa_whitepaper.pdf | Private insurers | A setting, but mixes prevention and recovery |
| Savings and recoveries | NY insurer SIUs: about $3.5B savings and $40.3M recoveries for 2024. **The same report gives $3B and $30.6M on p. 5 for "2024"; the second pair matches the prior year's figures (addendum row 7), so the p. 5 text is probably stale** | NY DFS 2025 report, pp. 1 and 5 to 6 (read) | Commercial, 59 SIUs | A. Recoveries are about 1% of savings: commercial SIU value is mostly prevention |
| Collection rate on fraud findings | 22% of fraud and abuse overpayments identified; 68% of non-fraud overpayments | HHS-OIG OEI-02-15-00260 (addendum row 3) | Medicaid MCO SIUs (commercial insurers) | A- |
| Staffing ratio | 1 SIU investigator per 60,000 enrollees (contract minimum) | NJ Comptroller 2013 (first pass, section 1) | NJ Medicaid HMO | B |
| Referral take-up by law enforcement | 23% (MFCU), 6% (Texas OIG) | First pass, section 1; addendum row 8 | Medicaid managed care | B |

Not used: the Coalition Against Insurance Fraud's investigator caseloads (field 10.7, desk 17 open referrals, 2020 study) are **property and casualty** SIUs and do not transfer to health.

### B.2 Coders and clinical reviewers

| KPI | Value | Source | Setting | Fit |
|---|---|---|---|---|
| Cost per claim review | Recovery Auditors $158 per review (contingency fee), SMRC $256; MAC cost not measurable | GAO-16-394, 2016 (data 2013 to 2014), https://www.gao.gov/products/GAO-16-394 (score 4.0 sources; summary page snippet) | Medicare, inpatient-heavy | B |
| Yield per review dollar | Recovery Auditors identified $14 of improper payments per $1 paid; SMRC $7 | GAO-16-394 | Medicare | B |
| Throughput | E/M professional-fee coding 10 to 15 charts an hour; ED coding minimum 10 an hour | AAPC forum posts and job postings (snippet) | Mixed | **C. No AAPC or AHIMA published standard found** |
| Accuracy standard | 95% or better on audit; 94% or less "below standard" | AAPC-hosted job posting (snippet) | Employer standard | C |
| Overturn of reviewer findings | Medicare RAC FY2021 Level 1, Part B: 41.7% fully and 7.6% partly favorable to the provider; Level 2 41.2% favorable; ALJ 56% (FY2010) | First pass, section 3 | Medicare | B |
| How often E/M is miscoded (what reviewers find) | 2010 Medicare E/M: 42.4% incorrectly coded (40.4% miscoded by level: 26.0% upcoded, 14.5% downcoded, as published; plus 2.0% other coding errors such as wrong code or unbundling); 19.0% lacking documentation (12.0% insufficient, 7.0% undocumented); 55% either; $6.7B improper (21% of E/M payments); 79% of miscoded claims off by one level, 17% upcoded by two; stratified random sample of 673 claims, 98.6% response | HHS-OIG, *Improper Payments for E/M Services Cost Medicare Billions in 2010*, OEI-04-10-00181, May 2014, https://oig.hhs.gov/oei/reports/oei-04-10-00181.pdf (read) | Medicare Part B, physicians | B (best physician E/M baseline found) |
| Recent error rate | FY2024 Medicare FFS improper payment rate 7.66% ($31.7B); established office visits about 5.5%; all E/M 10.3% | CERT summaries (snippet; FCSO and coding newsletters) | Medicare | C until checked against the CMS supplemental tables |

### B.3 Payment integrity teams

| KPI | Value | Source | Fit |
|---|---|---|---|
| Recovery net of cost | Medicare RAC FY2021: of $345.8M collected, 15.2% overturned at Level 1, 16.4% contingency fees, 8.7% CMS administration; 52% reached the Trust Fund | First pass, section 3; addendum row 6 | B |
| Internal cost of recovery | About 6% of recoveries in-house against a 15% vendor fee (assumption in a vendor blog); 8 to 10 times ROI on in-house tools | ClarisHealth blog, 2018 (addendum fees table) | C |
| Hit rate of edits, false-positive rate | **No published value found.** Vendors report relative gains only ("200% increase in clinical hit rate", Sagility; "improved savings rate of 120%", EXL; snippet) | Vendor pages | C |
| Conversion rate | Share of identified overpayments recovered within 3 or 12 months: defined by Cotiviti, no value published | Addendum, time table | C |
| Collection on ordinary findings | 68% (Medicaid MCOs, non-fraud); about 91% where findings stood (Vermont Medicaid SIU) | Addendum rows 3 and 5 | A-/B |

### B.4 Vendors

| KPI | Value | Source | Fit |
|---|---|---|---|
| Contingency fee | Commercial 15% to 30% (15% to 17% on recoveries in one Cotiviti contract snippet; 30% retained by BCBSND and BCBSM on self-funded clients); Medicare RAC 9% to 12.5% (early), 16.4% effective FY2021; Medicaid RAC 9.3% to 17% | Addendum, fees table | A/B |
| Dollars identified per dollar of fee | Recovery Auditors $14 identified per $1 paid | GAO-16-394 | B |
| Appeals reversal | Performant books revenue net of expected overturns; appeals found for providers $1.05M (2023) against $106.4M revenue, mostly COB | Addendum, fees table | C |
| Independent ratings | KLAS: Cotiviti and Optum offer the broadest payment-accuracy solutions; outcomes and value vary, particularly with Optum; payers shifting to prepay (KLAS 2023, https://klasresearch.com/report/payment-accuracy-and-integrity-solutions-2023-financial-outcomes-top-of-mind/3120; snippet) | KLAS | C |

### B.5 Providers

Initial claim denials (stage 4) are a different unit from post-payment audit findings (stage 5); the figures below are flagged where they are denials.

| KPI | Value | Source | Fit |
|---|---|---|---|
| Initial denial rate (stage 4) | Private payers about 15% of claims initially denied; Medicare Advantage 15.7% | Premier, *Trend Alert*, March 2024 (hospital survey, 516 hospitals, 2022 claims), https://premierinc.com/newsroom/blog/trend-alert-private-payers-retain-profits-by-refusing-or-delaying-legitimate-medical-claims | C (denials, hospitals) |
| Denial overturn (stage 4) | 54.3% of private-payer denials eventually overturned | Premier 2024 | C |
| Cost to contest a claim | $43.84 average; $63.76 commercial; $47.77 MA; $19.7B a year; a later Premier survey: $25.7B | Premier 2024 and later (snippet for the later figure) | C (denials) |
| Marketplace denials and appeals (stage 4, members) | 20% of in-network claims denied in 2023; under 1% appealed (376,508 internal appeals of 86M denials); 56% of appeals upheld | KFF, *Claims Denials and Appeals in ACA Marketplace Plans in 2023*, https://www.kff.org/private-insurance/claims-denials-and-appeals-in-aca-marketplace-plans-in-2023/ (read) | C (member appeals of denials) |
| Days in accounts receivable | Median about 35 to 40 days for primary care and multispecialty groups; top quartile under 30 | Vendor blogs citing MGMA (snippet); MGMA DataDive is subscription | C |
| Administrative cost of audits | Hospitals, 2013: 49% spent more than $25,000 and 12% more than $100,000 managing RAC audits; 17% hired consultants (average $91,636) | AHA RACTrac via Becker's and Healthcare Finance News (snippet) | C (hospitals, Medicare, old). **No physician-practice figure found** |
| AMA figures | **No AMA figure on the cost of payer audits found.** The AMA urged Cigna to rescind R49 (CMA and AAFP coverage, 2025; snippet) | | |
| Burden ranking | Downcoding is the issue MGMA members raise most and the largest increase over the past year; MGMA's 2026 regulatory burden report: 90% of practices saw a shift to MA, 79% of those said negative | Medical Economics, 2026-09-28, https://www.medicaleconomics.com/view/mgma-shops-draft-bill-to-curb-automatic-downcoding-in-medicare-advantage (read) | B (qualitative) |

### B.6 Payers (enterprise)

| KPI | Value | Source | Fit |
|---|---|---|---|
| MLR floors | 80% individual and small group, 85% large group, three-year average | KFF, *Medical Loss Ratio Rebates* (snippet); 45 CFR 158 | A |
| Rebates paid | $958M (2024), $1.6B (2025), $759M estimated (2026); 2025 simple loss ratios 93% individual, 87% small group, 91% large group. KFF's preliminary 2024 split by market is reported two ways in secondary sources; not resolved | KFF (snippet), https://www.kff.org/private-insurance/medical-loss-ratio-rebates/ | A |
| Headroom | All insurers: $37.1B above the floors in 2024 (about 7% of premium); one MLR point on the ten largest groups' fully insured commercial premium is about $2.8B | Repo: [market_tam_mlr_headroom.md](market_tam_mlr_headroom.md) | A |
| Administrative expense ratio | 11.5% (2023), aggregate loss ratio 86.7%; **all comprehensive hospital and medical business, not commercial only** | NAIC, *2023 Health Industry Snapshot*, https://content.naic.org/sites/default/files/topics-industry-snapshot-analysis-reports-2023-annual-report-health.pdf (snippet) | B |
| Provider satisfaction | **No published commercial payer score found** | | |

---

## C. Incentives and sensitivities

**Vendor contingency fees.** Vendors are paid a share of what they find or recover: commercial 15% to 30%, government 8% to 17% (addendum). Medicare RAC fees are refunded if a finding is overturned (addendum, fees table). The incentive is to find more, and the check on it is the appeal and refund. For self-funded clients the fee comes out of the employer's recovery: BCBS Michigan's Shared Savings Program enrolled all self-funded clients from January 2018 and kept 30% of overpayments recovered or prevented through third-party services; the Sixth Circuit revived the employer's ERISA claim in May 2025 (*Tiara Yachts v. BCBSM*, https://www.opn.ca6.uscourts.gov/opinions.pdf/25a0135p-06.pdf; secondary summaries read). Grade A.

**Employer fiduciary duty (self-funded plans).** An administrator that holds plan assets can be an ERISA fiduciary: in *Hi-Lex Controls v. BCBSM* the Sixth Circuit affirmed fiduciary status and a judgment of over $5.1M for undisclosed fees (2014; Haynes Boone summary, https://www.haynesboone.com/news/blogs/court-orders-third-party-administrator-to-pay-over--5-1-million-for-breach-of-fiduciary-duty). Cross-plan offsetting (recovering one plan's overpayment from payments owed under another employer's plan) was rejected as an unreasonable reading of the plan documents in *Peterson v. UnitedHealth Group*, 913 F.3d 769 (8th Cir. 2019); the court did not decide whether it violates ERISA, and the Department of Labor argued that it does (secondary summaries, e.g. https://www.proskauer.com/blog/eighth-circuit-decision-oncross-plan-offsetting-illustrates-importance-of-careful-plan-drafting). This bears directly on stage 6: UHC's Bulk Recovery Process offsets across UHC-administered plans (A.2). Recovery belongs to the plan, not the sponsor (*Tiara Yachts* district court, per summaries). Grade A.

**Medical loss ratio.** 45 CFR 158.140 (eCFR text, https://www.ecfr.gov/current/title-45/part-158/section-158.140; read through a page summary) treats two kinds of recovery differently:
- **Overpayment recoveries received from providers are deducted from incurred claims** (§158.140(b)(1)(ii)). An ordinary E/M coding recovery most likely falls here, so every recovered dollar lowers the plan's MLR numerator.
- **Claims payments recovered through fraud-reduction efforts are added back to incurred claims, but not beyond the amount of fraud-reduction expenses** (§158.140(b)(2)(iv)). Fraud work is therefore roughly MLR-neutral up to its cost, and only recoveries above that cost lower the MLR.
- What follows (inference): a plan above the floor keeps a lower MLR as margin; a plan at or below the floor owes part of any MLR reduction back to members as rebates (three-year average), so recoveries are worth less to it. Classification matters: CMS MLR examinations have flagged plans for reporting other recoveries (for example subrogation) as fraud recoveries (CMS, *Unity Health Plans WI Final MLR Exam Report*, https://www.hhs.gov/guidance/sites/default/files/hhs-guidance-documents/CMS/Unity-Health-Plans-WI-Final-MLR-Exam-Report.pdf; snippet).
- For the two-thirds of workers in self-funded plans there is no MLR (KFF EHBS 2025); the recovery belongs to the plan, less any fee. Grade A.

**Provider abrasion.** Audits cost providers time and money and can push providers out of network. Premier's $43.84 per contested claim is the abrasion unit score 4.0 uses (denials, not audits). Recent automated downcoding programs drew organized pushback:
- **Cigna R49** (*Evaluation and Management Coding Accuracy*): would reduce the level of 99204-99205, 99214-99215 and 99244-99245 claims when claim data did not support the level, from October 1, 2025. The California Medical Association called it unlawful; Cigna agreed to pause it pending California DMHC review (CMA, October 1, 2025, https://www.cmadocs.org/newsroom/news/view/ArticleId/50993/Cigna-agrees-to-pause-controversial-downcoding-policy; read). Cigna's statements that about 99% of in-network clinicians would be unaffected and that a provider could request exemption after five downcoded claims come from secondary summaries (snippet). **Status as of October 2025; a 2026 search found no confirmed rescission or implementation.**
- **Aetna Claim and Code Review**: reviews level 4 and 5 E/M claims since July 2024, expanded from 12 pilot states to all commercial states but Louisiana; Aetna says most claims stay at the billed level (AAO-HNS letter, September 2025, https://www.entnet.org/wp-content/uploads/2025/09/AAO-HNS_Aetna_Comment_Letter_Downcoding_9.2025.pdf; scope from secondary summaries, snippet).
- **Physician societies**: a coalition letter to CCIIO on insurer E/M downcoding (September 12, 2025, https://www.aans.org/files/final-physician-orgs-sign-on-to-cciio-insurer-em-downcoding-9-12-25; snippet); MGMA's draft bill to bar automatic downcoding by MA plans, with a fallback allowing it only after a plan shows a physician upcodes above a set rate and limiting it to 90 days (Medical Economics, 2026-09-28; read). Practice leaders at MGMA's 2026 conference asked that insurers pay for audit time when claims prove correct (Medical Economics, 2026-09-30, https://www.medicaleconomics.com/view/practice-leaders-want-insurers-to-pay-when-downcoding-audits-come-up-empty; read).
- Reading for the project: claim-only rules that downcode without records are the target of regulators and societies; a records-based postpay audit with a sample is the alternative that the critics' own argument (the record determines the level) supports. That is an inference, not a source.

**Network adequacy.** A plan that terminates or alienates providers must still meet network standards. The NAIC Network Access and Adequacy Model Act (#74, revised 2015) sets sufficiency and directory standards; few states adopted it whole (NAIC brief, https://content.naic.org/sites/default/files/government-affairs-brief-network-adequacy-model-act.pdf; snippet). Marketplace plans must meet quantitative time-and-distance or ratio standards; state rules vary (Georgetown CHIR, https://chir.georgetown.edu/the-next-big-thing-in-network-adequacy-the-naic-model-act/; snippet). No source quantifies how audits affect network participation. Grade B.

**Prompt pay and timely filing (stage 4).** They set the provider's happy path and the payer's float. See D.1. Prompt-pay penalties push plans to pay first and audit later, which is why postpay exists at all (inference).

**State recoupment limits.** 180 days (Texas) to 24 months (New York), with fraud excepted and self-funded ERISA plans exempt; extrapolation allowed by contract when the sample is valid. See the first pass, section 6. Additions from this pass: Rhode Island requires a post-payment audit that recoups to be **completed** within 18 months of payment for physicians too (R.I. Gen. Laws §§27-19-56 and 27-20-51, quoted in the BCBSRI policy; read), unless a negotiated contract sets other terms; California requires the written reimbursement request within 365 days, and offset only of uncontested overpayments when the contract authorizes it (28 CCR §1300.71(b)(5) and (d)(5); read). Grade A.

**Regulator scrutiny of recoveries.** Texas DOI ordered UnitedHealthcare to return $938,703 for 1,196 recovery requests sent after 180 days (first pass, section 6). Medicare Advantage plans have a separate federal duty to report and return their own overpayments **from CMS** within 60 days (42 CFR 422.326, https://www.law.cornell.edu/cfr/text/42/422.326); that is regulator context, not a rule on recouping from providers.

---

## D. Timeline: each hand-off, with sources

### D.1 Hand-off table

| # | Hand-off | Typical time | Medicare rule | Commercial example | Source and fit |
|---|---|---|---|---|---|
| 1 | Symptom to visit | Not researched | | | Out of scope |
| 2 | Visit to claim submitted | 1 to 5 days typical (charge lag targets 1 to 2 days, submission 2 days) | Must file within 12 months of service (42 CFR 424.44) | Contracted providers commonly 90 days (UHC, Aetna), Cigna 90 to 180 (billing blogs, snippet); California: a plan may not set less than 90 days for contracted providers, 180 for non-contracted (28 CCR §1300.71(b)(1), read) | Lag: vendor blogs (C). Deadlines: A for California, C for payer specifics |
| 3 | Claim to payment (prompt pay) | About 2 to 6 weeks for a clean claim | Payment floor: electronic claims paid no earlier than day 14, paper day 29; 95% of clean claims within 30 days; interest from day 31 (Noridian and FCSO, https://med.noridianmedicare.com/web/jddme/claims-appeals/claim-submission/clean; snippet) | California 30 working days (45 for HMOs) (28 CCR §1300.71(g), read); New York 30 days electronic and 45 paper (EmblemHealth, https://www.emblemhealth.com/providers/claims-corner/policies-procedures/prompt-payment-guidelines; snippet); New Hampshire 15 days electronic, 30 paper (RSA 420-A:17-d, snippet); states range 15 to 60 days (Florida Senate analysis, 2002; old) | A (state rules), B (Medicare) |
| 4 | Payment to audit selection | **No source.** Bounded by the look-back: the audit must start soon enough to finish (or send the demand) inside the state window | RAC look-back 3 years from paid date (CMS RAC improvements, 2017; snippet); reopening 1 year any reason, 4 years good cause, no limit for fraud | TX 180 days (recovery sought); IL 12 months; FL 12 months for physicians; CA 365 days (request); RI 18 months (audit completed); NY 24 months; fraud excepted | A (statutes, first pass section 6 and above); gap for the lag itself |
| 5 | Records request to response | 30 days, extensions to about 45 | ADR: 45 calendar days; no response means denial (PIM ch. 3, §3.2.3.2; snippet) | Blue Cross VT 30 calendar days, extension to 45 at the plan's discretion; after 45 days the plan may deny, require prepayment review or suspend (CPP_19, §III, read). BCBSRI 30 calendar days, at no cost; failure means recovery of the full claim (read). Medica 30 days, second request plus 14 (snippet) | A/B |
| 6 | Review time (records in to findings) | **Assumption: 30 to 60 days** | RAC complex review 30 days (snippet); UPIC postpay review 60 days, clock stops while waiting for records (snippet) | Blue Cross VT sets no review deadline; findings are delivered at a face-to-face meeting, then in writing (CPP_19, §VI) | B (Medicare); commercial not found |
| 7 | Findings to dispute | 30 days to dispute, 30 days to answer | RAC discussion period: 30 days after the results letter; RAC waits 30 days before sending adjustments (snippet) | Blue Cross VT: dispute within 30 days to Legal and the Medical Director, written answer within 30 days (CPP_19, §VI.b.i). California: contest within 30 working days of the notice (§1300.71(d)(4)) | A/B |
| 8 | Demand (settlement offer) to response | 30 days; settlement up to 60 | Medicare demand: interest from day 31, offset from day 41 unless a timely appeal (first pass, section 2) | Blue Cross VT: 30 calendar days to accept or ask to meet; if no agreement within 60 days of the offer, the plan may recoup the full extrapolated amount, require paper claims with records, audit further or terminate; accepting waives appeal (CPP_19, §VI.b.ii). California: repay within 30 working days if not contested (§1300.71(d)(5)). Medica: offset 45 days after the refund letter (snippet) | A/B |
| 9 | Appeal levels and durations | Commercial: one or two internal levels, about 30 to 45 working days each | Five levels: redetermination (file 120 days, decide 60), QIC (file 180, decide 60), ALJ (file 60, decide 90, in practice about 725 days on average in 2022, secondary source), Council (60/90), federal court (60 days to file) (ASCO table; CGS, https://cgsmedicare.com/hhh/appeals/five_levels_of_appeals.html; snippet) | California provider disputes: at least 365 days to file, written decision within 45 working days; about 91% of disputes resolved in time in 2023 (28 CCR §1300.71.38; DMHC 2023 report; snippet). Blue Cross VT: the Legal and Medical Director review is the dispute step; termination has its own appeal | A (CA), B |
| 10 | Offset start | About 30 to 60 days after an uncontested demand | Day 41 | California: only after 30 working days, only if uncontested, only if the contract allows (read); Blue Cross VT: after the 30 to 60-day settlement window; UHC: after one or two letters, across UHC-administered plans (snippet) | A |
| 11 | Final collection | 2 to 3 months by offset from a provider still billing; 12 to 24 months or never when appealed, referred or the provider has left | Medicare referrals: 20% collected 12 to 24 months later (addendum) | Valenz: 71% within 90 days (vendor, n = 2; C) | Addendum, time table |

### D.2 End-to-end composition (assumption)

Built on Blue Cross VT's steps, with the review time assumed. Two clocks matter, because state limits are triggered by different events.

| Milestone, counted from the records request | Steps | Elapsed |
|---|---|---|
| **Written findings or overpayment notice** | records 30 to 45 days; review 30 to 60 (assumption); meeting and written findings 14 to 28 days (assumption) | **about 2.5 to 4.5 months** |
| **Recoupment, undisputed** | notice, then settlement accepted or repayment within 30 days | **about 3.5 to 5.5 months** |
| **Recoupment, disputed** | notice; dispute 30 days and the plan's answer 30; settlement window up to 60 | **about 5.5 to 8.5 months** |
| **Appealed further or referred** | internal or external appeal, litigation, or law enforcement | **1 to 2+ years**, collection often partial (addendum: 16% to 24% for fraud-type cases) |

From the date of payment, add the lag to audit selection (no source). Each state limit against its own trigger (statutes as in the first pass, section 6, and C above):

| State | Limit and trigger | What it allows for selection after payment (assumption, from the table above) |
|---|---|---|
| Texas | 180 days; the recovery request must be sent | Notice at 2.5 to 4.5 months after the request, so selection and request within about **1.5 to 3.5 months** of payment |
| California | 365 days; written reimbursement request | Selection within about 7.5 to 9.5 months |
| Florida (physicians) | 12 months; overpayment claim (notice) | Selection within about 7.5 to 9.5 months |
| Illinois | 12 months; the recoupment or offset itself | The full cycle counts: selection within about 3.5 to 8.5 months, depending on dispute |
| Rhode Island | 18 months; the audit must be completed | Comfortable |
| New York | 24 months; recovery must have begun | Comfortable |

Texas is the binding case: a plan there must screen and request within a quarter or so of payment. The project's data cover one calendar year and model no demand date (first pass, section 6), so these clocks are not yet in the score.

---

## E. Data sources and files at each stage

| Stage | File or source | One line | Source |
|---|---|---|---|
| 1 | **834** enrollment | Employer or exchange sends member enrollment to the plan | CMS, *Adopted Standards and Operating Rules*, https://www.cms.gov/about-cms/what-we-do/administrative-simplification/hipaa/adopted-standards-operating-rules (snippet) |
| 1 | **270/271** eligibility | Provider asks whether the member is covered; 271 answers | Same |
| 1 | **Provider directory** | Plans must verify directory data at least every 90 days and update within 2 business days of a provider's change (No Surprises Act §116); New York requires 15-day verification | KFF Health News article; NY DFS Circular Letter 12 (2021), https://www.dfs.ny.gov/industry_guidance/circular_letters/cl2021_12 (snippet) |
| 2 | **EHR record and audit trail** | The visit note and the log of who wrote or changed it, when; the audit trail is the evidence for late or copied entries | OIG OEI-01-11-00571 (snippet); Blue Cross VT: records are audited as they exist on the date of the request, later changes do not count (CPP_19, §IV) |
| 3 | **837P** professional claim | Billed CPT, diagnoses, dates, rendering and billing NPIs, amounts; 98% of medical claims submitted electronically | CAQH Index 2024 (read), https://www.caqh.org/hubfs/Index/2024%20Index%20Report/CAQH_IndexReport_2024_FINAL.pdf |
| 3 | **277CA** acknowledgement | Clearinghouse or payer accepts or rejects the claim on receipt | CAQH Index 2024 |
| 4 | **Fee schedule and contract terms** | Contract pricing, timely filing, records-access, audit, extrapolation and offset clauses; the Medicare physician fee schedule is a common reference for commercial rates (assumption, not checked) | BCBSRI and Blue Cross VT policies (read) |
| 4 | **NCCI edits and MUEs; vendor edit libraries** | Code-pair and units edits applied before payment; voluntary for commercial plans; ClaimsXten and Cotiviti libraries in use | CMS NCCI FAQ; Vermont testimony (snippets) |
| 4 | **835** remittance and **EFT** | Payment and adjustment reasons; 89% of medical remittances electronic | CAQH Index 2024 |
| 4 | **276/277** claim status | Provider asks where a claim stands | CMS adopted standards |
| 5 | **Paid-claims history** | The screen's input: every paid claim by provider; the payer holds this and nothing else about the visit | Project [operating model](operating_model.md) |
| 5 | **NPPES (NPI registry)** | Provider identity, taxonomy and address, to link billing and rendering providers | CMS NPI Registry, https://npiregistry.cms.hhs.gov (not opened) |
| 5 | **Exclusion lists: OIG LEIE, SAM.gov, state Medicaid lists** | Excluded individuals and entities, checked at credentialing and in investigations | https://oig.hhs.gov/exclusions/ and https://sam.gov (not opened) |
| 5 | **HFPP shared data and studies** | 89.6 billion claim records across payers; cross-payer studies flag outliers a single plan cannot see | CMS HFPP report 2023 to 2024 (snippet) |
| 5 | **Tips and referrals** | FWA hotline, member complaints, internal referrals; reports to state fraud bureaus | Blue Cross VT CPP_19; NY DFS 2025 report |
| 5 | **Records request and attachments (275 or fax, portal, mail)** | Only 32% of medical attachments move electronically (no federal standard), which helps explain 30 to 45-day response windows | CAQH Index 2024 (read) |
| 5 | **External benchmarks** | OIG E/M audits, CERT error rates, published code distributions | OEI-04-10-00181 (read); CERT (snippet) |
| 6 | **Overpayment notice and settlement offer** | Claim list, basis, error rate and extrapolated amount, netting underpayments | Blue Cross VT CPP_19 §VI (read); 28 CCR §1300.71(d)(3) |
| 6 | **Offset on the 835** | Recoupment shows as a negative adjustment on later remittances | UHC Bulk Recovery (snippet) |
| 7 | **Appeal and dispute files; settlement agreements** | Provider's written dispute, the plan's decision, any waiver of appeal | Blue Cross VT; 28 CCR §1300.71.38 |
| 7 | **SIU annual reports and fraud referrals** | NY and California SIU filings to the state; referrals to the state fraud bureau or MFCU | NY DFS; CDI |
| 7 | **Vendor invoices and shared-savings statements** | Contingency fees billed against recoveries; for ASO clients, the fee share deducted from the employer's recovery | Addendum fees table; *Tiara Yachts* |

---

## What the sources do not say

1. **Physician-practice cost of a payer audit** (staff hours, consultant fees, per records request). The only cost survey found is AHA's RACTrac (hospitals, Medicare, 2013). Premier's figures are per contested *denial*, not per audit.
2. **Commercial post-payment audit overturn and appeal rates.** Only Medicare RAC appeal data exist; commercial disputes are internal and contract-based and unpublished.
3. **Vendor hit rates and edit false-positive rates.** Vendors publish relative improvements and case studies, not rates with a denominator.
4. **Coder and clinical-reviewer productivity standards.** No AAPC, AHIMA or payer standard was found; the 10 to 15 E/M charts an hour figure is from forum posts and job ads.
5. **Provider satisfaction with payers** as a published, comparable score.
6. **SIU staffing ratios** for commercial plans. NJ's 1 investigator per 60,000 enrollees is a Medicaid contract term; NY requires "objective criteria" but publishes no ratio; NHCAA's later surveys are members-only.
7. **The lag from payment to audit selection**, and how long a commercial review takes once records arrive.
8. **What share of audited providers leave the network**, or are terminated, after a finding (addendum open question 3).
9. **Cigna R49's status after October 2025**, and the full text of Aetna's Claim and Code Review policy; both were read through society letters and secondary summaries.
10. **Commercial prompt-pay and timely-filing terms by payer.** Statutes were read for California; New York, Texas and the payer-specific timely-filing limits come from secondary pages.
11. **Days in A/R and charge lag** from MGMA or HFMA directly; the figures here are vendor blogs citing them.
12. **Unopened primary pages** used through snippets: Medica's payment integrity manual (bot check, not bypassed), UHC Bulk Recovery, the CMS PIM chapter 3 text, CERT supplemental tables, KFF's 2024 MLR split, the HFPP report, KLAS, and the NSA directory rule text.
