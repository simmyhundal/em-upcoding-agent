"""Indicators and screens on the data 4.0 development seeds (issue 127). Free: claims and patients only, no model; the answer key is read to score, never by a screen.

For every development seed (d4_42, d4_1515 ... d4_2424) and every candidate screen (src/screen_methods_v4.py, beside the frozen ones of screen_methods.py) report, pooled over seeds and
SPLIT BY HABIT: recall in the top 5% and top 10% of providers, ROC AUC of that habit's upcoders against honest providers, dollar-weighted capture of the true overpayment in the top 10%, and how
an upcoder ranks against honest providers with a comparable provider effect (the caution in issue 127: systematic upcoders carry a planted panel-acuity shift, so a screen that only finds
extreme providers could look good without detecting any upcoding). Rankers combine the indicators and are scored leave-one-seed-out. Writes docs/screens_v4.md and experiments/screens_v4_scores.json.

Usage: python eval/screens_v4_eval.py [--rescore]
"""
import json
import os
import sys
from collections import defaultdict

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import make_d4_dev as md  # noqa: E402
import screen_methods as sm  # noqa: E402
import screen_methods_v4 as sv4  # noqa: E402
import screen_metrics as smet  # noqa: E402

SCORES = os.path.join(ROOT, "experiments", "screens_v4_scores.json")
DOC = os.path.join(ROOT, "docs", "screens_v4.md")
FROZEN = ["riskadj", "eb_ratio", "level_z", "eb_upper"]
NEW = ["eb_upper_c", "eb_upper_t", "pay_resid", "excess_usd", "rich_level_t", "same_patient", "drift", "hi_no_test"]
ALL = ["eb_ratio_t"] + FROZEN + NEW
HABITS = ["systematic", "opportunistic", "template"]
MATCH_WIDTH = 0.25
K5, K10 = 11, 22


def score_seed(seed):
    view = os.path.join(ROOT, "data", f"synthetic_v2_d4_{seed}", "view")
    out = sv4.score_v4(view)
    old = sm.score_all(view)
    for k in FROZEN:
        out[k] = old[k]
    return {k: {p: float(v) for p, v in d.items()} for k, d in out.items()}


def load_scores(rescore=False):
    if os.path.exists(SCORES) and not rescore:
        return json.load(open(SCORES))
    import multiprocessing as mp
    with mp.get_context("spawn").Pool(4) as pool:
        res = pool.map(score_seed, md.SEEDS)
    data = {str(s): r for s, r in zip(md.SEEDS, res)}
    json.dump(data, open(SCORES, "w"))
    return data


import functools  # noqa: E402


@functools.lru_cache(maxsize=None)
def key_of(seed):
    return json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_d4_{seed}.json")))["providers"]


def pct_rank(d):
    """Within-seed percentile (0 to 1, ties averaged) of each provider's score."""
    pids = sorted(d)
    vals = np.array([d[p] for p in pids])
    order = vals.argsort(kind="mergesort")
    ranks = np.empty(len(vals))
    i = 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2
        i = j + 1
    return dict(zip(pids, ranks / (len(vals) - 1)))


def ridge_logit(X, y, lam=1.0, iters=60):
    beta = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(X @ beta, -30, 30)))
        W = p * (1 - p)
        H = (X * W[:, None]).T @ X + lam * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p) - lam * beta)
        beta += step
        if np.abs(step).max() < 1e-8:
            break
    return beta


def feature_matrix(scores, seed, names):
    ranks = {k: pct_rank(scores[str(seed)][k]) for k in names}
    pids = sorted(scores[str(seed)][names[0]])
    return pids, np.column_stack([np.ones(len(pids))] + [[ranks[k][p] for p in pids] for k in names])


def add_rankers(scores):
    """Leave-one-seed-out logistic rankers over the within-seed percentile of each indicator: 'ranker_all' (every indicator), 'ranker_new' (the new ones only, no 99215 or level indicators)."""
    sets = {"ranker_all": ALL, "ranker_new": ["eb_ratio_t"] + NEW}
    for name, feats in sets.items():
        data = {s: feature_matrix(scores, s, feats) for s in scores}
        lab = {s: np.array([key_of(s)[p]["role"] == "upcoder" for p in data[s][0]], float) for s in data}
        for held in scores:
            X = np.vstack([data[s][1] for s in data if s != held])
            y = np.concatenate([lab[s] for s in data if s != held])
            beta = ridge_logit(X, y)
            pids, Xh = data[held]
            z = Xh @ beta
            scores[held][name] = dict(zip(pids, z.tolist()))
    return scores


def evaluate(scores):
    names = list(scores[next(iter(scores))])
    res = {n: {"pos": defaultdict(lambda: [0, 0, 0]), "auprc": [], "match": defaultdict(list), "rank_pct": defaultdict(list), "cap": [0.0, 0.0], "honest10": 0,
               "noisy10": 0, "list_p": []} for n in names}
    for s, sc in scores.items():
        K = key_of(s)
        pids = sorted(K)
        honest = [p for p in pids if K[p]["role"] != "upcoder"]
        for n in names:
            d = sc[n]
            order = sorted(pids, key=lambda p: (-d[p], p))
            top10, top5 = set(order[:K10]), set(order[:K5])
            pr = pct_rank(d)
            r = res[n]
            r["auprc"].append(smet.average_precision([d[p] for p in pids], [K[p]["role"] == "upcoder" for p in pids]))
            for p in pids:
                v = K[p]
                if v["role"] == "upcoder":
                    h = v["habit"] + (" (cloner)" if v["clones_notes"] else "")
                    for hh in {v["habit"], "all", h}:
                        c = r["pos"][hh]
                        c[0] += p in top5
                        c[1] += p in top10
                        c[2] += 1
                    r["rank_pct"][v["habit"]].append(pr[p])
                    r["rank_pct"]["all"].append(pr[p])
                    near = [q for q in honest if abs(K[q]["provider_effect"] - v["provider_effect"]) <= MATCH_WIDTH]
                    if len(near) >= 5:
                        below = sum((pr[q] < pr[p]) + 0.5 * (pr[q] == pr[p]) for q in near) / len(near)
                        r["match"][v["habit"]].append(below)
                        r["match"]["all"].append(below)
                    r["cap"][1] += v["true_overpay_gross"]
                    r["cap"][0] += v["true_overpay_gross"] * (p in top10)
            r["honest10"] += sum(p in top10 for p in honest)
            r["noisy10"] += sum(1 for p in honest if p in top10 and K[p]["net_rate"] >= 0.15)
    return res


def auc_by_habit(scores, names):
    """Pooled ROC AUC of one habit's upcoders against all honest providers, on within-seed percentile scores."""
    out = {n: {} for n in names}
    for n in names:
        for h in HABITS + ["all"]:
            pos, neg = [], []
            for s, sc in scores.items():
                K = key_of(s)
                pr = pct_rank(sc[n])
                for p, v in K.items():
                    if v["role"] == "upcoder" and (h == "all" or v["habit"] == h):
                        pos.append(pr[p])
                    elif v["role"] != "upcoder":
                        neg.append(pr[p])
            out[n][h] = smet.roc_auc(pos + neg, [1] * len(pos) + [0] * len(neg))
    return out


def main():
    scores = add_rankers(load_scores("--rescore" in sys.argv))
    names = ["eb_ratio_t"] + FROZEN + NEW + ["ranker_new", "ranker_all"]
    res = evaluate(scores)
    auc = auc_by_habit(scores, names)
    n_seed = len(scores)
    totals = {h: res["eb_ratio_t"]["pos"][h][2] for h in HABITS + ["all"]}
    L = ["# Indicators and screens on data 4.0 (issue 127)", "", "[Back to the README](../README.md) · [data 4.0](data_v4_0.md) · [the v4/v5 plan](v4_v5_plan.md)", "",
         f"Generated by `python eval/screens_v4_eval.py`. **Free:** claims and patients only, no model. {n_seed} development seeds (d4_42, d4_1515 to d4_2424; 216 providers each, 8 planted upcoders: "
         f"{totals['systematic']} systematic, {totals['opportunistic']} opportunistic, {totals['template']} template-driven). Screens are built beside the frozen ones (`src/screen_methods_v4.py`); rankers are fitted leave-one-seed-out. "
         "**Confirm only on fresh seeds (5555 and above), never here.** Easier by construction: the generator plants the habits these indicators look for, draws the lab line from the true complexity, and gives systematic "
         "upcoders an atypical panel (see the matched-provider column).", "",
         "## Recall in the top 10% of providers (22 of 216), by habit", "", "| Screen | All upcoders | Systematic | Opportunistic | Template-driven | Honest in list | AUPRC | Dollar-weighted capture |", "|---|---|---|---|---|---|---|---|"]
    for n in names:
        r = res[n]
        cells = [f"{r['pos'][h][1]} of {r['pos'][h][2]} ({r['pos'][h][1] / max(r['pos'][h][2], 1):.0%})" for h in ["all"] + HABITS]
        L.append(f"| {n} | " + " | ".join(cells) + f" | {r['honest10']} | {np.mean(r['auprc']):.3f} | {r['cap'][0] / max(r['cap'][1], 1):.0%} |")
    L += ["", "Top 5% of providers (11 of 216), recall by habit:", "", "| Screen | All | Systematic | Opportunistic | Template-driven |", "|---|---|---|---|---|"]
    for n in names:
        r = res[n]
        L.append(f"| {n} | " + " | ".join(f"{r['pos'][h][0] / max(r['pos'][h][2], 1):.0%}" for h in ["all"] + HABITS) + " |")
    L += ["", "## Does the gain survive against honest providers with a similar provider effect? (the systematic caution)", "",
          f"For each upcoder, the share of honest providers in the same seed whose provider effect lies within {MATCH_WIDTH} of its own that it outscores (0.5 = no better than chance, 1 = always). "
          "ROC AUC is the habit's upcoders against all honest providers. A systematic upcoder's effect is its generator draw plus the planted panel shift; honest providers carry only their draw.", "",
          "| Screen | ROC AUC: systematic | opportunistic | template | Outscores effect-matched honest: systematic | opportunistic | template |", "|---|---|---|---|---|---|---|"]
    for n in names:
        r = res[n]
        L.append(f"| {n} | " + " | ".join(f"{auc[n][h]:.2f}" for h in HABITS) + " | " + " | ".join(f"{np.mean(r['match'][h]):.2f}" if r["match"][h] else "-" for h in HABITS) + " |")
    def rec(n, h="all"):
        c = res[n]["pos"][h]
        return f"{c[1]} of {c[2]} ({c[1] / max(c[2], 1):.0%})"
    L += ["", "## Reading", "",
          f"- **The frozen screen cannot see the habits.** `eb_ratio_t` (the 99215 share against expected, used by workflow v2.3 to v2.5 and agent v3.3 to v3.5) lists {rec('eb_ratio_t')} of the upcoders in its top 10%: "
          f"{rec('eb_ratio_t', 'systematic')} systematic, {rec('eb_ratio_t', 'opportunistic')} opportunistic, {rec('eb_ratio_t', 'template')} template-driven. Opportunistic upcoders reach 99215 from 99214 at the borderline, so the 99215 share moves; the other habits do not move it.",
          f"- **A whole-distribution indicator at the 99214 boundary finds them.** `eb_upper_t` (the shrunk share billed 99214 or 99215 against what the patient mix and the test line predict) lists {rec('eb_upper_t')}: "
          f"{rec('eb_upper_t', 'systematic')} systematic, {rec('eb_upper_t', 'opportunistic')} opportunistic, {rec('eb_upper_t', 'template')} template-driven, and holds {res['eb_upper_t']['cap'][0] / res['eb_upper_t']['cap'][1]:.0%} of the true overpayment dollars. "
          f"Without the test line (`eb_upper_c`, count only) it is {rec('eb_upper_c')}; the gap between them is the lab link below.",
          "- **The systematic caution holds up.** Against honest providers whose provider effect is within 0.25 of the upcoder's own, the best indicators outscore nearly all of them (table above), so the systematic gain is not only the planted panel shift. "
          "The 99215-share screens, by contrast, rank systematic upcoders no better than chance (AUC about 0.5).",
          f"- **By construction.** The generator draws a visit's lab line from the TRUE complexity (a lab is 90% likely when the true data element is high, 10% otherwise). `hi_no_test` (high level with nothing after it) therefore finds {rec('hi_no_test')}: a planted covariate, not evidence "
          "that real claims behave so. Every indicator that uses the test line (`eb_upper_t`, `pay_resid`, `drift`, `rich_level_t`, the rankers) leans on it; `eb_upper_c`, `level_z` and `same_patient` do not (`same_patient` also needs shared patients, 35% of members here).",
          f"- **Other indicators.** `same_patient` is strong for systematic ({rec('same_patient', 'systematic')}) and weak for opportunistic ({rec('same_patient', 'opportunistic')}); `drift` finds template-driven upcoders ({rec('drift', 'template')}, whose selection skews late) and little else; "
          f"`excess_usd` (dollars, not rate) is {rec('excess_usd')} because it rewards big panels, though it holds {res['excess_usd']['cap'][0] / res['excess_usd']['cap'][1]:.0%} of the dollars. Group-level scoring is not possible: the detector view carries no tax ID.",
          f"- **Rankers** (logistic over the indicators' percentiles, leave-one-seed-out): `ranker_new` {rec('ranker_new')}, `ranker_all` {rec('ranker_all')}. They are fitted on the planted labels of the development seeds (a stand-in for past audits), so they need real audit outcomes before they mean anything; not chosen.",
          "- **Not done here:** the issue's hierarchical model of P(effect > margin) is approximated by the empirical-Bayes shrinkage; unsupervised outlier scores and adaptive sampling of the records budget were not run (the second belongs to the arms in #128); a cutoff by expected net dollars is left to the ask policy.",
          "- **The list is not the bottleneck under today's rules.** [screens_v4_pipeline.md](screens_v4_pipeline.md) runs the frozen workflow v2.3 (API-free) on each list: better lists let it find more upcoders (from 3 of 88 to 16) but still few of the up to 81 listed, because the frozen rules and policy, fitted on 99215 evidence in data 2.2, "
          "were not built for these habits; it also calls more honest providers, and score 4.0 stays about the same (every row is negative). A v4.0 and v5.0 decision layer that reads the 99214 boundary is #128's work.", "",
          "## Chosen screen", "",
          "**`eb_upper_t`** is the default screen of the v4/v5 line (workflow `flagging.py --method eb_upper_t`; the agent's `screen_providers` gets it when agent v5.0 is built in #128): best recall and dollar capture among the indicators that do not need audit labels, "
          "and the same shrinkage and test-line lineage as `eb_ratio_t`, so it is a change of threshold (99214 instead of 99215) and not a new kind of score. Fallback if the lab link proves too strong: `eb_upper_c`. Confirm on fresh seeds only, in #128."]
    open(DOC, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
