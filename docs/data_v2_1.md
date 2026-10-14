# Data v2.1 (draft): the note package a records request returns

**Status: generator and checks built (issue 57); not yet wired into the workflow or the agent.** Data v2.0 (`docs/v2_schemas.md`) stays frozen; v2.1 is a separate generator version with fresh seeds, so old and new results are never mixed.

## Why a note, and why more than three numbers
In v2.0 the "chart" for a visit is three MDM element levels and a minutes figure. A real response to a records request is a **note package**: the visit note, who signed it and when, the orders and results the note refers to, and any outside records. The reviewer's first job is to confirm that the claim's facts are real and consistent with the note (the right patient, provider and date; the problems and tests the claim shows). Only then do they score the level. Cloned or inflated notes are caught by comparing the note with the claim and with other notes, not by the level alone. So v2.1 includes an EHR note as text, so there is something to confirm the claim against, plus structured fields so the truth stays checkable.

What a plan gets back has to follow what a Medicare-style request asks for (Medicare contractor ADR guidance: the note for the date of service, orders and results, signature log or attestation): the note for the date of service, orders and results, and a signature log or attestation where a signature is missing. The EHR audit trail is **not** part of a standard request; it is a second, specific request, so it costs an extra round.

## Tables (the hidden "records universe"; the plan only sees what a request returns)
### `records/visit_notes.csv` (one row per visit)
| Field | Notes |
|---|---|
| `note_id`, `claim_id` | `claim_id` is the visit id used in the detector view |
| `member_id`, `rendering_npi`, `service_date` | must match the claim; a mismatch is a finding |
| `note_text` | short templated text: reason for visit, history line, exam line, assessment and plan lines naming the problems, a time statement if any |
| `problems_addressed` | ICD-10 codes the assessment and plan address (semicolon-separated) |
| `problems_level`, `data_level`, `risk_level` | the three MDM elements, 0 to 4, as in v2.0 |
| `documented_minutes`, `time_statement` | minutes (blank if none) and wording type: `total`, `face_to_face` or `none` |
| `outside_records_reviewed`, `independent_historian` | data-element flags |

### `records/note_authentication.csv` (one row per note)
`note_id`, `status` (signed, e_signed, unsigned, illegible), `signed_by_npi`, `signed_date`, `method` (handwritten or electronic), `signature_text` (the "electronically signed by" line), `amended` and `amended_date`. Late signatures (signed well after the service date) and edits after the request date are generated at tunable rates for honest and cloning providers alike.

### `records/note_orders.csv` and `records/note_results.csv`
Orders the note lists (`order_id`, `note_id`, type: lab, imaging, referral or prescription; code; `ordered_date`; `ordered_by_npi`; `signed`) and whether a result is attached for the date (`result_present`, `result_date`). Claim-side lab lines (v2.0 `claim_lines.csv`) are the other half of the comparison.

### `records/audit_trail.csv` (second-tier request only)
`note_id`, `created_ts`, `last_edited_ts`, `edit_count`, `copy_paste_events`, `template_id`. Returned only if the plan sends a follow-up asking for it, which costs a round and may be refused or slow.

### Answer key additions (eval only)
Which providers clone, which visits are cloned, and the visit each cloned note was copied from.

## What a reviewer (or the workflow, or the agent) can check
| Check | Compares | Confirms |
|---|---|---|
| Existence and identity | note against claim (member, provider, date) | the visit happened and the note belongs to the claim |
| Problems | `problems_addressed` against the claim's diagnoses | the problems level is supported by what was billed |
| Data reviewed | orders and results against claim lab lines and the claimed data level | the data element is real |
| Authentication | signature status, signed date against service date, edits after the request | the note is the provider's, written when the visit happened |
| Time statements | wording and minutes across a provider's notes, and one provider's total minutes in a day | the time claim is plausible |
| Text similarity | note text against the patient's previous note and the provider's other notes | copy-forward or template reuse |
| Audit trail (optional) | created and edited times, paste events | bulk creation or after-the-fact writing |

## Generator rules
- Honest notes are written from the visit's facts with natural variation. Honest providers also copy forward and use templates at a **baseline rate**, so similarity alone is not a trivial tell.
- A cloning provider's note for an upgraded visit reuses their template or an earlier high-level note with small edits, claims the inflated MDM elements and time, and does **not** gain the orders, results or diagnoses the claim lacks.
- Every signal is a parameter: `clone_signal_strength` (how many of the signals above appear), the honest baselines, the late-signature and unsigned rates, and the rate at which requests return an audit trail. Test with strong, weak and absent signals; a detector that only works when the signals are strong has not shown much.
- Out of scope for 2.1: phantom visits (a claim with no real visit behind it). The note package supports that scenario (no note, wrong patient or provider, wrong date) and it can be added later as another upcoding-adjacent fraud type.

## Office responses
New deficiency codes for the provider-office simulator: `MISSING_ORDERS`, `MISSING_RESULTS`, `LATE_SIGNATURE`, `AUDIT_TRAIL_REFUSED`. Existing ones (`MISSING_SIGNATURE`, `WRONG_DATES`, `ILLEGIBLE`, ...) stay.

## Decisions (made with the user)
1. **Templated note text is included** (structured fields stay the truth), so similarity checks are real.
2. **The audit trail is a second-tier request**: a follow-up that costs a round and can be refused or slow.
3. **Phantom visits stay out of 2.1.** The note package supports them for a later version.

## Built so far (issue 57)
- `src/generate_v2.py --data-version 2.1` (and `src/notes_v21.py`) writes the note package; claims and the records universe are byte-identical to data v2.0 for the same seed and settings. `--clone-signal-strength` sets how often each clone signal appears. The answer key records which visits were cloned and which honest providers use fixed templates.
- `src/note_checks.py`: claim-versus-note checks per visit and per provider (problems, data reviewed, signatures, late signatures, repeated time statements, near-duplicate notes, and with the audit trail bulk creation and paste-heavy notes).
- `eval/note_signal_analysis.py` -> [note_signals.md](note_signals.md): how well each signal separates cloners on the development seed (free, no model).
- Not yet done: the provider office returning note packages and the new deficiency codes, the workflow rules and agent tool using the checks, and the evaluation on fresh seeds.
