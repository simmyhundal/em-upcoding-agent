# 261016_1_code

v2 data (2.2), code only (no AI step). data 2.2 default noise on development seed 42, 3.7% planted upcoders, half clone notes.

- Screen: `flagged.csv` (top 25 by combined rank) and `flagged_threshold.csv` (suspicion at or above 5, at most 25); 10 providers flagged by the threshold.
- Records request for those providers plus a 30-provider control sample: 184 of 300 requested charts for the flagged providers came back in time (`documentation.csv`, `records_requests.csv`).
- Rules baselines on that evidence: `rules_documented_below_billed.csv` (documented level below billed in more than 15% of returned charts) and `rules_data_without_tests.csv` (note claims moderate-or-higher data reviewed but the claim has no lab or test line, more than 12%); at least 8 returned charts.
- Rule thresholds were chosen by looking at seed 42 and frozen before the other seeds were generated.
- Nothing here is an AI result. Answer key: `eval/answer_key/ground_truth_v2_261016_1_code.json` (gitignored).
