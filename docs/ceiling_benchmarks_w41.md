# Ceiling benchmarks for W4.1: what can a chart-based arm recover, and at what cost?

[Back to the README](../README.md) · [score 4.0 (S4.0)](score_40.md) · [data 4.0 (D4.0)](data_v4_0.md) · [the older ceiling test (#117)](ceiling_v4.md) · [the v4.1 loop](w_loop_v41.md), [confirmations](w_loop_v41_confirm.md)

**Versions this page is about:** score **S4.0** (records copy fee $90 per round; S4.1's $0 copy fee would lower every cost column, see [score_41.md](score_41.md)) · data **D4.0** (development batches 5 to 10: 60 seeds, 480 planted upcoders, none used to tune anything in this page) · arms **W4.0** (H8, frozen workflow v4.0) and the **W4.1 candidate H23** (H22 with a 4-provider list; [w_loop_v41_confirm.md](w_loop_v41_confirm.md)). Free: no model calls. Code: `eval/ceiling_benchmarks_41.py`, `eval/near_miss_charts_41.py`. Written 2026-10-22; closes the question behind issues #133 and #134.

## 1. How much did the upcoders really overbill?

True net overpayment per upcoder-year (answer key; 545 claims per upcoder on average):

| Habit | Upcoders | Mean | Median | Upcoded visits | Per upcoded visit | 99214 and 99215 visits unsupported | Chart audit finds, as a share of true | 30-chart bound, as a share of true |
|---|---|---|---|---|---|---|---|---|
| All | 480 | $4,524 | $2,660 | 154 of 545 | $31 | 33% | 50% | 16% |
| Systematic | 180 | $4,343 | $2,509 | 156 of 552 | $29 | 29% | 58% | 23% |
| Opportunistic | 180 | $4,306 | $2,669 | 143 of 513 | $32 | 35% | **26%** | **5%** |
| Template-driven | 120 | $5,121 | $2,732 | 169 of 584 | $32 | 36% | 69% | 21% |

Opportunistic upcoders overbill about as much as the others, but their documentation is padded, so about 70% of their upcoded visits read as supported on the chart. "Chart audit finds" means reading every chart at its documented level (`records_universe.csv`), S4.0 prices, netting on.

## 2. Benchmarks with the cost side (totals over the 60 seeds)

| Row | Recovery | Cost side | Net | Net per seed |
|---|---|---|---|---|
| True net overpayment (answer key) | $2,171,434 | n/a | n/a | n/a |
| Full chart audit, every chart read | $1,075,262 | $2,251,737 | −$1,176,475 | −$19,608 |
| Ask and demand all 480 upcoders, 30 charts | $347,272 | $357,471 | −$10,199 | −$170 |
| … 60 charts | $495,555 | $481,387 | +$14,167 | +$236 |
| … 90 charts | $587,864 | $605,304 | −$17,439 | −$291 |
| … 150 charts | $674,272 | $853,136 | −$178,864 | −$2,981 |
| Oracle, only the 138 worth pursuing, 30 charts | $271,097 | $102,773 | $168,324 | $2,805 |
| Oracle, only the 150 worth pursuing, 60 charts | $386,953 | $150,434 | $236,519 | $3,942 |
| Oracle, only the 134 worth pursuing, 90 charts | $438,381 | $168,981 | $269,400 | $4,490 |
| Oracle, only the 99 worth pursuing, 150 charts | $415,858 | $175,959 | $239,898 | $3,998 |
| **W4.0 (H8), actual** | $125,722 | $100,178 | $25,544 | $426 |
| **W4.1 candidate (H23), actual** | $163,385 | $97,175 | $66,210 | $1,103 |

Unit costs (S4.0): $8.61 per chart reviewed, $105.46 per request round (admin plus the $90 copy fee), $275.66 per demand. "Recovery" is the expected 90% lower bound of a random sample of n charts (6 seeded draws per upcoder), extrapolated under S4.0's rules (15% error gate, netting). The "cost side" of the actual arms includes triage and abrasion.

Reading it:
- **Asking every upcoder is break-even at best.** The mean lower bound per upcoder is $723, $1,032, $1,225 and $1,405 at 30, 60, 90 and 150 charts, against a cost of $745, $1,003, $1,261 and $1,777.
- **Reading every chart is far under water**: about $2.25 million of review cost to find $1.08 million.
- **Profit comes from selection.** An oracle that pursues only the upcoders whose expected bound beats their cost nets $2,805 to $4,490 per seed, best at 90 charts. The oracle knows which upcoders those are from the answer key, so it is an upper bound; it also leaves out triage and the requirement that the rules call each provider.
- **W4.0 and the H23 candidate** are at $426 and $1,103 per seed. H23 cut cost by about $3,000 over the 60 seeds and recovered about $38,000 more.
- Of the true $2.17 million, a full audit could find $1.08 million (50%), a 30-chart sample's bound about $347,000 (16%), and H23 recovered $163,000 (7.5%).

## 3. Would extra charts turn withdrawn near-misses into demands?

Workflow v4.0 on the same 60 seeds: 138 asked upcoders had a random sample; 43 were demanded; 33 more were called by the rules but withdrawn by the demand floor (30 of those had a point estimate above the $276 demand cost). From each sample's variance:

- Charts needed for the bound to just clear the cost: median **51** in total (about 21 more than the 30 drawn); 57% need 60 or fewer, 73% need 90 or fewer, 93% need 300 or fewer.
- Extending all 30 withdrawn near-misses to n charts (extra charts plus one more round, minus the demand cost when the bound clears it):

| Total charts | Demands gained | Net over 60 seeds | Per seed |
|---|---|---|---|
| 60 | 17 | $3,065 | $51 |
| 90 | 22 | $6,065 | $101 |
| 150 | 26 | $3,037 | $51 |
| 300 | 28 | −$20,068 | −$334 |

About $100 per seed at best, before regression to the mean (the extension is picked on a high point estimate, so a new sample's estimate comes out lower). H16 in the loop, which does this, scored +$34 per seed on batches 7 to 10. Another 37 asked upcoders were not called by the rules at all (26 systematic, 7 template-driven, 4 opportunistic); extending them would help only if the rules also called them, so the net values for that group in `eval/near_miss_charts_41.py` are upper bounds.

## 4. What this means

- **#133 (recovery per demand):** closed. H23 raised total recovery ($2,095 to $2,723 per seed) through more demands, but recovery per demand fell ($2,924 to $2,593). The sample-size lever left is worth about $100 per seed.
- **#134 (opportunistic habit):** closed. By chart review they are mostly out of reach: a full audit finds 26% of their true overpayment, and 3 of 180 were demanded under H23. A signal other than the chart test would be needed.
- The lever with room is choosing which providers to pursue and with how many charts, not more charts everywhere.

## Caveats
- All numbers are development seeds under S4.0 prices; the answer key defines "true". The $8.61 per chart (15 minutes of a coder at a BLS wage proxy times 1.4) and the other staff-time numbers are assumptions ([score_40.md](score_40.md)).
- The full-audit cost uses the mean of 545 claims per upcoder, not each provider's own count.
- Dollars are Medicare-sized per provider ([issue 145](https://github.com/simmyhundal/em-upcoding-agent/issues/145)), so the benchmarks scale with that assumption.
- The oracle and the near-miss net values are optimistic upper bounds, as stated above.
