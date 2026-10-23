# Data 4.2: a continuous truth for upcoding and for other fraud, waste and abuse

[Back to the README](../README.md) · [data 4.0](data_v4_0.md) · [score 4.0](score_40.md) · [plan of release 4.2](release_v42_plan.md) · [reference arms on data 4.2](d42_reference_arms.md) · code: `src/generate_v42.py` (issue #173)

Real life has no answer key, so data 4.2 does not hand the arms or the evaluation a world of "upcoders" and "honest providers". Data 4.0 plants exactly 8 upcoders per dataset (`role`) and counts "found of N". Data 4.2 has **no planted role**. Every provider has a true net upcoding rate drawn from one distribution, and some providers also commit other fraud, waste and abuse (FWA) with its own overpayment. An arm pursues whoever it thinks is worth pursuing; the evaluation measures dollars and abrasion, and abrasion is incurred when the provider's true level of upcoding or FWA does not justify the pursuit.

Build it with `generate_v2.py --data-version 4.2` (a sibling module with its own random streams, so **data 2.x and data 4.0 reproduce byte for byte**: `tests/test_generator_regression.py` for 2.x, `tests/test_d40_regression.py` for 4.0, hashes taken before data 4.2 existed). The tables, the records universe and the note package keep the data 4.0 layout, so the frozen workflows run on it unchanged.

## a. The distribution of each provider's true net rate
The true net rate of a provider is the share of its live visits billed above the justified level minus the share billed below (as in data 4.0 and score 4.0). Each provider draws one number from a mixture. There is no quota and no count of "upcoders"; the number above any line varies by dataset.

| Component | Share of providers | Rate | Mechanism |
|---|---|---|---|
| **Core** | 94.2% | N(0, 5 points), clipped to -15% and +15% | honest coding noise in both directions (data 4.0's non-upcoders, unchanged) |
| **Tail** | 5.8% | 6% + a log-normal with median 12% and sigma 0.8, clipped at 45% | a habit (below) |

Why these numbers (from data 4.0's calibration, `data_v4_0_stats.md`):
- The expected share of providers at 15% net or above is **3.7%** (8 of 216), the same as data 4.0's 8 planted upcoders, so results stay comparable in scale. Here it is an expectation: a dataset has about 8 providers at or above 15% and the count varies by seed (the tail has a Bernoulli draw per provider).
- The tail is heavy: about 1.6% of providers are at 25% or above (3 to 4 per dataset) and 0.8% at 35% or above, where data 4.0 had every upcoder uniform from 18% to 37%. About 6 per dataset sit between 6% and 15% (a grey zone data 4.0 did not have).
- The core keeps data 4.0's noise (mean N(0, 5 points), gross miscoding of at least |mean| + 2 points), so honest providers sit near zero with realized rates of about -17% to +23% on small panels, as measured in data 4.0.
- **Honest high-acuity panels** (data 4.0's hard negatives, 8 of 216) stay, drawn independently of the rate (3.7% of providers, a Bernoulli draw each). Panel volume is drawn independently of the rate: data 4.0's volume floor for upcoders (250 visits) is a tell and is dropped, so a small panel can have a high rate and little money.
- About 216 providers per dataset as before.

**Habits attach by rate**, not by a quota. Only tail providers have a habit:
- Rate below 15%: opportunistic 60%, template-driven 40% (a systematic habit needs a large share of 99213-level visits, which is a feature of the 15%-and-above range).
- Rate 15% and above: data 4.0's shares, systematic 3/8, opportunistic 3/8, template-driven 2/8.
- Systematic, opportunistic and template-driven mean exactly what they meant in data 4.0 (`data_v4_0.md`): the generators of the habits are copied unchanged.
- **Intent for level upcoding**: true for systematic and opportunistic, false for template-driven (an EHR default) and for core noise.
- **Cloned notes**: as in data 4.0, a tail provider with a systematic or opportunistic habit clones notes with probability 0.125 (the data 4.0 default, 1 in 8). Cloned notes are an intent flag; their dollars are the provider's level upcoding dollars and are not counted again.
- Habit providers are exempt from level-changing corrections (as data 4.0 upcoders) so their realized rate stays near the draw; core providers keep the corrections.

## b. Fraud, waste and abuse beyond the level
A second truth dimension, drawn **independently** of the level rate and of each other (real correlations are unknown; see the open questions). Each kind has payer-visible signals and its own true overpayment in dollars, kept separate from the level-upcoding dollars.

| Kind | Providers (expected) | What the provider does | Payer-visible signals | True overpayment | Status |
|---|---|---|---|---|---|
| **Services billed but not rendered** | 3.0% (about 6 per dataset) | Extra claims (4% to 15% of its normal volume) for visits that never happened, placed on a small set of "ghost" members of its panel (a dozen or so, each seen many times) | claim volume above peers; many visits per patient; **a records request cannot be answered**: the office has no chart for these visits | the full paid amount of the phantom claims (every line) | **done**, with the office behaviour below |
| **Impossible visits per day** | 1.5% (about 3 per dataset) | On 2 to 6 days, 32 to 50 extra visits dated that single day | the number of claims per rendering provider per day (an honest provider's busiest day is about 15 to 25 at most; checked in `data_v4_2_stats.md`); total claim volume | the full paid amount of the extra claims (no chart exists for them either) | **done** |
| **Unbundling** | 2.0% (about 4 per dataset) | On 15% to 50% of its visits, an extra separately paid line (a duplicate lab line) with modifier 25 on the E/M line | extra lines and modifier 25 in `claim_lines.csv`; the detector view carries only whether a test line exists, so the frozen arms have **no tool** for this | the paid amount of the extra line | **done** in the raw tables; no arm reads it |
| **Cloned or fabricated notes** | within the level habit (above) | Documented elements and time inflated to the bill | the data 2.1 clone signals (text duplication, paste events, timestamps) | the level dollars of that provider (not added again) | **reused**, as an intent flag |

Not done: fabricated notes that a provider can produce on request (a not-rendered claim never has a chart here; a real fraud ring might fabricate one), correlations between kinds, referral fraud and anything involving a second provider.

**Office behaviour for not-rendered claims (office version 4.2).** `src/provider_sim.py` gets a new version "4.2" (office 2.0 and 2.1 are untouched, so earlier runs replay). It is office 2.1 plus: a claim that was never rendered can never come back. When the office answers (complete or partial) it returns every other chart it would have returned and reports the phantom ones under a new deficiency code `NO_RECORD`, "The office has no record of a visit on that date". A follow-up does not change it. The list of phantom claims lives in `records/unrendered_claims.csv`, a simulator-side file read only by the office (and by the old control-sample code); the view never carries it. Every claim keeps a row in `records_universe.csv` and a note package, so no other code breaks. The control-sample reviews of providers outside the list (the baseline in each view) skip phantom claims the same way.

## c. The answer key schema (eval only, continuous, no role)
`eval/answer_key/ground_truth_v2_<code>.json` (gitignored). Provider entries have:
- `habit` (systematic, opportunistic, template, or none), `intent` = `{level_upcoding, cloned_notes, not_rendered, impossible_days, unbundling}` (booleans), `uses_template`, `clones_notes`;
- `target_net_rate` (the draw), `net_rate` (realized on the live rendered claims, the basis of score 4.0), `up_rate`, `down_rate`, `mean_net_rate`, `honest_miscode_rate`, `panel_acuity_shift`, `provider_effect`, `top_shift`, corrections;
- `true_overpay_level_net` and `true_overpay_level_gross` (dollars, level difference, same pricing as score 4.0), `true_overpay_fwa` = `{not_rendered, impossible_days, unbundling}` in dollars, `fwa_claims` = counts, `true_overpay_total` = max(level net, 0) + FWA dollars (what is available to recover);
- `high_acuity_panel` (a panel property, not a label), `volume`, `billing_npi`, `group_tin`.

At the top: `data_version`, the sampling parameters, `fraud_claims` = `{claim_id: kind}` for every phantom claim, `justified_cpt_by_claim` for every claim (a phantom claim is justified at its billed level: its overpayment is in the FWA dollars, not in the level difference, so S4.0's level truth is not changed by it), and `cloned_visits`.
It has **no** `role`, `planted`, `above_margin`, `above_p95`, `subtle`, `planted_below_line`, `upcoder_definition` or `upcoder_margin`. `tests/test_data_v42.py` checks the absence of each. The answer key never reaches the view or the office.

## d. Evaluation without a role: `eval/metrics_d42.py`
Everything is a function of the answer key's continuous numbers and of what an arm did (which providers it sent a demand, asked, listed).
- **Available dollars** A = sum over providers of `true_overpay_total`.
- **Dollars pursued over available**: true overpayment of the providers the arm sent a demand to, divided by A. Also reported for asked and listed providers, split into level and FWA dollars.
- **The justification threshold in dollars.** A provider is *justified* when its true overpayment is at least `m` times the cost of pursuing it: the staff cost of a 30-chart request and one demand under score 4.0's prices (charts, two rounds, demand work, triage; the number is printed by the module, about $750 to $800), with `m` in 0, 0.5, 1, 2 and 4. The primary view is m = 1; the others are the sweep. This is a derived, evaluation-time label and never reaches a generator or an arm. The 15% rate line of score 4.0 is reported beside it: the two views disagree on high-volume providers at 5% to 15% (many dollars, a low rate) and on low-volume providers above 15% (few dollars, a high rate), and on every FWA-only provider.
- **Precision in dollars and in providers**: the share of pursued providers that are justified; the share of the *recovered* dollars that came from justified providers; honest-looking pursuits (not justified) and the recovery taken from them.
- **Abrasion exposure**, two ways. (1) Score 4.0's, weighted by the true net rate (full at 0% or below, none at 15% or more). (2) A dollar basis, weighted by true overpayment against the threshold: weight 1 at zero, falling linearly to 0 at the threshold, times the same abrasion price (rounds x $43.84 + $2,000 per demand). The dollar basis counts the FWA dollars, so pursuing a not-rendered-claims provider with a flat level rate is not abrasive. Both are printed; neither changes score 4.0.
- **Score on data 4.2** = recovery - staff cost - abrasion, with score 4.0's recovery and staff cost unchanged (recovery from a chart sample is a level-difference estimate, so it can only reach the level dollars; it cannot reach FWA dollars: by construction, since the arms have no tool for them), with abrasion either way.
- **Graded ranking metrics for screens**: NDCG at K on `true_overpay_total` (linear gain) over the screen's full ranked list, and the share of available dollars in the top K.
- **The oracle with triage** (as `eval/ceiling_benchmarks_41.py`, but with the abrasion term it lacked: on data 4.2 an oracle that pursues a non-upcoder pays abrasion): pursue provider p only when its expected 30-chart recovery bound minus ask cost minus triage minus abrasion is positive.
- Any binary view ("justified at m") is derived here. Counts such as "found" are derived the same way and labelled.

## e. Compatibility with score 4.0 and the run scripts
Nothing in the run path of the reference arms reads the answer key (checked: `make_v2_runs`, `make_v2_ai_runs`, `workflow_policy_40`, the screens and the office read the view and the records only). Only evaluation code reads it, and score 4.0's `seed_result` needs `key[pid]["role"]`, a truth dict per provider, and `justified_cpt_by_claim`. So the adapter is pure evaluation code, `eval/d42_truth.py`:
- it loads the D4.2 key and builds, for each dataset, a **derived key** `{pid: {"role": "upcoder" if justified else "honest", "role_derived_at": "true_overpay_total >= m x pursuit cost"}}` clearly labelled as derived at evaluation time, for the functions that still count "found";
- it computes the **level truth** (`provider_truth`) on rendered claims only, so phantom claims do not dilute the net rate or inflate the abrasion weight, and passes it to `score_40.seed_result(..., truth=...)`;
- it builds its own run-folder ids and codes (`d42_<seed>`, `d42wl...`) so a D4.2 run never meets a D4.0 run with the same seed number; the seed registry is checked for data version "4.2".
`eval/score_40.py`, `recovery_40.py` and the D4.0 loop (`eval/w_loop.py`) are not edited.

## f. Open questions and my choices
1. **Is FWA independent of the level rate?** Chosen: independent draws per kind. In real life fraud rings do both; this choice makes level screens miss FWA-only providers. Easy to change (one probability per kind given the tail).
2. **Records not provided.** The Program Integrity Manual treats sampling units without records as overpayments. Score 4.0 does not model it ("not modeled", #68). So a provider with phantom claims is not penalized in recovery for failing to produce charts; the NO_RECORD fraction only shrinks the sample. Chosen: leave as is and say so.
3. **The justification threshold.** Chosen: true overpayment at least 1x the S4.0 cost of a 30-chart request and a demand, swept 0 to 4x. The 30-chart size is W4.0's first sample; a different cost basis moves the line.
4. **Dollar-basis abrasion** is an extension to S4.0, not S4.2 (issue #178 decides the real one). Reported beside S4.0's, not replacing it.
5. **Unbundling needs the claim lines** and the pre-flight data-quality checks might read a duplicate lab line as a defect; the test checks it and the doc below says so if it does.
6. **The agent.** Agent A5.x builds its office inside `Environment`; the new office version is not wired there. Reference arms are workflows only. Not done.
7. **Habit shares by rate** (60/40 below 15%) are assumptions with no source, like data 4.0's shares.
8. **The impossible-day threshold** (32 to 50 extra visits) is a modelling choice (about 14 hours or more of time-based visits); an honest day above 25 is vanishingly rare, but real days are not Poisson.
9. **Seeds.** Pools are keyed by (data version, seed). Development and confirm pools of 100 seeds each, a test pool of 10 and a reserved pool of 10 are named in the registry with numbers below 5555 that do not collide inside data 4.2; only the first two are built, and only part of the confirm pool.

## What is easier by construction
Documents are generated from the true complexity, as in data 4.0. Every FWA kind has a clean signal (a volume spike, a ghost panel, an extra line) that real fraud hides better. Phantom claims look like normal claims in the view; the office is the only thing that knows. The not-rendered kind is as detectable as a records request makes it, and no arm in this repository has a tool for it yet.
