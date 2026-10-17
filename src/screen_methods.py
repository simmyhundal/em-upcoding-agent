"""Candidate screen methods for issue 88: score every provider so that every upcoder lands in the top 25.

`baseline_riskadj.py` (the screen of v2.1 and v3.1) stays frozen. These are alternatives built beside it, all free (claims
and patients only, no model, no answer key). Every method returns {provider_id: score}, higher = more suspicious.

  zscore       plain share z-score (reference; baseline_zscore.py)
  riskadj      risk-adjusted 99215 z_adj (reference; baseline_riskadj.py, frozen)
  priority     rank average of ratio to expected and excess 99215 claims (v3.1, docs/priority_score.md), from riskadj's expectation
  eb_ratio     empirical-Bayes (gamma-Poisson) posterior mean of observed / expected 99215: small panels are shrunk toward 1
  eb_prob      posterior probability that the true 99215 rate is more than EB_MARGIN times expected
  eb_excess    shrunk excess in claims: expected count x (posterior mean - 1)
  level_z      whole-distribution score: mean billed level (99211 to 99215) against the level expected from the patient's
               chronic-condition count, so upgrades into 99214 count too; trimmed fit and robust rescale like riskadj
  rich_logit   99215 logistic on patient-level features (each condition, age band, risk score, first visit with the provider),
               scored like riskadj
  rich_level   mean billed level on the same patient-level features (OLS), scored like level_z
  eb_upper     the same shrinkage on the share billed 99214 or 99215, so upgrades from 99213 to 99214 count
  eb_two       rank average of eb_ratio and eb_upper
  ensemble     rank average of riskadj, eb_ratio and level_z

Honesty notes. In the synthetic data a visit's justified level depends only on the member's true chronic-condition count plus
provider-level coding-style effects, and billed level follows it, so (a) risk adjustment is flattered, (b) patient-level
features beyond the count carry no extra signal (age is drawn from the count; new versus established is not modeled), and
(c) the provider-level style effects are the honest noise every method fights. Real claims will behave differently.

Reads only agent-visible files (claims.csv, patients.csv). Never touches the answer key.
"""
import csv
import math
import os
from collections import defaultdict

import numpy as np

import baseline_riskadj as ra

LEVELS = ["99211", "99212", "99213", "99214", "99215"]
MAX_COUNT = ra.MAX_COUNT
TRIM_Z = ra.TRIM_Z
EB_MARGIN = 1.5            # eb_prob asks: is the true rate more than 1.5x what the panel predicts?
CONDITION_NAMES = ["hypertension", "type 2 diabetes", "hyperlipidemia", "COPD", "heart failure", "chronic kidney disease",
                   "depression", "obesity", "osteoarthritis", "asthma", "hypothyroidism", "atrial fibrillation"]
METHODS = ["zscore", "riskadj", "priority", "eb_ratio", "eb_prob", "eb_excess", "level_z", "rich_logit", "rich_level", "eb_upper", "eb_two", "ensemble"]


# --- loading ----------------------------------------------------------------

def load(data_dir):
    """Visit-level arrays: provider ids, level index 0..4 (visits billed outside 99211-99215 are dropped), patient features."""
    pat = {}
    with open(os.path.join(data_dir, "patients.csv")) as f:
        for r in csv.DictReader(f):
            conds = set(filter(None, (r.get("conditions") or "").split(";")))
            pat[r["patient_id"]] = (min(int(r["chronic_condition_count"]), MAX_COUNT), int(r["age"]),
                                    float(r.get("risk_score") or 0.0), conds)
    prov, level, cnt, age, risk, conds, date = [], [], [], [], [], [], []
    with open(os.path.join(data_dir, "claims.csv")) as f:
        for r in csv.DictReader(f):
            if r["cpt"] not in LEVELS:
                continue
            c, a, k, cs = pat[r["patient_id"]]
            prov.append(r["provider_id"])
            level.append(LEVELS.index(r["cpt"]))
            cnt.append(c)
            age.append(a)
            risk.append(k)
            conds.append(cs)
            date.append((r["patient_id"], r["service_date"]))
    prov = np.array(prov)
    first = _first_visit_flags(prov, date)
    return {"prov": prov, "level": np.array(level), "cnt": np.array(cnt), "age": np.array(age), "risk": np.array(risk),
            "conds": conds, "first": first}


def _first_visit_flags(prov, keys):
    """1 for a patient's earliest visit with this provider (a stand-in for new versus established)."""
    best = {}
    for i, (p, (pat, d)) in enumerate(zip(prov, keys)):
        k = (p, pat)
        if k not in best or d < best[k][0]:
            best[k] = (d, i)
    first = np.zeros(len(prov))
    for _, i in best.values():
        first[i] = 1.0
    return first


def design_count(cnt):
    return ra.design(cnt)


def design_rich(D):
    n = len(D["cnt"])
    cols = [np.ones(n)]
    cols += [(D["cnt"] == k).astype(float) for k in range(1, MAX_COUNT + 1)]
    cols += [np.array([c in s for s in D["conds"]], dtype=float) for c in CONDITION_NAMES]
    cols += [(D["age"] >= lo).astype(float) for lo in (40, 55, 70)]
    cols += [D["risk"], D["first"]]
    return np.column_stack(cols)


# --- shared scoring -----------------------------------------------------------

def _robust(z):
    center = np.median(z)
    scale = 1.4826 * np.median(np.abs(z - center))
    return (z - center) / scale


def _provider_sums(prov, arrays):
    """Sum each array over each provider's visits: {pid: [sums...]} with the visit count first."""
    out = {}
    for pid in np.unique(prov):
        m = prov == pid
        out[pid] = [int(m.sum())] + [float(a[m].sum()) for a in arrays]
    return out


def _binary_fit(D, X, trim=True, min_level=4):
    """Logistic fit for billed at or above `min_level` (4 = 99215, 3 = 99214 or 99215), trimmed like baseline_riskadj.
    Returns (p per visit, per-provider obs/exp/var/z_raw); `n_99215` in the scores holds the observed count of that outcome."""
    y = (D["level"] >= min_level).astype(float)
    prov = D["prov"]
    beta = ra.fit_logistic(X, y)
    p = 1 / (1 + np.exp(-X @ beta))
    sc = ra.provider_scores(prov, p, y)
    if trim:
        drop = {k for k, v in sc.items() if v["z_raw"] > TRIM_Z}
        keep = ~np.isin(prov, list(drop))
        beta = ra.fit_logistic(X[keep], y[keep])
        p = 1 / (1 + np.exp(-X @ beta))
        sc = ra.provider_scores(prov, p, y)
    return p, sc


def _level_fit(D, X, trim=True, ridge=1e-6):
    """OLS mean-level model with per-visit variance from the residuals. Trimmed on providers whose raw level z is high."""
    y = D["level"].astype(float)
    prov = D["prov"]

    def fit(mask):
        A = X[mask]
        return np.linalg.solve(A.T @ A + ridge * np.eye(X.shape[1]), A.T @ y[mask])

    keep = np.ones(len(y), bool)
    beta = fit(keep)
    for _ in range(2 if trim else 1):
        res = y - X @ beta
        s2 = float(np.var(res[keep]))
        z = {pid: res[prov == pid].sum() / math.sqrt(max(s2 * (prov == pid).sum(), 1e-12)) for pid in np.unique(prov)}
        if not trim:
            break
        drop = [pid for pid, v in z.items() if v > TRIM_Z]
        keep = ~np.isin(prov, drop)
        beta = fit(keep)
    res = y - X @ beta
    s2 = float(np.var(res[keep]))
    out = {}
    for pid in np.unique(prov):
        m = prov == pid
        out[pid] = res[m].sum() / math.sqrt(max(s2 * m.sum(), 1e-12))
    return out


# --- empirical Bayes ----------------------------------------------------------

def _fit_gamma_shape(obs, exp):
    """Maximum-likelihood shape a for theta ~ Gamma(a, a) (mean 1) with observed ~ Poisson(theta x expected): grid search."""
    best, best_ll = None, -1e300
    for a in np.exp(np.linspace(math.log(0.3), math.log(400), 160)):
        ll = 0.0
        for o, e in zip(obs, exp):
            ll += (math.lgamma(o + a) - math.lgamma(a) - math.lgamma(o + 1) + a * math.log(a / (a + e)) + o * math.log(e / (a + e)))
        if ll > best_ll:
            best, best_ll = a, ll
    return float(best)


def _gamma_tail(shape, rate, c):
    """P(X > c) for X ~ Gamma(shape, rate), Wilson-Hilferty normal approximation (no scipy)."""
    k = shape
    t = ((rate * c) / k) ** (1 / 3)
    z = (t - (1 - 1 / (9 * k))) / math.sqrt(1 / (9 * k))
    return 0.5 * math.erfc(z / math.sqrt(2))


def eb_scores(sc):
    """Gamma-Poisson shrinkage on riskadj-style observed and expected counts. Prior fit on providers not already extreme."""
    pids = list(sc)
    obs = np.array([sc[p]["n_99215"] for p in pids], dtype=float)
    exp = np.array([sc[p]["expected"] for p in pids], dtype=float)
    z = np.array([sc[p]["z_raw"] for p in pids])
    fit_on = z <= TRIM_Z
    a = _fit_gamma_shape(obs[fit_on], exp[fit_on])
    post_shape, post_rate = a + obs, a + exp
    mean = post_shape / post_rate
    return {
        "eb_ratio": dict(zip(pids, mean)),
        "eb_excess": dict(zip(pids, exp * (mean - 1))),
        "eb_prob": {p: _gamma_tail(s, r, EB_MARGIN) for p, s, r in zip(pids, post_shape, post_rate)},
        "_shape": a,
    }


# --- the methods ----------------------------------------------------------------

def _rank_avg(*score_dicts):
    pids = list(score_dicts[0])
    total = {p: 0.0 for p in pids}
    for s in score_dicts:
        order = sorted(pids, key=lambda p: (-s[p], p))
        for i, p in enumerate(order):
            total[p] += i
    return {p: -total[p] / len(score_dicts) for p in pids}


CORE = ("riskadj", "priority", "eb_ratio")


def score_core(data_dir):
    """The three scores the release 2 workflow and agent use, without fitting the other candidates (about 3x faster than score_all).
    Returns {"riskadj", "priority", "eb_ratio": {provider_id: score}, "_expected": {provider_id: expected count}}. Same numbers as score_all."""
    D = load(data_dir)
    _, sc = _binary_fit(D, design_count(D["cnt"]))
    zr = np.array([v["z_raw"] for v in sc.values()])
    ratio = {pid: (v["n_99215"] / v["expected"]) if v["expected"] else 0.0 for pid, v in sc.items()}
    excess = {pid: v["n_99215"] - v["expected"] for pid, v in sc.items()}
    return {"riskadj": dict(zip(sc, _robust(zr).tolist())), "priority": _rank_avg(ratio, excess), "eb_ratio": eb_scores(sc)["eb_ratio"],
            "_expected": {pid: v["expected"] for pid, v in sc.items()}}


def score_all(data_dir):
    """All candidate methods on one dataset directory (the view folder). Returns {method: {provider_id: score}}."""
    import baseline_zscore as bz
    D = load(data_dir)
    prov = D["prov"]
    out = {}
    z_rows, _, _ = bz.rank(data_dir, 25)
    out["zscore"] = {r["provider_id"]: r["z"] for r in z_rows}

    Xc = design_count(D["cnt"])
    p, sc = _binary_fit(D, Xc)
    zr = np.array([v["z_raw"] for v in sc.values()])
    adj = _robust(zr)
    out["riskadj"] = dict(zip(sc, adj.tolist()))
    n = {pid: v["n_claims"] for pid, v in sc.items()}
    ratio = {pid: (v["n_99215"] / v["expected"]) if v["expected"] else 0.0 for pid, v in sc.items()}
    excess = {pid: v["n_99215"] - v["expected"] for pid, v in sc.items()}
    out["priority"] = _rank_avg(ratio, excess)
    eb = eb_scores(sc)
    for k in ("eb_ratio", "eb_prob", "eb_excess"):
        out[k] = eb[k]

    zl = _level_fit(D, Xc)
    out["level_z"] = dict(zip(zl, _robust(np.array(list(zl.values()))).tolist()))

    Xr = design_rich(D)
    _, sc2 = _binary_fit(D, Xr)
    out["rich_logit"] = dict(zip(sc2, _robust(np.array([v["z_raw"] for v in sc2.values()])).tolist()))
    zl2 = _level_fit(D, Xr)
    out["rich_level"] = dict(zip(zl2, _robust(np.array(list(zl2.values()))).tolist()))

    _, sc3 = _binary_fit(D, Xc, min_level=3)
    out["eb_upper"] = eb_scores(sc3)["eb_ratio"]
    out["eb_two"] = _rank_avg(out["eb_ratio"], out["eb_upper"])

    out["ensemble"] = _rank_avg(out["riskadj"], out["eb_ratio"], out["level_z"])
    out["_meta"] = {"n_claims": n, "eb_shape": eb["_shape"]}
    return out
