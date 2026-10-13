# 261013_2_code

No AI. The frozen v2.0 workflow's fixed policy against the simulated provider office (`src/provider_sim.py`): for each provider the screen flagged in `experiments/261012_2_code/`, send a random request for 30 charts (30-day deadline), send one follow-up if the response had deficiencies, then close. Office behavior is drawn independently of upcoder status (correlation 0.0).

```
{
 "run": "261013_2_code",
 "screen_run": "261012_2_code",
 "correlation": 0.0,
 "providers_requested": 9,
 "end_states": {
  "complete": 5,
  "partial": 1,
  "non_responsive": 3
 },
 "mean_usable_charts": 19.333333333333332,
 "mean_rounds": 1.5555555555555556,
 "mean_days": 38.44444444444444,
 "requests_to_honest": 5,
 "rounds_on_honest": 8,
 "chart_rule_upcoders_found": 0,
 "chart_rule_honest_accused": 0
}
```

Compare with the single-draw request in `experiments/261012_2_code/` (about 18 usable charts per provider). Documentation is generated from the same hidden truth that defines an upcoded visit; the office behaviors and their probabilities are illustrative assumptions. Answer key: `eval/answer_key/ground_truth_v2_261012_2_code.json` (gitignored).
