"""Build specialty-level E/M baselines from CMS public aggregated data.

Source: CMS "Medicare Physician & Other Practitioners - by Provider and Service"
(data.cms.gov dataset 92396110-2aed-4d63-a6a2-5d6207d46a29), codes 99211-99215.

Privacy: provider NPIs are used only to group rows. They are replaced by a
per-run random-salted hash that is never stored, and only specialty-level
distributions are written. No provider-level rows leave this script.

Usage:
    python src/build_baselines.py pull RAW_DIR [STATE ...]   # download raw rows
    python src/build_baselines.py build RAW_DIR OUT_JSON     # aggregate to baselines
"""
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date

import numpy as np

API = "https://data.cms.gov/data-api/v1/dataset/92396110-2aed-4d63-a6a2-5d6207d46a29/data"
COLS = "Rndrng_NPI,Rndrng_Prvdr_Type,Rndrng_Prvdr_Ent_Cd,HCPCS_Cd,Place_Of_Srvc,Tot_Srvcs,Tot_Benes"
CODES = ["99211", "99212", "99213", "99214", "99215"]
DEFAULT_STATES = ["OH", "NC", "WA", "GA", "MI"]
MIN_PROVIDER_SERVICES = 50   # drop tiny panels (noisy shares)
MIN_PROVIDERS_PER_SPECIALTY = 30
PCTS = [5, 25, 50, 75, 95]


def _get(url):
    for attempt in range(4):
        try:
            return json.load(urllib.request.urlopen(url, timeout=120))
        except Exception as exc:  # noqa: BLE001
            print(f"retry {attempt}: {exc}", file=sys.stderr)
            time.sleep(3)
    raise SystemExit(f"failed: {url}")


def pull(raw_dir, states):
    os.makedirs(raw_dir, exist_ok=True)
    for state in states:
        rows = []
        for code in CODES:
            offset = 0
            while True:
                query = urllib.parse.urlencode(
                    {"size": 5000, "offset": offset, "column": COLS,
                     "filter[Rndrng_Prvdr_State_Abrvtn]": state,
                     "filter[HCPCS_Cd]": code},
                    safe="[],",
                )
                page = _get(f"{API}?{query}")
                rows += page
                if len(page) < 5000:
                    break
                offset += 5000
        with open(os.path.join(raw_dir, f"{state}.json"), "w") as f:
            json.dump(rows, f)
        print(state, len(rows))


def build(raw_dir, out_path):
    salt = os.urandom(16)  # discarded when the process exits
    providers = {}  # hashed key -> {"spec": str, "n": {code: services}}
    states = []
    for name in sorted(os.listdir(raw_dir)):
        if not name.endswith(".json"):
            continue
        states.append(name[:-5])
        with open(os.path.join(raw_dir, name)) as f:
            for r in json.load(f):
                if r["Rndrng_Prvdr_Ent_Cd"] != "I":  # individuals only
                    continue
                key = hashlib.sha256(salt + r["Rndrng_NPI"].encode()).hexdigest()
                p = providers.setdefault(key, {"spec": r["Rndrng_Prvdr_Type"], "n": defaultdict(float)})
                p["n"][r["HCPCS_Cd"]] += float(r["Tot_Srvcs"])

    by_spec = defaultdict(list)
    for p in providers.values():
        total = sum(p["n"].values())
        if total < MIN_PROVIDER_SERVICES:
            continue
        mix = [p["n"][c] / total for c in CODES]
        by_spec[p["spec"]].append((total, mix))

    specialties = {}
    for spec, items in sorted(by_spec.items()):
        if len(items) < MIN_PROVIDERS_PER_SPECIALTY:
            continue
        totals = np.array([t for t, _ in items])
        mixes = np.array([m for _, m in items])
        high = mixes[:, 3] + mixes[:, 4]  # 99214 + 99215 share
        specialties[spec] = {
            "n_providers": len(items),
            "total_em_services": {f"p{q}": round(float(np.percentile(totals, q)), 1) for q in PCTS},
            "mean_level_mix": {c: round(float(mixes[:, i].mean()), 4) for i, c in enumerate(CODES)},
            "share_99214_99215": {
                "mean": round(float(high.mean()), 4),
                "std": round(float(high.std(ddof=1)), 4),
                **{f"p{q}": round(float(np.percentile(high, q)), 4) for q in PCTS},
            },
        }

    out = {
        "source": "CMS Medicare Physician & Other Practitioners - by Provider and Service",
        "dataset_id": "92396110-2aed-4d63-a6a2-5d6207d46a29",
        "retrieved": date.today().isoformat(),
        "data_year": "UNVERIFIED - confirm on data.cms.gov",
        "sample": {"states": states, "note": "subset of states, whole providers; not a random national sample"},
        "filters": {"codes": CODES, "individuals_only": True, "min_provider_services": MIN_PROVIDER_SERVICES,
                    "min_providers_per_specialty": MIN_PROVIDERS_PER_SPECIALTY},
        "specialties": specialties,
    }
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"{len(providers)} providers -> {len(specialties)} specialties written to {out_path}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "pull" and len(sys.argv) >= 3:
        pull(sys.argv[2], sys.argv[3:] or DEFAULT_STATES)
    elif cmd == "build" and len(sys.argv) == 4:
        build(sys.argv[2], sys.argv[3])
    else:
        raise SystemExit(__doc__)
