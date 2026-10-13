# Simulated provider office

`src/provider_sim.py` plays the physician's office in a records request, so the fixed workflow and the investigator agent have to read responses and decide what to do next. Everything is synthetic and every probability is an illustrative assumption.

## What the plan can do
- `send_request(provider, sample, deadline)`: sample is `{"kind": "random", "n": N}` or `{"kind": "targeted", "cpt": "99215", "n": N}` or `{"kind": "targeted", "claim_ids": [...]}`.
- `follow_up(provider, addressed_codes, deadline, claim_ids=None)`: name the deficiencies; optionally narrow the scope.
- `close_request(provider, reason)`: ends in `complete`, `partial` or `non_responsive`.
- Caps: 3 rounds per provider (the request plus two follow-ups) and 120 elapsed days per provider.

## What comes back (payer-visible only)
Status, short text, structured deficiencies (`MISSING_VISITS`, `WRONG_CONTENT`, `MISSING_SIGNATURE`, `WRONG_DATES`, `ILLEGIBLE`, `SCOPE_UNCLEAR`, `EXTENSION`, `OBJECTION`, `NO_RESPONSE`), the claim IDs whose charts are usable, days elapsed, rounds left and the sample kind. Charts that arrive unsigned, with wrong dates or illegible are held back until a follow-up fixes them (with some probability). A response that misses the deadline arrives on the next round.

## Hidden behavior
Each provider is cooperative, slow, sloppy or evasive (55%, 15%, 20%, 10%), drawn from a seed. The agent never sees it. It is independent of upcoder status by default; `correlation` (0 to 1) raises the chance that upcoders are evasive or sloppy, because a perfect "stalls means guilty" link would be easier by construction. Only the simulator reads the records universe; a test checks that the module never touches the answer key.

## Rules
- **Non-response is never evidence of upcoding.** A provider with no usable charts ends `non_responsive`, and the summary step treats too few charts as inconclusive (`summary_rules.rule_leaning`; tested).
- **Only a random sample supports extrapolation.** A targeted request (a chosen code or claim list) is labelled `targeted` and `pi_estimate` must not extrapolate from it. Check current Medicare program integrity guidance before wording that for real use.
- Text is templated; a model never writes the outcome.

## Baseline run (no AI)
`python eval/run_office_baseline.py RUN_ID CODE_RUN` applies the fixed policy (one random request for 30 charts, one follow-up for any deficiency, then close) to the providers the screen flagged, and counts burden on honest doctors from the answer key. Results: `experiments/261013_1_code` (seed 42) and `261013_2_code` (seed 101). Compare with the single-draw request used in the v2.0 runs.
