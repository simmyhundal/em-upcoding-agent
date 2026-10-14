"""The v2.1 workflow's fixed records policy against the provider office (data v2.1). No judgment: every flagged provider is handled the same way.

1. Send a random request for 30 charts (30-day deadline); follow up once on any deficiency.
2. If fewer than 6 usable charts of the code the provider bills most at the top (99215) came back and the provider billed at least 20 of them,
   send a second, targeted request for 15 charts of 99215 (random first, targeted after); follow up once on any deficiency.
3. If the returned notes address fewer problems than their level implies (rate at least 0.35), request the audit trail for up to 20 of them.
4. Close.
Mirror of the agent's options in v3.1; the agent chooses, the workflow follows this script.
"""
import note_checks

RANDOM_N, TARGETED_N, MIN_TOP_CHARTS, MIN_TOP_BILLED, AUDIT_IF_PROBLEMS, AUDIT_MAX = 30, 15, 6, 20, 0.35, 20


def _follow(office, pid, resp):
    if resp.get("deficiencies") and resp.get("rounds_left", 0) > 0:
        return office.follow_up(pid, [d["code"] for d in resp["deficiencies"]], deadline=30)
    return resp


def run_policy_v21(office, provider_ids, claims_by_provider):
    for pid in provider_ids:
        resp = _follow(office, pid, office.send_request(pid, {"kind": "random", "n": RANDOM_N}, deadline=30))
        if "error" in resp:
            continue
        st = office.state[pid]
        billed = {r["claim_id"]: r["cpt"] for r in claims_by_provider.get(pid, [])}
        usable_top = [c for c in st["usable"] if billed.get(c) == "99215"]
        n_top_billed = sum(1 for v in billed.values() if v == "99215")
        if len(usable_top) < MIN_TOP_CHARTS and n_top_billed >= MIN_TOP_BILLED and st["round"] < office.max_rounds:
            _follow(office, pid, office.send_request(pid, {"kind": "targeted", "cpt": "99215", "n": TARGETED_N}, deadline=30))
        by_id = {r["claim_id"]: r for r in claims_by_provider.get(pid, [])}
        rows = [r for c, r in st["usable"].items() if r.get("note_id")]
        if rows and st["round"] < office.max_rounds:
            sig = note_checks.signals_from_docs(rows, by_id)
            if (sig.get("problems") or 0) >= AUDIT_IF_PROBLEMS:
                office.request_audit_trail(pid, [r["claim_id"] for r in rows][:AUDIT_MAX])
        office.close_request(pid, "fixed v2.1 policy")
