"""Generate synthetic Family Practice E/M providers, patients and claim lines.

Calibrated to the CMS GA Family Practice provider-level distribution
(see README, "Baseline data caveats"). Everything here is synthetic.

Model
-----
* Each patient has a chronic-condition count (complexity).
* Each visit has a *justified* level (99211-99215) drawn from an ordered logit
  on patient complexity plus a provider-level panel effect.
* Honest providers bill the justified level.
* Upcoders bill justified+1 on a fraction of visits (capped at 99215).
* Hard negatives are honest but have sicker panels, so they legitimately bill
  more 99214/99215.

Ground truth (justified levels, provider roles) is written separately and is
NOT part of what the agent sees.

Usage:
    python src/generate_synthetic.py OUT_DIR [--seed 42]
"""
import argparse
import json
import os
from datetime import date, timedelta

import numpy as np

CODES = ["99211", "99212", "99213", "99214", "99215"]

CONDITIONS = [
    ("hypertension", "I10"),
    ("type 2 diabetes", "E11.9"),
    ("hyperlipidemia", "E78.5"),
    ("COPD", "J44.9"),
    ("heart failure", "I50.9"),
    ("chronic kidney disease", "N18.3"),
    ("depression", "F32.9"),
    ("obesity", "E66.9"),
    ("osteoarthritis", "M19.90"),
    ("asthma", "J45.909"),
    ("hypothyroidism", "E03.9"),
    ("atrial fibrillation", "I48.91"),
]
# Higher-burden conditions are picked first as the chronic count grows.
CONDITION_WEIGHT = np.array([6, 5, 5, 2, 1.5, 1.5, 3, 4, 3, 2, 2, 1.5], dtype=float)
ACUTE_DX = [("URI", "J06.9"), ("back pain", "M54.50"), ("UTI", "N39.0"),
            ("rash", "R21"), ("abdominal pain", "R10.9"), ("annual follow-up", "Z09")]

# Fitted by scratchpad calibration against the GA Family Practice distribution.
PARAMS = {
    "beta": 0.505,                # latent shift per chronic condition
    "thresholds": [-4.046, -3.320, 0.170, 4.370],
    "lam_mu": 1.292,              # mean chronic conditions, typical panel
    "lam_sigma": 0.463,           # between-provider spread of panel severity (log scale)
    "eta_sigma": 0.620,           # provider-level coding-style effect (legitimate)
    "top_sigma": 0.633,           # provider-level shift on the 99215 threshold only
}
HARD_NEG_LAM_MULT = 2.0
UPCODER_FRACTION = (0.15, 0.40)  # share of visits upgraded by one level
VOLUME_MEDIAN, VOLUME_SIGMA = 283.0, 1.13   # lognormal, from CMS GA FP
VOLUME_MIN, VOLUME_MAX = 60, 2500
VISITS_PER_PATIENT = 2.3


def justified_levels(rng, chronic, eta, params, top_shift=0.0):
    """Ordered-logit justified level (0..4) for each visit.

    top_shift moves only the 99215 threshold, giving providers a separate,
    legitimate propensity for high-complexity visits (heavy upper tail).
    """
    latent = params["beta"] * chronic + eta + rng.logistic(size=chronic.shape)
    t = np.array(params["thresholds"], dtype=float)
    t[-1] += top_shift
    return (latent[:, None] > t[None, :]).sum(axis=1)


def simulate_provider(rng, params, n_visits, lam_mult=1.0, upgrade_frac=0.0):
    """Return (patient_chronic, visit_patient_idx, justified, billed)."""
    lam = params["lam_mu"] * lam_mult * np.exp(rng.normal(0, params["lam_sigma"]))
    n_pat = max(20, int(n_visits / VISITS_PER_PATIENT))
    chronic = np.minimum(rng.poisson(lam, size=n_pat), 8)
    visit_pat = rng.integers(0, n_pat, size=n_visits)
    eta = rng.normal(0, params["eta_sigma"])
    top_shift = rng.normal(0, params["top_sigma"])
    just = justified_levels(rng, chronic[visit_pat], eta, params, top_shift)
    billed = just.copy()
    if upgrade_frac > 0:
        up = (rng.random(n_visits) < upgrade_frac) & (just >= 1)
        billed = np.where(up, np.minimum(just + 1, 4), just)
    return chronic, visit_pat, just, billed


def build(out_dir, seed=42, n_normal=200, n_upcoders=8, n_hard_neg=8):
    rng = np.random.default_rng(seed)
    os.makedirs(out_dir, exist_ok=True)
    roles = ["normal"] * n_normal + ["upcoder"] * n_upcoders + ["hard_negative"] * n_hard_neg
    rng.shuffle(roles)

    providers, patients, claims, truth = [], [], [], {}
    pid_counter = 0
    claim_counter = 0
    start = date(2024, 1, 1)
    weekdays = [start + timedelta(days=i) for i in range(366)
                if (start + timedelta(days=i)).weekday() < 5 and (start + timedelta(days=i)).year == 2024]

    for i, role in enumerate(roles):
        prov = f"P{i + 1:04d}"
        volume = int(np.clip(rng.lognormal(np.log(VOLUME_MEDIAN), VOLUME_SIGMA), VOLUME_MIN, VOLUME_MAX))
        if role == "upcoder":
            volume = max(volume, 250)   # enough claims to be reviewable
        lam_mult = HARD_NEG_LAM_MULT if role == "hard_negative" else 1.0
        up = float(rng.uniform(*UPCODER_FRACTION)) if role == "upcoder" else 0.0
        chronic, vpat, just, billed = simulate_provider(rng, PARAMS, volume, lam_mult, up)

        # Patients: attributes visible to the agent.
        for j, c in enumerate(chronic):
            order = rng.choice(len(CONDITIONS), size=min(int(c), len(CONDITIONS)),
                               replace=False, p=CONDITION_WEIGHT / CONDITION_WEIGHT.sum())
            age = int(np.clip(rng.normal(52 + 4 * (c - 1.5), 15), 18, 96))
            patients.append({
                "patient_id": f"{prov}-N{j:04d}",
                "provider_id": prov,
                "age": age,
                "chronic_condition_count": int(c),
                "conditions": ";".join(CONDITIONS[k][0] for k in order),
                "_dx": [CONDITIONS[k][1] for k in order],
            })
        base = len(patients) - len(chronic)

        for v in range(volume):
            claim_counter += 1
            p = patients[base + int(vpat[v])]
            dx = list(p["_dx"][: int(rng.integers(1, 4))]) if p["_dx"] else []
            if rng.random() < 0.45 or not dx:
                dx.append(ACUTE_DX[int(rng.integers(len(ACUTE_DX)))][1])
            cid = f"C{claim_counter:07d}"
            claims.append({
                "claim_id": cid,
                "provider_id": prov,
                "patient_id": p["patient_id"],
                "service_date": weekdays[int(rng.integers(len(weekdays)))].isoformat(),
                "cpt": CODES[int(billed[v])],
                "place_of_service": "11",
                "diagnosis_codes": ";".join(dx),
            })
            truth[cid] = CODES[int(just[v])]

        providers.append({
            "provider_id": prov,
            "specialty": "Family Practice",
            "state": "GA",
            "n_claims": volume,
            "n_patients": len(chronic),
            "_role": role,
            "_upgrade_fraction": round(up, 3),
            "_panel_mean_chronic": round(float(chronic.mean()), 2),
        })

    # Agent-visible tables
    _write_csv(os.path.join(out_dir, "providers.csv"), providers, ["provider_id", "specialty", "state", "n_claims", "n_patients"])
    _write_csv(os.path.join(out_dir, "patients.csv"), patients, ["patient_id", "provider_id", "age", "chronic_condition_count", "conditions"])
    _write_csv(os.path.join(out_dir, "claims.csv"), claims,
               ["claim_id", "provider_id", "patient_id", "service_date", "cpt", "place_of_service", "diagnosis_codes"])
    # Ground truth (kept apart; never shown to the agent)
    with open(os.path.join(out_dir, "ground_truth.json"), "w") as f:
        json.dump({
            "seed": seed,
            "providers": {p["provider_id"]: {"role": p["_role"], "upgrade_fraction": p["_upgrade_fraction"],
                                             "panel_mean_chronic": p["_panel_mean_chronic"]} for p in providers},
            "justified_cpt_by_claim": truth,
        }, f)
    return providers


def _write_csv(path, rows, cols):
    import csv
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    provs = build(a.out_dir, a.seed)
    print(f"wrote {len(provs)} providers to {a.out_dir}")
