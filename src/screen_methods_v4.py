"""Candidate indicators and screens for data 4.0 (issue 127; spec docs/v4_v5_plan.md). Built beside screen_methods.py, which stays frozen.

Data 4.0's habits move the 99215 share little (systematic: 99213 to 99214; template: any level up to 99214), so the screens of releases 2 to 5 miss most upcoders. Every score here uses
payer-visible files only (the detector view: claims.csv and patients.csv) and returns {provider_id: score}, higher = more suspicious.

  eb_ratio_t    the frozen screen of workflow v2.3 to v2.5 and agent v3.3 to v3.5 (the reference)
  eb_upper_c    the same shrinkage on the share billed 99214 or 99215 with the chronic-condition count only (no test line), the version that does not use the lab link
  eb_upper_t    the same shrinkage on the share billed 99214 or 99215, with the lab or test line as a covariate, so upgrades into 99214 count
  pay_resid     whole-distribution, dollar-weighted: allowed amount per visit against the amount expected from the patient's chronic-condition count and the test line, shrunk
  excess_usd    pay_resid times the provider's visits: the shrunk excess dollars (what a recovery could be worth), the score that follows the dollar reward
  rich_level_t  mean billed level on a per-claim expectation (conditions, age, risk, first visit, diagnosis counts, test line), robust z
  same_patient  the provider's level against the level the same patients were billed by OTHER providers (case mix cancels); needs shared patients
  drift         the slope of a provider's monthly level residual over the year (a break in its level mix over time)
  hi_no_test    visits billed 99214 or 99215 with no lab or test line, against what the patient mix predicts (high level with nothing after it)
  group_level   not built: the detector view carries no tax ID, so providers cannot be grouped into offices from payer-visible files here

Honesty notes. The synthetic generator draws a visit's lab line from the TRUE complexity (a lab is far likelier when the true data element is high), so any indicator using the test line has a
planted covariate, and the habits are the ones these indicators look for. Patient features other than the chronic-condition count carry no extra signal in the generator. See docs/screens_v4.md.
"""
import csv
import math
import os

import numpy as np

import baseline_riskadj as ra
import screen_methods as sm

LEVELS = sm.LEVELS
MIN_SAME_PATIENT = 20


def load_v4(view):
    """Visit arrays as screen_methods.load, plus patient id, month, diagnosis counts and the allowed amount (same order, so arrays align)."""
    D = sm.load(view)
    pid_, month, n_dx, allowed = [], [], [], []
    with open(os.path.join(view, "claims.csv")) as f:
        for r in csv.DictReader(f):
            if r["cpt"] not in LEVELS:
                continue
            pid_.append(r["patient_id"])
            month.append(int(r["service_date"][5:7]))
            n_dx.append(len([c for c in r["diagnosis_codes"].split(";") if c]))
            allowed.append(float(r["allowed_amount"]))
    D["patient"], D["month"], D["n_dx"], D["allowed"] = np.array(pid_), np.array(month), np.array(n_dx, dtype=float), np.array(allowed)
    return D


def _ols(X, y, mask, ridge=1e-6):
    A = X[mask]
    return np.linalg.solve(A.T @ A + ridge * np.eye(X.shape[1]), A.T @ y[mask])


def _trimmed_resid(prov, X, y, rounds=2):
    """OLS residuals with the providers whose raw z is high left out of the fit (as screen_methods._level_fit)."""
    keep = np.ones(len(y), bool)
    beta = _ols(X, y, keep)
    for _ in range(rounds):
        res = y - X @ beta
        s2 = float(np.var(res[keep]))
        drop = []
        for pid in np.unique(prov):
            m = prov == pid
            if res[m].sum() / math.sqrt(max(s2 * m.sum(), 1e-12)) > sm.TRIM_Z:
                drop.append(pid)
        keep = ~np.isin(prov, drop)
        beta = _ols(X, y, keep)
    return y - X @ beta, keep


def eb_mean(prov, resid):
    """Empirical-Bayes shrunk provider means of a visit-level residual: {pid: (posterior mean, visits)}. Between-provider variance by moments; shrinks small panels toward 0."""
    pids = np.unique(prov)
    n = np.array([(prov == p).sum() for p in pids], dtype=float)
    mu = np.array([resid[prov == p].mean() for p in pids])
    s2 = float(np.mean([resid[prov == p].var() for p in pids]))
    tau2 = max(float(np.var(mu)) - float(np.mean(s2 / n)), 1e-9)
    post = mu * tau2 / (tau2 + s2 / n)
    return {p: (float(m), int(k)) for p, m, k in zip(pids, post, n)}


def score_v4(view, only=None):
    """All candidate scores for one view folder: {method: {provider_id: score}}. `only` limits the work to a list of method names."""
    D = load_v4(view)
    prov = D["prov"]
    Xc = sm.design_count(D["cnt"])
    Xt = np.hstack([Xc, D["test"][:, None]])
    want = lambda k: only is None or k in only
    out = {}
    if want("eb_ratio_t"):
        out["eb_ratio_t"] = sm.eb_ratio_t(D)
    if want("eb_upper_t"):
        _, sc = sm._binary_fit(D, Xt, min_level=3)
        out["eb_upper_t"] = sm.eb_scores(sc)["eb_ratio"]
    if want("eb_upper_c"):                    # the same shrinkage without the test-line covariate (count only): the version that does not lean on the generator's lab-line link
        _, sc = sm._binary_fit(D, Xc, min_level=3)
        out["eb_upper_c"] = sm.eb_scores(sc)["eb_ratio"]
    if want("pay_resid") or want("excess_usd"):
        res, _ = _trimmed_resid(prov, Xt, D["allowed"])
        post = eb_mean(prov, res)
        out["pay_resid"] = {p: m for p, (m, k) in post.items()}
        out["excess_usd"] = {p: m * k for p, (m, k) in post.items()}
    if want("rich_level_t"):
        Xr = np.hstack([sm.design_rich(D), D["test"][:, None], D["n_dx"][:, None]])
        z = sm._level_fit(D, Xr)
        out["rich_level_t"] = dict(zip(z, sm._robust(np.array(list(z.values()))).tolist()))
    if want("same_patient"):
        by_pat = {}
        for i, (pt, p) in enumerate(zip(D["patient"], prov)):
            by_pat.setdefault(pt, []).append(i)
        diff = np.full(len(prov), np.nan)
        lvl = D["level"].astype(float)
        for idx in by_pat.values():
            if len(idx) < 2:
                continue
            for i in idx:
                others = [j for j in idx if prov[j] != prov[i]]
                if others:
                    diff[i] = lvl[i] - lvl[others].mean()
        ok = ~np.isnan(diff)
        post = eb_mean(prov[ok], diff[ok] - np.nanmean(diff))
        out["same_patient"] = {p: (post[p][0] if p in post and post[p][1] >= MIN_SAME_PATIENT else 0.0) for p in np.unique(prov)}
    if want("drift"):
        res, _ = _trimmed_resid(prov, Xt, D["level"].astype(float))
        w = D["month"].astype(float) - 6.5
        z = {}
        for p in np.unique(prov):
            m = prov == p
            sw = float((w[m] ** 2).sum())
            sd = float(np.std(res[m])) or 1.0
            z[p] = float((w[m] * res[m]).sum() / sw) / (sd / math.sqrt(max(sw, 1e-9)))
        out["drift"] = dict(zip(z, sm._robust(np.array(list(z.values()))).tolist()))
    if want("hi_no_test"):
        y = ((D["level"] >= 3) & (D["test"] == 0)).astype(float)
        beta = ra.fit_logistic(Xc, y)
        p = 1 / (1 + np.exp(-Xc @ beta))
        sc = ra.provider_scores(prov, p, y)
        out["hi_no_test"] = sm.eb_scores(sc)["eb_ratio"]
    return out
