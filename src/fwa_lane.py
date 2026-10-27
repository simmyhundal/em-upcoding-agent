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


def _ask(office, pid, claim_ids, persist):
    """One records request for `claim_ids` with its follow-ups (one on a fixable deficiency, then up to `persist` more while nothing usable and no NO_RECORD has come back)."""
    resp = office.send_request(pid, {"kind": "targeted", "claim_ids": claim_ids}, deadline=30)
    if "error" in resp:
        return resp
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
    return resp


def _no_record(office, pid):
    nr = set()
    for e in office.transcript:
        if e.get("provider_id") == pid:
            for d in e.get("deficiencies", []):
                if d["code"] == "NO_RECORD":
                    nr.update(d["claim_ids"])
    return nr


def break_even_lower_bound():
    """Score 4.3's break-even for a fraud referral in terms of the sample's lower bound: collected at the referral rate it must cover the referral cost and the expected appeal handling."""
    import recovery_43 as r43
    p = r43.params43()
    appeal = p["P_APPEAL"] * p["APPEAL_HANDLING_HOURS"] * r4.hourly("coder", p)
    return (p["REFERRAL_COST"] + appeal) / p["COLLECTION_REFERRAL"]


def review(office, pid, rows, hot_days, seed=1, n=SAMPLE_N, p=None, persist=0, break_even="demand", probe=None):
    """One provider through the lane. Returns the lane record (JSON-able): stratum, sample, what came back, the payer's own estimate and the demand decision.
    break_even "demand" (workflow v4.2): demand when the lower bound covers a demand's staff cost; "s43" (workflow v4.3): when the lower bound, collected at the referral rate, covers the referral cost.
    probe {"n", "k", "more"} (workflow v4.3): request `n` claims first and `more` further ones only if the office reported NO_RECORD for at least `k` of them."""
    import dollar_reward as dr
    p = p or r42.params42()
    ids = stratum_ids(rows, hot_days)
    rng = random.Random(f"{seed}:fwa:{pid}")
    first = sorted(rng.sample(ids, min(probe["n"] if probe else n, len(ids))))
    sample = first
    rec = {"stratum_ids": ids, "sample_ids": sample, "hot_days": list(hot_days), "rounds": 0, "charts": 0, "no_record": [], "levels": {}, "demand": False}
    resp = _ask(office, pid, first, persist)
    if "error" in resp:
        rec["error"] = resp["error"]
        return rec
    if probe and len(_no_record(office, pid)) >= probe["k"]:
        rest = [c for c in ids if c not in set(first)]
        more = sorted(rng.sample(rest, min(probe["more"], len(rest))))
        if more and "error" not in _ask(office, pid, more, probe.get("persist", 1)):
            sample = sorted(first + more)
            rec["sample_ids"] = sample
    nr = _no_record(office, pid)
    st = office.state[pid]
    rec["rounds"] = st["round"]
    rec["charts"] = len(st["usable"])
    rec["no_record"] = sorted(nr)
    rec["levels"] = dr.level_of_rows(list(st["usable"].values()))
    est = r42.recovery_stratified([r for r in rows if r["claim_id"] in set(ids)], sample, rec["levels"], p, no_record=nr)
    cost = r4.staff_cost(0, 0, 0, 1, 0, p)[0] if break_even == "demand" else break_even_lower_bound()
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
    office = provider_sim.Office(data, base, seed=1, version=opts.get("office_version", "4.2"))     # "4.3" on data 4.3 (workflow v4.3); the frozen workflow v4.2 keeps office 4.2
    out = {"opts": opts, "providers": {}}
    flagged = flag(claims, opts.get("day_max", DAY_MAX), opts.get("max_flagged", MAX_FLAGGED))
    veto = set(opts.get("veto_ids", ()))
    if opts.get("veto_fraction"):                  # evaluation mode (gate 1): a person vetoes a seeded random fraction of the flagged providers (docs/evaluation_modes.md)
        rng = random.Random(f"{opts.get('veto_seed', 1)}:{src}:lane-gate1")
        veto |= {pid for pid, _t, _h in flagged if rng.random() < opts["veto_fraction"]}
    for pid, top, hot in [f for f in flagged if f[0] not in veto]:
        v = review(office, pid, claims[pid], hot, n=opts.get("n", SAMPLE_N), persist=opts.get("persist", 0), break_even=opts.get("break_even", "demand"), probe=opts.get("probe"))
        v["busiest_day"] = top
        out["providers"][pid] = v
    d = os.path.join(root, "experiments", rid)
    json.dump(out, open(os.path.join(d, "fwa_lane.json"), "w"))
    office.write_transcript(os.path.join(d, "fwa_office_transcript.jsonl"))
    return out
