# How it works (version 3)

[Back to the README](../README.md)

The agent design, what each of its actions does, and how the versions differ. **Status:** `v3.0` and `v3.1` are frozen and evaluated. `v3.1`, shown in the figure, adds the actions marked *v3.1* below and runs on data 2.1; on ten fresh seeds it found 27 of 80 upcoders against 18 for `v3.0`, and was not reliably different from workflow `v2.1` (32 of 80; [eval61.md](eval61.md)).

## The agent and its actions
![The agent and the actions it chooses from: screen, look closer, request charts, follow up, check notes, estimate, review, submit findings; simulated practices answer, checks gate the findings, people review the drafts](images/agent.svg)

**The data.** A fake (synthetic) population of 216 family doctors in Georgia and about 120,000 office visits, shaped like what a health plan holds: members, claim headers and lines, remittance with denials, replacements and voids, and conditions derived from the diagnosis codes on claims. Eight doctors are planted upcoders (half of them clone their notes so the charts match the bill), eight are honest but treat unusually sick patients, and the rest are typical. Because the answer is known, the tools can be graded; the agent never sees it.

**The agent.** A model picks the next action within hard caps: 60 tool calls, 80 turns, $3 per run (with a notice at 80%) and at most 15 practices asked for records. Every action is a tool written in plain code; what the model itself writes is the leaning, headline and interpretation it submits. Tools, limits and what the agent can see: [agent_tools.md](agent_tools.md).

The actions:
1. **Screen.** Ranks doctors by how often they bill the top visit code compared with what their patients' conditions explain (plain z-score, risk-adjusted score or, in *v3.1*, a priority order), with any cutoff, as often as the agent likes. It is a wide net: it catches the upcoders but also many honest doctors.
2. **Look closer.** The evidence card and peer comparison for one doctor: billing mix, complexity table, sample claims and any charts already received.
3. **Request charts.** Asks a simulated practice for a sample of charts. Only a random sample supports an overpayment estimate. *v3.1:* a second, targeted request is allowed after the random one.
4. **Follow up.** Answers the practice's deficiencies (missing visits, unsigned notes, wrong dates) or closes the request. Silence is never treated as evidence of upcoding. *v3.1:* the agent can also ask for the EHR audit trail, which the practice may refuse.
5. **Check notes** (*v3.1*). Compares the returned notes with the claims: problems addressed, data review the claim can back, signatures, copy-forward and paste events. Rates, not proof.
6. **Estimate.** Extrapolates an overpayment from a random sample, with a confidence range. *v3.1:* the estimate is marked unreliable when too few charts were reviewed.
7. **Review.** The chart rule and the summary rules settle the clear cases; a model is consulted only where both are silent, and only when that option is on (it was off in every v3.0 run).
8. **Submit findings.** A leaning for each doctor examined (looks like upcoding, like a sicker patient base, or unclear) with a short interpretation. Code checks that every cited visit exists and belongs to that doctor and that every number matches the evidence. *v3.1:* unsupported or contradictory findings are refused, and every screened candidate left out needs a stated reason.

**Around the agent.** Simulated practices answer requests: complete, partial, late, unsigned, an objection or silence. Every tool call and result is logged. People review the drafts: SIU reviewers read the cases, payment integrity decides which records to request, and nothing is sent or decided automatically.

In short: statistics cast a wide net, the agent chooses what to examine and decides who the suspected upcoders are, code limits and checks it, and people decide what happens next. Version 2 does the same job as a fixed workflow in which code, not a model, chooses each step. On the reserved test seeds the workflow found more upcoders than the agent (6 against 4 of 16, with no honest doctor accused by either), and neither is good enough yet: [results and evaluation](results-and-evaluation.md).

## How it has changed
![A table of the three versions: the data, the screen, how records are obtained, who writes the summary, who decides the next step and headline evaluation results](images/progression.svg)

Each tagged version has its own figure: [v1.0](images/how_it_works_v1.0.svg), [v2.0](images/how_it_works_v2.0.svg), [v3.0](images/how_it_works_v3.0.svg). What each version fixes and what it does not: [docs/versioning.md](versioning.md).
