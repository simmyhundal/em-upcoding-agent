"""Fit workflow v4.0's ask-or-skip on score 4.0 (issue 131, hypothesis H8): a ridge regression of each listed provider's net value of being asked (recovered minus staff-hours cost minus abrasion,
from the ask-everyone diagnostic run D7 with the demand floor) on what the payer sees before asking (policy_25.ask_vector: rank, log ratio, excess claims, log claims, screen score, adjusted z).
Ask when the predicted value is above zero. Writes the model as JSON (mu, sd, beta, the seeds it was fitted on). Free. Usage: python eval/fit_ask_40.py OUT.json BATCH [BATCH ...]"""
import csv
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v4 as pool  # noqa: E402
import policy_25 as p25  # noqa: E402
import score_40 as s4  # noqa: E402

LAM = 3.0


def table(batches):
    rows = []
    for b in batches:
        for seed in pool.BATCHES[b - 1]:
            code = f"d4_{seed}"
            flags = {r["provider_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "experiments", code, "flagged_eb_upper_t_10.csv"))) if r["flagged"] == "True"}
            pp = s4.per_provider(f"wld7_{seed}", code)
            for pid, fr in flags.items():
                rows.append({"seed": seed, "x": p25.ask_vector(fr), "net": pp[pid]["net"] if pid in pp else 0.0})
    return rows


def fit(batches):
    rows = table(batches)
    X, y = np.array([r["x"] for r in rows]), np.array([r["net"] for r in rows])
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    beta = np.linalg.solve(Z.T @ Z + LAM * np.eye(Z.shape[1]), Z.T @ y)
    return {"unit": "dollars, score 4.0 net value of asking one listed provider (staff-hours cost and abrasion included, triage excluded)", "features": p25.ASK_FEATURES, "mu": mu.tolist(), "sd": sd.tolist(),
            "beta": beta.tolist(), "lambda": LAM, "fit_on_batches": batches, "fit_on_seeds": sorted({r["seed"] for r in rows}), "providers": len(rows)}


if __name__ == "__main__":
    out = fit([int(b) for b in sys.argv[2:]])
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    print("wrote", sys.argv[1], "fitted on", out["providers"], "providers from", len(out["fit_on_seeds"]), "seeds")
