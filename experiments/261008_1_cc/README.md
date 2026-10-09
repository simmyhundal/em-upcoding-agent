# Experiment: in-session preview of case summaries (3 providers)

**What this is:** a quick look at what the case-summary step produces, before an API key was available. Claude wrote
three summaries by hand in a chat session, from the evidence packets and the same system prompt `src/case_summary.py`
uses. It is **not** an API run and **not** a scored sample.

- Providers: the three highest-ranked on the combined list (P0215, P0014, P0143), seed-42 synthetic data.
- Written from the packets only; the answer key was not opened until afterwards.
- `summaries.jsonl` - the summaries. `summaries_checked.jsonl` - after the citation guardrail (3/3 passed, 13/13 citations valid).

## Result against the answer key (checked afterwards)
| Provider | Leaning written | Actual role |
|---|---|---|
| P0215 | pattern consistent with upcoding | upcoder |
| P0014 | pattern consistent with high-acuity panel | hard negative (honest, sicker panel) |
| P0143 | pattern consistent with upcoding | upcoder |

All three leanings matched. P0014 is the useful one: it had the highest plain z-score in the whole set, and the summary still separated its sick panel from a billing pattern.

## Limits
- n = 3, and these are the top-ranked providers, which are the easier cases. This says nothing about the harder middle of the list.
- Not the Opus 5.5 API call: no schema-constrained output, no fixed effort setting, and the writer knew the project context.
- The packet gives the writer the complexity-by-complexity numbers, so the leaning is largely readable off the packet; a weaker or cold model may do worse.
- Do not treat this as ground truth or as the eval. The eval metrics are in `reports/eval_report.md`.

## Correction (added later)
The P0215 summary says the high-complexity examples "all three ... come from one patient". That was wrong: I had only
looked at the first three claims printed from the packet. The packet's high-complexity sample has 10 claims across
7 different patients. The leaning and the other numbers are unaffected, but that sentence overstated a concern.
Lesson: a summary is only as good as the part of the packet its writer actually read.
