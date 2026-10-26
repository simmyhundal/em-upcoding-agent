# Data 4.3 design (SEALED until the release 4.3 test is done)

**Sealed.** This page is for the data builder and for close-out. The session that develops the workflow and agent arms must not read it before the release's test (docs/process.md, "Sealed data design"). At close-out it moves to `docs/` and is linked from the release notes. The public description is the data card, `docs/data_v4_3.md`.

**What this page is.** How data 4.3 is generated: every mechanism, its parameters (the defaults in `V43_DEFAULTS`, `src/generate_v43.py`), why they were chosen, what they overlap with, and the statistics measured on a few development builds. Built 2026-10-25 by the data-builder sub-agent from issues 197, 220, 201, 137 and 144.

## Structure and reproducibility
- `src/generate_v43.py` is a sibling of `generate_v42.py`. It copies data 4.2's build path and adds the new mechanisms. Random streams are `[seed, 43, k]`. Streams k = 0 to 13 play data 4.2's roles, and k = 31 is the defects stream. The note generator uses `[seed, 43, 17]`, where data 2.1 to 4.2 use `[seed, 17]`. New streams: 50 for per-provider attributes (a fixed 16 uniforms plus two Beta draws per provider), 51 for chart variability, 52 for diagnosis confounders, 53 for extra visits and batching, 54 for padded days and fabrication, 55 for the lab and unneeded tests, and 56 for coverage pairs and office profiles. Each new mechanism draws a fixed number of numbers whatever the options, so switching one family off does not move the others.
- Data 4.3 has its own stream family so that comparing a data 4.2 build and a data 4.3 build with the same seed number reveals nothing. For example, seed 1741 is in both development pools. `stream_family=42` with `OFF_43` reproduces data 4.2's files byte for byte; this is tested.
- Data 4.2 regression hashes (data and offices 2.0, 2.1, 4.2) were taken on unmodified code before any data 4.3 edit: `tests/test_d42_regression.py`, `tests/generator_hashes_v42.json`.
- The answer key writes `config_hash` and `config_profile` instead of data 4.2's full `parameters` block, so the key does not carry the settings verbatim.

## a. Calibration (issues 137 and 144)
| Parameter | Data 4.2 | Data 4.3 default | Why |
|---|---|---|---|
| Habit shares, rate 15% or more | systematic 3/8, opportunistic 3/8, template 2/8 | 0.30 / 0.45 / 0.25 | An assumption, still unsourced: borderline (opportunistic) upcoding is taken to be the commoner pattern. The systematic share is lowered because it is the easiest habit to see in a code mix. |
| Habit shares, below 15% | opportunistic 0.6, template 0.4 | 0.65 / 0.35 | Same reasoning. |
| Time recorded | flat 0.65 per visit | per provider, Beta(mean 0.65, kappa 6) | Documentation styles differ by practice. A flat share made "time missing" uninformative across providers; now it is a provider trait. |
| Lab line | P(line) = 0.9 when the true data element is 3 or more, else 0.1 | `test_link` 0.5. P = 0.5 x (data 4.2's) + 0.5 x q, where q = clip(lab_rate x (0.5 + 0.25 x chronic count), 0.02, 0.9) and lab_rate ~ Beta(0.30, kappa 5) per provider | Issue 144: the link exists but data 4.2's was too pure. Provider style and panel chronicity now drive half of it. |
| In-house lab | every practice | 70% of practices. For the rest the test is ordered in the note (orders file) but has no claim line. | Outside labs bill on their own claims, which are not in this extract. This confounds `data_without_tests`-type rules. |
| Unneeded tests | none | 35% of systematic or opportunistic providers add a test to 30% to 80% of their upcoded visits that had none | An upcoder supports the data element. The paid test line is recorded as `unneeded_test_paid` and is not in `true_overpay_total`. |
| Date range | 1 year | 1 year (`years` option; volume scales; drift runs across the whole range) | Multi-year is an option, not the default. `derive.py` computes age as 2024 minus birth year. |

Not done under issue 137: the check of the synthetic 99213 and 99214 shares against the CMS public file (no source access in this session), and the sweep of which v4/v5 conclusions survive each setting. That sweep is an experiment for the arm session or a later release. The base code mix, thresholds and volume distribution are unchanged from data 4.2.

## b. Legitimate high volume (issue 197)
All of these are real, rendered visits billed at the justified level. Their level truth and dollars are counted like any other visit.

| Mechanism | Who | Parameters | Effect |
|---|---|---|---|
| Mid-level visits under the physician's number (shared NPI / incident-to) | 8% of providers | volume x (1 + U(0.25, 0.75)); panel unchanged | more visits per patient and per day |
| Coverage for an absent colleague | 6% of providers cover one colleague (same TIN if any, else anyone) | block of 5 to 15 weekdays. The colleague's visits in the block are moved to the nearest allowed day. The coverer gets round(colleague volume x block / W) extra visits on the colleague's members, dated inside the block. | busy days with patients from another panel, which is a ghost-panel look-alike |
| Short clinic week | 15% of providers | 2 or 3 clinic weekdays (more when volume / (52 x days) would exceed 26 per day). Visit dates snap to the nearest clinic day in the member's coverage window. | every day is busier |
| Quick-visit clinic days | 10% of providers | 1 to 4 days, 10 to 32 extra visits each. Complexity is drawn from U(t0 - 0.8, t1 - 0.05), giving 99211 and 99212. Distinct panel members within the day while possible. | honest spike days |
| Batched service dates | 5% of providers | 1 to 3 batch days. Visits in the 8 weekdays before a batch day take its date with probability 0.6, at one claim per member and date. 50% of the paid ones are later replaced by a frequency-7 correction carrying the true date. The note keeps the true date. | a spike day of real visits; a claim-to-note date mismatch; corrections |

## c. Suspicious volume that overlaps the honest tail (issue 197)
| Mechanism | Kind in `fraud_claims` | Data 4.2 | Data 4.3 default |
|---|---|---|---|
| Ghost panel | not_rendered | 3% of providers, 4% to 15% of volume, ghosts 8% of panel | 2.5%, 3% to 10% of volume, ghosts 15% of panel (less concentrated) |
| Spike days | impossible_days | 1.5%, 2 to 6 days, 32 to 50 extra visits | 2%, 3 to 10 days, 8 to 26 extra visits on top of the day's real load |
| Padded days (new family) | not_rendered | none | 2.5%, 20 to 70 clinic days, 1 to 4 extra visits each on distinct panel members covering that date and not already seen that day |
| Unbundling | (dollars only) | 2%, 15% to 50% of visits | unchanged |

Phantom claims are billed at the justified level of an imagined complexity and are always paid, as in data 4.2. All three phantom kinds are drawn independently of the level rate and of each other.

**Overlap measured** on six development builds (seeds 1003, 1044, 1085, 1126, 1167, 1208; 216 providers; built in temporary folders by `generate_v2.build`, not registered as runs). For each seed: the busiest day of the spike-days providers, against the busiest day among honest providers with a legitimate-volume flag and among plain honest providers.

| Seed | Spike-day providers' busiest day | Legitimate-volume providers, top 5 | Plain providers, max |
|---|---|---|---|
| 1003 | 25 | 31, 33, 36, 38, 41 | 22 |
| 1044 | 20, 24, 24, 25, 26, 27, 28 | 31, 31, 33, 46, 79 | 22 |
| 1085 | 18, 20, 23, 24, 27, 29, 30 | 33, 33, 34, 37, 37 | 21 |
| 1126 | 20, 22, 26, 26, 27, 27 | 33, 34, 41, 46, 61 | 22 |
| 1167 | 20, 25, 28, 29 | 31, 32, 33, 33, 60 | 21 |
| 1208 | 22, 24, 28, 28, 28, 33 | 34, 36, 39, 42, 42 | 19 |

Under data 4.2 the busiest honest day was at most about 25 and every spike-day provider was at 34 or more. Under data 4.3 the spike-day providers sit inside the honest range, and several honest providers are busier than any of them. A fixed visits-per-day threshold of 30 (workflow v4.2's lane) now flags mostly honest providers and misses most spike-day providers. Padded days barely move the busiest day at all; they show only in volume per member, the panel and charts.

Phantom claims per dataset on these seeds: 920 to 2,667 (ghost panel 37 to 172, spike days 144 to 913, padded days 474 to 1,607). Batched claims: 61 to 185. Legitimate-volume flags per dataset: shared NPI 16 to 27, coverage 10 to 17 pairs, short week 28 to 38, quick days 17 to 27, batching 4 to 11.

## d. Charts for visits that never happened (issues 220 and 201)
- `fabricate_prob` 0.5: a provider with any phantom mechanism produces charts. Each of its phantom claims has a chart with probability U(0.6, 1.0) (per provider). Of those, 40% become available only from the second answer (`available_from_round` 2); the first answer reports them as missing visits.
- The chart supports the bill: two of the three elements (a random one is left at its noisy reading) are raised to the billed level. When time is recorded, the minutes fall in the billed level's band.
- Tells, none of them certain:
  - created_ts is 30 to 270 days after the service date for half of them;
  - pasted-text events go up by 0 to 5;
  - addenda are more likely (25%);
  - when the chart arrives on a second answer, 70% are signed on the request date.
- Honest charts also have late signatures (4%), addenda (3%) and signatures added on request.
- Measured on the six seeds: 5 to 13 fabricating providers per dataset, and 312 to 846 claims with a fabricated chart.
- Office 4.3 drops these claims from its "no record" set. Office 4.2 still reports NO_RECORD for them; the control sample (`records.py`) skips every never-rendered claim either way.
- Recovery effect: a fabricated chart supports the billed level, so a chart sample recovers nothing from it, and NO_RECORD (score 4.2's records-not-provided rule) is never triggered. Phantom dollars stay in `true_overpay_fwa` and the oracle can still count them.

## e. Claims-based confounders (issue 197)
- Diagnosis inflation: 30% of systematic or opportunistic providers and 2% of others. Each adds 1 (60%) or 2 chronic codes the member does not have, weighted to risk-heavy conditions (heart failure, COPD, CKD, diabetes), on U(0.3, 0.7) of their claims. This raises the derived risk score of their patients across every provider those patients see.
- Sparse coding: 12% of the remaining providers list only 1 or 2 of the member's chronic codes, plus the acute code. This lowers the derived risk of their panels, so an honest provider looks like it bills high for a healthy panel.
- Measured: inflated 1 to 9, sparse 20 to 32 per dataset.

## f. Chart variability (issue 220)
All of this is post-processing on stream 51. The note text is written first, from the elements before any change.

| Mechanism | Share | What changes |
|---|---|---|
| Contradiction | 8% of visits | One element moves ±1 (75%) or ±2. The note text is unchanged, so the structured level disagrees with the note. |
| Missing element | 3% | One element reads 0 (left blank in the EHR). |
| Rounded time | 35% of recorded times | Rounded to 5 minutes, or to 15 minutes (30% of those). Note text and minutes are changed together. |
| Ranged time | 8% of recorded times | The note says "approximately A to B minutes" (a 10-minute range). The structured minutes are blank and `time_statement` is `range`. |
| Stale copied-forward problem | 10% of repeat patients | `problems_addressed` gains a code from the patient's previous claim with this provider that is not on this claim. |
| Template boilerplate | 50% of notes of honest template users | A boilerplate sentence, and the risk element +1. |
| Late signature | 4% of signed notes | Signed 8 to 44 days after the visit. |
| Addendum | 3% honest, 10% habit, 25% fabricated | `amended` 1, amended 5 to 84 days after the visit; addendum sentence; last edit moved. |

## g. Office 4.3 (issue 201)
- **Plan file `records/office_chart_plan.csv`.** It is written for every claim whose settings differ from office 4.2 (with case-dependent coder noise, nearly all of them).
  - `available_from_round`: 0 = never, 1 = normal, 2 = only after a second ask.
  - `coder_disagreement`: 0.05 + 0.28 x exp(-gap / 0.6) + 0.05 if the note is thin (no time and at most one problem) + 0.10 if the chart contradicts its note, capped at 0.45. The gap is the distance of the visit's complexity to the nearest level threshold. The mean measured on the six seeds is 0.158 to 0.160, against office 4.2's flat 0.15, so borderline and thin charts are read less reliably at about the same average.
  - `signs_on_request`: unsigned notes signed when the request arrives. 30% honest, 45% habit, 70% of fabricated charts that arrive late.
  - `release_levels`: the levels a held-back note shows when it comes back. 10% honest, 50% habit, 60% fabricated. With probability 0.7 every element is raised to the billed level, otherwise only the risk element.
- **The request date** is the last service date in the claims plus 60 days, plus the provider's elapsed days, plus 0 to 5 days. A signature added on request carries that date.
- **Profiles `records/office_profiles.csv`.**
  - Each billing entity draws a behaviour: cooperative 0.55, slow 0.15 (+0.10 for groups of 4 or more), sloppy 0.20, evasive 0.10.
  - An honest clinician takes the entity's behaviour with probability 0.7, else draws its own from the base mix.
  - A provider with phantom claims that does not fabricate draws from evasive 0.30, slow 0.25, sloppy 0.20, cooperative 0.25. One that fabricates draws from cooperative 0.45, slow 0.35, sloppy 0.15, evasive 0.05. A systematic or opportunistic provider draws from cooperative 0.45, slow 0.15, sloppy 0.25, evasive 0.15. Each takes the entity's behaviour with probability 0.35.
  - So non-response is mildly linked to non-fabricating fraud, and fabricators look cooperative but slow.
  - Measured behaviour counts per dataset: cooperative 78 to 123, slow 36 to 69, sloppy 30 to 72, evasive 18 to 25.
- **Response tables** (`FIRST`, `LATER`, `DAYS`) are office 2.1's, unchanged. Not done: the check against public records-request response data (issue 201).
- **The lane** (`src/fwa_lane.py`) hard-codes office 4.2. On data 4.3 it therefore sees NO_RECORD for fabricated claims too, which is unrealistic. The data card says so, without the reason.

## h. Held-out families
`FAMILIES` in the generator maps each family to the options that switch it off; `holdout_families` applies them after the defaults and the explicit options. No family is held out by default. Suggested for a held-out test (a decision for the release plan, not made here): `padded_days` (a fraud shape with no spike) or `fabricated_charts` (the office answers with a chart instead of "no record").

## i. Checks done (no performance numbers)
- Level truth from the view on rendered claims equals the key's `true_overpay_level_net` for every provider on the six seeds (0 mismatches).
- The data-quality pre-flight returns ok on every check on the six seeds.
- A 216-provider build takes about 15 to 45 seconds.
- Smoke test: seeds 1003 and 1044 were built with `eval/make_d43_dev.py`. The H28 workflow spec ran on office 4.3 (`make_v2_office_workflow_runs.run(..., office_version="4.3")`) and `eval/score_42.seed_result` read both runs. The run folders were deleted afterwards and no score was recorded.
- Other measured facts: providers at 15% net or more per dataset: 3 to 8. Share of view claims with a test line: 0.29 to 0.34.

## What is still easier by construction
- The level truth and the chart elements come from one continuous complexity.
- Fabricated charts raise exactly two elements to the billed level.
- The legitimate mechanisms are independent of each other and of fraud. A real fraud ring may also run a short clinic week.
- Coder disagreement is symmetric (±1).
- The office tables are not sourced.
- Phantom claims never have a denial.
