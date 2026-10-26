# What each data version contains: files, fields and how they changed

[Back to the README](../README.md) · [versions](versioning.md) · [data model of 2.0](v2_schemas.md) · [data 2.1](data_v2_1.md) · [data 2.2](data_v2_2.md) · [data 4.0](data_v4_0.md) · [data 4.2](data_v4_2.md)

**What this page is.** For a reader who wants the data in detail: which files and fields a payer holds in each data version, which of them the provider sends (the 837P claim and the chart returned on a records request), and how each version changed the data from the one before. Everything is synthetic. The shapes follow general knowledge of 837P, 835 and 834 files, not a spec. Field lists were read from datasets built with each version's generator (`src/generate_synthetic.py` for data 1, `src/generate_v2.py --data-version V` for the others).

## Who sends what
| File | Real-world equivalent | Sent by | When |
|---|---|---|---|
| `claims_header.csv`, `claim_lines.csv` | 837P professional claim (header and service lines) | the provider | with every claim |
| a chart (rows returned for a requested claim) | the visit note and documentation | the provider | only when the payer asks for records |
| second-tier audit trail | the record system's edit log for a note | the provider | only on a second request, and it may be refused |
| `remittance.csv` | 835 payment advice | the payer | at payment |
| `members.csv` | 834 eligibility | the payer | held |
| `providers.csv`, `reference/*` | provider directory, fee schedule, place-of-service and peer-group tables | the payer | held |
| `records/records_universe.csv`, `records/unrendered_claims.csv`, the answer key | the simulator's truth | nobody: simulator only, never shown to an arm | |

## The 837P claim (provider to payer)
| File | Field | Meaning | Since |
|---|---|---|---|
| `claims_header.csv` | `claim_id` | claim key | 2.0 |
| | `member_id` | the patient (links to `members.csv`) | 2.0 |
| | `billing_npi` | who bills (a group's organizational number in group billing) | 2.0 |
| | `rendering_npi` | the clinician who saw the patient; blank on some claims | 2.0 (always equal to billing before 2.2; differs and can be blank from 2.2) |
| | `claim_frequency` | 1 original, 7 replacement, 8 void | 2.0 |
| | `original_claim_id` | the claim a replacement or void refers to | 2.0 |
| | `service_date` | date of the visit | 2.0 |
| | `dx1` to `dx6` | diagnosis codes in position order | 2.0 |
| `claim_lines.csv` | `claim_id`, `line_no` | line key | 2.0 |
| | `cpt` | procedure code: the E/M level (99211 to 99215) or a test or procedure | 2.0 |
| | `modifiers` | for example 25 (separately identifiable E/M) | 2.0 |
| | `units`, `place_of_service`, `dx_pointer` | units, setting, which diagnosis the line points to | 2.0 |
| | `billed_amount`, `allowed_amount`, `paid_amount` | charge, fee-schedule allowed amount, amount the plan paid (plan-side adjudication stored on the line) | 2.0 |
| `claims.csv` (data 1 only) | `claim_id`, `provider_id`, `patient_id`, `service_date`, `cpt`, `place_of_service`, `diagnosis_codes` | one flat table, one code per claim | 1 only |

## The chart (provider to payer, on request)
| Field | Meaning | Since |
|---|---|---|
| `documented_problems_level`, `documented_data_level`, `documented_risk_level` | the three medical decision-making elements (the second highest sets the level) | 2.0 |
| `documented_mdm_level` | the level a coder reads from them (minimal to high; 15% of reads disagree by one level) | 2.0 (data 1 hands over the level and minutes directly, up front) |
| `documented_minutes` | total time on the date of the visit, when recorded | 2.0 |
| `note_id`, `note_text` | the note, templated text | 2.1 |
| `problems_addressed`, `time_statement`, `outside_records_reviewed` | what the note says about problems, time and outside records | 2.1 |
| `auth_status`, `signed_date` | signed, unsigned, illegible or attested; when | 2.1 |
| `order_count`, `results_present` | orders in the note and how many results came back | 2.1 |
| `created_ts`, `last_edited_ts`, `copy_paste_events`, `template_id` | the audit trail (second request only) | 2.1 |
| no chart | a visit that never happened returns "no record" instead of a chart | 4.2 |

The chart's fields reach an arm as rows of `documentation.csv`; the claims reach it as a derived view (`claims.csv` with `provider_id`, `patient_id`, `has_test_line` and the allowed and paid amounts; `patients.csv` with derived conditions and `risk_score`), built from the 837P and 834 files by `src/derive.py`.

## The payer's own files
| File | Fields | Since |
|---|---|---|
| `members.csv` | `member_id`, `birth_year`, `sex`, `coverage_start`, `coverage_end`, `product_line`, `pcp_npi` | 2.0 |
| `remittance.csv` | `claim_id`, `status` (paid, denied, reversed), `paid_amount`, `adjustment_amount`, `denial_reason` | 2.0 |
| `providers.csv` | data 1: `provider_id`, `specialty`, `state`, `n_claims`, `n_patients`; from 2.0: `npi`, `taxonomy`, `specialty`, `state`, `zip3`, `group_tin`, `network_status` | 1, changed in 2.0 |
| `patients.csv` (data 1 only) | `patient_id`, `provider_id`, `age`, `chronic_condition_count`, `conditions` (stored, not derived) | 1 only |
| `reference/fee_schedule.csv`, `place_of_service.csv`, `specialty_peer_groups.csv` | codes, descriptions, peer groups | 2.0 |
| `control_totals.csv` | `service_month`, `claims`, `paid_usd` (what the payer expects to have received) | 2.2 |

## How each version changed the data from the one before
- **Data 1 to 2.0: the data model.** One flat claim table, a stored condition count and a documentation table handed to the detectors become plan-shaped tables (837P header and lines, 834 members, 835 remittance, a provider directory). Conditions are derived from claims. Charts exist only behind a records request, built from the three decision-making elements and time. Some upcoders clone notes (documented levels and time inflated to match the bill).
- **2.0 to 2.1: the note package.** Charts gain note text, signatures, orders and results and a second-tier audit trail; clone signs (text duplication, paste events, timestamps) are tunable. **The claims and the records universe are identical to 2.0 for the same seed.**
- **2.1 to 2.2: realism and defects.** Same columns, new behavior in the values: honest providers miscode in both directions (about 8% of visits), so an upcoder is billing above the honest baseline by a margin; group billing under an organizational number (billing and rendering numbers differ, the rendering number is sometimes blank); incident-to billing; optional diagnosis truncation; claims lag; replacement claims, some of which change the E/M level; optional injected defects (duplicate claims, orphan replacements, unknown members, blank rendering numbers). New file: `control_totals.csv`. With every option at zero a 2.2 build reproduces 2.1 byte for byte.
- **2.2 to 4.0: provider rates and habits.** Same columns. Exactly 8 upcoders per dataset, each with a net rate of 15% to 40% and one habit (systematic, opportunistic or template-driven); other providers' rates are centred on zero with noise in both directions; each visit has a continuous complexity, so a borderline visit can read either side of a level; fewer cloned notes (12.5% of upcoders); more patients seen by two or more providers (35%); one calendar year.
- **4.0 to 4.2: no planted upcoder, and fraud.** Same columns. No `role` in the answer key: every provider has a continuous true rate from one distribution (about 9 providers per dataset at 15% or more). Claims for visits that never happened (about 6 providers), days with 32 to 50 extra visits (about 3 providers) and unbundling (an extra separately paid line, modifier 25 on the E/M line; about 4 providers) are added to the claims. New simulator-only file: `records/unrendered_claims.csv`; office 4.2 answers "no record" for such a claim.

Planned: [data 4.3](https://github.com/simmyhundal/em-upcoding-agent/issues/197), a messier volume signal and larger datasets; calibration of habit shares, the lab line and the date range ([#137](https://github.com/simmyhundal/em-upcoding-agent/issues/137), [#144](https://github.com/simmyhundal/em-upcoding-agent/issues/144)).
