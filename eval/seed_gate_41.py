"""H19 (workflow v4.1, issue 132): a seed-level gate. Free. Features (declared in advance, eval/w_loop_v41_decl.py): (1) mean screen score of the listed providers, (2) mean screen score of ranks 1 to 5 minus
that of ranks 6 to 22, (3) log total allowed dollars on the listed providers' claims. Ridge lambda 10 (intercept free) to H8's score 4.0 per seed on batches 1 to 4; skip a seed (score 0) when the
predicted score is below 0. Reports leave-one-batch-out R-squared on batches 1 to 4 first, applies the gate to batches 5 and 6, writes experiments/w_loop/H19.json (zeros on gated seeds, H8's values elsewhere)."""
import csv
import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v4 as pool  # noqa: E402
import w_loop as wl  # noqa: E402

LAM = 10.0


def features(seed):
    code = f"d4_{seed}"
    rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "experiments", code, "flagged_eb_upper_t_10.csv"))) if r["flagged"] == "True"]
    rows.sort(key=lambda r: int(r["rank"]))
    sc = [float(r["screen_score"]) for r in rows]
    ids = {r["provider_id"] for r in rows}
    dollars = sum(float(r["allowed_amount"]) for r in csv.DictReader(open(os.path.join(ROOT, "data", f"synthetic_v2_{code}", "view", "claims.csv"))) if r["provider_id"] in ids)
    return [float(np.mean(sc)), float(np.mean(sc[:5]) - np.mean(sc[5:])), math.log(dollars)]


def ridge(X, y):
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    pen = LAM * np.eye(Z.shape[1])
    pen[0, 0] = 0
    return mu, sd, np.linalg.solve(Z.T @ Z + pen, Z.T @ y)


def predict(m, X):
    mu, sd, b = m
    return b[0] + ((X - mu) / sd) @ b[1:]


def main():
    h8 = json.load(open(os.path.join(wl.CACHE_DIR, "H8.json")))
    b14, b56 = sum(pool.BATCHES[:4], []), sum(pool.BATCHES[4:6], [])
    X = {s: features(s) for s in b14 + b56}
    y = {s: h8[str(s)]["score"] for s in b14 + b56}
    A = np.array([X[s] for s in b14])
    Y = np.array([y[s] for s in b14])
    oof = np.zeros(len(b14))
    for f in range(4):
        te = np.arange(len(b14)) // 10 == f
        oof[te] = predict(ridge(A[~te], Y[~te]), A[te])
    r2 = 1 - ((Y - oof) ** 2).sum() / ((Y - Y.mean()) ** 2).sum()
    # R-squared against the training mean of the other batches (the fair null), computed fold by fold
    null = np.zeros(len(b14))
    for f in range(4):
        te = np.arange(len(b14)) // 10 == f
        null[te] = Y[~te].mean()
    r2_null = 1 - ((Y - oof) ** 2).sum() / ((Y - null) ** 2).sum()
    m = ridge(A, Y)
    pred = {s: float(predict(m, np.array([X[s]]))[0]) for s in b14 + b56}
    skip = {s for s in b14 + b56 if pred[s] < 0}
    out = {}
    for s in b14 + b56:
        r = dict(h8[str(s)])
        if s in skip:
            r = {k: 0 for k in wl.KEEP}
        out[str(s)] = r
    json.dump(out, open(os.path.join(wl.CACHE_DIR, "H19.json"), "w"), indent=0)
    res = {"cv_r2_vs_zero_mean": r2, "cv_r2_vs_fold_training_mean": r2_null, "coef_standardized": m[2].tolist(), "skipped_b1to4": sum(s in skip for s in b14), "skipped_b5_6": sum(s in skip for s in b56),
           "corr_pred_actual_b5_6": float(np.corrcoef([pred[s] for s in b56], [y[s] for s in b56])[0, 1]),
           "skipped_b5_6_h8_mean_score": float(np.mean([y[s] for s in b56 if s in skip])) if any(s in skip for s in b56) else None,
           "kept_b5_6_h8_mean_score": float(np.mean([y[s] for s in b56 if s not in skip]))}
    json.dump(res, open(os.path.join(wl.CACHE_DIR, "H19_gate.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
