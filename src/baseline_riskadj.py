"""Baseline 2: risk-adjusted observed vs expected 99215 share.

For every visit, a pooled logistic model predicts P(billed 99215) from the
patient's chronic-condition count. A provider's expected 99215 count is the sum
of those probabilities over their visits (so it reflects visit-weighted panel
complexity). The score is (observed - expected) / sqrt(variance), then rescaled
by the robust spread across providers, because legitimate provider-to-provider
differences make the raw binomial z too wide (overdispersion).

Reads only agent-visible files (claims.csv, patients.csv). Never touches ground
truth. Caveat: in the synthetic data billed level depends on complexity by
construction, so this baseline is helped by how the data was built.

Usage:
    python src/baseline_riskadj.py DATA_DIR OUT_CSV [--top-n 25] [--no-trim]
"""
import argparse
import csv
import os
from collections import defaultdict

import numpy as np

TARGET_CODE = "99215"
MAX_COUNT = 6          # chronic counts above this share one category
TRIM_Z = 3.0           # pass 2 drops providers with raw z above this from the fit


def load(data_dir):
    chronic = {}
    with open(os.path.join(data_dir, "patients.csv")) as f:
        for r in csv.DictReader(f):
            chronic[r["patient_id"]] = min(int(r["chronic_condition_count"]), MAX_COUNT)
    prov, cat, y = [], [], []
    with open(os.path.join(data_dir, "claims.csv")) as f:
        for r in csv.DictReader(f):
            prov.append(r["provider_id"])
            cat.append(chronic[r["patient_id"]])
            y.append(1.0 if r["cpt"] == TARGET_CODE else 0.0)
    return np.array(prov), np.array(cat), np.array(y)


def design(cat):
    X = np.zeros((len(cat), MAX_COUNT + 1))
    X[np.arange(len(cat)), cat] = 1.0   # one intercept per chronic-count category
    return X


def fit_logistic(X, y, iters=50):
    """IRLS logistic regression; tiny ridge keeps empty categories finite."""
    beta = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ beta))
        W = p * (1 - p)
        H = (X * W[:, None]).T @ X + 1e-6 * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p) - 1e-6 * beta)
        beta += step
        if np.abs(step).max() < 1e-9:
            break
    return beta


def provider_scores(prov, p, y):
    out = {}
    for pid in np.unique(prov):
        m = prov == pid
        obs, exp, var = y[m].sum(), p[m].sum(), (p[m] * (1 - p[m])).sum()
        out[pid] = {"n_claims": int(m.sum()), "n_99215": int(obs), "expected": exp,
                    "z_raw": (obs - exp) / np.sqrt(var)}
    return out


def rank(data_dir, top_n=25, trim=True):
    prov, cat, y = load(data_dir)
    X = design(cat)
    keep = np.ones(len(y), bool)
    beta = fit_logistic(X, y)
    p = 1 / (1 + np.exp(-X @ beta))
    scores = provider_scores(prov, p, y)
    if trim:  # refit without extreme providers so outliers do not pull the model toward themselves
        drop = {k for k, v in scores.items() if v["z_raw"] > TRIM_Z}
        keep = ~np.isin(prov, list(drop))
        beta = fit_logistic(X[keep], y[keep])
        p = 1 / (1 + np.exp(-X @ beta))
        scores = provider_scores(prov, p, y)
    z = np.array([v["z_raw"] for v in scores.values()])
    center = np.median(z)
    scale = 1.4826 * np.median(np.abs(z - center))   # robust sd across providers
    rows = []
    for pid, v in scores.items():
        rows.append({
            "provider_id": pid, "n_claims": v["n_claims"], "n_99215": v["n_99215"],
            "share_99215": round(v["n_99215"] / v["n_claims"], 5),
            "expected_share": round(v["expected"] / v["n_claims"], 5),
            "z_raw": round(v["z_raw"], 4),
            "z_adj": round((v["z_raw"] - center) / scale, 4),
        })
    rows.sort(key=lambda r: (-r["z_adj"], r["provider_id"]))
    for i, r in enumerate(rows, 1):
        r["rank"], r["flagged"] = i, i <= top_n
    return rows, beta, scale


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir")
    ap.add_argument("out_csv")
    ap.add_argument("--top-n", type=int, default=25)
    ap.add_argument("--no-trim", action="store_true")
    a = ap.parse_args()
    rows, beta, scale = rank(a.data_dir, a.top_n, trim=not a.no_trim)
    os.makedirs(os.path.dirname(os.path.abspath(a.out_csv)), exist_ok=True)
    with open(a.out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["rank", "provider_id", "n_claims", "n_99215", "share_99215",
                                          "expected_share", "z_raw", "z_adj", "flagged"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} providers; robust spread of raw z = {scale:.2f}; top {a.top_n} flagged -> {a.out_csv}")
