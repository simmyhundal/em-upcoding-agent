# r2_2121

v2 data (2.2), code only (no AI step). release 2 evaluation (issue 90): seed 2121, 216 doctors, 8 planted upcoders, half clone notes, data 2.2 defaults.

- Screen: `flagged.csv` (top 25 by combined rank) and `flagged_threshold.csv` (suspicion at or above 5, at most 25); 2 providers flagged by the threshold.
- Records request for those providers plus a 30-provider control sample: 36 of 60 requested charts for the flagged providers came back in time (`documentation.csv`, `records_requests.csv`).
- Rules baselines on that evidence: `rules_documented_below_billed.csv` (documented level below billed in more than 15% of returned charts) and `rules_data_without_tests.csv` (note claims moderate-or-higher data reviewed but the claim has no lab or test line, more than 12%); at least 8 returned charts.
- Rule thresholds were chosen by looking at seed 42 and frozen before the other seeds were generated.
- Nothing here is an AI result. Answer key: `eval/answer_key/ground_truth_v2_r2_2121.json` (gitignored).
