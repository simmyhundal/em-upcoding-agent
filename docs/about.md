# About this project

[Back to the README](../README.md)



## Built responsibly
- **Synthetic data only.** No real patients, providers or claims, and no real provider is ever flagged.
- **The AI advises; people decide.** Statistics choose who is reviewed. The AI sorts the flagged cases (upcoding, sicker patients, or unclear) as advice to a reviewer, and nothing happens to anyone without a person checking the records.
- **A guardrail on the AI.** Invented evidence is rejected automatically.
- **Honest reporting.** The reports state what is easier by construction, what is simulated, and where the data is thin.
- **Nothing here accuses anyone.** The recovery packet is draft material for human, compliance and legal review. It does not write demand letters or make findings.


## What this project demonstrates
- Framing an open-ended problem (fraud versus legitimate complexity) as something measurable.
- Designing and calibrating synthetic data against public Medicare statistics so a method can be graded against a known answer.
- Evaluation design and candid reporting: baselines, a ground-truth answer key kept apart from the tools, results tables with caveats, and a log of what went wrong (see the experiment READMEs).
- Putting an LLM in a pipeline with guardrails and tests, rather than trusting its output.
- Building for the downstream user: charts a reviewer can read, and a packet the recovery team can act on.
- Test-driven delivery: 7 test files, and work tracked as GitHub issues grouped into milestones.


## Explore the repo
- **Case pages (the review queue):** [experiments/261009_1_api/cases/index.md](../experiments/261009_1_api/cases/index.md), with charts in [experiments/261009_1_api/charts/](../experiments/261009_1_api/charts/)
- **Eval report:** [reports/eval_report.md](../reports/eval_report.md)
- **Recovery packets (simulated review):** [experiments/261009_1_api/pi_packets/](../experiments/261009_1_api/pi_packets/), explained in [docs/payment_integrity.md](payment_integrity.md). Each run keeps its own charts, case pages and packets in its folder, so a later run never overwrites them.
- **Data design and calibration notes:** [docs/synthetic_data.md](synthetic_data.md)
- **Experiments and what they do and do not show:** [experiments/README.md](../experiments/README.md)
- **Open and closed work:** the GitHub issues and milestones for this repository
- **For AI agents working on this repo:** [CLAUDE.md](../CLAUDE.md)

To rebuild the figures above: `python docs/make_figures.py`.

---

