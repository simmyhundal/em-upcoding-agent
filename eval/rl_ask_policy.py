"""Release 4, Stage 1 of the learning plan (issue 108): an offline contextual bandit for the workflow's ask-or-skip decision. Free (simulated office, rules 2.3, no model calls).

Data: the 20 development seeds (release 2 seeds 1515 to 2424 and release 3 seeds 2525 to 3434; data 2.2), the top-10% eb_ratio_t list of 22 providers per seed, workflow v2.3
run as is (every listed provider is asked, so the outcome of asking is observed for all 440 providers; the outcome of skipping is 0 by definition). Per provider:
features the payer sees before asking (rank, ratio of billed 99215 share to expected, excess 99215 claims, claim count, screen score, z_adj) and the outcome of asking
(upcoder found by rules 2.3, honest practice bothered, honest doctor called). The answer key supplies the outcome only; it is never a feature.

Policy: ask when  P(found | x) - lambda * P(honest | x) - kappa * P(honest called | x) > 0, with the three probabilities from small logistic models on standardized features
(kappa = 1). lambda is swept over a grid fixed here (0 to 1). Evaluated by leave-seeds-out cross-validation (5 folds of 4 seeds): each fold's providers are scored by
models fitted on the other 16 seeds. The comparison is the hand-set ratio gate (ask only if ratio >= t), on the same providers.

Usage: python eval/rl_ask_policy.py            (writes docs/rl_ask_policy.md and experiments/rl_ask_dataset.json)
"""
import json
import multiprocessing as mp
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import baseline_riskadj as ra  # noqa: E402
import case_summary as cs  # noqa: E402
import dev_release3 as dev3  # noqa: E402
import dev_release4 as dev4  # noqa: E402
import make_v2_office_workflow_runs as mw  # noqa: E402
import summary_rules as sr  # noqa: E402

LAMBDAS = [0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]
KAPPA = 1.0
FEATURES = ["rank", "log_ratio", "excess", "log_claims", "screen_score", "z_adj"]
DATA = os.path.join(ROOT, "experiments", "rl_ask_dataset.json")


def provider_rows(job):
    code_pre, seed = job
    src = f"{code_pre}_{seed}"
    name = dev3.write_flagged(src, "eb_ratio_t", 10)
    view, office, flagged_file = mw.build_view(f"rl{seed}", src, name, version="2.4", tier1_n=dev4.TIER1_N, policy24={})
    import csv
    flagged = {r["provider_id"]: r for r in csv.DictReader(open(flagged_file)) if r["flagged"] == "True"}
    out = cs.run(view, flagged_file, os.path.join("/tmp", f"rl{seed}.jsonl"), dry_run=True, rules="2.3")
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{src}.json")))["providers"]
    rows = []
    for o in out:
        pid = o["provider_id"]
        f = flagged[pid]
        exp, share, n = float(f["expected_share"]), float(f["share_99215"]), int(f["n_claims"])
        called = sr.rule_leaning_23(o["packet"])[0] == sr.UPCODING
        up = key[pid]["role"] == "upcoder"
        rows.append({"seed": seed, "set": code_pre, "pid": pid, "rank": int(f["rank"]), "ratio": share / exp if exp else 0.0, "excess": n * (share - exp), "claims": n,
                     "screen_score": float(f["screen_score"]), "z_adj": float(f["z_adj"]), "upcoder": up, "found": up and called, "honest_called": (not up) and called,
                     "rounds": office._st(pid)["round"]})
    return rows


def matrix(rows):
    X = np.array([[r["rank"], np.log(max(r["ratio"], 0.05)), r["excess"], np.log(r["claims"]), r["screen_score"], r["z_adj"]] for r in rows], float)
    return X


def fit(X, y):
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    if y.sum() == 0 or y.sum() == len(y):
        return lambda Xn: np.full(len(Xn), y.mean())
    beta = ra.fit_logistic(Z, y.astype(float))
    return lambda Xn: 1 / (1 + np.exp(-np.column_stack([np.ones(len(Xn)), (Xn - mu) / sd]) @ beta))


def cv_scores(rows, folds=5):
    seeds = sorted({r["seed"] for r in rows})
    fold_of = {s: i % folds for i, s in enumerate(seeds)}
    X = matrix(rows)
    f = np.array([fold_of[r["seed"]] for r in rows])
    p_found, p_hon, p_hc = np.zeros(len(rows)), np.zeros(len(rows)), np.zeros(len(rows))
    for k in range(folds):
        tr, te = f != k, f == k
        for target, out in (("found", p_found), ("honest", p_hon), ("honest_called", p_hc)):
            y = np.array([(not r["upcoder"]) if target == "honest" else r[target] for r in rows])
            out[te] = fit(X[tr], y[tr])(X[te])
    return p_found, p_hon, p_hc


def totals(rows, ask):
    return {"found": int(sum(r["found"] and a for r, a in zip(rows, ask))), "honest_asked": int(sum((not r["upcoder"]) and a for r, a in zip(rows, ask))),
            "honest_called": int(sum(r["honest_called"] and a for r, a in zip(rows, ask))), "asked": int(sum(ask))}


def main():
    if not os.path.exists(DATA):
        with mp.Pool(4) as pool:
            rows = [r for part in pool.map(provider_rows, dev4.SEEDS) for r in part]
        json.dump(rows, open(DATA, "w"))
    rows = json.load(open(DATA))
    pf, ph, phc = cv_scores(rows)
    base = totals(rows, [True] * len(rows))
    gates = {}
    for t in (2.5, 3.0, 3.5):
        gates[f"ratio >= {t:g} (light tier only)"] = totals(rows, [(r["rank"] <= dev4.TIER1_N) or r["ratio"] >= t for r in rows])
        gates[f"ratio >= {t:g} (whole list)"] = totals(rows, [r["ratio"] >= t for r in rows])
    learned = {lam: totals(rows, list(pf - lam * ph - KAPPA * phc > 0)) for lam in LAMBDAS}
    L = ["# Release 4, Stage 1: a learned ask-or-skip policy against the hand-set ratio gate (issue 108)", "", "[Back to the README](../README.md)", "",
         "Generated by `python eval/rl_ask_policy.py`. Free. 20 development seeds, 440 listed providers (22 per seed), data 2.2. Learned policy = offline contextual bandit "
         "(logistic estimates of the reward of asking, one-step reinforcement learning); every number for it is **leave-seeds-out cross-validated** (5 folds of 4 seeds). "
         "Hand-set gates have no fitted parameters here (their cutoffs were chosen on these seeds, see `dev_release4.md`). Features are payer-visible only; the answer key gives the reward.", "",
         f"Reference, ask everyone (workflow v2.3): {base['found']} upcoders found, {base['honest_asked']} honest practices asked, {base['honest_called']} honest doctors called.", "",
         "| Policy | Providers asked | Upcoders found | Honest practices asked | Honest doctors called | Honest asked per upcoder found |", "|---|---|---|---|---|---|"]
    for name, t in gates.items():
        L.append(f"| {name} | {t['asked']} | {t['found']} | {t['honest_asked']} | {t['honest_called']} | {t['honest_asked'] / max(t['found'], 1):.2f} |")
    for lam, t in learned.items():
        L.append(f"| learned, lambda = {lam:g} | {t['asked']} | {t['found']} | {t['honest_asked']} | {t['honest_called']} | {t['honest_asked'] / max(t['found'], 1):.2f} |")
    # dominance at matched burden
    L += ["", "## At matched burden", "", "| Hand-set gate | Honest asked | Found | Best learned policy with no more honest asked | Found |", "|---|---|---|---|---|"]
    for name, t in gates.items():
        ok = [(v["found"], lam) for lam, v in learned.items() if v["honest_asked"] <= t["honest_asked"]]
        best = max(ok) if ok else (0, None)
        L.append(f"| {name} | {t['honest_asked']} | {t['found']} | lambda = {best[1]} | {best[0]} |")
    L += ["", "## Reading", "",
          "- This is the simplest reinforcement-learning form (a one-step contextual bandit with a reward we can compute for both actions), chosen because the ask or skip decision has no hidden state "
          "beyond the screen features. It does not yet learn the follow-up and escalation decisions (Stage 2).",
          "- A learned policy that only matches the hand-set gate is still a result: it shows the gate is about as good as these features allow. One that beats it at matched burden is "
          "a hypothesis for the fresh test, not a finding.",
          "- Cross-validation here is by seed within development data that the hand-set gates were also chosen on; the fresh 10-seed test is the only unbiased comparison."]
    open(os.path.join(ROOT, "docs", "rl_ask_policy.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
