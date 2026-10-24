# The operating model: claims first, records on request, people at both ends

[Back to the README](../README.md) · [how it works](how-it-works.md) · [limitations](limitations.md) · [concepts](concepts/README.md)

**What this page is.** The product decision behind everything else in this repository: what data a payer is assumed to have, what it has to ask for, and where people sit in the process. It was implicit in the code and the README; an outside review asked for it in writing. It describes what is built, what is simulated, and what is deliberately not assumed.

## The decision
**The payer starts with its claims and asks for records only for selected cases.** It is assumed to hold every paid claim (billed code, diagnoses, dates, amounts, provider) and nothing else about the visit. Clinical documentation reaches it only when a provider answers a records request. This makes the product a **claims-triage and targeted-records-request** tool: rank providers and claims from claims alone, choose whom to ask, read what comes back, estimate what a sample supports, and decide whether pursuing is worth its cost.

What this does **not** assume: clinical notes available for every claim at scale, a feed from providers' record systems, or the right to sample records without a request. If a payer did have notes at scale the product would be a different one (extract documentation evidence from every note, apply coding rules, escalate hard cases to certified coders). That product is not built here; a hybrid (score all claims, read notes where they exist, request records only for high-value or uncertain cases) is the likely practical answer and is not built either.

## Two stages, a person at each end
```
 all paid claims
      |  claims screens (the level screen, the volume screen), run on every provider
      v
 shortlist  ----->  [person 1: PI team reviews the shortlist, decides whom to pursue, sends the records requests]
                         |   providers answer in days to weeks (some never do)
                         v
                    records review (chart rules, conservative estimate, break-even rule)
                         |
                         v
                    drafted cases  ----->  [person 2: PI team signs off each demand]
```
- **Stage A (screen):** code over all claims. Output: a [shortlist](concepts/shortlist.md) of providers, with a [request recommendation](concepts/request-recommendation.md) for each.
- **Gate 1 (a person):** a payment integrity team reviews the shortlist and sends the requests. Time passes here and in the office's reply.
- **Stage B (records):** [chart review](concepts/chart-review.md) of what returned, a conservative recovery estimate, a demand only if it covers its cost.
- **Gate 2 (a person):** the team reviews drafted cases; nothing is sent or decided automatically.

## What is simulated today
Every number in the README is a **full run with both gates set to "accept all, no delay"**: the workflow or agent takes the shortlist straight to records requests and the drafts straight to demands. The people at gates 1 and 2 cost nothing but the [triage](concepts/triage.md) and demand-work minutes in the score, never say no, and never delay. The office (the provider side) does respond with delays, silence and deficiencies, from the simulated response table in `src/provider_sim.py`. The charts that return are structured fields (problem, data and risk levels, minutes) plus a templated note, not free text.

## What we plan to measure: stage and gate parameters
Added to the evaluation harness, not to the arms (the arms stay as they are):

| Parameter | Values | What it measures |
|---|---|---|
| Stage | **screen only** (score the shortlist: dollars in the list, ranking quality), **records only** (start from a given list: the screen's, the oracle's, or a human-edited one; score net dollars from there), **full** | Where the loss is. The records-only mode separates the review's value from the screen's. |
| Gate 1: shortlist acceptance | accept all (today), accept the top k, a person vetoes a fraction of the list (random or by a rule such as small panels), plus a delay in days | How good the screen must be if people reject part of it, and what delay does to recovery. |
| Gate 2: demand sign-off | accept all (today), accept only above an estimate, reject a fraction | The same question at the other end. |

Presets keep the grid small. The gates are a **model of a person**, an assumption, not evidence about how teams decide; results will say "if reviewers reject 30% at random" and no more. Filed in the milestone "v4.3 and v5.3".

## Open questions this model does not answer
Whether a given payer has the contractual right to request records at this volume and to extrapolate from a sample, how fast providers answer in practice, whether notes are available for any slice of claims, and what a person at gate 1 actually does with a shortlist. Each changes parameters (delays, response rates, acceptance), not the structure.
