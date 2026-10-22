"""Fit workflow v4.1's ask-or-skip (issue 132, hypothesis H13): the same ridge regression as fit_ask_40.py, on the same ask-everyone run (D7) and the same seeds, but with ask features built on the
eb_upper_t screen (policy_40.ask_vector_41) instead of the 99215-only ones. Free. Usage: python eval/fit_ask_41.py OUT.json BATCH [BATCH ...]"""
import csv
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v4 as pool  # noqa: E402
import policy_40 as pol  # noqa: E402
import score_40 as s4  # noqa: E402

LAM = 3.0


def table(batches):
    rows = []
    for b in batches:
        for seed in pool.BATCHES[b - 1]:
            code = f"d4_{seed}"
            claims = {}
            for r in csv.DictReader(open(os.path.join(ROOT, "data", f"synthetic_v2_{code}", "view", "claims.csv"))):
                claims.setdefault(r["provider_id"], []).append(r)
            flags = {r["provider_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "experiments", code, "flagged_eb_upper_t_10.csv"))) if r["flagged"] == "True"}
            pp = s4.per_provider(f"wld7_{seed}", code)
            for pid, fr in flags.items():
                rows.append({"seed": seed, "x": pol.ask_vector_41(fr, claims.get(pid, [])), "net": pp[pid]["net"] if pid in pp else 0.0})
    return rows


def fit(batches):
    rows = table(batches)
    X, y = np.array([r["x"] for r in rows]), np.array([r["net"] for r in rows])
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    beta = np.linalg.solve(Z.T @ Z + LAM * np.eye(Z.shape[1]), Z.T @ y)
    return {"unit": "dollars, score 4.0 net value of asking one listed provider (staff-hours cost and abrasion included, triage excluded)", "features_version": "4.1", "features": pol.ASK_FEATURES_41,
            "mu": mu.tolist(), "sd": sd.tolist(), "beta": beta.tolist(), "lambda": LAM, "fit_on_batches": batches, "fit_on_seeds": sorted({r["seed"] for r in rows}), "providers": len(rows)}


if __name__ == "__main__":
    out = fit([int(b) for b in sys.argv[2:]])
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    print("wrote", sys.argv[1], "fitted on", out["providers"], "providers from", len(out["fit_on_seeds"]), "seeds; beta", [round(b) for b in out["beta"]])
