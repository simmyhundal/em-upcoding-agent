# E/M Upcoding Agent

A small agent that reviews outpatient E/M billing (99211–99215) on **synthetic** Medicare claims, separates likely upcoders from providers who legitimately see sicker patients, and writes case summaries an SIU investigator could act on.

Built to understand the problem of agent-driven fraud, waste and abuse detection, with the eval as the main deliverable.

## The bet
Statistics already find outliers. The agent's job is to tell **real upcoders** apart from **legitimately high-acuity providers**, and to ground every call in specific claim lines. If it can't beat a z-score baseline on that, the LLM isn't earning its place.

## Approach
1. **Baselines** — realistic E/M level mix per specialty, from CMS's public *Medicare Physician & Other Practitioners — by Provider and Service* file (aggregated, no PHI).
2. **Synthetic data** — ~200 normal providers, 8 planted upcoders, 8 hard negatives (high E/M share explained by complex patient panels).
3. **Stats layer** — 99214+99215 share, z-scored against specialty peers; flag the top ~25.
4. **Agent** — reviews each flagged provider's claims and patient complexity; returns `{decision, confidence, rationale, cited_claim_ids[]}`.
5. **Guardrail** — rejects any output citing claim IDs that don't exist for that provider.

## Eval
| Metric | Target |
|---|---|
| Recall on planted upcoders | ≥ 7 of 8 |
| False-flag rate on hard negatives | Lower than z-score baseline |
| Citation accuracy | 100% |
| Case summary usefulness (1–5 rubric) | ≥ 4 average |

Results go in `reports/`, always agent vs baseline side by side.

## Repo layout
```
data/baselines/   CMS public aggregates (not committed if large)
data/synthetic/   generated providers, patients, claims
src/              data generation, stats layer, agent
eval/             eval harness and rubric
reports/          results and failure-mode write-ups
```

## Ground rules
- Synthetic data only. No real claims, no PHI.
- Never flag real, named providers, even from public data.
- Synthetic claims are cleaner than real ones, and patient complexity is a simplified proxy for documentation. Results don't transfer directly to production.

## Status
Scoped. Build planned over two days: data and baseline first, then agent and eval.
