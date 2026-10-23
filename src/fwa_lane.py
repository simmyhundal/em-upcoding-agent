"""The claims-data lane (workflow v4.2, agent v5.2; docs/concepts/volume-screen.md): find providers who billed an impossible number of visits on one day, from claims alone, then request charts for a random
sample of the claims on those days and demand what the sample supports. Payer-visible only: claims, the office's answers, the payer's own estimate. No answer key.

Why this lane exists: a provider's claims on a single service date are counted by every payer's edits; a visit total no clinician can see in a day is a standard analytic. On data 4.2 the busiest
honest day is at most about 25 visits and an impossible-days provider's is at least 34, so the signal is CLEAN BY CONSTRUCTION; real claims are messier (docs/score_42.md, limitations).

Steps for each flagged provider: (1) the stratum = the provider's claims dated on its flagged days; (2) a random sample of up to `n` claims within the stratum, requested as one targeted request
(one follow-up when the office names a fixable deficiency); (3) the stratum estimate (recovery_42.recovery_stratified: NO_RECORD claims count at their paid amount, 90% lower bound); (4) a demand when
that lower bound is at least the staff cost of a demand (the break-even rule).
"""
import csv
import json
import os
import random
from collections import Counter, defaultdict

import recovery_40 as r4
import recovery_42 as r42

DAY_MAX = 30          # E/M claims by one provider on one service date at or above which the provider is flagged (chosen on data 4.2 development seeds, docs/w_loop_v42.md)
SAMPLE_N = 30         # random claims requested within the stratum
MAX_FLAGGED = 10      # a cap on providers taken into the lane per dataset (analyst capacity)
PERSIST = 3           # extra follow-ups while the office has given nothing usable (workflow v4.2 hypothesis H28; H24 is the same lane with 0)


def busiest_days(claims_by_provider):
    """{provider_id: {service_date: number of claims}} for every provider (payer-visible: the claims view)."""
    out = {}
    for pid, rows in claims_by_provider.items():
        out[pid] = Counter(r["service_date"] for r in rows)
    return out


def flag(claims_by_provider, day_max=DAY_MAX, max_flagged=MAX_FLAGGED):
    """[(provider_id, busiest day count, [flagged service dates])] by busiest day, descending, at most `max_flagged`."""
    out = []
    for pid, days in busiest_days(claims_by_provider).items():
        hot = sorted(d for d, n in days.items() if n >= day_max)
        if hot:
            out.append((pid, max(days.values()), hot))
    out.sort(key=lambda t: (-t[1], t[0]))
    return out[:max_flagged]


def stratum_ids(rows, hot_days):
    hot = set(hot_days)
    return sorted(r["claim_id"] for r in rows if r["service_date"] in hot)


def review(office, pid, rows, hot_days, seed=1, n=SAMPLE_N, p=None, persist=0):
    """One provider through the lane. Returns the lane record (JSON-able): stratum, sample, what came back, the payer's own estimate and the demand decision."""
    import dollar_reward as dr
    p = p or r42.params42()
    ids = stratum_ids(rows, hot_days)
    rng = random.Random(f"{seed}:fwa:{pid}")
    sample = sorted(rng.sample(ids, min(n, len(ids))))
    rec = {"stratum_ids": ids, "sample_ids": sample, "hot_days": list(hot_days), "rounds": 0, "charts": 0, "no_record": [], "levels": {}, "demand": False}
    resp = office.send_request(pid, {"kind": "targeted", "claim_ids": sample}, deadline=30)
    if "error" in resp:
        rec["error"] = resp["error"]
        return rec
    if resp.get("deficiencies") and resp.get("rounds_left", 0) > 0:
        fixable = [d["code"] for d in resp["deficiencies"] if d["code"] != "NO_RECORD"]
        if fixable:
            resp = office.follow_up(pid, fixable, deadline=30)
    for _ in range(persist):                       # H28 (workflow v4.2 loop): while the office has given nothing usable and has not reported NO_RECORD, follow up again (caps: rounds and days of the office)
        if office.state[pid]["usable"] or any(d["code"] == "NO_RECORD" for e in office.transcript if e.get("provider_id") == pid for d in e.get("deficiencies", [])):
            break
        if resp.get("rounds_left", 0) <= 0 or resp.get("days_left", 1) <= 0 or "error" in resp:
            break
        codes = [d["code"] for d in resp.get("deficiencies", []) if d["code"] != "NO_RECORD"]
        resp = office.follow_up(pid, codes, deadline=30)
    nr = set()
    for e in office.transcript:
        if e.get("provider_id") == pid:
            for d in e.get("deficiencies", []):
                if d["code"] == "NO_RECORD":
                    nr.update(d["claim_ids"])
    st = office.state[pid]
    rec["rounds"] = st["round"]
    rec["charts"] = len(st["usable"])
    rec["no_record"] = sorted(nr)
    rec["levels"] = dr.level_of_rows(list(st["usable"].values()))
    est = r42.recovery_stratified([r for r in rows if r["claim_id"] in set(ids)], sample, rec["levels"], p, no_record=nr)
    cost = r4.staff_cost(0, 0, 0, 1, 0, p)[0]
    rec["estimate"] = {k: (round(v, 2) if isinstance(v, float) else v) for k, v in est.items()}
    rec["demand_cost"] = round(cost, 2)
    rec["demand"] = est["value"] >= cost
    office.close_request(pid, "claims-data lane")
    return rec


def run(rid, src, opts, root):
    """Run the lane on a stored workflow run's dataset and write experiments/<rid>/fwa_lane.json and fwa_office_transcript.jsonl."""
    import provider_sim
    data = os.path.join(root, "data", f"synthetic_v2_{src}")
    base = os.path.join(data, "view")
    claims = defaultdict(list)
    for r in csv.DictReader(open(os.path.join(base, "claims.csv"))):
        claims[r["provider_id"]].append(r)
    office = provider_sim.Office(data, base, seed=1, version="4.2")
    out = {"opts": opts, "providers": {}}
    for pid, top, hot in flag(claims, opts.get("day_max", DAY_MAX), opts.get("max_flagged", MAX_FLAGGED)):
        v = review(office, pid, claims[pid], hot, n=opts.get("n", SAMPLE_N), persist=opts.get("persist", 0))
        v["busiest_day"] = top
        out["providers"][pid] = v
    d = os.path.join(root, "experiments", rid)
    json.dump(out, open(os.path.join(d, "fwa_lane.json"), "w"))
    office.write_transcript(os.path.join(d, "fwa_office_transcript.jsonl"))
    return out
