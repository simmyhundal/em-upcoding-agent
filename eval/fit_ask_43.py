"""Fit workflow v4.3's ask-or-skip (hypothesis H33): the ridge regression of eval/fit_ask_41.py, on the ask-everyone run D7 on data 4.3 development seeds, with the target scored by score 4.3
(collected value of the demand after the appeal reduction and collection rate, staff cost incl. appeal handling, abrasion; triage excluded). Free. Usage: python eval/fit_ask_43.py OUT.json BATCH [BATCH ...]"""
import csv
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v43 as pool  # noqa: E402
import policy_40 as pol  # noqa: E402
import recovery_43 as r43  # noqa: E402
import score_40 as s4  # noqa: E402
import score_43 as s43  # noqa: E402

LAM = 3.0


def per_provider(rid, code, p=None):
    """score 4.3 split by provider for a level-only run: {pid: net dollars of asking this provider}"""
    p = p or r43.params43()
    claims, key, rate = s43.context(code)
    i = s4.run_inputs(rid, code)
    nr = __import__("score_42").no_record_ids(rid)
    out = {}
    for pid in set(i["rounds"]) | i["called"]:
        called = pid in i["called"]
        referral = bool(nr.get(pid))
        lb = r43.recovery(claims.get(pid, []), i["random"].get(pid, set()), i["level"], p, no_record=nr.get(pid, frozenset()))["value"] if called else 0.0
        got = r43.collected(lb, p, referral=referral)
        rounds, charts = i["rounds"].get(pid, 0), i["charts"].get(pid, 0)
        staff = r43.staff_cost(0, rounds, charts, 1 if called and not referral else 0, 1 if called and referral else 0, 0.0, p)[0]
        abr = s4.abrasion_weight(rate.get(pid, 0.0), p) * (rounds * p["C_BURDEN"] + (p["C_DEMAND_ABRASION"] if called else 0.0))
        out[pid] = got - staff - abr
    return out


def table(batches):
    rows = []
    for b in batches:
        for seed in pool.BATCHES[b - 1]:
            code = f"d43_{seed}"
            claims = {}
            for r in csv.DictReader(open(os.path.join(ROOT, "data", f"synthetic_v2_{code}", "view", "claims.csv"))):
                claims.setdefault(r["provider_id"], []).append(r)
            flags = {r["provider_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "experiments", code, "flagged_eb_upper_t_10.csv"))) if r["flagged"] == "True"}
            pp = per_provider(f"d43wld7_{seed}", code)
            for pid, fr in flags.items():
                rows.append({"seed": seed, "x": pol.ask_vector_41(fr, claims.get(pid, [])), "net": pp.get(pid, 0.0)})
    return rows


def fit(batches):
    rows = table(batches)
    X, y = np.array([r["x"] for r in rows]), np.array([r["net"] for r in rows])
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    beta = np.linalg.solve(Z.T @ Z + LAM * np.eye(Z.shape[1]), Z.T @ y)
    return {"unit": "dollars, score 4.3 net value of asking one listed provider (staff-hours cost, appeal handling and abrasion included, triage excluded)", "features_version": "4.1", "features": pol.ASK_FEATURES_41,
            "mu": mu.tolist(), "sd": sd.tolist(), "beta": beta.tolist(), "lambda": LAM, "fit_on_batches": batches, "fit_on_seeds": sorted({r["seed"] for r in rows}), "providers": len(rows), "mean_net": float(y.mean())}


if __name__ == "__main__":
    out = fit([int(b) for b in sys.argv[2:]])
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    print("wrote", sys.argv[1], "providers", out["providers"], "mean net", round(out["mean_net"]), "beta", [round(b) for b in out["beta"]])
