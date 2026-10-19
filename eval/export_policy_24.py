"""Fit the Stage 2 policy on ALL 20 development seeds at the pre-registered lambda and write src/policy_24.json (issue 108). Free.

lambda rule (fixed on issue 108 before the fresh test): among the grid values for which the leave-seeds-out result is at least the hand-set rule on upcoders found and no worse
on honest doctors called and honest rounds, take the one finding the most upcoders: 0.05 (docs/rl_escalate_policy.md).

Usage: python eval/export_policy_24.py
"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import baseline_riskadj as ra  # noqa: E402
import rl_escalate_policy as r2  # noqa: E402

LAMBDA, KAPPA = 0.05, 1.0


def logit_coef(Z, y):
    if y.sum() == 0 or y.sum() == len(y):
        return [20.0 * (1 if y.mean() > 0.5 else -1)] + [0.0] * (Z.shape[1] - 1)
    return [float(b) for b in ra.fit_logistic(Z, y.astype(float))]


def fit_policy(rows, lam=LAMBDA):
    """The policy dict (the JSON content) fitted on `rows` of the Stage 2 dataset."""
    X = r2.matrix(rows)
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    out = {"features": r2.STATE, "mu": [float(v) for v in mu], "sd": [float(v) for v in sd], "lambda": lam, "kappa": KAPPA,
           "fit_on_seeds": sorted({r["seed"] for r in rows}), "providers": len(rows),
           "honest": logit_coef(Z, np.array([not r["upcoder"] for r in rows])), "branches": {}}
    for b in r2.BRANCHES:
        extra = np.array([r[b]["rounds"] - r["STOP"]["rounds"] for r in rows], float)
        ridge = np.linalg.solve(Z.T @ Z + 1.0 * np.eye(Z.shape[1]), Z.T @ extra)
        out["branches"][b] = {"found": logit_coef(Z, np.array([r[b]["found"] for r in rows])), "hc": logit_coef(Z, np.array([r[b]["honest_called"] for r in rows])),
                              "extra": [float(v) for v in ridge]}
    return out


def main():
    out = fit_policy(json.load(open(r2.DATA)))
    path = os.path.join(ROOT, "src", "policy_24.json")
    json.dump(out, open(path, "w"), indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()
