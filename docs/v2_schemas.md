# v2 data model: what a payer actually has

Everything is synthetic. v2 replaces the v1 shortcut (provider, patient, claim and documentation tables handed to the detectors) with tables shaped like what a health plan holds. The shapes are written from general knowledge of 837P, 835 and 834 data, **not from a spec**: they are simplified and should be reviewed by someone who works with those files before anyone relies on the field names.

Regenerate with `python src/generate_v2.py data/synthetic_v2 --seed 42` (answer key goes to `eval/answer_key/ground_truth_v2.json`, outside the data folder).

## Tables the plan has
Files are in `data/synthetic_v2/`. "In a real plan this comes from" says where the equivalent lives.

### `members.csv` (eligibility; 834-style)
| Field | Type | Notes |
|---|---|---|
| `member_id` | string, key | |
| `birth_year` | int | the plan holds a full date of birth; the year is enough here |
| `sex` | F / M | |
| `coverage_start`, `coverage_end` | date | one coverage span per member here; real members can have several |
| `product_line` | string | one value here |
| `pcp_npi` | string | primary care attribution; may differ from who the member actually saw |

In a real plan this comes from the enrollment / eligibility warehouse. **There is no condition or risk field on a member**: conditions are derived from claims (see below).

### `providers.csv` (provider directory)
`npi` (key), `taxonomy` (207Q00000X, family medicine), `specialty`, `state`, `zip3` (location stand-in), `group_tin` (billing group; several providers share one), `network_status` (in / out). In a real plan this comes from the provider directory and credentialing system.

### `claims_header.csv` (837P header-style)
| Field | Notes |
|---|---|
| `claim_id` | key |
| `member_id`, `billing_npi`, `rendering_npi` | the doctor who saw the patient is `rendering_npi` |
| `claim_frequency` | 1 original, 7 replacement, 8 void |
| `original_claim_id` | set on replacements and voids; points to the claim being replaced or voided |
| `service_date` | |
| `dx1` ... `dx6` | ordered ICD-10 diagnosis positions (837P allows up to 12) |

### `claim_lines.csv` (837P service lines)
`claim_id`, `line_no` (key together), `cpt`, `modifiers` (semicolon-separated, up to 4), `units`, `place_of_service`, `dx_pointer`, `billed_amount`, `allowed_amount`, `paid_amount`. A visit has one E/M line (99211 to 99215) and sometimes a lab line (80053 or 85025).

### `remittance.csv` (835-style adjudication)
`claim_id`, `status` (paid / denied / reversed), `paid_amount`, `adjustment_amount`, `denial_reason`. About 3% of claims are denied; a voided claim reverses the claim it points to.

### `reference/`
`fee_schedule.csv` (CPT to allowed amount, from the CMS GA Family Practice averages in `data/baselines/`; lab prices are invented), `place_of_service.csv`, `specialty_peer_groups.csv`.

## What the plan does NOT have at screening time
### `records/records_universe.csv` (the medical record systems)
One row per visit: `claim_id`, `problems_level`, `data_level`, `risk_level` (the three MDM elements, 0 to 4), `documented_minutes` (blank when time was not recorded). **This file stands in for the charts sitting in physician offices.** Detectors and the AI never read it directly: `src/records.py` models a records *request* (sample size, response rate, late responses, coder disagreement) and writes only what came back to `documentation.csv` in the detector view.

Documented level = the level of the second-highest MDM element (two of three must meet a level) or the level the minutes support, **whichever is higher**. Cutoffs are illustrative; check current CPT and CMS guidance.

### Answer key (`eval/answer_key/ground_truth_v2.json`, eval only)
Provider roles, whether an upcoder clones its documentation, the justified CPT for every visit.

## Detector view (what the screen and the AI read)
`src/derive.py` collapses the plan tables into the v1 shapes the detectors already read (`providers.csv`, `patients.csv`, `claims.csv`) so v1 and v2 results are comparable. Rules:
- One row per **visit**: replacements supersede their original; voids and denied claims are dropped.
- A visit belongs to its **rendering** provider. Panel attribution (`pcp_npi`) is used only to describe a member's home provider.
- Conditions and the risk score are derived from diagnosis codes on all of a member's accepted claims, across every provider the member saw (see `docs/synthetic_data.md`).
- Documentation exists only for providers a records request covered.

## Known simplifications
- One coverage span, one product line, one specialty and state; no referrals, no specialist claims, no rejected-then-resubmitted churn beyond a few replacements and voids.
- Lab lines are the only non-E/M services; "data reviewed" is judged from them.
- The generator still draws the justified level first (from the CMS-calibrated ordered logit) and then builds MDM elements consistent with it, rather than deriving the level from visit facts. Deriving it the other way round would need recalibration to the CMS mix.
