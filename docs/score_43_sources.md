# Score 4.3 sources: what the literature supports for each parameter

[Back to the README](../README.md) · [score 4.2](score_42.md) · [the proposal](score_43_proposal.md) · issue 200

**What this page is.** The research behind the parameters proposed for score 4.3: for each one, the figures found, where they come from, how far they support our use, and what was not found. Done 2026-10-25 by a research sub-agent (web search and page reads, no code); URLs and years are given so each claim can be traced. Most hard numbers are Medicare or Medicaid; commercial evidence is mostly contract language and state statutes.

Research for issue #200, done 2026-10-25. Read-only: no repo files were changed. Wage rates below use score 4.0's rule (BLS median x 1.4 / 2,080 hours): investigator $52.50/h ($78,000), nurse $65.66/h ($97,550), coder $34.42/h ($51,140), and attorney **$107.47/h**. The attorney rate is new and comes from the BLS lawyer median of $159,670 for May 2025 (https://www.bls.gov/ooh/legal/lawyers.htm). Every derived number below shows its arithmetic.

## Summary

There is little published commercial-payer data on any of the six parameters. Almost every hard number is Medicare or Medicaid. The commercial evidence is contract and policy language (two Blue plans, one Medicaid managed-care manual) and state prompt-pay statutes.

**1. Fraud referral cost.** The figure closest to a payer's own SIU is a secondary report of the 2013 NHCAA survey: an average SIU budget of $2.66M against an average of 769 closed investigations, about $3,459 each. That is a blended average; half of the cases closed within 60 days. Medicare's benefit-integrity contractors cost $14.2K to $23.7K per investigation started, but those are government costs, fully loaded with overhead.

- Recommended total cost per referral: **$4,000**, which is about **$3,700 more than a $276 demand**. This is an assumption, cross-checked bottom-up.
- Recommended range: $2,000 to $15,000.

**2. Collection.**

- Medicare benefit-integrity overpayments: MACs recovered about 24% of the amount referred. This is the closest anchor for referrals.
- Overpayments found in OIG audits: CMS reported collecting 55% of the sustained amount, with documentation for 24%. These are mostly institutional providers.
- No commercial figure was found. For in-network demands, which the plan can recoup by offsetting future claims, the recommended default is 85% (assumption). For referrals, 25% (sourced in kind).

**3. Appeals.** In the Medicare RAC data for FY2021, the dollars overturned at Level 1 alone were **15.2%** of the dollars collected. Part B Level 1 decisions were 41.7% fully and 7.6% partly favorable to the provider. The appeal rate falls between 6.7% and 30.7% depending on the year and the denominator. No commercial post-payment-audit appeal data was found.

**4. Records copy fee.** The $0 default is **partly sourced**. A Blue plan's audit policy requires copies "at no cost" (hospitals), and a Medi-Cal managed-care manual puts the copy cost on the provider. HIPAA's fee limits cover only a patient's own request. Medicare RACs pay practitioners $0.15 a page, up to $15 per record. Keep $90 as the sensitivity.

**5. Extrapolation error gate.** No payer or contractor publishes a numeric threshold based on the share of claims overpaid. Medicare requires a "sustained or high level of payment error" but sets no number. Recent practice (a 2023 OIG integrity agreement with a physician, amended in 2025, and Blue Cross VT's policy) extrapolates every sample. Older OIG Corporate Integrity Agreements used a **5% net dollar error rate** to trigger a full statistical sample. The recommendation is to switch the unit to a net dollar error rate, default 5% (assumption anchored to CIAs), with sensitivity at 0% (no gate) and at today's 15% claim share.

**6. Look-back and extrapolation rights.** State limits on recoupment run from 180 days (Texas) and 12 months (Illinois; Florida for physicians) to 365 days (California), 18 months (BCBSRI hospital contracts) and 24 months (New York). Fraud is excepted almost everywhere, and self-funded ERISA plans are exempt. Extrapolation is allowed by contract, and in New York by regulator opinion, when the sample is statistically valid. Texas bills to ban it (2017 and 2023) died in Senate committee.

---

## 1. Fraud referral cost (payer cost per provider case beyond a demand)

| Figure | Source and URL | Year | Setting | What it measures | How far it supports our use |
|---|---|---|---|---|---|
| Average SIU operating budget >$2.66M; median SIU 10.5 FTE; average 769 fraud investigations closed per year; half closed within 60 days, nearly a third took more than 9 months; 52 private insurers responded | NHCAA Anti-Fraud Management Survey 2013, as reported by FierceHealthcare, https://www.fiercehealthcare.com/antifraud/nhcaa-survey-results-provide-a-benchmark-for-sius. **Secondary trade report. The page returned 403, so the figures come from search-result text; the NHCAA survey itself is members-only** | data 2013 | Commercial SIUs (right setting) | Whole-unit budget and caseload | Best setting match, weakest provenance. $2.66M / 769 = **$3,459 per closed investigation**. This divides an average budget by an average caseload, and the caseload includes quick closes and member cases, so it is not the cost of one provider referral. It suggests a provider case costs more than $3.5K. 10.5 FTE / 769 is about 73 cases per FTE a year, roughly 28 staff hours per closed case (blended) |
| Medicare benefit-integrity contractors (PSCs, ZPICs, MEDIC): paid $116.4M (2012) and $124.4M (2013); 8,197 and 5,243 investigations started; 768 and 639 case referrals to law enforcement | HHS-OIG, *Medicare Benefit Integrity Contractors' Activities in 2012 and 2013: A Data Compendium*, OEI-03-13-00620, Figures 3, 4 and 17, https://www.oversight.gov/sites/default/files/oig-reports/oei-03-13-00620.pdf | 2016 (data 2012 to 2013) | Medicare FFS fraud contractors (closest analog to an SIU working for a payer) | Contract cost against output | **$14,195 (2012) and $23,730 (2013) per investigation started; $151.5K and $194.7K per law-enforcement referral.** These costs are fully loaded (data analysis, law-enforcement support, overhead) and paid by the government. Treat them as an upper bound for a single payer case, not the marginal cost |
| MFCUs: $395.8M spent (state plus federal), 16,688 open investigations at year end (13,528 fraud), 2,183 staff | HHS-OIG, *MFCU Annual Report FY2024*, OEI-09-25-00090, and its FY2024 Statistical Chart, https://oig.hhs.gov/reports/all/2025/medicaid-fraud-control-units-annual-report-fiscal-year-2024 | 2025 | State law enforcement (Medicaid) | Prosecution-side cost | $23,719 per open investigation ($29,260 per fraud investigation). **Paid by the government, not the plan.** Context only: what a case costs once a plan has referred it |
| MCO referrals to MFCUs: 4,650 received, 1,078 opened (23%) | Same report, p. 8 | 2025 | Medicaid managed care | Share of plan referrals law enforcement takes up | Most referrals are not taken up, so the plan carries the case (and any recovery) itself. Supports pricing the referral as the plan's own investigation |
| Staffing minimum: 1 SIU investigator per 60,000 enrollees | NJ Office of the State Comptroller, *Compliance Audit of UnitedHealthcare Community Plan of NJ's SIU*, July 2013, https://www.nj.gov/comptroller/news/docs/report_mfd_hmo.pdf | 2013 | NJ Medicaid HMO contract (similar to NJ's rule for commercial plans) | Required staffing | Context for SIU capacity, not cost per case |
| Attorney $107.47/h; investigator $52.50/h; nurse $65.66/h | BLS OOH, lawyers, May 2025 median $159,670, https://www.bls.gov/ooh/legal/lawyers.htm; other wages as in score 4.0 | 2025 | National wages | Loaded hourly cost (x1.4) | Inputs for the bottom-up check |
| Hours per case (investigator, legal, clinical review) | **No source found** | | | | Assumption below |

**Bottom-up cross-check (assumption).** These hours are assumptions; the rates are sourced.

- Typical provider case: investigator 40 h ($2,100), nurse or medical-director review 8 h ($525), certified coder re-review 16 h ($551), attorney 10 h ($1,075). Total **$4,251**.
- Low case: investigator 20 h, nurse 4 h, attorney 4 h. Total $1,743.
- High case: investigator 120 h, attorney 40 h, nurse and coder 30 h. Total about $12,600.
- The typical case lands just above the NHCAA blended $3,459 and well below the contractor's fully loaded $14K to $24K.

**Recommended default (assumption, anchored to NHCAA 2013 and the bottom-up check):** **$4,000 total per referral**, which replaces score 4.0's $275.66 demand cost for a referred provider. That is about **$3,700 above a demand**.

- Range: **$2,000 to $15,000**. The low end is near NHCAA's blended figure; the high end sits below the federal contractor cost per investigation.
- Keep issue #200's sensitivity points ($0, $2,000, $5,000) and add $15,000.
- Do not use the MFCU figure, which is government spending.

## 2. Collection rate on identified or demanded overpayments

| Figure | Source and URL | Year | Setting | What it measures | How far it supports our use |
|---|---|---|---|---|---|
| Overpayments referred by benefit-integrity contractors: $375.4M (2012) and $405.3M (2013). Recovered by MACs: $90.1M and $96.7M (**24.0% and 23.9%**) | HHS-OIG OEI-03-13-00620, Figure 25 and Appendix B (URL above) | 2016 (data 2012 to 2013) | Medicare fraud and abuse cases | Same-year recovered against referred; OIG notes recovered is not a subset of referred | **Closest anchor for the referral lane**: fraud cases, provider-level. Not a cohort measure |
| $647M recommended in 148 OIG audits; $498M sustained by CMS (77%); CMS reported collecting $272M (**55% of sustained**), with documentation for only $120M (**24%**). Uncollected amounts include those in appeal and those barred by the 4-year reopening period | HHS-OIG, *CMS Reported Collecting Just Over Half of the $498 Million in Medicare Overpayments Identified by OIG Audits*, A-04-18-03085, https://www.oversight.gov/sites/default/files/documents/reports/2022-11/41803085.pdf | 2022 (audits 2014 to 2016, status June 2020) | Medicare, mostly institutional and cost-report audits | Collected against sustained | Poor analog for a physician E/M demand (institutions, cost reports, statutes of limitation). The 55% already nets out appeals and the time bar, so do not stack it on an appeal parameter |
| Earlier audit: $416M sustained, $84M reported collected (about 20%) | HHS-OIG, *Obstacles to Collection of Millions in Medicare Overpayments*, A-04-10-03059, https://oig.hhs.gov/reports/all/2012/obstacles-to-collection-of-millions-in-medicare-overpayments/ | 2012 | Same | Same | Same caveats |
| MFCU "recoveries ... may not reflect actual collections" | MFCU FY2024 Statistical Chart, footnote 2 (URL in item 1) | 2025 | Medicaid fraud | Definition | Criminal and civil recovery figures overstate cash; supports a low collection rate for referrals |
| Recoupment by offset starts on day 41 after the demand letter; interest from day 31; a Level 1 or Level 2 appeal filed in time stops recoupment (SSA 1893(f)(2)) | CMS MLN overpayment brochure, https://www.cms.gov/Outreach-and-Education/Medicare-Learning-Network-MLN/MLNProducts/downloads/overpaymentbrochure508-09.pdf; CMS Financial Management Manual ch. 4, https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/downloads/fin106c04.pdf | current | Medicare | Time to collect | Typical time to collect an unappealed Medicare demand: about 1.5 to 3 months by offset. Appealed demands wait for the Level 2 decision, and Level 3 backlogs ran to years (GAO-16-366, https://www.gao.gov/products/gao-16-366: Level 3 filings up 936% from FY2010 to FY2014) |
| Blue Cross VT: on failed settlement, the plan "recoup[s] overpayments from provider for the full extrapolated amount" and may require prepayment review or terminate the provider | Blue Cross VT Payment Policy CPP_19, effective 2025-03-01, https://www.bluecrossvt.org/documents/cpp19-provider-audit-sampling-extrapolation-and-re-audit-process-policy | 2025 | Commercial | Collection mechanism | Shows commercial plans collect by offset and can reduce the settlement "at Plan's sole discretion". No rate given |
| Commercial collection rate | **No source found** | | | | Assumption below |

**Recommended defaults.** Apply each rate to the amount left **after** appeals, so the two parameters do not double-count.

- **Demand to an in-network provider: 85% collected (assumption).** Range 55% to 95%. The low end is OIG's reported collection on sustained Medicare overpayments. The high end reflects offset against the claims of a provider who stays in the network. Time to collect is about 2 months (Medicare analog), with no discounting in the score.
- **Fraud referral: 25% collected (sourced in kind:** Medicare benefit-integrity recovered against referred, 24% in both years). Range 10% to 55%.

## 3. Appeals: share appealed, share overturned or reduced, dollar effect

| Figure | Source and URL | Year | Setting | What it measures | How far it supports our use |
|---|---|---|---|---|---|
| RAC FY2021: $345.76M collected; **$52.72M overturned on appeal at Level 1 (15.2% of collected dollars)**; 209,711 claims with collected overpayments | CMS, *FY2021 Medicare FFS Recovery Audit Report to Congress, Appendices*, App. B and C, https://www.cms.gov/files/document/fy-2021-medicare-ffs-rac-report-congress-appendicespdf.pdf | about 2023 | Medicare FFS, all claim types (RACs rarely review physician E/M) | Dollar reduction from Level 1 appeals | **Best dollar anchor.** Level 1 only, so a lower bound on the total reduction |
| RAC FY2021 Level 1: 35,934 decisions; fully favorable to the provider 34.0%, partly 3.8%, unfavorable 57.3%, dismissed 4.9%. **Part B claims only (A/B MACs): 11,357 decisions; fully favorable 41.7%, partly 7.6%, unfavorable 46.3%, dismissed 4.3%** (summed from App. M) | Same, App. M | about 2023 | Medicare Part B (practitioner claims, not only E/M) | Outcome given appeal | Supports about 45% to 50% of appealed practitioner findings reduced at Level 1 |
| RAC FY2021 Level 2 (QIC): 8,439 decisions; 41.2% favorable, 0.8% partly, 55.1% unfavorable | Same, App. N | about 2023 | Medicare | Outcome at Level 2 | Second-level reversal is also substantial |
| Level 1 decisions / claims with collected overpayments: 35,934 / 209,711 = **about 17%** | Derived from App. C and M | FY2021 | Medicare | Proxy appeal rate | Denominators differ (decisions in a year against claims corrected in a year) |
| FY2011: 6.7% of overpayment claims appealed, 43.6% of those overturned | CMS FY2011 RAC Report to Congress, https://www.cms.gov/research-statistics-data-and-systems/monitoring-programs/recovery-audit-program/downloads/fy-2011-report-to-congress_508.pdf (figures via Becker's summary) | 2013 | Medicare | Appeal and overturn rates | Range point |
| FY2013: 30.7% of claims with overpayment determinations appealed; 18.1% of appealed claims overturned; 9.3% of all determinations overturned | CMS FY2013 RAC Report to Congress (via RevCycleIntelligence, https://revcycleintelligence.com/news/cms-releases-fy2013-rac-report-to-congress) | 2014 | Medicare (inpatient-heavy years) | Same | Range point; inpatient short-stay dispute years |
| ALJs ruled for the appellant in 56% of appeals decided in FY2010 | HHS-OIG, *Improvements Are Needed at the ALJ Level of Medicare Appeals*, OEI-02-10-00340, https://oig.hhs.gov/reports/all/2012/improvements-are-needed-at-the-administrative-law-judge-level-of-medicare-appeals | 2012 | Medicare Level 3 | Outcome at Level 3 | Old; shows late-level reversal is common |
| OIG-recommended $647M, sustained $498M (77%) | A-04-18-03085 (item 2) | 2022 | Medicare | Reduction before collection | Another view: about 23% of identified dollars fall away before or during review |
| Private payers overturned 54.3% of initially denied claims (all denials 51.7%); providers spend $43.84 per contested claim (**later Premier figures: about 70% overturned, $57.23 per claim**) | Premier Inc., *Trend Alert*, March 2024, https://premierinc.com/newsroom/blog/trend-alert-private-payers-retain-profits-by-refusing-or-delaying-legitimate-medical-claims; 2025 figures via Premier's April 2025 letter to CMS (methodology not checked) | 2024, 2025 | Commercial | **Initial claim denials, not post-payment audit findings** | Not the same unit. Context only. (Score 4.0's $43.84 abrasion per round comes from this survey; a 2025 update may exist) |
| Blue Cross VT: the provider may dispute within 30 days to the Legal Department and Medical Director; accepting a settlement **waives appeal rights** | CPP_19 (item 2) | 2025 | Commercial | Appeal process | Commercial appeal paths are internal and contract-based. A settlement option lowers the appeal rate |
| Commercial post-payment-audit appeal or overturn rates; state external review of provider overpayments | **No source found.** State external review covers mainly members' coverage disputes | | | | Assumption below |

**Recommended default (sourced, Medicare analog):** a **15% expected reduction of demanded dollars by appeal.** This is FY2021 RAC Level 1 overturned dollars over collected dollars.

- Range: **9% to 30%**. The low end is FY2013's 9.3% of all determinations overturned. The high end is about 30% appealed x about 50% reduced, for E/M level disputes, which are judgment calls and so are likely to be reduced in part.
- How an overturn changes the dollars: a full overturn sets that claim's overpayment to 0. A partial one moves the supported level (for E/M, often by one level). For an extrapolated demand, either outcome recomputes the estimate from the revised sample. That is why the reduction should be modeled as a share of dollars, not a share of claims.
- The payer's own cost of handling appeals: **no source found**. Suggested assumption: 2 to 4 coder or nurse hours per appealed provider.

## 4. Records copy fees paid by commercial payers

| Figure | Source and URL | Year | Setting | What it measures | How far it supports our use |
|---|---|---|---|---|---|
| "Upon request, the provider shall provide BCBSRI copies of such records at no cost" | BCBS Rhode Island, Payment Policy *Hospital Audit Process*, last updated 2021-02-17, https://www.bcbsri.com/providers/sites/providers/files/policies/2021/02/2021%20Hospital%20Audit%20.pdf | 2021 | Commercial, hospitals | Contract term | Direct support for $0, but for hospitals, not physicians |
| The provider carries the cost of copies for claims and benefit determinations; no other fees are charged to the plan | Health Net California provider library, Medi-Cal manual, https://providerlibrary.healthnetcalifornia.com/medi-cal/provider-manual/medical-records/medical-records-all.html | current | Medicaid managed care (not commercial) | Contract term | Supports in kind |
| Contracted providers must "promptly provide medical records upon request" under the agreement and Chapter 12 of the Administrative Guide (no fee mentioned) | UnitedHealthcare, California commercial notice, https://uhcprovider.com/content/dam/provider/docs/public/health-plans/commercial/CA-COMM-IMRRR.pdf | current | Commercial | Duty to supply records | Duty confirmed; the fee term is in the guide, which was not opened |
| HIPAA fee limit applies "if the individual requests a copy" | 45 CFR 164.524(c)(4), https://www.law.cornell.edu/cfr/text/45/164.524 | current | Federal | Patient-access fees | **HIPAA sets no fee for a payer's audit request.** That disclosure is for payment or operations (45 CFR 164.506), so contract and state law govern |
| Medicare RACs pay practitioners **$0.15 per page plus postage, up to $15 per record** (mail, fax, CD), or $0.15 per page plus $2 per case up to $27 (esMD); hospital PPS providers $0.12 per page; critical access hospitals nothing | CMS Transmittal 786 (Pub. 100-08, CR 10529), 2018, https://cms.gov/regulations-and-guidance/guidance/transmittals/2018downloads/r786pi.pdf | 2018 | Medicare RACs only | What a federal contractor pays | The source of score 4.0's $90 (30 records x 20 pages x $0.15). An E/M visit note is probably 2 to 10 pages (assumption), which gives $9 to $45 per 30-record round plus postage. Whether MACs, UPICs or SMRCs pay copy fees was not checked |
| State laws on what a payer pays for copies | **No source found** for payer-specific copy-fee statutes; state copy-fee laws found address patient requests | | | | |

**Recommended default: $0 per request round (partly sourced:** commercial contract language at BCBSRI for hospitals and Health Net Medi-Cal; HIPAA sets no fee for payer audits).

- Sensitivity: **$90** (the Medicare RAC practitioner rate at 20 pages) and **$25** (the same rate at about 5 pages per E/M note).

## 5. Error-rate gate before extrapolation

| Figure | Source and URL | Year | Setting | What it measures | How far it supports our use |
|---|---|---|---|---|---|
| Statistical sampling is used "when it has been determined that a sustained or high level of payment error exists". The means include high error rates against similar providers, history, payment suspension, law-enforcement information, allegations and OIG audits. **No number is given.** The determination "is not subject to administrative or judicial review" | CMS, Program Integrity Manual ch. 8, §8.4.1.2 and §8.4.1.4 (Rev. 12127, 2023; chapter Rev. 13762, 2026-05-27), https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/downloads/pim83c08.pdf; SSA §1893(f)(3) | 2023, 2026 | Medicare contractors | Legal gate | The gate is a determination about the provider, often made from data before sampling ("high error rate ... compared to similar service providers"). **Our screen already meets that criterion**, so a gate on the sample's own rate is our addition |
| Physician integrity agreement (2023, amended 2025): random sample of **30** paid claims each quarter; "Error Rate" = net overpayment / paid dollars in the sample; the provider repays "the lower limit of the two-sided 90% confidence interval". **No error-rate threshold; always extrapolated** | HHS-OIG, Amendment to the Integrity Agreement with Arun Arora, MD (Appendix C), 2025-05-20, https://www.oig.hhs.gov/documents/cias/10282/Arun_Arora_MD_Amendment_05202025.pdf | 2025 | OIG enforcement, physician | Current OIG sampling practice | Strong support for score 4.0's 30-claim sample and its **two-sided 90% lower bound**, and for **no gate** |
| Older CIAs: a 50-claim Discovery Sample; a **net financial error rate of 5% or more** triggers a Full Sample (90% confidence, 25% precision) and a Systems Review; below 5%, no further work | OIG CIA Claims Review FAQ (archived), https://webharvest.gov/peth04/20041021045712/http://oig.hhs.gov/fraud/cia/docs/ciafaqcr.pdf; OIG open letter 2001, https://www.oig.hhs.gov/documents/open-letters/828/openletter111901.htm.html; HCCA handout 2014, https://assets.hcca-info.org/Portals/0/PDFs/Resources/Conference_Handouts/Compliance_Institute/2014/tue/607print2.pdf | 2001 to 2014 | OIG enforcement | Numeric gate | The only numeric gate found. **Its unit is net dollars over paid dollars, not the share of claims overpaid.** Older practice |
| Blue Cross VT: probe sample of 20 to 40 members; a statistical sample with ≥95% confidence; "the lower limit error rate will be extrapolated" (95% CI); settlement error rate = sample overpayment dollars / audited paid dollars, net of underpayments. **No threshold** | CPP_19 (item 2) | 2025 | Commercial | Commercial gate and bound | No numeric gate. Dollar-based error rate. More conservative bound (95%) than ours. Netting confirmed |
| New York: insurers may extrapolate if the sample is statistically valid (adequate size, random); **not where medical necessity is disputed** | NY Insurance Dept., OGC Opinion 04-12-32, https://www.dfs.ny.gov/insurance/ogco2004/rg041232.htm | 2004 | Commercial, NY | Legal condition | No numeric gate; validity is the condition |
| Commercial numeric threshold | **No source found** | | | | |

**Recommended default (assumption anchored to CIA practice):** change the gate's unit to the **net dollar error rate** (sample overpayment net of underpayments over sample paid dollars) and set it at **5%**.

- Sensitivity: **0%** (no gate, as in the 2025 OIG integrity agreement and Blue Cross VT), **15% share of claims** (score 4.0's), and 10% dollars.
- Related finding: the bound in score 4.0 (two-sided 90%, `BOUND`) matches the 2025 OIG integrity agreement exactly. Medicare's PIM asks for one-sided 90% and Blue Cross VT uses 95%, so keep both as sensitivity.

## 6. Extrapolation rights and look-back windows (brief)

| Rule | Source and URL | Year | Setting | Notes |
|---|---|---|---|---|
| Texas: recovery must be sought within **180 days** of payment (fully insured PPO and HMO) | Tex. Ins. Code §1301.132, 28 TAC §21.2818; TDI disciplinary order against UnitedHealthcare (1,196 requests sent after 180 days; $938,703 returned), https://www.tdi.texas.gov/commissioner/disciplinary-orders/documents/20269872.pdf | current; order 2025 to 2026 | Commercial, TX | Not ERISA self-funded plans (TMA, https://www.texmed.org/Overpayments/) |
| Florida: overpayment claims barred after **30 months**, and after **12 months for physicians** (chapters 458, 459 and others); fraud exception for providers convicted of fraud | Fla. Stat. §627.6131(6) and (18), 2026, http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0600-0699/0627/Sections/0627.6131.html | 2026 | Commercial, FL | Physician-specific: directly relevant to E/M |
| Illinois: no recoupment or offset **12 months or more** after payment; exceptions include a formal finding of fraud or material misrepresentation | 215 ILCS 5/368d(c) (FindLaw text, https://codes.findlaw.com/il/chapter-215-insurance/il-st-sect-215-5-368d/; 18 to 12 months from 2022-01-01 per ILCHIRO, https://ilchiro.org/?p=5949) | 2022 to 2025 | Commercial, IL | Statute text not opened on ilga.gov (certificate error); enactment history slightly inconsistent between sources |
| California: refund requests limited to **365 days** from payment unless fraud or misrepresentation | Knox-Keene, Health & Safety Code §1371.1 and 28 CCR §1300.71(b)(5) (statute pages blocked); DMHC cease-and-desist against Anthem and 2014 court judgment, CMA, https://cmadocs.org/newsroom/news/view/ArticleId/26971/Anthem-Special-Investigations-Unit-may-be-recouping-beyond-statutory-timeframe | 2015 | Commercial (Knox-Keene plans) | Secondary source for the 365 days; section numbers from code, not opened |
| New York: no recovery begun more than **24 months** after payment; exceptions for reasonable belief of fraud or abusive billing, self-insured plans and government programs; contract look-backs cannot extend it | NY Ins. Law §3224-b(b), https://codes.findlaw.com/ny/insurance-law/isc-sect-3224-b/; OGC Opinion 07-08-15, https://www.dfs.ny.gov/insurance/ogco2007/rg070815.htm | current | Commercial, NY | 2025 bills (S5209, A3365) would change it; not enacted as far as found |
| BCBSRI: audit notice within **18 months** of payment (hospitals) unless the contract says otherwise | BCBSRI Hospital Audit Process (item 4) | 2021 | Commercial contract | |
| Blue Cross VT: re-audit 6 to 24 months after the first audit; settlement waives appeal; extrapolation in contract policy | CPP_19 (item 2) | 2025 | Commercial contract | |
| Ten states had retroactive-denial limits in 2007, from 6 to 30 months, usually excepting fraud | Connecticut OLR Report 2007-R-0205, https://www.cga.ct.gov/2007/rpt/2007-R-0205.htm | 2007 | Survey | Dated |
| State limits do not apply to self-funded ERISA plans, Medicare (including Medicare Advantage), FEHBP or TRICARE | APMA News, Sept/Oct 2019, https://nxtbook.com/nxtbooks/apma/news_20190910/index.php?startid=34 | 2019 | Secondary | |
| Medicare: reopen within 1 year for any reason, 4 years for good cause, no limit for fraud or similar fault | PIM ch. 8 note citing 42 CFR §405.980 (URL in item 5) | current | Medicare | |
| Texas bills to ban extrapolation in commercial audits: HB 1649 (2017) and HB 895 (2023) each passed the House and **died in Senate committee** | Texas Legislature Online, https://capitol.texas.gov/BillLookup/History.aspx?LegSess=85R&Bill=HB1649 and https://capitol.texas.gov/BillLookup/History.aspx?LegSess=88R&Bill=HB895 | 2017, 2023 | Commercial, TX | Shows extrapolation is contested but generally permitted |

**Recommended statement for score 4.3 (assumption):**

- Extrapolation is allowed under contract when the sample is random and valid. In New York it is not allowed for medical-necessity disputes, but E/M level disputes are coding, not necessity, though that line is arguable.
- Default look-back: **12 months from payment** (Illinois; Florida for physicians), with a fraud exception for the referral lane. Sensitivity: 180 days (Texas) and 24 months (New York).
- **Data 4.0 covers one calendar year** (`docs/data_v4_0.md`: "one calendar year (2024)"). A 12-month look-back therefore binds only if the simulated demand date is set after year end; that date is not modeled today. A 180-day look-back would cut about half the year.

## Recommended parameters at a glance

| Parameter | Default | Range or sensitivity | Status |
|---|---|---|---|
| Fraud referral cost (total per referred provider) | $4,000 (about $3,700 above a demand) | $0, $2,000, $5,000, $15,000 | assumption (NHCAA 2013 blended $3,459; bottom-up $4,251; contractor $14K to $24K as upper context) |
| Collection, demand to an in-network provider (after appeals) | 85% | 55% to 95% | assumption (low end OIG A-04-18-03085) |
| Collection, fraud referral (after appeals) | 25% | 10% to 55% | sourced in kind (OEI-03-13-00620: about 24%) |
| Appeal reduction of demanded dollars | 15% | 9% to 30% | sourced, Medicare analog (FY2021 RAC Level 1) |
| Records copy fee per request round | $0 | $25, $90 | partly sourced (BCBSRI, Health Net Medi-Cal, HIPAA scope) |
| Extrapolation gate | 5% net dollar error rate | 0% (none), 10% dollars, 15% claim share | assumption anchored to CIA practice; no numeric gate in Medicare or commercial sources |
| Lower bound | two-sided 90% (unchanged) | one-sided 90% (PIM), 95% (Blue Cross VT) | sourced (2025 OIG integrity agreement) |
| Look-back | 12 months; fraud excepted | 180 days, 24 months | sourced (state statutes); binding only once a demand date is modeled |

## Open questions

1. **NHCAA provenance.** The 2013 survey figures come from a trade summary that could not be opened. Can someone with NHCAA membership supply the latest Anti-Fraud Management Survey (budget, FTEs, cases opened and closed, cost per case), ideally split into provider and member cases?
2. **Payer appeal-handling cost.** No source was found. Should appealed demands carry a payer staff cost (suggested 2 to 4 hours), and should the provider's appeal cost add to abrasion?
3. **Premier's abrasion figure may be stale.** Score 4.0's $43.84 per round is from the 2024 report. Premier's 2025 letter cites $57.23 per claim for private payers. Re-source it? (Outside #200's list.)
4. **Collection and appeals ordering.** This document assumes appeals first, then collection on what remains. Confirm before building, so the two do not double-count.
5. **Gate unit.** Moving from a claim-share gate to a dollar error rate changes which providers are extrapolated. Is that in scope for score 4.3, or should the unit stay and only the number change?
6. **Demand date and look-back.** To make a look-back meaningful on one-year data, the score needs a demand date (for example, three months after year end). Should score 4.3 model it?
7. **Referral lane recovery.** When a fabricated-visit provider is referred, does the payer still recover through its own stratified-sample demand (at the referral collection rate), or does recovery wait for law enforcement? The figures above assume the payer pursues its own recovery.
8. **Do Medicare MACs, UPICs and SMRCs pay copy fees?** Not checked. Only RAC rates (Transmittal 786) were verified.
9. **Unopened primary texts.** The California (H&S §1371.1 and 28 CCR §1300.71) and Illinois (215 ILCS 5/368d) statute pages were blocked here. Check them on leginfo and ilga before citing in `docs/score_43.md`.
