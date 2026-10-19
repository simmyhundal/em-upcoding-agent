"""Release 5 (issue 109): the reward in dollars, the PRIMARY score from the start of release 5 (Simmy's decision); release 4 used points. Free (stored runs and the simulated office).

Recovery model (Simmy's decision, release 5, option 2 of issue 109): for each upcoder the arm calls, a sampled 99215 whose note shows ANY note-level cloning sign (signed late, problems addressed below
the level, bulk-created or paste-heavy in the audit trail, text duplicated across patients) is DENIED IN FULL (its whole paid amount, not only the level difference), because contractors treat cloned
documentation as lacking patient-specific detail and deny and recoup the service (NGS, Palmetto and CGS statements, see issue 109); every other sampled claim contributes the level difference as
before. The per-claim amounts are extrapolated stratified by billed code and the 90% lower bound is the value. RECOVERY = "downcode" gives the level difference only (option 1). One late signature
is enough to flag a note, and honest doctors sign late on about 4% of notes, which is why this option is optimistic; options 1 and 3 are reported as sensitivity.

Net dollars for one arm on one seed =
    value      the overpayment the arm would demand: for each upcoder it calls, the 90% LOWER BOUND of the overpayment extrapolated from the RANDOM charts the arm obtained (src/pi_estimate.py,
               the same arithmetic as the agent's estimate_overpayment tool; Program Integrity Manual chapter 8 recommends the lower bound; a negative bound counts as 0; a provider with
               no random charts adds 0). BOUND = "point" gives the release 4 groundwork's point estimate,
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
import math  # noqa: E402

import note_checks as nc  # noqa: E402
import pi_estimate as pe  # noqa: E402

RECOVERY = "doc_denial"               # "doc_denial": option 2 above (release 5); "downcode": option 1 (level difference only, the release 4 groundwork)
SIGNS = ("late", "problems", "bulk_created", "paste_heavy")      # note-level signs that deny a sampled 99215 in full (text duplication is added in flagged_notes)
BOUND = "ci_low"                      # "ci_low": the 90% lower bound (release 5); "point": the point estimate (release 4 groundwork)
C_COPY, C_BURDEN, C_REVIEW, C_FALSE = 90.0, 43.84, 158.0, 2000.0
CODES = rec.CODES


def flagged_notes(note_rows, claims_by_id):
    """Claim ids whose returned note shows a note-level cloning sign: signed late, problems below the level, bulk-created or paste-heavy (when an audit trail came back), or text
    duplicated in another patient's note of the same provider. note_rows: {claim_id: documentation row} for ONE provider; claims_by_id: its claims."""
    rows = [r for r in note_rows.values() if r.get("note_id") and r["claim_id"] in claims_by_id]
    audit = any(r.get("created_ts") for r in rows)
    pkgs = {r["claim_id"]: nc.pkg_from_doc_row(r, claims_by_id[r["claim_id"]]) for r in rows}
    flagged = set()
    for cid, pkg in pkgs.items():
        f = nc.visit_flags(pkg, claims_by_id[cid], with_audit=audit and "audit" in pkg)
        if any(f.get(sg) for sg in SIGNS):
            flagged.add(cid)
    sh = {cid: nc._shingles(p["note"]["note_text"]) for cid, p in pkgs.items()}
    ids = list(pkgs)
    for i in ids:
        for j in ids:
            if i != j and pkgs[i]["note"]["member_id"] != pkgs[j]["note"]["member_id"] and sh[i] and sh[j] and len(sh[i] & sh[j]) / len(sh[i] | sh[j]) >= nc.DUP_JACCARD:
                flagged.add(i)
                break
    return flagged


def _extrapolate(frame_sizes, vals_by_code):
    """Stratified extrapolation as in src/pi_estimate.py: (point estimate, 90% lower bound floored at 0)."""
    total = var = 0.0
    n_all = k = 0
    for code, N in frame_sizes.items():
        vals = vals_by_code.get(code, [])
        n = len(vals)
        if not n:
            continue
        mean = sum(vals) / n
        s2 = (sum((v - mean) ** 2 for v in vals) / (n - 1)) if n > 1 else 0.0
        total += N * mean
        var += N * N * (1 - n / N) * s2 / n
        n_all += n
        k += 1
    half = pe.t_crit(max(n_all - k, 1), 0.90) * math.sqrt(var)
    return total, max(0.0, total - half)


def point_estimate(pid, claim_rows, random_ids, level_of, note_rows=None, recovery=None):
    """Value (dollars, at least 0) of one called upcoder from its random charts: the 90% lower bound (BOUND) of the extrapolated recovery under the recovery model (RECOVERY, or `recovery`).
    level_of: {claim_id: supported level index} for returned charts; note_rows: {claim_id: documentation row} for the provider's returned notes (needed for option 2)."""
    recovery = recovery or RECOVERY
    by = {r["claim_id"]: r for r in claim_rows}
    ids = [c for c in sorted(random_ids) if c in by and c in level_of]
    if not ids:
        return 0.0
    allowed = rec.allowed()
    amounts = {r["claim_id"]: (float(r["allowed_amount"]), float(r["paid_amount"])) for r in claim_rows if r.get("allowed_amount")}
    denied = flagged_notes({c: note_rows[c] for c in ids if note_rows and c in note_rows}, by) if recovery == "doc_denial" else set()
    vals = {}
    for c in ids:
        b = by[c]["cpt"]
        v = pe.overpay(b, CODES[level_of[c]], allowed, amounts.get(c))
        if c in denied and b == "99215" and c in amounts:
            v = max(v, amounts[c][1])                                   # denied in full: the whole paid amount
        vals.setdefault(b, []).append(v)
    point, low = _extrapolate(dict(Counter(r["cpt"] for r in claim_rows)), vals)
    return low if BOUND == "ci_low" else point


def level_of_rows(rows):
    return {r["claim_id"]: rec._supported_level(r) for r in rows}


def seed_result(called, key, claims_by_provider, random_ids_of, level_of, rounds_of, charts_of, note_rows=None):
    """called: set of provider ids called upcoding. Returns the components for one seed."""
    ups = [p for p in called if key[p]["role"] == "upcoder"]
    mine = lambda p: {c: note_rows[c] for c in (note_rows or {}) if c in {r["claim_id"] for r in claims_by_provider.get(p, [])}}
    value = sum(point_estimate(p, claims_by_provider.get(p, []), random_ids_of(p), level_of, mine(p)) for p in ups)
    value_downcode = sum(point_estimate(p, claims_by_provider.get(p, []), random_ids_of(p), level_of, None, "downcode") for p in ups)
    honest_called = sum(key[p]["role"] != "upcoder" for p in called)
    all_rounds = sum(rounds_of.values())
    honest_rounds = sum(n for p, n in rounds_of.items() if key[p]["role"] != "upcoder")
    reviewed = sum(1 for p, n in charts_of.items() if n > 0)
    return {"value": value, "value_downcode": value_downcode, "honest_called": honest_called, "all_rounds": all_rounds, "honest_rounds": honest_rounds, "reviewed": reviewed,
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
    return seed_result(called, key, claims, lambda p: rnd.get(p, set()), level, dict(rounds), dict(charts), {r["claim_id"]: r for r in docs})


def net(c, scale=1.0, c_false=C_FALSE, cost_scale=1.0, value_key="value"):
    cost = cost_scale * (C_COPY * c["all_rounds"] + C_BURDEN * c["honest_rounds"] + C_REVIEW * c["reviewed"]) + c_false * c["honest_called"]
    return scale * c[value_key] - cost


def add(parts):
    keys = ("value", "value_downcode", "honest_called", "all_rounds", "honest_rounds", "reviewed", "found", "upcoders")
    return {k: sum(p[k] for p in parts) for k in keys}
