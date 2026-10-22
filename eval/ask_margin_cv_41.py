"""Workflow v4.1, hypothesis H14 (issue 132): choose the stop-loss margin m of the ask step by leave-one-batch-out cross-validation on batches 1 to 4 (batches 5 and 6 are not touched).
For each held-out batch the ridge of eval/fit_ask_40.py is fitted on the other three, and a listed provider is asked when the predicted value exceeds m; the realized value is the sum of the stored
ask-everyone (D7) net values of the providers asked (skipped providers cost and earn nothing). Free. Usage: python eval/ask_margin_cv_41.py [OUT.json]"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import fit_ask_40 as fa  # noqa: E402

GRID = [0, 50, 100, 200, 300, 500]


def cv():
    tabs = {b: fa.table([b]) for b in (1, 2, 3, 4)}
    res = {m: [] for m in GRID}
    asks = {m: [] for m in GRID}
    for hold in tabs:
        tr = [r for b in tabs if b != hold for r in tabs[b]]
        X, y = np.array([r["x"] for r in tr]), np.array([r["net"] for r in tr])
        mu, sd = X.mean(0), X.std(0) + 1e-9
        Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
        beta = np.linalg.solve(Z.T @ Z + fa.LAM * np.eye(Z.shape[1]), Z.T @ y)
        te = tabs[hold]
        pred = np.array([beta[0] + ((np.array(r["x"]) - mu) / sd) @ beta[1:] for r in te])
        net = np.array([r["net"] for r in te])
        for m in GRID:
            sel = pred > m
            res[m].append(float(net[sel].sum()) / 10)   # per seed (ten seeds per batch)
            asks[m].append(int(sel.sum()))
    return res, asks, {b: float(sum(r["net"] for r in tabs[b])) / 10 for b in tabs}


if __name__ == "__main__":
    res, asks, everyone = cv()
    best = max(GRID, key=lambda m: (np.mean(res[m]), -m))
    for m in GRID:
        print(m, [round(v) for v in res[m]], "mean", round(np.mean(res[m])), "asks", asks[m])
    print("ask everyone per seed by batch", {b: round(v) for b, v in everyone.items()}, "best", best)
    json.dump({"grid": GRID, "per_seed_by_fold": res, "asks_by_fold": asks, "mean": {m: float(np.mean(res[m])) for m in GRID}, "chosen": best}, open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "experiments", "w_loop", "ask_margin_cv.json"), "w"), indent=1)
