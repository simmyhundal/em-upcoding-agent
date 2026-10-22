"""Pre-declared reason, grid and choice rule for hypotheses H15 to H19 of the workflow v4.1 loop (issue 132). Committed BEFORE each hypothesis was run; docs/w_loop_v41.md quotes it."""

CHOICE_RULE = ("Any parameter is chosen on batches 1 to 4 only, by the highest mean score 4.0 per seed over those 40 seeds (ties go to the setting closest to H8); the chosen setting is then run once on "
               "batches 5 and 6 (out of sample) and never adjusted after seeing them. Bonferroni: eight hypotheses are tried (H13 to H20), so alpha = 0.05 / 8 = 0.00625 per look. "
               "(The first five were run under a bar of 0.05 / 7 = 0.0071; H20 was added afterwards. No result below clears either.)")

DECL = {
    "H15": {"title": "H15: probe then extend (cost side)",
            "reason": "296 listed providers were asked but only 77 were demanded from (74% of asked providers ended with no demand), and each asked provider is sent 30 charts, so most chart-review and request cost "
                      "is spent on providers who turn out clean. H10 (a flat 20-chart sample) was rejected, but a flat cut also thins the sample of the real upcoders.",
            "change": "The first request is 10 random charts. If at least k of the returned documented 99214 and 99215 charts are unsupported by the chart test's own reading (documented level or minutes below the billed level, "
                      "as the rules count them), a second RANDOM request of 20 more charts is sent (office 2.1 allows a further request with new charts); otherwise the request is closed. The estimate and the rules use all random charts.",
            "grid": "k in {2, 3, 4} (H15k2, H15k3, H15k4)"},
    "H16": {"title": "H16: near-miss extension (recovery side)",
            "reason": "The demand floor withdrew 65 of the 142 rules-called providers because the 90% lower bound of the recovery estimate fell below the cost of a demand. The bound is the total minus t times a standard error that "
                      "shrinks with the sample, so for a provider whose point estimate clears the cost but whose bound does not, 30 more random charts could tighten the bound enough to turn the call into a demand. "
                      "H11 (45 charts for everyone) was rejected because it pays for providers who do not need it.",
            "change": "After the first 30 charts and the rules call, for rules-called providers whose point estimate (recovery_40.recovery) is at least c times the cost of a demand but whose lower bound is below it, a second "
                      "random request of 30 charts is sent and the rules and the estimate are recomputed before the floor decides.",
            "grid": "c in {1, 1.5, 2} (H16c1, H16c1.5, H16c2)"},
    "H17": {"title": "H17: let the money decide (decision layer)",
            "reason": "236 upcoders had usable charts but the rules called only 142, and across the 100 development seeds workflow v4.0 called zero honest providers: the rules' chart test may be stricter than needed because the demand "
                      "floor is already a money gate (an honest provider's lower bound is about zero, below the floor, so a wrong call is withdrawn).",
            "change": "The pooled 99214 and 99215 chart test of rules 4.0 is loosened through a version option (POOL_MIN_40, POOL_UP_40, ALPHA_40 as arguments; the module defaults and agent v5.0 are unchanged); the demand floor stays.",
            "grid": "(minimum documented charts, minimum unsupported share, alpha): L1 = (8, 0.20, 0.05), L2 = (6, 0.15, 0.10), L3 = (5, 0.10, 0.20); H8 is (10, 0.25, 0.05)"},
    "H18": {"title": "H18: a dollar-weighted list (screen)",
            "reason": "docs/screens_v4_pipeline.md scored the pay_resid list best under the frozen pipeline on 11 development seeds (-$13,674 per seed against -$15,156 for eb_upper_t; recall differences small); it ranks by shrunk "
                      "excess allowed dollars, so it favours providers whose recoveries are larger, and no alternative list has been run through the final v4.0 pipeline on the 100-seed pool.",
            "change": "The top 10% by pay_resid is listed instead of eb_upper_t. The ask model is refitted on that list's own ask-everyone run (same recipe as D7: rules 4.1, floor, no escalation) on batches 1 to 4, ridge lambda 3.",
            "grid": "none (one list, one refit)"},
    "H19": {"title": "H19: a seed-level gate (portfolio)",
            "reason": "Batch means swing from -$977 to +$3,763 and 5 of 10 batches were negative, so most of the variance is between seeds. If a seed's value can be predicted from what the payer sees before asking, a gate that skips "
                      "the whole seed when the predicted H8 score is below a margin would move the result toward zero in bad seeds. H14 changed the margin per provider; this changes it per run.",
            "change": "A ridge (lambda 10, fixed) on three pre-declared pre-ask features, fitted on the 40 seeds of batches 1 to 4 to H8's score 4.0 per seed: (1) the mean screen score of the 22 listed providers, (2) the gap between the "
                      "mean screen score of ranks 1 to 5 and of ranks 6 to 22, (3) the log of the total allowed dollars on the listed providers' claims. A seed is skipped (score 0, nothing asked) when the predicted score is below 0. "
                      "The cross-validated R-squared (leave one batch out) on batches 1 to 4 is reported first.",
            "grid": "none (lambda, features and margin declared in advance)"},
}

DECL["H20"] = {"title": "H20: ask only the first K listed providers (decision layer)",
               "reason": "In the ask-everyone run (wld7, 60 seeds, batches 1 to 6, demand floor on) the mean net value per seed of asking only the top k listed providers by rank is +$954 (k=1), +$942 (2), +$754 (3), +$629 (4), +$399 (5), +$218 (6), "
                         "-$574 (8), -$1,900 (11), -$6,916 (22); workflow v4.0 averages about +$729 on the same six batches. The first two or three providers earn the money and deeper asking loses it. "
                         "(The screen's top 2 were true upcoders in 200 of 200 development seeds; the true net overpayment of the top 2 averages $14,807 per seed, so the limit is proof, not detection.)",
               "change": "The ask-or-skip model is replaced by: ask the first K listed providers by rank (the integer `ask` option). Everything else is H8's.",
               "grid": "Two separate sweeps on batches 1 to 4 only, real workflow runs (not the D7 profile). (a) K in {1, 2, 3, 4, 5, 6, 8} with the first sample at 30 charts (H20k<K>). (b) With the K chosen in (a), "
                       "first-sample size n in {10, 20, 30, 45, 60, 90} random charts (H20n<n>). Each parameter is chosen by leave-one-batch-out over batches 1 to 4: for each held-out batch, the setting with the best mean on the "
                       "other three is taken and its realized score on the held-out batch recorded (ties to the smaller); the final setting is the one with the best mean over all 40 seeds (ties to the smaller). "
                       "Choosing two parameters on 40 seeds gives selection bias in sample; the out-of-sample test on batches 5 and 6 decides."}


# H20c: written and committed BEFORE any H20c run (the corrected H20). It counts as the ninth hypothesis tried (H13 to H20 and H20c), so the Bonferroni bar is alpha = 0.05 / 9 = 0.0056 per look.
H20C_RULE = ("Same choice rule as H15 to H20 (leave-one-batch-out on batches 1 to 4, real runs, ties to the smaller; then one run on batches 5 and 6 against H8). H20c is the ninth hypothesis tried (H13 to H20 and H20c), so the "
             "Bonferroni bar is alpha = 0.05 / 9 = 0.0056 per look, applied to both the out-of-sample and the in-sample p.")
DECL["H20c"] = {"title": "H20c: H20 corrected, list only K providers (decision layer)",
                "reason": "H20 asked only the first K of the 22 listed providers but still wrote a checked summary for all 22, and score 4.0 charges triage (15 minutes of analyst time, about $13) for every provider with a checked summary "
                          "(docs/score_40.md; `listed` in eval/score_40.py run_inputs). So H20 paid about $289 of triage per seed for providers it never looked at. A top-K rule needs only K providers reviewed. "
                          "(The D7 profile of top-k values, which promised +$954 per seed for K = 1, also left triage out; the real H20 run scored +$649 on batches 5 and 6.)",
                "change": "The same change as H20 (ask the first K providers by rank, a first sample of n random charts, everything else H8's: eb_upper_t ranking, rules 4.0, demand floor, no escalation), but the list is only the top K of the "
                          "eb_upper_t screen (a flagged file whose first K rows stay flagged, same ranking and order), so only K providers are summarized and triaged. The baseline of unflagged providers' reviews still leaves out the whole 22, "
                          "so H20c differs from H20 only in which providers are listed and triaged.",
                "grid": "Two sweeps on batches 1 to 4 only, real workflow runs: (a) K in {1, 2, 3, 4, 5, 6, 8} with n = 30 (H20c_k<K>_n30); (b) with the K chosen in (a), n in {10, 20, 30, 45, 60, 90} random charts (H20c_k<K>_n<n>). "
                        "Each chosen by leave-one-batch-out over batches 1 to 4 (the held-out batch's realized mean score, ties to the smaller), the final setting the best mean over the 40 seeds (ties to the smaller). "
                        "Then (K, n) is run once on batches 5 and 6 against H8 and against zero. Sanity check before the sweeps, on seeds 1515, 1616 and 1717: H20c and H20 at the same (K, n) must ask the same providers and the same charts, "
                        "and differ in score by the triage saved (about $13 per provider not listed)."}
