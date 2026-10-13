"""Records requests: what a plan actually gets back when it asks a physician's office for charts.

At screening time a plan has claims only. After a provider is flagged it can request records for a sample of that provider's
visits. This module models that request instead of handing out a ready-made documentation file:
  * a limited sample size per provider
  * a response rate and a response delay; responses later than the deadline are late and unusable
  * coder disagreement: the documented MDM level a reviewer reads off the chart is off by one some of the time
  * a small control sample of unflagged providers stands in for prior record reviews, giving a peer baseline

Documented level (what a reviewer takes from a chart) = the level the MDM supports (two of the three elements must reach
it, i.e. the second-highest element) or the level the recorded minutes support, whichever is higher. Cutoffs are illustrative;
check current CPT and CMS guidance.

Also holds two rules-only baselines on the same records evidence, to measure what the AI adds:
  * documented_below_billed: share of a provider's documented visits whose documented level is below the billed level
  * data_without_tests: share of documented visits whose note claims moderate-or-higher data reviewed (data level 3+) but
    whose claim has no lab or test line. This is the check against claim facts that catches cloned documentation.

Reads only plan tables, the detector view and the records universe. Never the answer key.

Usage:
    python src/records.py V2_DIR VIEW_DIR FLAGGED_CSV [--sample 30] [--control 30] [--seed 1] [--response-rate 0.8]
"""
import argparse
import csv
import os
import random
from collections import defaultdict

MDM_LEVELS = ["minimal", "straightforward", "low", "moderate", "high"]
CODES = ["99211", "99212", "99213", "99214", "99215"]
MIN_FLOOR = [0, 10, 20, 30, 40]        # minutes at which each level is supported (illustrative)
DEADLINE_DAYS = 45
CODER_NOISE = 0.15
DOC_COLS = ["claim_id", "documented_mdm_level", "documented_minutes", "documented_problems_level",
            "documented_data_level", "documented_risk_level"]


def mdm_level(problems, data, risk):
    """Two of the three elements must reach a level: the second-highest element."""
    return sorted([problems, data, risk])[1]


def level_from_minutes(minutes):
    if minutes in ("", None):
        return -1
    m = int(minutes)
    return max(i for i, floor in enumerate(MIN_FLOOR) if m >= floor)


def supported_level(mdm, minutes):
    """The level a reviewer would assign: MDM or time, whichever supports the higher level."""
    return max(mdm, level_from_minutes(minutes))


def _rows(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def read_chart(u, rng, coder_noise=CODER_NOISE):
    """What a reviewer takes from one chart (a records-universe row): the MDM-derived level, with coder disagreement."""
    p, d, r = int(u["problems_level"]), int(u["data_level"]), int(u["risk_level"])
    lvl = mdm_level(p, d, r)
    if rng.random() < coder_noise:                        # coders disagree on borderline calls
        lvl = max(0, min(4, lvl + rng.choice([-1, 1])))
    return {"claim_id": u["claim_id"], "documented_mdm_level": MDM_LEVELS[lvl], "documented_minutes": u["documented_minutes"],
            "documented_problems_level": p, "documented_data_level": d, "documented_risk_level": r}


def request_records(v2_dir, view_dir, provider_ids, sample_n, rng, response_rate=0.8, deadline=DEADLINE_DAYS,
                    coder_noise=CODER_NOISE):
    """Simulate a records request. Returns (documentation rows, one status row per provider)."""
    universe = {r["claim_id"]: r for r in _rows(os.path.join(v2_dir, "records", "records_universe.csv"))}
    by_prov = defaultdict(list)
    for r in _rows(os.path.join(view_dir, "claims.csv")):
        by_prov[r["provider_id"]].append(r["claim_id"])
    docs, status = [], []
    for pid in provider_ids:
        ids = sorted(by_prov.get(pid, []))
        pick = rng.sample(ids, min(sample_n, len(ids)))
        got = late = missing = 0
        for cid in pick:
            if rng.random() >= response_rate:
                missing += 1
                continue
            if rng.randint(10, 60) > deadline:
                late += 1
                continue
            docs.append(read_chart(universe[cid], rng, coder_noise))
            got += 1
        status.append({"provider_id": pid, "requested": len(pick), "received": got, "late": late, "no_response": missing})
    return docs, status


def run_requests(v2_dir, view_dir, flagged_csv, sample_n=30, control_n=30, seed=1, response_rate=0.8):
    rng = random.Random(f"records:{seed}")
    flagged_rows = _rows(flagged_csv)
    flagged = [r["provider_id"] for r in flagged_rows if r["flagged"] == "True"]
    others = sorted(r["provider_id"] for r in flagged_rows if r["flagged"] != "True")
    control = rng.sample(others, min(control_n, len(others)))
    docs, st = request_records(v2_dir, view_dir, flagged + control, sample_n, rng, response_rate)
    for row in st:
        row["kind"] = "flagged" if row["provider_id"] in set(flagged) else "control"
    with open(os.path.join(view_dir, "documentation.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=DOC_COLS)
        w.writeheader()
        w.writerows(docs)
    with open(os.path.join(view_dir, "records_requests.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["provider_id", "kind", "requested", "received", "late", "no_response"])
        w.writeheader()
        w.writerows(st)
    return docs, st


def rules_flags(view_dir, rule="documented_below_billed", threshold=0.15, min_docs=8, providers=None):
    """Providers a simple rule flags on records evidence alone. Returns {provider_id: (rate, n_docs)} for flagged ones."""
    claims = {r["claim_id"]: r for r in _rows(os.path.join(view_dir, "claims.csv"))}
    tot, bad = defaultdict(int), defaultdict(int)
    for d in _rows(os.path.join(view_dir, "documentation.csv")):
        c = claims.get(d["claim_id"])
        if not c or (providers is not None and c["provider_id"] not in providers):
            continue
        pid = c["provider_id"]
        tot[pid] += 1
        if rule == "documented_below_billed":
            lvl = supported_level(MDM_LEVELS.index(d["documented_mdm_level"]), d["documented_minutes"])
            bad[pid] += lvl < CODES.index(c["cpt"])
        elif rule == "data_without_tests":
            bad[pid] += int(d["documented_data_level"]) >= 3 and c["has_test_line"] == "0"
        else:
            raise ValueError(rule)
    return {p: (bad[p] / tot[p], tot[p]) for p in tot if tot[p] >= min_docs and bad[p] / tot[p] > threshold}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("v2_dir")
    ap.add_argument("view_dir")
    ap.add_argument("flagged_csv")
    ap.add_argument("--sample", type=int, default=30, help="visits requested per flagged provider")
    ap.add_argument("--control", type=int, default=30, help="unflagged providers whose records stand in for prior reviews")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--response-rate", type=float, default=0.8)
    a = ap.parse_args()
    docs, st = run_requests(a.v2_dir, a.view_dir, a.flagged_csv, a.sample, a.control, a.seed, a.response_rate)
    req = sum(s["requested"] for s in st)
    print(f"{len(st)} providers asked, {req} records requested, {len(docs)} usable -> {a.view_dir}/documentation.csv")
