# The learned policy in plain words (workflow v2.4, issue 108)

[Back to the README](../README.md)

**Workflow v2.4 is still a fixed workflow.** Every run executes the same code in the same order, with the same numbers; nothing is learned while it runs. The only difference from v2.3 is how one decision is made.

## The one decision
A workflow asks a practice for 30 charts and follows up on any problem. After that **first sample** it must decide what to do next:
- **STOP:** nothing more.
- **Targeted request:** ask for 15 more charts of the top code (99215).
- **Audit trail:** ask for the EHR audit trail of the notes.
- **Both.**

In **v2.3 a person wrote that decision as rules**: ask for the targeted charts only for the first 5% of the list and only if fewer than 6 usable 99215 charts came back; ask for the audit trail only if the notes show cloning signs.

In **v2.4 the same decision is a small scoring formula**. For each of the four choices it estimates, from what the first sample returned (charts back, share unsupported, notes, late-signature rate, whether the office was silent, rounds used) and the provider's screen rank and ratio, how likely the choice is to find an upcoder, to wrongly flag an honest doctor, and how many extra rounds it costs an honest practice. It picks the choice with the best balance. The formula's numbers are in a plain file, `src/policy_24.json`.

## Where the "reinforcement learning" is
Before the workflow ever runs, the formula's numbers are **learned offline** from the simulator: we run every listed provider under every choice on 20 development seeds, see what each choice would have found and cost (the answer key supplies the outcome, never an input), and fit the numbers that give the best reward. That is the simplest form of reinforcement learning, a one-step contextual bandit: pick an action from a state, observe a reward, learn which action pays. It is not an agent that learns during a run, and the Claude agent (v3.x) does not use it yet.

## What "lambda" is
The reward for a choice is: **+1 per upcoder found, minus 1 per honest doctor wrongly flagged, minus lambda per extra request round sent to an honest practice.** Lambda is the price of bothering an honest practice. Higher lambda means a more cautious policy that escalates less. We tried a grid (0 to 0.5) and picked **0.05** by a rule fixed in advance: the largest number of upcoders found among settings that, in cross-validation, found at least as many as v2.3, called no more honest doctors and sent no more rounds to honest practices.

## The "stages"
- **Stage 1:** learn **ask or skip** before the first request. Cross-validated, it did not beat the simple "ratio to expected at least 2.5" gate on upcoders found, so it is not used.
- **Stage 2:** learn the **stop or escalate** decision above. Cross-validated by seed on the development data, it beat the hand-set rule (more upcoders found, fewer honest doctors flagged, fewer rounds). This is what v2.4 uses.

## What is and is not shown
All of this is on development seeds (cross-validated by seed, but the same data the other settings were tuned on) and on simulated practices. The fresh ten-seed test posted on issue 108 is the real comparison. The variants tested there: G (the light tier gated at ratio 2.5, from issue 102), L (the learned decision), GL (both), against v2.3.
