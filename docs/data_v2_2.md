# Data 2.2: realism and data defects

[Back to the README](../README.md)

Release 2 pairs data 2.2 with workflow `v2.2` and agent `v3.2` (see [versioning.md](versioning.md)). Data 2.2 is data 2.1 plus the changes below, each
behind its own option of `src/generate_v2.py --data-version 2.2`. Claims, the records universe and the note package of data 2.0 and 2.1 are never changed:
with every 2.2 option at zero a 2.2 build reproduces the 2.1 files byte for byte (`tests/test_v22.py`).

## Where the defaults come from

The defaults below were first picked on seed 42 for plausibility. A web search for published figures (October 2026) found the following; the first column says what each source can and cannot support.

| Default | What the search found | How far it supports the default |
|---|---|---|
| `honest_miscode_rate` 0.08 | HHS OIG, claims for 2010: [42% of Medicare E/M claims were incorrectly coded](https://oig.hhs.gov/reports/all/2014/improper-payments-for-evaluation-and-management-services-cost-medicare-billions-in-2010/) (up and down) and 19% lacked documentation; a [secondary summary](https://www.oalaw.com/2014/05/hhs-oig-2010-medicare-audit-6-7-billion-misspent-for-evaluation-and-management-services/) says far more were upcoded than downcoded. CMS CERT puts established office visits at a payment-error rate of about 6 to 7% ([secondary source](https://medlearn.com/racmonitor/essential-information-to-protect-your-facility-from-auditors/); dollar-based and counts documentation errors). Observed family-practice visits matched the physician's code only [52 to 55% of the time](https://www.aafp.org/pubs/fpm/issues/2005/0600/p17.html) (Chao 1998, King 2001, as summarized in secondary reports). | Published error rates run from about 7% (payment) to about 45% (audit mismatch), and most of the high figures include a reviewer disagreeing with the coder, which this simulation models separately (`records.CODER_NOISE`, 15% of charts read one level off). 0.08 for the claim itself, plus 0.15 at chart review, lands between the two. It is a judgment, not a measurement. The evaluation should vary it (0.05, 0.08, 0.15) instead of trusting one value. |
| `honest_up_share` 0.5 | Medicare audits found errors mostly upcoded; primary-care studies of observed visits found them [evenly split or mostly undercoded](https://www.aafp.org/pubs/fpm/issues/2005/0600/p17.html) for established patients (a pediatric study: 44% undercoded, 1% overcoded). | Evidence points both ways; 0.5 is the middle. Vary it (0.3, 0.5, 0.7). |
| `honest_miscode_spread` 0.4, `honest_miscode_max` 0.12 | None found. OIG did find that [high-coding physicians](https://oig.hhs.gov/reports/all/2012/coding-trends-of-medicare-evaluation-and-management-services) bill high levels consistently, which supports provider-to-provider variation but not its size. | Unsourced. Chosen so honest noise stays below the upcoder margin. |
| correction share 0.25, up 0.4, group billing, blank rendering 0.3 | None found for the share of corrected claims that change the level, or for how often a single-clinician claim leaves rendering blank. | Unsourced. Treat as structure to test the pipeline, not as realism. |
| upcoder 15 to 40% of visits, subtle 8 to 12% | No published distribution of upcoding intensity was found. OIG's 2012 study found about 1,700 physicians who consistently billed the highest levels, [without deciding the claims were wrong](https://oig.hhs.gov/reports/all/2012/coding-trends-of-medicare-evaluation-and-management-services). | Unsourced; the 15 to 40% range predates data 2.2. |

Nothing in the search justified changing a default, so none changed. The searches returned secondary summaries more than the CMS and OIG tables themselves; before quoting any
of these figures outside this repository, check them against the original CMS CERT supplemental tables and OIG reports.

## Honest coding noise and an upcoder defined as above the honest baseline (issue 74)

Before, honest providers billed exactly the justified level; the only noise was a coder disagreeing when a chart was read. Now every provider, upcoders
included, miscodes a share of its visits (a separate random stream, so nothing else moves).

| Option | Default | Meaning |
|---|---|---|
| `--honest-miscode-rate` | 0.08 | mean share of an honest provider's visits billed one level off the justified level |
| `--honest-up-share` | 0.5 | share of those slips that go up; the rest go down |
| `--honest-miscode-spread` | 0.4 | provider-to-provider coefficient of variation of the rate (a Beta distribution), so some doctors are careful and some are aggressive but defensible |
| `--honest-miscode-max` | 0.12 | cap on any provider's rate |
| `--upcoder-fraction LO HI` | 0.15 0.40 | share of visits an obvious upcoder bills one level up (unchanged from before) |
| `--subtle-upcoder-share` | 0.25 | share of upcoders drawn from the subtle range |
| `--subtle-upcoder-fraction LO HI` | 0.08 0.12 | the subtle range |
| `--upcoder-margin` | 0.06 | an upcoder's upcoding rate must exceed the honest baseline by at least this many points of visits |
| `--upcoder-definition` | `payer` | `payer`: the margin test **and** a rate above the 95th percentile of the honest providers ([why](#the-payer-based-upcoder-definition-built-the-default)); `margin`: the margin test alone |

**The defaults are illustrative.** They are not calibrated to a published coding-error rate (none was used). They were chosen on the development seed 42 for
plausibility and so that honest noise stays below the margin; the sweep below is the check, and it was not used to tune toward a result.

**Answer key (evaluation only).** Each provider records its `planted` role, whether it is `subtle`, its `honest_miscode_rate`, and its realised `upcode_rate`
and `downcode_rate` (share of visits billed above and below the justified level). The key's top level records `honest_baseline_upcode_rate` (the mean
`upcode_rate` of providers planted honest) and the margin. The `role` that every evaluation reads is now **`upcoder` under the payer-based definition** ([below](#the-payer-based-upcoder-definition-built-the-default)): the provider's `upcode_rate` is above the 95th percentile of the honest providers' rates and at least the margin above their mean (`--upcoder-definition margin` drops the first test); otherwise `hard_negative` (a planted high-acuity panel) or `normal`. The key also records `honest_p95_upcode_rate`, `above_margin`, `above_p95` and `planted_below_line` for each provider. Consequences, said plainly:

- A planted upcoder whose realised rate fails either test is labeled `normal` (`planted_below_line`). In seed 42 one of eight planted upcoders (a subtle one at a 9.6% rate: above the honest 95th percentile of 6.8%, but under the margin line of 10.1% = baseline 4.1% + 6 points)
  is therefore not counted: the data has 7 upcoders, not 8.
- An honest provider that passes both tests would be labeled `upcoder`. None did in seed 42 (highest honest rate 9.6%, which passes the percentile test but not the margin test); a margin closer to the honest spread would produce such cases.
- Everything that reads `role` (screen, scoreboard, judges) keeps working; the number of upcoders can now differ from the number planted.
- Cloned notes still apply to every visit a cloning provider bills above the justified level, including honest slips upward. Small, and only for cloners.

### The payer-based upcoder definition (built, the default)

**What payers use.** None of the sources found defines an upcoder by intent. Payers and Medicare contractors work in two steps, and the numbers in the second step are not published:

1. **Find outliers against specialty peers.** CMS Comparative Billing Reports compare a provider's code use with state and national peers in the same specialty by percentile ([secondary summary](https://AAO.ORG/eyenet/article/comparative-billing-reports-2)); a Blue Cross plan describes a vendor review of high-level E/M codes (99204, 99205, 99214, 99215, 99244, 99245) to find practitioners billing a higher share than like-specialty peers ([Blue Cross Minnesota](https://bluecrossmn.com/sites/default/files/DAM/2021-11/P11GA_13148857.pdf)); the HHS OIG's list of high-coding physicians used the top 1% of average code level in a specialty and about 95% of services in the two highest levels (secondary summaries of the [2012 report](https://oig.hhs.gov/reports/all/2012/coding-trends-of-medicare-evaluation-and-management-services); I did not retrieve the report's methodology section, so check the exact thresholds).
2. **Confirm by reviewing a sample of claims against the records.** In Medicare's Targeted Probe and Educate, a contractor reviews 20 to 40 claims per round, up to three rounds, and computes a **claims error rate** (claims in error divided by claims reviewed) and a **payment error rate** (allowed dollars in error divided by allowed dollars); the threshold is set by the contractor and sent in the provider's letter, and a provider still above it after round three can face extrapolation, 100% prepayment review or referral ([CGS Medicare](https://www.cgsmedicare.com/parta/mr/tpe_process.html), [CGS FAQs](https://cgsmedicare.com/parta/mr/tpe_faqs.html)). A non-response counts as an error.

**Definition: use the same two tests on the true values** (built as `--upcoder-definition payer`, Simmy's decision). A provider is an upcoder when its true overbilling rate, the share of its live claims billed above the level the chart supports, is
(a) **above the 95th percentile of the honest providers' rates**, so a peer-percentile screen would call it an outlier, **and** (b) **at least a stated margin above the honest mean** (6 points of visits as built), so a claims-error-rate review of a sample would confirm it as material.
`--upcoder-definition margin` is test (b) alone; (a) is added so a lucky honest provider does not cross the line. The numbers 95th percentile and 6 points are our choices: the sources fix the structure, not the thresholds (the OIG used top 1%; TPE thresholds are per contractor and unpublished).
Consequence, said plainly: a planted subtle upcoder under the line (`planted_below_line` in the key) is **not** an upcoder, because a payer following these rules would not act on it either; the evaluation reports it separately as "planted below the payer line" instead of hiding it. The dollar side stays in the key (excess paid dollars per provider) so misses can be weighed.

An earlier idea (labels fixed by planted intent) was dropped: payers cannot see intent, and a label no payer rule could reproduce would make the evaluation less comparable to practice.

### What honest noise does (development seed 42, free, one draw per row)

<!-- sweep:start -->
| Honest miscode rate | Counted upcoders (of 8 planted) | Honest baseline upcoding | `riskadj` top 25: upcoders / honest | `eb_ratio` top 25: upcoders / honest | Chart rule on screened doctors: upcoders / honest accused |
|---|---|---|---|---|---|
| 0% | 8 | 0.2% | 8 / 17 | 8 / 17 | 1 / 0 (of 11 sent) |
| 4% | 8 | 2.2% | 8 / 17 | 8 / 17 | 1 / 0 (of 10 sent) |
| 8% | 7 | 4.1% | 7 / 18 | 6 / 19 | 1 / 0 (of 9 sent) |
| 16% | 7 | 5.6% | 6 / 19 | 6 / 19 | 1 / 0 (of 10 sent) |
<!-- sweep:end -->

Read with care: one dataset per row, 7 to 8 upcoders, so a difference of one doctor is noise (the 0% row still shows a 0.2% baseline because the corrections of issue 79 move a few levels). The rate column is the rate asked for; the cap
(0.12) holds the 16% row to a lower realised rate, which the baseline column shows (5.5% of visits billed above the justified level). What the table
supports: the screen still ranks planted upcoders high under honest noise (it works on the 99215 share, which honest slips both raise and lower), with
`riskadj` and `eb_ratio` each missing about one upcoder from the top 25 once noise is on.

What it changes more clearly is the evidence from charts. Honest doctors now bill about 4% of visits above the level the chart supports (and about 4%
below), so **a chart that supports a lower level than billed is no longer proof of upcoding**. The earlier zero-false-accusation result for the chart rule
was partly built in, but this sweep cannot size the effect: with noise on, the chart rule accused no honest doctor in any of the four runs (it faced 9 to 11
doctors each time and selected only the one upcoder). That is too small a sample to estimate a false-accusation rate; it belongs to the release 2
evaluation on fresh seeds. The structural point stands: the chart rule's earlier zero was partly guaranteed by construction, and is no longer.

### Figure

`docs/images/expected_billed_2_2.svg`: the same expected-versus-billed grids as `expected_billed.svg`, on seed 42 data 2.2. Normal and high-acuity
doctors now show visits billed above the supported level.

![Expected level versus billed level on data 2.2](images/expected_billed_2_2.svg)

## Billing provider is the group; rendering NPI omitted when it equals billing (issue 75)

Real professional claims are usually billed by the group (an organizational NPI) with the treating clinician as rendering provider, and the rendering
field is often left blank when it equals billing. Before, `billing_npi` equalled `rendering_npi` on every claim and `group_tin` was never used.

| Option | Default | Meaning |
|---|---|---|
| `--group-billing` / `--no-group-billing` | on | clinicians sharing a `group_tin` with at least one other clinician bill under an organizational NPI (starts with 2); single-clinician groups bill under their own NPI |
| `--rendering-omitted-share` | 0.3 | share of single-clinician claims (billing equals rendering) with the rendering NPI left blank; its own random stream, so changing it moves no billed level |

`src/derive.py` (the detector view) attributes each visit to the **clinician who saw the patient**: the rendering NPI, or the billing NPI when rendering is
blank and billing is an individual. A blank rendering NPI under an organizational billing NPI cannot be attributed; that visit is dropped and counted.
When any visit used the fallback, was group billed, or was unattributed, the view gets `attribution.json` with the counts, the share of visits that
fell back to billing, and `billing_entity` (clinician to the NPI that receives actions). Views of earlier data get no such file and are byte-identical.

- **Scoring is never done at the group level.** The screen, the metrics and every finding are per clinician. Seed 42: 187 of 216 clinicians bill under an
  organizational NPI that is not their own; 3.3% of visits (3,899) fell back to billing; 0 were unattributed.
- **Actions go to the billing entity.** `derive.billing_entity(view_dir)` gives the NPI a records request or recovery would be addressed to. The simulated
  provider office (`provider_sim.py`) still behaves per clinician; modelling a group office that answers for several clinicians is not built.
- What this does not do: the claims are not otherwise harder to read. It tests that the pipeline attributes visits correctly when the rendering field is
  absent or the biller is an organization, and it is the plumbing the data-quality check (issue 81) reports on ("share of claims missing a rendering NPI").

## Diagnosis-code truncation in the plan's extract (issue 77)

`claims_header` carries `dx1` to `dx6` (an 837P allows 12) and nothing tested what happens when a plan's warehouse or extract keeps fewer. Truncation lowers
derived condition counts, so sick panels look healthier and honest high-acuity doctors look like upcoders.

| Option | Default | Meaning |
|---|---|---|
| `--dx-cap N` | 0 (off) | keep only the first N diagnosis positions in the delivered `claims_header` (the claim, and the visit note, had more) |
| `--dx-cap-months M ...` | all | service months the cap applies to (a re-extract of some months only) |

The answer key records the defect under `defects.dx_truncation` (cap, months, number of claims shortened) so a data-quality check can be graded
(issue 81). Truncation uses no random numbers: nothing else in the data moves.

**Measured on the development seed 42** (`python eval/dx_cap_effect.py --write`; free; one draw per row):

<!-- dxcap:start -->
| Diagnosis positions kept | Claims shortened | Mean derived conditions per patient | High-acuity doctors: 99215 share / expected | Doctors with suspicion >= 5 | `riskadj` top 25: upcoders / high-acuity / ordinary | `riskadj` AUPRC | `eb_ratio` top 25: upcoders / high-acuity / ordinary | `eb_ratio` AUPRC |
|---|---|---|---|---|---|---|---|---|
| 6 (no cap) | 0 | 1.54 | 1.16 | 9 | 7 / 1 / 17 | 0.456 | 6 / 1 / 18 | 0.751 |
| 4 | 9,118 | 1.49 | 1.19 | 8 | 6 / 2 / 17 | 0.454 | 6 / 1 / 18 | 0.779 |
| 3 | 19,294 | 1.38 | 1.34 | 8 | 6 / 2 / 17 | 0.450 | 6 / 2 / 17 | 0.735 |
| 2 | 38,696 | 1.16 | 1.54 | 10 | 5 / 4 / 16 | 0.413 | 6 / 2 / 17 | 0.582 |
<!-- dxcap:end -->

Reading it: a cap of 4 or 3 changes little (the mean derived count falls from 1.54 to 1.49 and 1.38, one more high-acuity doctor enters the top 25); a cap of
2 is clear: the mean count falls to 1.16, the high-acuity doctors' 99215 share rises from 1.16 to 1.54 times what the model expects, four of them reach the
top 25 (one before), and `riskadj` loses two upcoders from its top 25. `eb_ratio` is affected less in the top 25 but its AUPRC falls from 0.75 to 0.58.
One dataset, 8 high-acuity doctors and 7 upcoders, so single doctors move these counts; the direction (sicker panels look healthier, honest
high-acuity doctors look worse) is what the generator guarantees and the table confirms. Only the first `N` positions survive, and the generator puts
chronic conditions first, so a low cap removes chronic conditions before acute ones; a plan that orders diagnoses differently would truncate differently.

**Response when truncation is suspected** (built with the data-quality check, issue 81): findings that rely on risk adjustment are held or marked
low-confidence, and a person asks the plan for a full-fidelity re-extract from its original claim records. The agent does not request data itself.

## Corrected claims that change the billed level (issue 79)

Before, every replacement claim (frequency 7) was an exact copy of its original ("original replaced by a corrected claim with the same content"), so a
correction never changed the code. Real corrections move the level up or down.

| Option | Default | Meaning |
|---|---|---|
| `--correction-level-change-share` | 0.25 | share of replacement claims whose E/M line moves one level (amounts follow the new level) |
| `--correction-up-share` | 0.4 | share of those that go up; the rest go down (at the edge of the range the direction flips) |

Own random stream, so changing it moves no other claim. The original is reversed and the replacement is the live claim; `derive.py` already keeps the
live version, so the detector view shows the corrected level (a test checks it). The answer key's `upcode_rate` and `downcode_rate` use the **live**
claim: a provider whose claims are corrected downward is not an upcoder for the visits it fixed. Per-provider `corrections`, `corrections_up` and
`corrections_down` are recorded.

**Context signal, not evidence.** `derive.correction_stats(v2_dir)` gives each clinician's corrections and their direction, so a reviewer can see a
provider's correction rate against peers. Honest providers correct in both directions, and a provider who corrects downward is fixing its own overbilling:
the screen sees only the live level, so frequent correctors are not penalized for the original. On seed 42:

<!-- corr:start -->
- 122,716 visits and 2,443 corrected claims (2.0%); 613 corrections changed the level (241 up, 372 down).
- Correction rate per clinician with at least 100 visits: median 1.9%, 5th to 95th percentile 0.7% to 3.4%, maximum 4.5%.

The five clinicians with the most downward corrections:

| Clinician | Visits | Corrections | Down | Up | Role | Screen rank (of 216) |
|---|---|---|---|---|---|---|
| 1000000110 | 2500 | 54 | 10 | 9 | normal | 43 |
| 1000000069 | 2198 | 52 | 9 | 7 | normal | 209 |
| 1000000056 | 2105 | 33 | 8 | 1 | normal | 14 |
| 1000000058 | 2500 | 44 | 8 | 3 | normal | 214 |
| 1000000075 | 2500 | 42 | 8 | 3 | normal | 210 |
<!-- corr:end -->

One of the five (1000000056, screen rank 14) is high in the screen for its 99215 share; its corrections are eight down and one up, so they lower its count if
anything. The other four rank 43 to 214. Corrections are about 2% of visits, spread evenly across providers by the generator (no provider-level propensity), so "providers who correct often" here
are sampling spread, not a modeled behavior. A provider-level correction habit is not built.

## Injected data defects and the plan's control totals (issue 80)

The synthetic data is clean, so any data-quality check would pass trivially. Data 2.2 can inject defects into the **delivered extract** (the plan tables), each
off by default, with its own random stream so nothing else moves (`src/defects_v22.py`; the diagnosis cap of issue 77 is the fifth defect).

| Option | Default | Defect |
|---|---|---|
| `--defect-duplicate-share` | 0 | share of paid claims delivered twice, the copy under a new claim id (the copy also gets a records-universe row and a justified level; it has no note) |
| `--defect-orphan-share` | 0 | share of replacements and voids whose original claim is missing from the extract |
| `--defect-unknown-member-share` | 0 | share of claims whose member id does not join to eligibility (`members.csv`) |
| `--defect-no-rendering-share` | 0 | share of group-billed claims with the rendering NPI blank, so no clinician can be named |
| `--dx-cap`, `--dx-cap-months` | off | diagnosis truncation ([above](#diagnosis-code-truncation-in-the-plans-extract-issue-77)) |
| `--control-totals` | on | writes `control_totals.csv`: claims and paid dollars by service month **as the plan says it delivered**, computed from the clean extract before any defect |

With no defect the delivered tables reconcile with the control totals exactly (a test checks it); each defect breaks the reconciliation by exactly the
injected rows (duplicates add claims and dollars, missing originals remove them). The answer key records every injected defect under `defects` (counts and
claim ids) so the checks can be graded. `derive.py` drops visits whose member does not join and visits it cannot attribute to a clinician, and counts both in
`attribution.json`; it does not remove duplicates, because finding them is the data-quality check's job.

A graded example, seed 42, data 2.2 with defects (`experiments/261016_2_code`, data folder gitignored):
duplicates 1% (1,190 claims), orphans 30% (737 replacements and 378 voids lose their original), unknown members 0.5% (562 claims), no rendering NPI 3% of
group-billed claims (2,981), diagnosis cap 3 from July (9,677 claims shortened). It is development data for building and grading the check (issue 81).
Defects are not part of the default release 2 settings; whether the release 2 evaluation uses them is a decision for the evaluation plan.

## Defect profiles for the evaluation runs with defects

The release 2 evaluation includes runs on data with defects (a plan's extract is never clean). Two named profiles (`--defect-profile`; explicit `--defect-*` options override a profile):

| Profile | Duplicates | Orphan chains | Unknown members | No rendering NPI (group-billed) | Diagnosis cap | Meant to be |
|---|---|---|---|---|---|---|
| `moderate` | 0.5% | 10% | 0.3% | 2% | 4, last three months | the ordinary problems a plan finds and fixes; the pre-flight should warn and the screens should still work |
| `severe` | 1% | 30% | 0.5% | 3% | 3, from July | the graded stress dataset of issue 80; the pre-flight should hold findings |

Defects are about the extract, not the doctors: the answer key's upcoders are unchanged, so a run on a defect profile is paired with the same seed without defects.

## Not yet built

Not built in this release 2 work so far: incident-to billing (issue 76), claims lag and monthly feeds (issue 78) and the X12 ingestion path (issue 82).
