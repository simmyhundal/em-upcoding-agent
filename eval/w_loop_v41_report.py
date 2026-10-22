"""The RL loop for workflow v4.1 (issue 132): the same 100-seed development pool and protocol as workflow v4.0 (docs/w_loop_v4.md, left as it was), one hypothesis at a time against H8 (workflow v4.0).
Free (API-free). Writes docs/w_loop_v41.md. Usage: python eval/w_loop_v41_report.py"""
import json
import os
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v4 as pool  # noqa: E402
import w_loop as wl  # noqa: E402
import w_loop_v41_decl as decl  # noqa: E402
import w_loop_v41_extra as extra  # noqa: E402

CANDIDATES = [("H13", "H8 with ask features built on the eb_upper_t screen (shrunk score, panel size, observed share and count of 99214 and 99215 visits) instead of the 99215-only ones; fitted on batches 1 to 4"),
              ("H14", "H8 asking only when the predicted value exceeds a stop-loss margin of $50 (chosen by leave-one-batch-out cross-validation on batches 1 to 4; same model, screen, sample, rules and demand floor)")]


B14, B56 = sum(pool.BATCHES[:4], []), sum(pool.BATCHES[4:6], [])


def load(n):
    return json.load(open(os.path.join(wl.CACHE_DIR, f"{n}.json")))


def asks_per_seed(name, seeds):
    n = 0
    for s in seeds:
        seen = set()
        for line in open(os.path.join(ROOT, "experiments", f"wl{name.lower()}_{s}", "office_transcript.jsonl")):
            e = json.loads(line)
            if e.get("action") == "send_request" and "error" not in e:
                seen.add(e["provider_id"])
        n += len(seen)
    return n / len(seeds)


def paired(name, bar=0.00625):
    out = []
    for seeds, tag in ((B14, "batches 1 to 4 (in sample: parameter chosen, and the ask model fitted, here)"), (B56, "batches 5 and 6 (out of sample, run once)")):
        c = wl.compare(name, "H8", seeds)
        out.append("- " + wl.line(c, name, "H8") + f" ({tag}). Clears alpha = {bar}: {'yes' if c['p'] <= bar else 'no'}.")
    d = load(name)
    z = wl.perm_p([d[str(x)]["score"] for x in B56])
    out.append(f"- Against zero on batches 5 and 6: mean {st.mean(d[str(x)]['score'] for x in B56):,.0f} per seed, one-sided p = {z:.3f} (H8 itself: {wl.perm_p([load('H8')[str(x)]['score'] for x in B56]):.3f}); not distinguishable from zero.")
    return out


def comp_table(names):
    h8 = load("H8")
    L = ["", "Per seed means (components of score 4.0):", "", "| Seeds | Version | Score | Asks | Rounds | Found | Honest called | Recovered | Staff cost |", "|---|---|---|---|---|---|---|---|---|"]
    for lab, seeds in (("Batches 1 to 4", B14), ("Batches 5 and 6", B56)):
        for n in ["H8"] + names:
            d = load(n)
            g = lambda k: st.mean(d[str(x)][k] for x in seeds)
            a = f"{asks_per_seed(n, seeds):.2f}" if n != "H19" else "n/a"
            L.append(f"| {lab} | {n} | {g('score'):,.0f} | {a} | {g('rounds'):.1f} | {g('found'):.2f} | {g('honest_called'):.2f} | {g('recovered'):,.0f} | {g('staff_cost'):,.0f} |")
    return L


def head(h):
    d = decl.DECL[h]
    return [f"## {d['title']}", "", f"**Reason (declared before running).** {d['reason']}", "", f"**Change.** {d['change']}", "", f"**Grid and choice (declared before running).** {d['grid']}", ""]


def grid_table(prefix, values, label):
    sel = json.load(open(os.path.join(wl.CACHE_DIR, f"{prefix}_select.json"))) if os.path.exists(os.path.join(wl.CACHE_DIR, f"{prefix}_select.json")) else None
    L = ["", f"| {label} | B1 | B2 | B3 | B4 | mean B1 to 4 |", "|---|---|---|---|---|---|"]
    for v in values:
        d = load(f"{prefix}{v}")
        bm = [st.mean(d[str(x)]["score"] for x in pool.BATCHES[b]) for b in range(4)]
        L.append(f"| {v} | " + " | ".join(f"{x:,.0f}" for x in bm) + f" | {st.mean(bm):,.0f} |")
    return L, sel


def more_sections():
    L = ["", "# Hypotheses H15 to H20", "", "Added after H13 and H14, one change each on top of H8, same pool and paired comparison. " + decl.CHOICE_RULE + " "
         "H8 on batches 1 to 4 is 735 per seed and on batches 5 and 6 is 719 (H8's ask model was fitted on batches 1 to 4, so batches 5 and 6 are out of sample for every version here, except that the H8 batch means are "
         "themselves a draw of +/-$1,450). The grid and the choice rule for each hypothesis are in `eval/w_loop_v41_decl.py`, committed before the runs. Verdicts are my reading; the numbers are generated.", ""]
    # H15
    L += head("H15")
    g, _ = grid_table("H15k", (2, 3, 4), "k")
    L += g + ["", "Chosen k = 3 (best mean on batches 1 to 4: -547); the other two were -555 and -753, all far below H8's 735."]
    L += [""] + paired("H15")
    a, b = extra.probe_stats("H15", B14), extra.probe_stats("H15", B56)
    L += ["", f"What the probe did: on batches 1 to 4, {a['asked']} providers were asked, {a['extended']} ({a['extended'] / a['asked']:.0%}) were extended to 30 charts, none was blocked by the round or day cap, and the first 10 charts held {a['mean_hi_charts_at_probe']:.1f} documented "
          f"99214 or 99215 charts on average. Rules 4.0 need at least 10 pooled 99214 and 99215 charts (POOL_MIN_40), so a provider who is not extended can be called only if all 10 charts are 99214 or 99215 and 10 happen to be documented; in practice the probe decides the call. "
          "By construction, the estimate then rests on a sample whose size depends on its own first results (not a fixed-design random sample), so the lower bound is not exactly 90%."]
    L += comp_table(["H15"])
    L += ["", "**Verdict: rejected.** On batches 1 to 4 it loses $1,282 per seed against H8 (found 21 against 34 upcoders): (an inference) the probe misses real upcoders, who are caught by a 10-chart look less often than by a 30-chart look, and the extra requests add rounds (7.2 against 5.8 per seed) because the follow-up and the second request each count. "
          "The positive difference on batches 5 and 6 (+$183, p = 0.42, better on 10 of 20) is noise around a rule that lost on the 40 seeds it was chosen on; it is not evidence for the hypothesis."]
    # H16
    L += [""] + head("H16")
    g, _ = grid_table("H16c", ("1", "1.5", "2"), "c")
    L += g + ["", "All three c give the same result: every provider whose lower bound was below the cost of a demand but whose point estimate was above it had a point estimate of at least $1,027, which is 3.7 times the $276 cost of a demand, so c between 1 and 2 selects the same 14 providers. "
              "By the pre-declared tie rule (closest to H8) c = 2 is chosen."]
    L += [""] + paired("H16")
    a, b = extra.extension_stats("H16", B14), extra.extension_stats("H16", B56)
    L += ["", f"What the extension did: {a['extended']} providers were extended on batches 1 to 4 and {a['demanded_after_extension']} of them were demanded from after the second sample (the rest stayed below the floor); on batches 5 and 6, {b['extended']} and {b['demanded_after_extension']}. "
          f"The floor withdrew {extra.withdrawn('H16', B14)} calls on batches 1 to 4 (H8: {extra.withdrawn('H8', B14)}) and {extra.withdrawn('H16', B56)} on batches 5 and 6 (H8: {extra.withdrawn('H8', B56)}). No second request was blocked."]
    L += comp_table(["H16"])
    L += ["", "**Verdict: not supported at the bar; the most plausible lead of the six, but a small one.** The mechanism worked as designed (found 23 against 17 on batches 5 and 6; recovery +$543 per seed for +$285 of staff cost), the out-of-sample gain is +$257 per seed, but it comes from a few seeds "
          "(better on 4 of 20 and 8 of 40, the rest equal or worse) and p = 0.23 out of sample and 0.027 in sample, neither below 0.00625. A difference this size on 20 seeds is below the batch noise. It would need a new test on fresh seeds before being adopted."]
    # H17
    L += [""] + head("H17")
    g, _ = grid_table("H17", ("L1", "L2", "L3"), "setting")
    L += g + ["", "L1 = (8 charts, 20%, alpha 0.05), L2 = (6, 15%, 0.10), L3 = (5, 10%, 0.20); H8 = (10, 25%, 0.05). Chosen L3 (best mean on batches 1 to 4: 898); the more the test is loosened, the better it did on these 40 seeds, so L3 is the end of the declared grid and the trend may continue beyond it (not tested)."]
    L += [""] + paired("H17")
    L += comp_table(["H17"])
    L += ["", "No honest provider was called under any setting on these seeds (honest called 0 in all rows) and the abrasion component did not change: the demand floor withdraws the weak calls, as the hypothesis expected. Rounds are identical to H8 by construction, since the rules act after the requests.",
          "", "**Verdict: not supported at the bar.** +$291 per seed out of sample (p = 0.12; better on only 3 of 20 seeds, the rest equal or worse) and +$163 in sample (p = 0.015). The gain is real in direction on both and has no visible cost on honest providers here, "
          "but it rests on a handful of seeds where one more provider was demanded from. It is a lead for a fresh-seed test, not a result."]
    # H18
    L += [""] + head("H18")
    L += ["Diagnostic run `D7p` (ask-everyone on the pay_resid list, batches 1 to 4) gave a per-seed score of -7,376 when every listed provider is asked (D7 on eb_upper_t is stored in `wld7_*`). The ask model refitted on it is `experiments/w_loop/ask_model_pay_resid_b1to4.json` (same six features, lambda 3). "
          "The features suit the new list (the file has the same columns), so no change to them was needed; whether they predict well on it is shown by the result."]
    L += [""] + paired("H18")
    L += comp_table(["H18"])
    L += ["", "**Verdict: rejected.** -$282 per seed out of sample (p = 0.96) and -$47 in sample (p = 0.69). The list finds more upcoders in sample (found 40 against 34 on batches 1 to 4), but the extra providers it lists cost more asks (3.4 against 3.05 per seed out of sample) and rounds than they return; the earlier screen comparison on 11 seeds under the frozen pipeline did not carry over to the final v4.0 pipeline."]
    # H19
    gate = json.load(open(os.path.join(wl.CACHE_DIR, "H19_gate.json")))
    L += [""] + head("H19")
    L += [f"**First, can the seed score be predicted?** Cross-validated (leave one batch out) R-squared on batches 1 to 4: {gate['cv_r2_vs_zero_mean']:.2f} against the pooled mean of the 40 seeds and {gate['cv_r2_vs_fold_training_mean']:.2f} against each fold's own training mean. **Both are below zero, so the model predicts worse than a constant: the gate is not supported.** "
          "With 40 points and three features this is what a weak signal looks like. The gate is reported anyway, as asked.", ""]
    L += ["Standardized coefficients (intercept, mean score, top-5 gap, log dollars): " + ", ".join(f"{c:,.0f}" for c in gate["coef_standardized"]) + f". The gate skips {gate['skipped_b1to4']} of 40 seeds on batches 1 to 4 (in sample) and {gate['skipped_b5_6']} of 20 on batches 5 and 6; "
          f"the correlation between predicted and actual H8 score on batches 5 and 6 is {gate['corr_pred_actual_b5_6']:.2f}. The seeds skipped on batches 5 and 6 averaged {gate['skipped_b5_6_h8_mean_score']:,.0f} under H8, the kept ones {gate['kept_b5_6_h8_mean_score']:,.0f}.", ""]
    L += paired("H19")
    L += comp_table(["H19"])
    L += ["", "(Asks are not reported for H19: gated seeds ask nobody and the run folders are H8's.)", "",
          "**Verdict: not supported.** The out-of-fold R-squared is negative, so the gate has no basis. On the 20 out-of-sample seeds it adds +$115 per seed (p = 0.065, better on 4 of 20) by skipping 6 seeds that happened to be losing; with a model that fails cross-validation this is a chance draw, "
          "and the in-sample +$168 on batches 1 to 4 is by construction (the model was fitted to those scores)."]
    # H20
    L += [""] + head("H20")
    g, sel = grid_table("H20k", (1, 2, 3, 4, 5, 6, 8), "K")
    L += ["", "Sweep (a): K with 30 charts."] + g
    L += ["", "Leave-one-batch-out for K: held-out batches 1 to 4 each chose K = 1 (realized " + ", ".join(f"{f['realized']:,.0f}" for f in sel["folds"]) + f"; mean {sel['lobo_mean']:,.0f}). Chosen K = {sel['chosen']}."]
    g, sel = grid_table("H20n", (10, 20, 30, 45, 60, 90), "n at K=1")
    L += ["", "Sweep (b): first-sample size n at K = 1."] + g
    L += ["", "Leave-one-batch-out for n: held-out folds chose " + ", ".join(f"n = {f['chosen']} (realized {f['realized']:,.0f})" for f in sel["folds"]) + f"; mean {sel['lobo_mean']:,.0f}. Chosen n = {sel['chosen']}. Chosen (K, n) = (1, 30), which is the sweep (a) run K = 1."]
    L += [""] + paired("H20")
    L += comp_table(["H20"])
    L += ["", "**Verdict: rejected.** Asking only the top-ranked provider reduces asks from 3.05 to 1.0 per seed and rounds from 5.9 to 2.0, and cuts staff cost, but it also cuts recovery (found 0.45 against 0.85 upcoders per seed), "
          "so the net is -$69 per seed out of sample (p = 0.60) and -$61 in sample, equal to H8 within noise. The real run for K = 1 gives +$674 on batches 1 to 4, below the D7 profile's +$954 on batches 1 to 6 (different seed set, and D7 runs rules 4.1). "
          "The sweep is monotone in K, so the choice sits at the edge of the grid (smaller K is not a policy); selecting two parameters on 40 seeds adds some selection bias in sample, which the out-of-sample result does not show. Asking one provider is also a high-variance policy (one provider per seed)."]
    # summary
    L += ["", "## Summary of H15 to H20", "", "Bar: Bonferroni alpha = 0.05 / 8 = 0.00625 per look (0.0071 for the first five when run), applied to both the out-of-sample and the in-sample p.", "",
          "| Hypothesis | Chosen | Batches 5 and 6 vs H8 | p | Batches 1 to 4 vs H8 | p | Clears the bar | Verdict |", "|---|---|---|---|---|---|---|---|"]
    chosen = {"H15": "k = 3", "H16": "c = 2", "H17": "L3", "H18": "pay_resid list", "H19": "gate at 0", "H20": "K = 1, n = 30"}
    verdict = {"H15": "rejected", "H16": "lead, not supported", "H17": "lead, not supported", "H18": "rejected", "H19": "not supported (negative CV R-squared)", "H20": "rejected"}
    for h in chosen:
        a, b = wl.compare(h, "H8", B56), wl.compare(h, "H8", B14)
        L.append(f"| {h} | {chosen[h]} | {a['mean_diff']:+,.0f} | {a['p']:.3f} | {b['mean_diff']:+,.0f} | {b['p']:.3f} | {'yes' if min(a['p'], b['p']) <= 0.00625 and a['p'] <= 0.00625 else 'no'} | {verdict[h]} |")
    L += ["", "None of the six clears the bar, and none changes workflow v4.0. All are about as large as the batch-to-batch swing (+/-$1,450). Nothing here was run on fresh seeds."]
    return L


def h20c_section():
    """H20c (the corrected H20), appended after the H15 to H20 text, which is left as generated."""
    import recovery_40 as r40
    import score_40 as s4
    N = "H20c_k1_n30"
    triage1 = r40.staff_cost(1, 0, 0, 0, 0, s4.PARAMS)[1]["triage"]
    L = ["", "# Hypothesis H20c: H20 corrected (list only K providers)", "", "Added after H20. " + decl.H20C_RULE + " The grid and the reason were declared in `eval/w_loop_v41_decl.py` and committed before any H20c run.", ""]
    L += head("H20c")
    kd = json.load(open(os.path.join(wl.CACHE_DIR, "H20c_k_select_n30.json")))
    L += ["", "Sweep (a): K with n = 30 charts (H20c_k<K>_n30), score 4.0 per seed by batch:", "", "| K | B1 | B2 | B3 | B4 | mean B1 to 4 | H20 at the same K (mean) |", "|---|---|---|---|---|---|---|"]
    for k in (1, 2, 3, 4, 5, 6, 8):
        d = load(f"H20c_k{k}_n30")
        bm = [st.mean(d[str(x)]["score"] for x in pool.BATCHES[b]) for b in range(4)]
        h = load(f"H20k{k}")
        L.append(f"| {k} | " + " | ".join(f"{x:,.0f}" for x in bm) + f" | {st.mean(bm):,.0f} | {st.mean(h[str(x)]['score'] for x in B14):,.0f} |")
    L += ["", "Leave-one-batch-out for K: held-out batches 1 to 4 each chose K = 1 (realized " + ", ".join(f"{f['realized']:,.0f}" for f in kd["folds"]) + f"; mean {kd['lobo_mean']:,.0f}). Chosen K = {kd['chosen']}, the edge of the grid, as in H20."]
    nd = json.load(open(os.path.join(wl.CACHE_DIR, "H20c_k1_n_select.json")))
    L += ["", "Sweep (b): first-sample size n at K = 1 (H20c_k1_n<n>):", "", "| n | B1 | B2 | B3 | B4 | mean B1 to 4 |", "|---|---|---|---|---|---|"]
    for n in (10, 20, 30, 45, 60, 90):
        d = load(f"H20c_k1_n{n}")
        bm = [st.mean(d[str(x)]["score"] for x in pool.BATCHES[b]) for b in range(4)]
        L.append(f"| {n} | " + " | ".join(f"{x:,.0f}" for x in bm) + f" | {st.mean(bm):,.0f} |")
    L += ["", "Leave-one-batch-out for n: held-out folds chose " + ", ".join(f"n = {f['chosen']} (realized {f['realized']:,.0f})" for f in nd["folds"]) + f"; mean {nd['lobo_mean']:,.0f}. Chosen n = {nd['chosen']}. Chosen (K, n) = (1, 30), the sweep (a) run at K = 1."]
    L += ["", "**Sanity check (before the sweeps, seeds 1515, 1616, 1717, K = 3, n = 30).** H20c and H20 asked the same providers with the same requests and received the same charts (identical office transcripts); H20c wrote 3 summaries and H20 wrote 22. "
          "The score differs by exactly 19 providers x $13.125 of triage = $249.38 on each seed. Over all 40 development seeds at K = 1 the difference H20c minus H20 is +$276 on every seed (sd 0), which is 21 providers x $13.125.", ""]
    for seeds, tag in ((B14, "batches 1 to 4 (in sample: K and n chosen here, the ask model of H8 fitted here)"), (B56, "batches 5 and 6 (out of sample, run once)")):
        c = wl.compare(N, "H8", seeds)
        L.append("- " + wl.line(c, N, "H8") + f" ({tag}). Clears alpha = 0.0056 (0.05 / 9): {'yes' if c['p'] <= 0.05 / 9 else 'no'}.")
    d = load(N)
    z = wl.perm_p([d[str(x)]["score"] for x in B56])
    L.append(f"- Against zero on batches 5 and 6: mean {st.mean(d[str(x)]['score'] for x in B56):,.0f} per seed, one-sided p = {z:.3f} (H8 itself: {wl.perm_p([load('H8')[str(x)]['score'] for x in B56]):.3f}). Clears 0.0056: {'yes' if z <= 0.05 / 9 else 'no'}.")
    for seeds, tag in ((B14, "batches 1 to 4"), (B56, "batches 5 and 6")):
        L.append("- " + wl.line(wl.compare(N, "H20", seeds), N, "H20 (same K, n)") + f" ({tag}). Identical asks, charts and found; the difference is the triage of the providers no longer listed.")
    # components with triage
    L += ["", "Per seed means (components of score 4.0; triage is the listed providers' share of staff cost):", "", "| Seeds | Version | Score | Listed | Triage | Asks | Rounds | Found | Honest called | Recovered | Staff cost |", "|---|---|---|---|---|---|---|---|---|---|---|"]

    def listed(name, seeds):
        return st.mean(sum(1 for x in open(os.path.join(ROOT, "experiments", f"wl{name.lower()}_{s}", "case_summaries_checked.jsonl")) if x.strip()) for s in seeds)
    for lab, seeds in (("Batches 1 to 4", B14), ("Batches 5 and 6", B56)):
        for n, shown in (("H8", "H8"), ("H20", "H20 (K = 1, n = 30)"), (N, "H20c (K = 1, n = 30)")):
            dd = load(n)
            g = lambda k: st.mean(dd[str(x)][k] for x in seeds)
            lst = listed(n, seeds)
            L.append(f"| {lab} | {shown} | {g('score'):,.0f} | {lst:.0f} | {lst * triage1:,.0f} | {asks_per_seed(n, seeds):.2f} | {g('rounds'):.1f} | {g('found'):.2f} | {g('honest_called'):.2f} | {g('recovered'):,.0f} | {g('staff_cost'):,.0f} |")
    c56 = wl.compare(N, "H8", B56)
    saved = 21 * triage1
    L += ["", "**What is triage and what is asking.** A one-provider list saves 21 providers x $13.125 = $%s of triage per seed against H8's 22 (and against H20). H20c beats H8 by $%s per seed out of sample, so the asking itself contributes %+d: "
          "the asking policy alone (one provider per seed, %.2f upcoders found per seed against H8's %.2f) is worth about $70 less than H8's. All of H20c's gain over H8 (and all of its gain over H20) is staff cost that is not spent because the list is shorter, "
          "which is true by construction of the score (score 4.0 charges triage for every provider with a checked summary), not a better decision. The same triage saving is not available to H8 without changing its list to a shorter one, which is what H20c is."
          % (f"{saved:,.0f}", f"{c56['mean_diff']:,.0f}", round(c56["mean_diff"] - saved), st.mean(load(N)[str(x)]["found"] for x in B56), st.mean(load("H8")[str(x)]["found"] for x in B56)), ""]
    a56 = c56
    a14 = wl.compare(N, "H8", B14)
    L += ["**Verdict: rejected as an improvement of the asking; the score gain over H8 is triage saved by construction, and it is not distinguishable from noise.** "
          f"Out of sample the gain over H8 is {a56['mean_diff']:+,.0f} per seed (sd {a56['sd_diff']:,.0f}, better on {a56['wins']} of 20, one-sided p = {a56['p']:.3f}) and in sample {a14['mean_diff']:+,.0f} (p = {a14['p']:.3f}); neither clears the Bonferroni bar of alpha = 0.05 / 9 = 0.0056 "
          "(nine hypotheses tried: H13 to H20 and H20c), and both are smaller than the batch noise of about +/-$1,450. The gain over H20 is exactly the triage saved ($276 per seed, p ~ 0 only because the difference is a constant by construction, not evidence about asking). "
          "H20c does not change workflow v4.0. Caveats: a one-provider list finds 0.28 to 0.45 of the 8 upcoders per seed, so it forgoes the dollars H8 recovers on the deeper list, and it is a high-variance policy (one provider per seed); the screen's score and rank are the payer's, so nothing here uses the answer key; "
          "nothing here was run on fresh seeds. A different question, not tested here, is whether the other hypotheses (H15 to H19) would look different once triage is charged only for the providers a policy reviews; they all list 22."]
    return L


def main():
    cv = json.load(open(os.path.join(wl.CACHE_DIR, "ask_margin_cv.json")))
    d8 = json.load(open(os.path.join(wl.CACHE_DIR, "H8.json")))
    L = ["# Workflow v4.1: the loop's hypotheses (issue 132)", "", "[Back to the README](../README.md) · [workflow v4.0's loop](w_loop_v4.md) · [score 4.0](score_40.md)", "",
         "Generated by `python eval/w_loop_v41_report.py`. **Free** (API-free workflow versions). The development pool and protocol are the ones of workflow v4.0: batches of ten from `eval/dev_pool_v4.py`, score 4.0 per seed, each hypothesis against H8 (workflow v4.0), "
         "one change at a time. H8's ask model was fitted on batches 1 to 4; so was H13's, so **batches 1 to 4 are in sample for both and batches 5 and 6 are out of sample for both**. Batches 7 to 10 have no ask-everyone run to fit on and were not run for H13. "
         "Fresh seeds were not touched.", "", "## Score 4.0 per seed, by batch", "", "| Version | " + " | ".join(f"B{b}" for b in range(1, 7)) + " | Batches 5 and 6 |", "|---|" + "---|" * 7]
    for n, label in [("H8", "H8: workflow v4.0")] + [(c, f"{c}: " + t.split(" (")[0]) for c, t in CANDIDATES]:
        d = d8 if n == "H8" else json.load(open(os.path.join(wl.CACHE_DIR, f"{n}.json")))
        cells = [f"{st.mean(d[str(s)]['score'] for s in pool.BATCHES[b - 1]):,.0f}" for b in range(1, 7)]
        oos = [str(s) for b in (5, 6) for s in pool.BATCHES[b - 1]]
        L.append(f"| {label} | " + " | ".join(cells) + f" | {st.mean(d[s]['score'] for s in oos):,.0f} |")
    L += ["", "## H13 against H8", ""]
    for name, seeds, tag in (("H13", sum(pool.BATCHES[:4], []), "batches 1 to 4 (in sample for both)"), ("H13", sum(pool.BATCHES[4:6], []), "batches 5 and 6 (out of sample for both)")):
        L.append("- " + wl.line(wl.compare(name, "H8", seeds), name, "H8") + f" ({tag}).")
    L += ["", "## Reading of H13", "", "- **H13 is rejected: it does not improve on workflow v4.0.** The out-of-sample difference is -$69 per seed (it is better on 2 of 20 seeds), about the same amount of asking (118 rounds against 118), and the in-sample difference is +$7. "
          "Different inputs barely change how much the ask model asks, so the 99215-only features were probably not what held back asking.",
          "- What this leaves: the ask model skips most listed upcoders because its predicted value of asking is below zero for them, with either set of features (an inference from this one test). The next hypotheses are on what happens after asking (the demand floor, the recovery estimate) and on a stop-loss at the ask step, not on the ask inputs.",
          "- One hypothesis tried; with the protocol's correction for several (alpha is split over those tried), this one does not come close to the bar."]
    L += ["", "## H14: a stop-loss at the ask step", "",
          "H14 changes one thing: a listed provider is asked for charts only when the ask model's predicted net value exceeds a margin m instead of zero (`margin` key in the model file; H8 has none, so it is unchanged). "
          "Everything else is H8's: screen, coefficients, 30 random charts, rules 4.0, demand floor. Idea: the loss on fresh seeds was staff cost spent on asks that did not pay, so skip the marginal asks.", "",
          "**Choosing m** (declared before batches 5 and 6 were run; `eval/ask_margin_cv_41.py`): grid {0, 50, 100, 200, 300, 500} dollars. For each of batches 1 to 4 held out, the ridge is fitted on the other three, a provider is asked if predicted value > m, "
          "and the realized value is the sum of the stored ask-everyone (D7) net values of those asked. Score 4.0 per seed (ten seeds per batch):", "",
          "| m | fold B1 | fold B2 | fold B3 | fold B4 | mean | asks (of 880 listed in all) |", "|---|---|---|---|---|---|---|"]
    for m in cv["grid"]:
        v = cv["per_seed_by_fold"][str(m)]
        L.append(f"| {m} | " + " | ".join(f"{x:,.0f}" for x in v) + f" | {st.mean(v):,.0f} | {sum(cv['asks_by_fold'][str(m)])} |")
    L += ["", f"Chosen m = ${cv['chosen']} (best mean, ties to the smaller). It beats m = 0 by only $%d per seed, which is far inside the fold-to-fold swing (about $1,800), so the CV does not show that any margin helps; larger margins do worse." % round(cv["mean"][str(cv["chosen"])] - cv["mean"]["0"]), "",
          "**H14 against H8**, paired per seed:", ""]
    for seeds, tag in ((sum(pool.BATCHES[:4], []), "batches 1 to 4 (the margin was chosen on these; the ridge is in sample for both)"), (sum(pool.BATCHES[4:6], []), "batches 5 and 6 (out of sample for both)"), (sum(pool.BATCHES[:6], []), "all six batches")):
        L.append("- " + wl.line(wl.compare("H14", "H8", seeds), "H14", "H8") + f" ({tag}).")
    d14 = json.load(open(os.path.join(wl.CACHE_DIR, "H14.json")))
    L += ["", "Per seed means, H14 against H8 (components of score 4.0):", "", "| Seeds | Version | Score | Rounds | Found | Honest called | Recovered | Staff cost |", "|---|---|---|---|---|---|---|---|"]
    for lab, seeds in (("Batches 1 to 4", sum(pool.BATCHES[:4], [])), ("Batches 5 and 6", sum(pool.BATCHES[4:6], []))):
        for n, d in (("H8", d8), ("H14", d14)):
            g = lambda k: st.mean(d[str(x)][k] for x in seeds)
            L.append(f"| {lab} | {n} | {g('score'):,.0f} | {g('rounds'):.1f} | {g('found'):.2f} | {g('honest_called'):.2f} | {g('recovered'):,.0f} | {g('staff_cost'):,.0f} |")
    diff = lambda seeds: sum(d8[str(x)]["score"] != d14[str(x)]["score"] for x in seeds)
    L += ["", "## Reading of H14", "",
          "- **H14 is rejected.** Out of sample (batches 5 and 6) the difference is -$12 per seed with a standard deviation of $241 (better on 2 of 20 seeds, the rest equal or worse; one-sided p = 0.62). In sample (batches 1 to 4) it is +$51 (p = 0.076), which is not out of sample and does not clear the bar either.",
          f"- The margin barely changes what is asked: H14's run differs from H8's on {diff(sum(pool.BATCHES[4:6], []))} of 20 seeds in batches 5 and 6 and {diff(sum(pool.BATCHES[:4], []))} of 40 in batches 1 to 4, and rounds fall from 230 to 208 over 40 seeds (118 to 112 over 20). The providers just above zero are few, and removing them moves the score less than the batch noise.",
          "- The bar: with H13 and H14 tried, the Bonferroni alpha is 0.025 per look. H14's out-of-sample p is 0.62 and its in-sample p 0.076; neither clears 0.025.",
          "- Against doing nothing: both H8 and H14 are above zero on the pooled batches 5 and 6 (H8 +$719, H14 +$707 per seed), but this comes from batch 5 (H8 +$1,483, H14 +$1,459); batch 6 is -$46 for both. Per-batch swings of +/-$1,450 mean this is not a reliable lead over zero, and on ten fresh seeds H8 scored -$1,161. This is an inference from six batches, not a test of H14.",
          "- What this leaves: the loss is in the staff cost of asking that the ask model cannot tell apart by a small margin; the ask model's predictions are too weak to separate good asks from bad ones at the edge. Nothing here changes workflow v4.0."]
    L += more_sections()
    L += h20c_section()
    open(os.path.join(ROOT, "docs", "w_loop_v41.md"), "w").write("\n".join(L) + "\n")
    print("wrote docs/w_loop_v41.md")


if __name__ == "__main__":
    main()
