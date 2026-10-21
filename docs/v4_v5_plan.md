# The v4/v5 line: data 4.0, score 4.0, workflow v4.0 and agent v5.0

[Back to the README](../README.md) · [version history](versioning.md) · [roadmap](roadmap.md)

Product direction set by Simmy on 2026-10-20. This page is the specification for the next release; nothing on it is built yet. Issues are in the GitHub milestone "v4.0 and v5.0" (milestone 15).

## Why new major versions
Two things change what the product is measured against:
- **The data model.** A provider stops being "upcoder or not" and gets a true **upcoding rate** and, for upcoders, a **habit**.
- **The score.** Net dollars becomes **dollars recovered minus staff-hours cost minus provider abrasion**, with recovery from any provider whose charts show overpayment.

So the majors move, keeping the shared minor: release Y on this line is **data 4.Y, workflow v4.Y, agent v5.Y**. The workflow stays API-free. Every feature lands in both designs, or `versioning.md` records why it is one-sided.

## Order of work
| Step | Issue | Depends on |
|---|---|---|
| 1. Score 4.0 module | [#125](https://github.com/simmyhundal/em-upcoding-agent/issues/125) | none |
| 2. Free check: score 4.0 on stored release 2 to 5 runs (data 2.2 answer keys) | [#126](https://github.com/simmyhundal/em-upcoding-agent/issues/126) | 1 |
| 3. Data 4.0 generator | [#124](https://github.com/simmyhundal/em-upcoding-agent/issues/124) | none |
| 4. Indicators and screens on data 4.0 | [#127](https://github.com/simmyhundal/em-upcoding-agent/issues/127) | 2, 3 |
| 5. Agent text (code-checked headline and rationale) | [#116](https://github.com/simmyhundal/em-upcoding-agent/issues/116) | none (replays stored findings) |
| 6. Obey-the-advice counterfactual | [#118](https://github.com/simmyhundal/em-upcoding-agent/issues/118) | none (stored runs) |
| 7. Ceiling test, redone on data 4.0 | [#117](https://github.com/simmyhundal/em-upcoding-agent/issues/117) | 2, 3 |
| 8. Reference arms, build v4.0 and v5.0, fresh-seed evaluation | [#128](https://github.com/simmyhundal/em-upcoding-agent/issues/128) | all of the above |

Step 3 runs in parallel with steps 1 and 2; steps 5 and 6 need neither and can run any time. Later: SIU hours cap, appeals and an expected-recovery tool ([#129](https://github.com/simmyhundal/em-upcoding-agent/issues/129)); lighter actions for no-intent upcoding ([#123](https://github.com/simmyhundal/em-upcoding-agent/issues/123)). Both are in M7.

## Data 4.0 (decided)
- **True net upcoding rate for every provider:** the share of visits billed above the justified level minus the share billed below.
- **Upcoders: exactly 8 per dataset.** Each upcoder's net rate is drawn from 15% to 40%, and its habit produces that rate. Data 2.2's 8 to 12% "subtle" band is dropped. So 15% net is the line between the two groups, and the abrasion weight below uses it. Each upcoder has one habit:
  - **Systematic:** always bills 99214 for 99213-level visits.
  - **Opportunistic:** inflates only borderline visits, whose complexity sits just under the next level's cutoff.
  - **Template-driven:** an EHR default sets a higher level, with no intent. It is still a target. The template text repeats across patients without being copied from one patient's note.
- **Non-upcoders:** each has a mean net rate between -15% and +15%, so coding noise runs in both directions. Hard negatives (honest high-acuity panels) are kept.
- **Answer key:** `role` stays binary: the planted 8, with no relabeling by data 2.2's 95th-percentile-plus-margin rule. Beside it the key holds the rate, the habit and the true overpayment dollars. Missed upcoders, false calls, precision and AUPRC therefore still compute.
- **Structural change:**
  - Each visit gets a continuous complexity (an MDM score and minutes), and the justified level is derived from it. "Borderline" needs this.
  - Today the order is reversed: the level is drawn first and the MDM elements are built to fit it (issue 45).
- **Realism added:**
  - fewer cloned notes (10 to 20% of upcoders)
  - time padding just over the time cutoffs
  - risk-element inflation
  - drift over time
  - patients shared across providers
  - reviewer disagreement: a reviewer-determined level with noise around the true level. Scoring uses true dollars.
- **Expectations:**
  - Honest noise of ±15% is much wider than data 2.2's, so expect screen recall to fall.
  - Habit shares and parameters are assumptions; no published breakdown of upcoding by mechanism was found.
  - Easier by construction: we plant the habits that the new screens look for.

## Score 4.0 (direction set; parameters are assumptions)
Per seed: **score = dollars recovered - staff-hours cost - provider abrasion.**

1. **Dollars recovered.**
   - **Who:** any provider an arm sends a demand to, whatever its `role`. A non-upcoder whose charts show a 10% overpayment is recovered from in proportion to the estimate, as payers do; intent does not matter for an overpayment.
   - **How much:** the smaller of two amounts:
     - the 90% lower bound of the overpayment extrapolated from the provider's random sample, on the level-difference basis;
     - the provider's true overpayment dollars. A demand above that would be overturned.
   - **When extrapolation applies:** only when the sample shows a sustained or high error rate, or after documented education has failed to correct the billing. Medicare allows extrapolation only in those cases (Social Security Act section 1893(f)(3)). The error-rate threshold is a stated parameter; the education path waits for the lighter actions in #123. Below it, only the sampled claims' overpayment is recovered.
   - **Full denial:** a sampled claim is denied in full only for a documentation failure that cannot be cured, such as a missing signature with no attestation. Template text alone never triggers it, because under release 5's option 2 it would deny no-intent offices in full.
   - To verify: whether underpayments found in the sample are netted (CMS Program Integrity Manual, chapter 8).
2. **Staff-hours cost.**
   - **Formula:** activity counts × minutes × loaded hourly wage, plus cash costs: the $90 copy fee per request round and the agent's API dollars.
   - **Starting assumptions:**
     - 15 minutes of analyst triage per listed provider
     - 30 minutes of admin per request round
     - about 15 minutes of certified-coder review per E/M chart
     - 4 hours of investigator time plus 1 hour of nurse time per demand
   - **Wages:** Bureau of Labor Statistics medians, to verify, × 1.4 for benefits.
   - **GAO figure:** reconcile with GAO-16-394's $158, checking whether it is per claim or per case, and report both as a range. If it is per claim, release 5 understated review cost.
3. **Provider abrasion**, driven by the provider's true net rate r, not the estimate:
   - **Weight:** w(r) = 1 for r ≤ 0, falling linearly to 0 at r ≥ 15% (the upcoder floor).
   - **Abrasion** = w(r) × (request rounds × $43.84 + $2,000 if a demand was sent).
   - **Effect:** a provider that truly overbilled 10% carries a third of the abrasion of one that billed correctly. An upcoder carries none.
   - **Sensitivity:** $2,000 also at $0 and $10,000; the weight's end points are assumptions too.

**Reported beside the score:**
- upcoders found, by binary `role`
- dollar-weighted recall: the share of all true overpayment dollars held by providers that were sent a demand
- demands, by band of true rate

The release 5 score (`eval/dollar_reward.py`) stays frozen; score 4.0 is a new versioned module.

## Arms and seeds
- **Reference arms:** frozen workflow v2.5 and agent v3.5 run unchanged on data 4.0 and are scored with score 4.0. This separates the data change from the method change, so v4.0 and v5.0 carry real features from the start.
- **Fresh seeds:** start at 5555, in steps of 101. They no longer have to be named on an issue before they are generated. Record them in every run, never tune on them, and never call a seed held out once anything was tuned on it.
- **Paid runs:** agent runs cost money. State the estimate and get Simmy's OK first.

## Out of scope here
- **Claim-level pre-payment review:** pay, pend, downcode or deny at submission. This is a different product, with a claim stream instead of provider-years, prompt-pay deadlines, and pend-rate and abrasion metrics, so it belongs in its own repository; it could reuse this generator.
- **Bridge into this repo:** putting a flagged provider on pre-payment review for future claims is part of [#123](https://github.com/simmyhundal/em-upcoding-agent/issues/123).
