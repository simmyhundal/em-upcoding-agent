"""Release 4: the reward in dollars (issue 108). Free (stored runs and the simulated office).

Net dollars for one arm on one seed =
    value      the overpayment the arm would demand: for each upcoder it calls, the point estimate extrapolated from the RANDOM charts the arm obtained (src/pi_estimate.py,
               the same arithmetic as the agent's estimate_overpayment tool; a negative estimate counts as 0; a provider with no random charts adds 0),
  - C_COPY     per request round to a practice (records the plan pays for),
  - C_BURDEN   per request round to an honest practice (staff time the practice spends),
  - C_REVIEW   per practice whose charts came back (a clinical review of the returned charts),
  - C_FALSE    per honest doctor called upcoding (the demand is wrong and is reversed; the extrapolated amount is NOT counted as value).
The estimate is what the arm would demand, not the dollars actually overpaid: a payer recovers only what it can document and extrapolate, so an upcoder found on thin or targeted
charts is worth less (or nothing) and a missed one is worth nothing.

Cost parameters and where they come from (all US dollars; the first three are published figures, the last two are stated assumptions, shown with a sensitivity range):
  C_COPY    $90 per round: a round asks for 30 records; CMS tells Recovery Auditors to pay providers $0.15 per page up to $15 per record (Medicare Program Integrity Manual
            Transmittal 786, 2018); 30 records x about 20 pages x $0.15 = $90. MACs are not required to pay for records, so this is an upper-middle figure.
  C_BURDEN  $43.84 per round: Premier's 2022 survey of 516 hospitals, the average cost of fighting one denied claim (staff time, not clinical labor), used as a proxy for a practice's
            handling cost per round.
  C_REVIEW  $158 per practice reviewed: GAO-16-394 (2016): Recovery Auditors cost CMS an average $158 per review, the Supplemental Medical Review Contractor $256 (2013-2014 data).
  C_FALSE   $2,000 per honest doctor called: ASSUMPTION (no published figure found); the 2016 Change Healthcare estimate of $118 per reworked claim times a typical sample of about 17
            claims is about $2,000; sensitivity at $0 and $10,000.
Scale caveat: a synthetic provider has about 240 claims a year, far fewer than a real family-practice provider, so extrapolated recoveries are small beside fixed per-round costs. Read the
net dollars as a relative ranking and look at the break-even scale (the factor by which values would have to grow for the arm to break even), not as a business case.

Usage: python eval/dollar_reward.py     (writes docs/dev_arm_dollars.md)
"""
import csv
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import eval61_recovery as rec  # noqa: E402
import pi_estimate as pe  # noqa: E402

C_COPY, C_BURDEN, C_REVIEW, C_FALSE = 90.0, 43.84, 158.0, 2000.0
CODES = rec.CODES


def point_estimate(pid, claim_rows, random_ids, level_of):
    """Extrapolated overpayment (dollars, at least 0) for one provider from its random charts. level_of: {claim_id: supported level index} for returned charts."""
    by = {r["claim_id"]: r for r in claim_rows}
    ids = [c for c in sorted(random_ids) if c in by and c in level_of]
    if not ids:
        return 0.0
    plan = {"provider_id": pid, "frame_sizes": dict(Counter(r["cpt"] for r in claim_rows)), "sampled_claims": {c: by[c]["cpt"] for c in ids}}
    reviewed = {c: CODES[level_of[c]] for c in ids}
    amounts = {r["claim_id"]: (float(r["allowed_amount"]), float(r["paid_amount"])) for r in claim_rows if r.get("allowed_amount")}
    return max(pe.estimate(plan, reviewed, rec.allowed(), 0.90, claim_amounts=amounts)["point_estimate"], 0.0)


def level_of_rows(rows):
    return {r["claim_id"]: rec._supported_level(r) for r in rows}


def seed_result(called, key, claims_by_provider, random_ids_of, level_of, rounds_of, charts_of):
    """called: set of provider ids called upcoding. Returns the components for one seed."""
    value = sum(point_estimate(p, claims_by_provider.get(p, []), random_ids_of(p), level_of) for p in called if key[p]["role"] == "upcoder")
    honest_called = sum(key[p]["role"] != "upcoder" for p in called)
    all_rounds = sum(rounds_of.values())
    honest_rounds = sum(n for p, n in rounds_of.items() if key[p]["role"] != "upcoder")
    reviewed = sum(1 for p, n in charts_of.items() if n > 0)
    return {"value": value, "honest_called": honest_called, "all_rounds": all_rounds, "honest_rounds": honest_rounds, "reviewed": reviewed,
            "found": sum(key[p]["role"] == "upcoder" for p in called), "upcoders": sum(v["role"] == "upcoder" for v in key.values())}


def from_run(rid, code):
    """Components for a stored run folder (workflow or agent): its summaries, office transcript and returned charts."""
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))["providers"]
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    claims = {}
    for r in csv.DictReader(open(os.path.join(data, "view", "claims.csv"))):
        claims.setdefault(r["provider_id"], []).append(r)
    docs = list(csv.DictReader(open(os.path.join(data, f"view_{rid}", "documentation.csv"))))
    owner = {r["claim_id"]: r["provider_id"] for rows in claims.values() for r in rows}
    level = level_of_rows(docs)
    called = {x["provider_id"] for x in map(json.loads, open(os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")))
              if x["summary"]["leaning"] == "pattern_consistent_with_upcoding"}
    rnd = rec.random_ids(rid)
    rounds, charts = Counter(), Counter()
    for line in open(os.path.join(ROOT, "experiments", rid, "office_transcript.jsonl")):
        e = json.loads(line)
        if e.get("action") in ("send_request", "follow_up", "audit_trail") and "error" not in e:
            rounds[e["provider_id"]] += 1
            charts[e["provider_id"]] += len(e.get("usable_claim_ids", []))
    return seed_result(called, key, claims, lambda p: rnd.get(p, set()), level, dict(rounds), dict(charts))


def net(c, scale=1.0, c_false=C_FALSE, cost_scale=1.0):
    cost = cost_scale * (C_COPY * c["all_rounds"] + C_BURDEN * c["honest_rounds"] + C_REVIEW * c["reviewed"]) + c_false * c["honest_called"]
    return scale * c["value"] - cost


def add(parts):
    keys = ("value", "honest_called", "all_rounds", "honest_rounds", "reviewed", "found", "upcoders")
    return {k: sum(p[k] for p in parts) for k in keys}
