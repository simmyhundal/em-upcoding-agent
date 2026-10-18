"""The v2.3 workflow's fixed records policy (data 2.2; issue 99). No judgment: every flagged provider is handled by rank in the same way.

The list is the top 10% by eb_ratio_t (twice the v2.2 list). Providers in the first `tier1_n` ranks (the old top 5%) get the full v2.1 policy; the rest get a light tier:
1. Tier 1 and tier 2: a random request for 30 charts (30-day deadline); follow up once on any deficiency. (An office that goes silent is followed up by the
   same rule, up to the office's 5 rounds: nothing more can be asked of it, and what follows non-response is out of scope, issue 68.)
2. Tier 1 always, tier 2 only when the returned notes show cloning signs (signed late at INFLATED_LATE or more, or problems addressed below the level at
   AUDIT_IF_PROBLEMS): if fewer than 6 usable 99215 charts came back and the provider billed at least 20 of them, send a second, targeted request for 15 charts.
3. Audit trail for up to 20 notes when the notes show those signs (v2.1 asked only on the problems sign; v2.3 also on late signatures).
4. Close.
Tier 2 holds the honest-practice burden down: one request and one follow-up unless the notes give a reason to look closer.
"""
import note_checks
import summary_rules as sr
import workflow_policy_v21 as v21

# W2.3 default (Simmy's decision on #99): list = top 10% by eb_ratio_t, tier 1 = the first 5% of providers; the narrow top-5% list is the alternative (V3 in dev_release3.md)
DEFAULT_SCREEN, LIST_PCT, TIER1_PCT = "eb_ratio_t", 10, 5
RANDOM_N, TARGETED_N, MIN_TOP_CHARTS, MIN_TOP_BILLED, AUDIT_MAX = v21.RANDOM_N, v21.TARGETED_N, v21.MIN_TOP_CHARTS, v21.MIN_TOP_BILLED, v21.AUDIT_MAX
AUDIT_IF_PROBLEMS, AUDIT_IF_LATE, MIN_NOTES = v21.AUDIT_IF_PROBLEMS, sr.INFLATED_LATE, sr.MIN_NOTES_SIGNALS


def cloning_signs(rows, by_id):
    """True when at least MIN_NOTES returned notes show late signatures or too few problems for their level at the rates above."""
    if len(rows) < MIN_NOTES:
        return False
    sig = note_checks.signals_from_docs(rows, by_id)
    return (sig.get("late") or 0) >= AUDIT_IF_LATE or (sig.get("problems") or 0) >= AUDIT_IF_PROBLEMS


def run_policy_23(office, provider_ids, claims_by_provider, tier1_n):
    for rank, pid in enumerate(provider_ids):
        resp = v21._follow(office, pid, office.send_request(pid, {"kind": "random", "n": RANDOM_N}, deadline=30))
        if "error" in resp:
            continue
        st = office.state[pid]
        billed = {r["claim_id"]: r["cpt"] for r in claims_by_provider.get(pid, [])}
        by_id = {r["claim_id"]: r for r in claims_by_provider.get(pid, [])}
        rows = [r for c, r in st["usable"].items() if r.get("note_id")]
        look_closer = rank < tier1_n or cloning_signs(rows, by_id)
        usable_top = [c for c in st["usable"] if billed.get(c) == "99215"]
        n_top_billed = sum(1 for v in billed.values() if v == "99215")
        if look_closer and len(usable_top) < MIN_TOP_CHARTS and n_top_billed >= MIN_TOP_BILLED and st["round"] < office.max_rounds:
            v21._follow(office, pid, office.send_request(pid, {"kind": "targeted", "cpt": "99215", "n": TARGETED_N}, deadline=30))
            rows = [r for c, r in st["usable"].items() if r.get("note_id")]
        if rows and st["round"] < office.max_rounds and cloning_signs(rows, by_id):
            office.request_audit_trail(pid, [r["claim_id"] for r in rows][:AUDIT_MAX])
        office.close_request(pid, "fixed v2.3 policy")
