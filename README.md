# E/M Upcoding Agent

A proof of concept for spotting likely **E/M upcoding** (billing office visits 99211-99215 at a higher level than the visit justified) on **synthetic** Medicare claims, and for writing case summaries an SIU investigator could act on.

Scope: **Family Practice, Georgia**. Built to understand agent-assisted fraud, waste and abuse detection, with the eval as the main deliverable.

## The bet
Statistics find outliers, but a raw outlier is not an upcoder: some providers legitimately see sicker patients. The key signal is **billed level versus justified level**, meaning what a provider billed against what their patients' complexity would predict. That comparison is numeric, so **statistics make the call**. The LLM's job is to turn each flagged provider's claims into a grounded case summary that cites specific claim lines.

This is "Path B". An alternative where the LLM makes the call from clinical notes ("Path A") is parked; see Milestones.

## Approach
1. **Baselines** - realistic E/M level mix for Family Practice in GA, from CMS's public *Medicare Physician & Other Practitioners - by Provider and Service* file (aggregated, no PHI).
2. **Synthetic data** - ~200 normal providers, 8 planted upcoders, 8 hard negatives (high 99215 share explained by sicker panels), with synthetic patients and claim lines, calibrated to the CMS distribution.
3. **Detectors** (the main metric is each provider's 99215 share):
   - *Baseline 1*: plain z-score of 99215 share against peers.
   - *Baseline 2*: risk-adjusted observed-versus-expected, using patient complexity (visit-weighted chronic-condition count).
4. **Flagging** - rank providers and take the top N for review.
5. **Case summaries (LLM)** - for each flagged provider, summarise the claims and patient complexity as `{decision_rationale, cited_claim_ids[]}`. The LLM does not set the flag.
6. **Guardrail** - rejects any summary citing claim IDs that don't exist for that provider.

## Eval
| Metric | Target |
|---|---|
| Recall on planted upcoders | >= 7 of 8 |
| False-flag rate on hard negatives | Lower than the plain z-score; compared with the risk-adjusted baseline too |
| Citation accuracy | 100% |
| Case summary usefulness (1-5 rubric) | >= 4 average |

Results go in `reports/`, always detectors side by side. Note that in the synthetic data, billed level depends on patient complexity by construction, so the risk-adjusted baseline is helped by how the data was built. Report that plainly.

## Repo layout
```
data/baselines/   CMS-derived specialty distributions (small, no provider-level rows)
data/synthetic/   generated providers, patients, claims (regenerated from a seed)
src/              baseline builder, data generator, detectors, summary step
eval/             eval harness and rubric
reports/          results and failure-mode write-ups
```

## Baseline data caveats
`data/baselines/em_specialty_baselines.json` is built by `src/build_baselines.py` from the CMS file above. Read these before relying on it:
- **Small-cell suppression distorts the mix.** CMS hides provider-code rows with 10 or fewer beneficiaries, so low-volume codes drop out. Shares of higher codes are biased, and many providers show zero 99215 only because it is hidden. Treat the shares as biased, not as true billing mix.
- **Not a national sample.** The committed baseline covers all individual providers in five states (OH, NC, WA, GA, MI), not a random national draw. The GA Family Practice pull is the calibration target for the synthetic data.
- **Data year is unverified.** The JSON records `UNVERIFIED` until the release year is confirmed on data.cms.gov.
- **Office-visit codes only.** Established-patient 99211-99215; new-patient codes (99202-99205) are excluded.
- **Privacy.** NPIs are used only to group rows, then replaced by a discarded salted hash. Only aggregate distributions are saved; no provider-level rows.

## Ground rules
- Synthetic data only. No real claims, no PHI.
- Never flag real, named providers, even from public data.
- Synthetic claims are cleaner than real ones, and patient complexity is a simplified proxy for documentation. Results don't transfer directly to production.

## Roadmap
- **Milestone 1 - PoC (Path B):** statistics decide, the LLM writes case summaries. In progress.
- **Milestone 2 - Path A (parked):** the LLM judges from synthetic clinical notes. Not being worked on.

## Status
Synthetic data generator and Baseline 1 (plain z-score) done. Next: risk-adjusted baseline, flagging, case summaries, eval. First scorecard line, plain z-score top 25: 7/8 upcoders found, 3/8 hard negatives and 15/200 normal providers falsely flagged. Details in `docs/synthetic_data.md`.
