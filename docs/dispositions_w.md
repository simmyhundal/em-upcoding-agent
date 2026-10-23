# Dispositions for the workflow (issue 66)

The agent must say what it did with every provider on its list (`set_aside`, agent v3.1 on). The workflow now has the same table. It is written after the run from what the payer sees. It is a post-hoc table, not a refusal gate: the workflow's code already decides every provider, and the table records what it decided and why.

Build it with `python3 eval/dispositions_w.py RID` (code in `eval/dispositions_w.py`, free, no model call). It reads the screen file, `office_transcript.jsonl`, `case_summaries_checked.jsonl` and `demand_floor.json` of the run folder, and the ask model in `src/policy_40.py`. It writes `experiments/<rid>/dispositions.csv`. It reads nothing from the answer key (`tests/test_dispositions.py` checks this).

One row per provider on the screen list. A run with a short list (`list_k`, H23) also gets a row for each provider beyond the short list, marked `not listed`. Columns: rank, screen score, ask decision (asked or skipped) and the reason, charts requested and usable, the rules leaning and its reason string, whether the demand floor withdrew a call (with the estimate and the cost), and the final disposition with its reason. The dispositions are `demanded`, `examined and set aside` and `not examined`.

## Example (run `wlh8_1616`, workflow v4.0 on development seed 1616)

| Rank | Ask decision and reason | Charts usable | Rules leaning | Disposition and reason |
|---|---|---|---|---|
| 3 | asked: ask model predicts net value $969, above the margin $0 | 30 of 30 | upcoding | examined and set aside: rules called upcoding (33% of 30 documented charts below the billed level, peer rate 11%); no demand, because the estimated recovery (lower bound $0) is below the staff cost of a demand ($276) |
| 4 | asked: ask model predicts net value $519, above the margin $0 | 30 of 30 | inconclusive | examined and set aside: documented 99215 claims are too few and the pooled result is not lopsided |
| 5 | skipped: ask model predicts net value -$63, not above the margin $0 | 0 of 0 | inconclusive | not examined: the ask model's predicted value of asking is below the margin |

## Share of listed providers with a stated reason

A listed provider has a stated reason when its row has a reason for the ask decision and, if it was asked, a rules reason string for the result. Stored runs only (no new runs). Development batches 5 and 6 are 20 seeds.

| Runs | Listed providers | With a stated reason | Demanded | Set aside | Not examined | Calls withdrawn by the floor |
|---|---|---|---|---|---|---|
| `wlh8_<seed>` (v4.0, batches 5 and 6) | 440 | 440 (100%) | 17 | 44 | 379 | 13 |
| `wlh22_<seed>` (H22, batches 5 and 6) | 440 | 440 (100%) | 26 | 35 | 379 | 13 |
| `wlh23_n4_<seed>` (H23, list of 4, batches 5 and 6) | 80 | 80 (100%) | 24 | 31 | 25 | 12 |
| `fr40_<seed>` (v4.0, fresh seeds 5555 to 6464) | 220 | 220 (100%) | 3 | 28 | 189 | 4 |

The ask decision is re-derived from the policy (ask model or first K) and matches the transcript for all 960 development rows and all 220 fresh rows.

## What 100% means

The share is 100% by construction. The workflow is rule-driven, so every provider already has a reason string. The table does not show that the reasons are good. It makes them visible in one place, with the ask model's value and the demand floor's estimate beside them. The agent's table is stricter: it refuses to submit without the reasons. The workflow's table does not stop a run.

The table is not a refusal gate and has no model-written text. Providers the ask model skipped carry the rules' "too few records" leaning only because the rules ran on an empty sample; the table shows the ask reason as the stated reason for those.
