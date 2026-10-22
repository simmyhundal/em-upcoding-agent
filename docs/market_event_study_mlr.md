# Do payer share prices fall when the medical loss ratio comes in worse? An exploratory event study

[Back to the README](../README.md)

Research note, 2026-10-21. First pass, free data only. Code: `eval/payer_event_study.py`. Per-event results: `experiments/payer_event_study.csv`. Nothing here uses the synthetic claims data. Nothing here is a finding about willingness to pay for our product.

## Bottom line

1. **Guidance moves the stock far more than the loss ratio does.** A cut or raise of the full-year adjusted EPS guidance midpoint goes with about 0.9 percentage points of abnormal return per 1% of revision on the release day (107 revisions, R-squared 0.22). The ratio, measured against the year-ago quarter, goes with about -0.2 points per percentage point (R-squared 0.02), and that is not clearly different from zero.
2. **The sign is what you would expect, the size is small.** Release-day abnormal return averaged -1.7% when the ratio rose by 3 points or more (27 events), -0.8% for a rise of 1 to 3 points (42), +0.6% when it was flat (60) and +0.7% when it fell by 1 point or more (31).
3. **The "cynic's hypothesis" (a higher ratio is later offset by repricing, so profits recover) is not supported by this first pass, and not rejected either.** After a rise of 1 point or more, the ratio four quarters later was lower in 47% of cases, but back near its pre-rise level in only 9 of 55. Next-year guidance was not higher than usual. The 250-day return was higher after rises, but that difference does not survive removing the pandemic base years and is mixed up with calendar time.
4. **The sample is biased in a way that matters.** The earnings-release exhibit could not be read for 56 of the 229 filings (32 of 33 Molina, 11 of 32 Elevance, 13 others). Nine of the 20 largest one-day moves are in that group. They are in the return statistics but not in the regressions.
5. **Everything is exploratory.** About 160 usable events, seven firms, no consensus, overlapping news. No causal claim.

## Question and method

**Question.** Do payer share prices fall when the medical loss ratio (MLR) comes in worse, or guidance is cut? Is there any sign that a higher MLR is later offset by repricing?

**Events.** Every 8-K filing with Item 2.02 (results of operations) from 2019-01 to 2026-10 for seven payers: UnitedHealth (UNH), Elevance (ELV), Cigna (CI), CVS Health (CVS), Humana (HUM), Centene (CNC) and Molina (MOH). That is 229 filings. Most are quarterly results. A few are pre-announcements or guidance withdrawals.

**Day 0.** The release day if the release came before the 9:30 open, otherwise the next trading day. The timing comes from, in order: the acceptance time in the EDGAR header (54 filings), the conference-call time in the release text (169 filings; for example "call at 8:30 a.m. Eastern time today"), and for six filings the converted time in the SEC submissions file. The 8-K is often accepted hours after the press release, so the acceptance time alone would have put about 120 pre-market releases on the next trading day. 195 events are pre-open and 34 are not. I checked this choice against prices: for the 122 filings where the text says pre-market but the 8-K was accepted after the open, the mean absolute abnormal return was 3.9% on the day I assigned (the filing day) and 1.7% on the next day; for the 30 Molina filings accepted after the close, 6.6% on the assigned next day and 1.1% on the filing day. This departs from the brief, which named the acceptance time as the rule, and the prices support the departure.

**Return.** Abnormal return = stock return minus beta times the return of the health care sector fund XLV. Beta is estimated by least squares on the 250 trading days ending 30 calendar days before the event (mean 1.07, firm means 0.91 to 1.16). The simple excess return over XLV is reported too. Windows are day 0, and days 0 to +1 (sum of daily abnormal returns). Units are percent.

**Fields read from each release** (Python regular expressions per firm, a field is dropped when unsure):
- MLR-type ratio for the quarter and the year-ago quarter: UNH medical costs over premiums from the income statement, cross-checked with the text; ELV benefit expense ratio; CI Cigna Healthcare medical care ratio; CVS medical benefit ratio (Health Care Benefits segment); HUM benefit ratio (Insurance segment from 2023, consolidated before); CNC health benefits ratio. The regressor is the change in percentage points.
- Adjusted EPS, this quarter and year-ago. The regressor is growth in percent, defined only when the year-ago value is positive, and winsorized at plus or minus 100.
- Full-year adjusted EPS guidance (low, high), and the revision of its midpoint against the last guidance for the same fiscal year in the list. A revision is left blank if a release in between is missing from our list, or if guidance was withdrawn in between (UNH, July 2025). The guidance form (range, point, "at least") is recorded; of 107 revisions, 55 are range to range, 38 "at least" to "at least", 8 point to point and 6 change form.
- The guided full-year MLR when stated (43 events). It is not used in any test.

**Regressions.** Abnormal return on each regressor alone and together, pooled and with firm fixed effects. Standard errors three ways: heteroskedasticity-robust (HC1), clustered by firm, clustered by calendar quarter (all payers report in the same weeks and share sector news). With six or seven firms, the firm-cluster errors are not reliable. The quarter clusters (about 30) are the better guide.

## Data and its limits

- **MLR is compared with the year-ago quarter, not with consensus.** Consensus MLR is paid data. Markets react to the ratio against what they expected, so this is a weak test of "worse MLR".
- **The release exhibit is missing for 56 of 229 filings.** The downloaded file is the EDGAR cover page, not the EX-99.1 press release. Missing: MOH 32 of 33 (all but one, and that one is not parsed), ELV 11 (2024-04-18, 2024-07-17, 2024-10-17, 2025-01-23, 2025-04-17, 2025-04-22, 2025-07-17 and four from 2026), UNH 3 (2026-04-21, 2026-07-16, 2026-10-13), CNC 4 (2019-01-07, 2020-01-13, 2024-07-23, 2026-04-28), CVS 3 (2022-01-11, 2023-01-09, 2024-01-05), CI 2 (2022-05-06, 2025-07-31), HUM 1 (2024-01-18). The accession numbers are in the `accession` column of the CSV where `release_text` is "no (cover page only)". No more data was downloaded.
- **What this does to the result.** The missing group holds many of the largest recent moves (Molina's 2024 to 2026 reactions, Elevance's July 2025 drop). 37% of all absolute day-0 movement is in events without a parsed MLR. Of the 20 largest absolute moves, 10 have an MLR change and 4 have a guidance revision. So the regressions describe the moves we can explain, and the biggest ones are less represented.
- **Events overlap.** EPS, guidance and the ratio arrive together. The ratio and EPS growth have a correlation of -0.59 in the common sample. Peer news also spills over: Centene withdrew guidance on 2025-07-01 and Molina fell 22.0% on 2025-07-02 against -1.0% for XLV, with no Molina release of its own that day.
- **The benchmark is a sector fund** that contains all seven payers (UNH alone is a large weight). It mutes payer-wide moves and cannot separate payer news from sector news.
- **Special periods.** The 2020 pandemic (29 events) and UnitedHealth 2025 (4 events) are shown separately. The 2021 quarters have a year-ago base from 2020, so ratio changes of +10 to +15 points are base effects, not cost shocks.
- **Cigna.** The four events reporting 2019 results (Express Scripts restructuring, no comparable year-ago base) are in the return statistics only. The Cigna ratio definition changed with the February 2022 release; each release is read against its own restated year-ago figure. Humana's year-ago figures were recast for the 2023 exit of employer group commercial business; the recast figure is used. Centene and Humana special items are excluded by using the adjusted EPS the firms report.
- **Cut-offs.** The 1-point spike threshold, the 250-day beta window and the 30-day gap were set in the brief. Dropping 2020 and 2021 as base years was added after I saw the 2021 base effects, so treat those rows as a robustness check I chose after the fact.

## Extraction error rate

I drew 30 releases at random with a fixed seed from the 165 events that parsed as quarterly results (5 each for UNH, ELV, CI, CVS, HUM, CNC; Molina has no text) and read the table or sentence behind every extracted value. I then read 12 more chosen because they looked risky (large revisions, 2025 and 2026 layouts). I also checked 22 guidance revisions automatically against the "previous" or "from" figure that the release itself states (CVS, HUM, ELV).

| field | values in the random 30 | wrong | missed |
|---|---|---|---|
| MLR, quarter and year-ago | 26 | 0 | 0 |
| adjusted EPS, quarter and year-ago | 30 | 0 | 0 |
| full-year EPS guidance | 27 | 0 | 3 |
| guidance revision (needs the earlier release too) | 16 | 0 | n/a |

- The 12 risky releases: no wrong value. The 22 automatic checks: all matched.
- This measures accuracy on parsed events. It does not measure what was missed: 56 cover pages, 4 Cigna 2019 events, and the Humana, Molina, CVS and Centene pre-announcements are outside it. The sample was also drawn after I had fixed problems found on the whole set, so it is a check of the final extractor, not an unbiased estimate of an untuned one.
- With no errors in 26 to 30 values, the 95% upper bound on the error rate is about 10% to 11% (17% for the 16 revisions). That is the honest reading of "clean".
- The 3 misses (CI 2019-05 and 2019-08, CNC 2025-10) were guidance wordings my first patterns did not catch. I added patterns and checked those three again. They are right now.
- Errors found and fixed while building, before the random sample: a footnote-label miss for UNH 2024-04; Humana guidance picking the quarter's EPS; Centene 2019 guidance picking the pre-split 2018 actual; basis-point wording misread for UNH 2024-07 and CNC 2026-02; dotted leaders in the UNH 2026 layout; guided-MLR picking a historical range for CVS (fixed; 12 of 12 checked guided values are now right).
- Molina has no extractor: 32 of its 33 files are cover pages and the other is not parsed.
- Counts of the 229 events: **clean MLR change 160, clean adjusted EPS growth 159, clean guidance revision 107.** Guidance level is clean for 160. By firm (MLR / EPS / revision): UNH 29 / 29 / 19, ELV 21 / 21 / 13, CI 24 / 24 / 14, CVS 26 / 31 / 22, HUM 30 / 27 / 21, CNC 30 / 27 / 18, MOH 0 / 0 / 0. Fewer revisions than levels because a revision needs the previous release for the same fiscal year, and the first guidance of a year (the Q4 release) has none.
- Seven prior-year MLR values are filled from the release a year earlier because the release does not state them (CI 2020 x3, HUM 2025-02, 2026-04, 2026-07, CNC 2026-02). They are marked in `mlr_method`.

## Results

### Descriptives

Day-0 abnormal return over all 227 events with prices: mean -0.48%, standard deviation 6.7%, mean absolute move 4.7%. Days 0 to +1: mean -0.48%, standard deviation 7.4%. The standard deviation of the MLR change is 3.6 points (range -13.7 to +14.9); of the guidance revision 2.6% (range -15.7 to +8.1).

Guidance revisions are mostly small raises: 69 raises (mean day-0 abnormal return +1.3%), 7 cuts (-6.8%), 31 unchanged (-0.2%).

### Table 1. Day 0, beta-adjusted, pooled (percent per unit of regressor)

| model | variable | coef | se HC1 | se firm | se quarter | n | R-squared |
|---|---|---|---|---|---|---|---|
| MLR only | MLR change (pp) | -0.202 | 0.131 | 0.147 | 0.139 | 160 | 0.017 |
| guidance only | guidance revision (%) | 0.931 | 0.258 | 0.267 | 0.273 | 107 | 0.224 |
| EPS only | EPS growth (%) | 0.009 | 0.014 | 0.017 | 0.016 | 159 | 0.004 |
| MLR + EPS | MLR change | -0.224 | 0.134 | 0.148 | 0.137 | 154 | 0.019 |
| | EPS growth | -0.002 | 0.015 | 0.018 | 0.017 | 154 | 0.019 |
| all three | MLR change | -0.204 | 0.140 | 0.124 | 0.169 | 103 | 0.251 |
| | guidance revision | 0.940 | 0.268 | 0.265 | 0.284 | 103 | 0.251 |
| | EPS growth | -0.026 | 0.019 | 0.026 | 0.020 | 103 | 0.251 |

### Table 2. Days 0 to +1, beta-adjusted, pooled

| model | variable | coef | se HC1 | se firm | se quarter | n | R-squared |
|---|---|---|---|---|---|---|---|
| MLR only | MLR change | -0.246 | 0.124 | 0.124 | 0.143 | 160 | 0.023 |
| guidance only | guidance revision | 1.006 | 0.316 | 0.315 | 0.316 | 107 | 0.206 |
| EPS only | EPS growth | 0.016 | 0.013 | 0.016 | 0.014 | 159 | 0.010 |
| all three | MLR change | -0.162 | 0.143 | 0.098 | 0.186 | 103 | 0.219 |
| | guidance revision | 0.995 | 0.328 | 0.320 | 0.334 | 103 | 0.219 |
| | EPS growth | -0.014 | 0.022 | 0.033 | 0.023 | 103 | 0.219 |

### Table 3. Sensitivity, day 0 (coefficient, with the quarter-cluster se in brackets)

| sample | MLR only (n) | guidance only (n) | all three: MLR / guidance / EPS (n) |
|---|---|---|---|
| all events, pooled | -0.20 (0.14) (160) | 0.93 (0.27) (107) | -0.20 (0.17) / 0.94 (0.28) / -0.03 (0.02) (103) |
| firm fixed effects | -0.20 (0.14) (160) | 0.93 (0.29) (107) | -0.21 (0.16) / 0.94 (0.29) / -0.03 (0.02) (103) |
| simple excess return over XLV | -0.21 (0.14) (160) | 0.93 (0.28) (107) | -0.20 (0.17) / 0.94 (0.29) / -0.02 (0.02) (103) |
| without UNH 2025 (4 events) | -0.19 (0.15) (156) | 0.70 (0.26) (105) | -0.23 (0.17) / 0.70 (0.27) / -0.03 (0.02) (101) |
| without 2020 (29 events) | -0.34 (0.16) (138) | 1.00 (0.27) (91) | -0.33 (0.17) / 0.97 (0.30) / -0.03 (0.03) (88) |
| without both | -0.34 (0.16) (134) | 0.77 (0.25) (89) | -0.39 (0.13) / 0.71 (0.28) / -0.03 (0.03) (86) |
| without results for fiscal 2020 and 2021 (base years) | -0.31 (0.36) (113) | 1.05 (0.28) (75) | -0.17 (0.32) / 1.11 (0.29) / -0.04 (0.03) (72) |
| guidance revisions with the same form only | | 0.98 (0.28) (103) | -0.20 (0.17) / 0.98 (0.29) / -0.02 (0.02) (99) |

Reading Tables 1 to 3:
- The guidance coefficient is stable around 0.7 to 1.0 and large next to its error in every cut. About 1% on the guidance midpoint goes with about 1% on the share price the same day. It leans on seven cuts (mean -6.8%); removing UNH 2025 lowers it to 0.70.
- The MLR coefficient is negative in every cut, -0.2 to -0.4 per point. One standard deviation of the ratio change (3.6 points) is then worth about -0.7% (-1.2% without 2020). Against a day-0 standard deviation of 5.5% for these events, that is small. It is within noise in most cuts and about two standard errors without calendar 2020. It is not close to significant (se 0.36) once all fiscal 2020 and 2021 results are dropped: the pandemic and base-year quarters, with ratio changes of 10 points or more, supply much of the variation in the ratio.
- Adding guidance leaves the MLR coefficient unchanged, so the two carry mostly separate information (correlation -0.18). EPS growth adds nothing once the other two are in, but it is strongly tied to the ratio (-0.59), so this does not say that EPS does not matter.
- Table 4 shows the same pattern without a straight-line assumption.

### Table 4. Day-0 abnormal return by MLR change

| MLR change versus year-ago | n | mean (%) | median (%) |
|---|---|---|---|
| fell by 1 point or more | 31 | +0.73 | +0.74 |
| within 1 point | 60 | +0.57 | +1.44 |
| rose 1 to 3 points | 42 | -0.80 | -0.78 |
| rose 3 points or more | 27 | -1.65 | -2.13 |

### Ten largest negative and positive day-0 abnormal returns (all 227 events with prices)

Blank cells mean the release text is not available (cover page only) or the field does not apply. "Flags" are keyword hits in the first part of the release text and are crude; the notes below say what I could read.

| firm | filing date | AR day 0 (%) | AR days 0-1 (%) | MLR change (pp) | guidance revision (%) | EPS growth (%) | what the release text shows |
|---|---|---|---|---|---|---|---|
| CNC | 2025-07-01 | -39.6 | -41.0 | | | | guidance withdrawn (pre-announcement; released after the close, so day 0 is 07-02) |
| MOH | 2026-02-05 | -27.6 | -29.8 | | | | text not available |
| UNH | 2025-04-17 | -21.7 | -25.5 | +0.5 | -11.8 | +4 | outlook cut; CEO quote "did not perform up to our expectations" |
| UNH | 2026-01-27 | -17.7 | -12.9 | +4.7 | | -69 | Q4 2025 results and 2026 outlook; guidance first issued, no revision |
| MOH | 2025-10-22 | -17.6 | -16.1 | | | | text not available |
| CI | 2025-10-30 | -17.6 | -18.6 | +2.0 | | +4 | outlook reaffirmed; the release also announces a rebate-free pharmacy benefit model, which may be what the market reacted to (not checked) |
| CVS | 2024-05-01 | -17.0 | -19.0 | +5.8 | -15.7 | -40 | guidance cut to at least $7.00 from $8.30; CEO commentary on Medicare Advantage |
| MOH | 2025-07-23 | -16.5 | -12.7 | | | | text not available |
| HUM | 2024-01-25 | -11.5 | -10.4 | +4.0 | | -100 | Q4 2023 loss; initial 2024 guidance of about $16.00 "assumes the higher Medicare Advantage medical costs persist" |
| ELV | 2025-07-17 | -11.1 | -18.9 | | | | text not available |
| MOH | 2024-10-23 | +18.3 | +19.4 | | | | text not available |
| CVS | 2025-02-12 | +15.1 | +19.6 | +6.3 | | -44 | Q4 2024 ratio 94.8% against 88.5%; the release gives 2025 guidance of $5.75 to $6.00, and without consensus I cannot say how that compared |
| MOH | 2026-04-22 | +14.3 | +16.2 | | | | text not available |
| CNC | 2026-04-28 | +13.7 | +23.3 | | | | text not available |
| CNC | 2025-10-29 | +13.6 | +7.2 | +3.5 | | -69 | ratio up 3.5 points, yet 2025 EPS forecast raised to at least $2.00 from $1.75 and segments "in line with expectations" |
| MOH | 2024-07-24 | +12.8 | +15.7 | | | | text not available |
| HUM | 2025-07-30 | +12.6 | +11.1 | +0.4 | +4.6 | -10 | 2025 adjusted EPS guidance raised to about $17.00 from $16.25 |
| CVS | 2024-11-06 | +11.2 | +3.1 | +9.5 | | -51 | third-quarter charges ($1.1 billion premium deficiency reserves) were already pre-announced on 2024-10-18, when the stock fell 5.8% |
| CNC | 2022-10-25 | +9.4 | +9.5 | +0.2 | +0.4 | +3 | fourth guidance raise of 2022 |
| MOH | 2020-02-10 | +8.5 | +11.4 | | | | text not available |

What this list says:
- 9 of the 20 moves are in events without release text (Molina is 7 of them, Elevance 1, Centene 1). A tenth, Centene 2025-07-01, is a pre-announcement without quarterly results.
- Several large rises happened with a much worse ratio against the year-ago quarter (CVS 2024-11 and 2025-02, CNC 2025-10). That is the pattern you would see if the market reacts to the ratio against expectation, not against last year. A pre-announced or telegraphed bad ratio is already in the price.
- The big falls come with guidance cuts, withdrawals or a weak outlook. None of the ten falls is explained by the year-ago change in the ratio alone.
- Other news on the same day (policy notices, peer releases, CEO changes outside the release text) is not visible here and was not checked.

### Cynic test (exploratory, small sample)

A "spike" is a quarter where the ratio rose by 1 point or more against the year-ago quarter: 69 events.

**(a) Did the same ratio fall back four quarters later?** 55 of the 69 spikes have a result four quarters later (matched by fiscal quarter).

| group | n with t+4 | mean change from t to t+4 (pp) | share that fell | share that fell by 1 point or more |
|---|---|---|---|---|
| spikes | 55 | -0.11 | 47% | 38% |
| spikes, without 2021 events (base 2020) | 43 | +0.33 | 40% | 28% |
| spikes, without 2020 and 2021 | 38 | +0.32 | 39% | 29% |
| other events, without 2020 and 2021 | 49 | +1.01 | 27% | 12% |

The table uses the ratio at t+4 minus the ratio at t, two numbers from different releases. A same-definition version uses the year-on-year change reported in the t+4 release itself (its year-ago value is the restated quarter-t ratio, which matters for Cigna 2022 and Humana 2023). It gives the same answer: -0.06 pp for all spikes (47% fell, 38% by 1 point or more), +0.32 pp without 2020 and 2021 (39% and 29%), against +1.00 pp for other events (27% and 12%).

The ratio four quarters after a spike was back within 0.5 point of its pre-spike level (or lower) in 9 of 55 cases; on average it was 3.5 points above the pre-spike level. Against other events, spikes drifted about 0.7 point lower (0.32 against 1.01), but any noisy ratio does that (mean reversion), and the ratio rose on average across the period. This is not a repricing signal.

**(b) Cumulative abnormal return from day +2 to day +250.**
- Spikes (n=60): mean +3.5%, median +5.2%. Other events with an MLR (n=83): mean -5.1%, median -3.2%.
- Regression on a spike dummy: +8.6 points (se 4.0 firm, 3.8 quarter, n=143). Without 2020 and 2021: +7.9 (se 6.0, 3.8, n=96). On the size of the change: +1.5 points per point of ratio (se 0.5, 0.7), or +2.8 without 2020 and 2021 (se 1.6, 1.2).
- But the spikes alone, without 2020 and 2021, averaged -0.9% (n=41). The gap comes from the other events doing badly (many of their windows cover the 2024 to 2025 sell-off). It is calendar time, not a recovery after a bad ratio. The 250-day windows of events from the same firm overlap heavily, so 143 events are far fewer independent observations. Nine spikes are too recent for a 250-day window.
- Reading: no sign of continued underperformance after a bad ratio; no robust sign of recovery either.

**(c) Did next year's guidance recover?** I compared the first guidance midpoint for the next fiscal year (usually the Q4 release) with the last guidance midpoint of the spike's year.

| group | n | mean change (%) | share above zero |
|---|---|---|---|
| spikes | 57 | +6.4 | 88% |
| other events | 85 | +4.7 | 89% |
| spikes, without 2020 and 2021 | 38 | +5.0 | 82% |
| other events, without 2020 and 2021 | 57 | +2.8 | 84% |

The 57 spikes are only 28 firm-fiscal-years, and the 85 other events 33 (19 and 24 without 2020 and 2021), because every event in a firm-year inherits the same next-year figure. Next-year guidance was higher in most cases whether or not the ratio had risen, so that alone is not evidence of repricing recovery. Exceptions after spikes: Humana (2023-11, -43%) and CVS (2023 and 2024, -3.5% and -10%). The spikes come from seven firms in a few episodes, so treat this as a description, not a test.

## What this does NOT show

- It does not show that a worse MLR, in general, lowers a share price. It shows that the change against the year-ago quarter has a weak negative link on the release day.
- It does not test "worse than expected". That needs consensus MLR and EPS (paid).
- It does not show cause. EPS, guidance, ratio, segment commentary and policy news arrive together, and the sector fund holds the payers themselves.
- It does not test repricing. The cynic's hypothesis is about premium rates and the ratio over several years; stock prices are an indirect and noisy view of that. Net of base effects, the ratio did not clearly fall back within four quarters.
- It does not cover the largest recent moves in full: Molina and Elevance 2024 to 2026 are mostly missing.
- Standard errors with six or seven firms are rough. About 30 quarter clusters are better, but a few quarters (2020, 2024, 2025) carry the largest moves. I ran several specifications and report all of them; with this many looks, one result at two standard errors is not strong.
- It says nothing about E/M coding or about willingness to pay for upcoding detection.

## Next steps

1. **Approve one fetch of the 56 missing exhibits** (list by accession in the CSV; Molina first, then Elevance 2024 to 2026, UNH 2026). Then re-run: the script is ready, Molina needs an extractor.
2. **Add consensus** (paid, or analyst notes read by hand for the 20 largest moves) to turn the year-ago change into a surprise.
3. **Intraday timing** for the 34 post-open or after-close events and the pre-announcements, and a check of same-day policy news (Medicare Advantage rate notices).
4. **Test the repricing story where it lives**: premium rate filings or reported premium yield against the ratio over two to three years, by firm. That is a better test of the cynic's hypothesis than returns.
5. **Wild cluster bootstrap** or quarter-level aggregation, and more payers (smaller plans) to widen the sample.

## Reproduce

```bash
D=<folder with earnings8k.json, rel/, sub/, prices/>
python3 -I eval/payer_event_study.py extract --data $D --out /tmp/payer_extract.csv
python3 eval/payer_event_study.py analyze --data $D --extract /tmp/payer_extract.csv --out experiments/payer_event_study.csv --report /tmp/payer_report.txt
```

The first stage reads the downloaded HTML and JSON, which are untrusted, with the standard library only (`-I`). The second stage needs numpy and reads the extract and the price files. `accept_et` in the CSV is the header time or the converted submissions time; it is not the release time, and `timing_src` says what decided day 0.
