"""Fit the W2.5 policy (ask-or-skip and stop-or-escalate on net dollars) on ALL 30 development seeds and write src/policy_25.json (issue 109). Free.

Usage: python eval/export_policy_25.py
"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import release5_train as tr  # noqa: E402
import rl_ask_policy as rl1  # noqa: E402
import rl_escalate_policy as r2  # noqa: E402


def ridge(X, y):
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    beta = np.linalg.solve(Z.T @ Z + 1.0 * np.eye(Z.shape[1]), Z.T @ y)
    return {"mu": [float(v) for v in mu], "sd": [float(v) for v in sd], "beta": [float(v) for v in beta]}


def fit_policy(rows):
    X = r2.matrix(rows)
    branches = {b: ridge(X, np.array([r[b]["dollars"] for r in rows]) / 1000.0) for b in r2.BRANCHES}
    pred = {b: np.column_stack([np.ones(len(X)), (X - np.array(branches[b]["mu"])) / np.array(branches[b]["sd"])]) @ np.array(branches[b]["beta"]) for b in r2.BRANCHES}
    best = [max(r2.BRANCHES, key=lambda b: pred[b][i]) for i in range(len(rows))]
    ask = ridge(rl1.matrix(rows), np.array([r[b]["dollars"] for r, b in zip(rows, best)]) / 1000.0)
    return {"unit": "thousands of dollars, option 2 lower bound", "ask_features": rl1.FEATURES, "state": r2.STATE, "ask": ask, "branches": branches,
            "fit_on_seeds": sorted({r["seed"] for r in rows}), "providers": len(rows)}


def main():
    out = fit_policy(json.load(open(tr.DATA)))
    path = os.path.join(ROOT, "src", "policy_25.json")
    json.dump(out, open(path, "w"), indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()
