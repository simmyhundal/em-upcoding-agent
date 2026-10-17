"""Ranking metrics for the screen score (issue 83): AUPRC, ROC AUC and precision at K.

The screen produces a score for every provider, so its ranking can be judged across all cutoffs, not only at the top 25 or
at suspicion >= 5. Positives are the planted upcoders; hard-negative and normal providers are negatives. Evaluation only
(uses the answer key); the screen itself never sees it.

  * AUPRC is average precision: the sum over positives of (recall step) x (precision at that rank), the usual step-wise
    area under the precision-recall curve. A random ranking scores about the upcoder rate, so read it against that rate.
    Tied scores are treated as one block (the precision is taken after the whole block), as scikit-learn does.
  * ROC AUC is the chance that a random upcoder outscores a random honest doctor (ties count half). It can look excellent
    while most of the top flags are wrong when upcoders are rare, so it is secondary.
  * Precision at K is the share of the K highest scores that are upcoders; ties at the K-th place are broken by provider id
    so the number is reproducible.

Usage:
    python eval/screen_metrics.py            # print the table for the release-1 datasets
    python eval/screen_metrics.py --write    # also write docs/screen_metrics.md
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KS = (10, 25)


def average_precision(scores, labels):
    """Step-wise area under the precision-recall curve. Returns None when there are no positives."""
    pos = sum(labels)
    if pos == 0:
        return None
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    tp = seen = 0
    ap = 0.0
    i = 0
    while i < len(order):
        j = i
        while j < len(order) and scores[order[j]] == scores[order[i]]:
            j += 1
        block_pos = sum(labels[k] for k in order[i:j])
        seen += j - i
        tp += block_pos
        ap += (block_pos / pos) * (tp / seen)
        i = j
    return ap


def roc_auc(scores, labels):
    """Probability a random positive outscores a random negative (ties half). None unless both classes exist."""
    pos = [s for s, y in zip(scores, labels) if y]
    neg = [s for s, y in zip(scores, labels) if not y]
    if not pos or not neg:
        return None
    ranked = sorted(zip(scores, labels))
    # rank-sum with average ranks for ties
    rank_sum = 0.0
    i = 0
    while i < len(ranked):
        j = i
        while j < len(ranked) and ranked[j][0] == ranked[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2
        rank_sum += avg_rank * sum(y for _, y in ranked[i:j])
        i = j
    return (rank_sum - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


def precision_at_k(scores, labels, k, ids=None):
    """Share of the k highest scores that are positives; ties broken by id when given (else by position)."""
    ids = ids if ids is not None else list(range(len(scores)))
    order = sorted(range(len(scores)), key=lambda i: (-scores[i], str(ids[i])))
    top = order[:k]
    return sum(labels[i] for i in top) / len(top) if top else None


def recall_at_k(scores, labels, k, ids=None):
    pos = sum(labels)
    ids = ids if ids is not None else list(range(len(scores)))
    order = sorted(range(len(scores)), key=lambda i: (-scores[i], str(ids[i])))
    return sum(labels[i] for i in order[:k]) / pos if pos else None


def metrics(rows, truth, score_key="z_adj", ks=KS):
    """AUPRC, ROC AUC and precision at K for flagged-csv rows scored by `score_key`. Evaluation only."""
    ids = [r["provider_id"] for r in rows]
    scores = [float(r[score_key]) for r in rows]
    labels = [1 if truth["providers"][p]["role"] == "upcoder" else 0 for p in ids]
    out = {"auprc": average_precision(scores, labels), "roc_auc": roc_auc(scores, labels),
           "upcoder_rate": sum(labels) / len(labels)}
    for k in ks:
        out[f"p_at_{k}"] = precision_at_k(scores, labels, k, ids)
    return out


# --- the report -------------------------------------------------------------

RELEASE1 = ["x1_s42", "e404", "e505", "e606", "e707", "e808", "e909", "e1010", "e1111", "e1212", "e1313",
            "e1414_r05", "e1414_r1", "e1414_r2"]


def load_dataset(key, reg=None):
    reg = reg or json.load(open(os.path.join(ROOT, "experiments", "runs.json")))
    d = reg["datasets"][key]
    truth = json.load(open(os.path.join(ROOT, d["truth"])))
    rows = list(csv.DictReader(open(os.path.join(ROOT, d["flagged"]))))
    return rows, truth, d


def table(keys=RELEASE1):
    reg = json.load(open(os.path.join(ROOT, "experiments", "runs.json")))
    res = []
    for k in keys:
        rows, truth, d = load_dataset(k, reg)
        m = metrics(rows, truth)
        n_up = round(m["upcoder_rate"] * len(rows))
        res.append({"key": k, "seed": d["seed"], "providers": len(rows), "upcoders": n_up, **m})
    return res


def markdown(res):
    lines = ["| Dataset | Seed | Providers | Upcoders | Rate | AUPRC | AUPRC / rate | ROC AUC | Precision at 10 | Precision at 25 |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        lines.append(f"| {r['key']} | {r['seed']} | {r['providers']} | {r['upcoders']} | {r['upcoder_rate']:.1%} | {r['auprc']:.3f} "
                     f"| {r['auprc'] / r['upcoder_rate']:.1f}x | {r['roc_auc']:.3f} | {r['p_at_10']:.2f} | {r['p_at_25']:.2f} |")
    return "\n".join(lines)


def by_rate(res):
    groups = {}
    for r in res:
        groups.setdefault(round(r["upcoder_rate"], 3), []).append(r)
    lines = ["| Upcoder rate | Datasets | AUPRC (mean) | Random AUPRC (about the rate) | ROC AUC (mean) | Precision at 10 (mean) | Precision at 25 (mean) |",
             "|---|---|---|---|---|---|---|"]
    for rate in sorted(groups, reverse=True):
        g = groups[rate]
        mean = lambda k: sum(x[k] for x in g) / len(g)
        lines.append(f"| {rate:.1%} | {len(g)} | {mean('auprc'):.3f} | {rate:.3f} | {mean('roc_auc'):.3f} | {mean('p_at_10'):.2f} | {mean('p_at_25'):.2f} |")
    return "\n".join(lines)


def report():
    res = table()
    return ("# Screen ranking metrics (issue 83)\n\n[Back to the README](../README.md)\n\n"
            "Generated by `python eval/screen_metrics.py --write` from each dataset's `flagged.csv` (the risk-adjusted suspicion score, "
            "`z_adj`) and the answer key. Definitions are in `eval/screen_metrics.py`. The same four numbers are columns of "
            "`experiments/results.csv` for every screen row (`screen_auprc`, `screen_roc_auc`, `screen_p_at_10`, `screen_p_at_25`).\n\n"
            "Positives are planted upcoders; hard-negative and normal providers are negatives. **AUPRC** (average precision) is the headline "
            "for a rare-positive problem: a random ranking scores about the upcoder rate. **ROC AUC** is secondary: with few upcoders it can "
            "look excellent while most flags are wrong. **Precision at K** is the share of the K highest scores that are upcoders (K = 10 and "
            "25, the investigators' capacity). The workflow's and agent's final calls are yes or no, so they keep precision and recall.\n\n"
            "## By upcoder rate\n\n" + by_rate(res) + "\n\n## Per dataset (the 14 release-1 datasets)\n\n" + markdown(res) +
            "\n\n## How to read this\n\n"
            "- Precision at 25 is capped by the number of upcoders: with 8 upcoders in 216 doctors the best possible is 8/25 = 0.32, and "
            "with 3 upcoders it is 0.12. Precision at 10 is capped at 0.8 for 8 upcoders and 0.3 for 3. Read these against the cap, not "
            "against 1.0. Recall in the top 25 per screen method is in [screen_methods.md](screen_methods.md).\n"
            "- These datasets are all development data now (release 1 evaluated on them), and the screen was never tuned on them, but "
            "they are not fresh seeds.\n"
            "- In this synthetic data the billed level depends on patient complexity by construction, which flatters risk adjustment, and "
            "honest providers bill exactly the justified level (data 2.0 and 2.1), so every score here is easier than real claims. "
            "Issue 74 (data 2.2) adds honest coding noise.\n"
            "- One draw per dataset, 3 to 12 upcoders each: a difference of one doctor moves precision at 10 by 0.1. The low-rate rows "
            "(600 doctors) are single datasets.\n")


if __name__ == "__main__":
    res = table()
    print(by_rate(res))
    print()
    print(markdown(res))
    if "--write" in sys.argv:
        path = os.path.join(ROOT, "docs", "screen_metrics.md")
        open(path, "w").write(report())
        print("->", path)
