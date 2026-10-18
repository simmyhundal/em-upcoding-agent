"""Workflow v2.4 candidate records policies (issue 102; development only until one is chosen). Built on policy 2.3 (eval/workflow_policy_23.py).

Options, all off by default (which reproduces policy 2.3):
- gate_t, gate_all: a provider whose ratio of billed 99215 share to expected is below gate_t is not asked at all. By default only the light tier (ranks beyond the
  first tier1_n) is gated; gate_all gates tier 1 too. This is what agent v3.3 does in practice (docs/release4_agent_narrowing.md).
- stop_silent: a practice that returned no usable chart after the first request and its follow-up is closed; no targeted request, no audit trail, no further rounds.
"""
import workflow_policy_23 as p23
import workflow_policy_v21 as v21


def run_policy_24(office, provider_ids, claims_by_provider, tier1_n, ratio, gate_t=None, gate_all=False, stop_silent=False):
    for rank, pid in enumerate(provider_ids):
        if gate_t is not None and (gate_all or rank >= tier1_n) and ratio.get(pid, 0.0) < gate_t:
            continue
        resp = v21._follow(office, pid, office.send_request(pid, {"kind": "random", "n": p23.RANDOM_N}, deadline=30))
        if "error" in resp:
            continue
        st = office.state[pid]
        if stop_silent and not st["usable"]:
            office.close_request(pid, "no usable charts after a request and a follow-up (policy 2.4)")
            continue
        billed = {r["claim_id"]: r["cpt"] for r in claims_by_provider.get(pid, [])}
        by_id = {r["claim_id"]: r for r in claims_by_provider.get(pid, [])}
        rows = [r for c, r in st["usable"].items() if r.get("note_id")]
        look_closer = rank < tier1_n or p23.cloning_signs(rows, by_id)
        usable_top = [c for c in st["usable"] if billed.get(c) == "99215"]
        n_top_billed = sum(1 for v in billed.values() if v == "99215")
        if look_closer and len(usable_top) < p23.MIN_TOP_CHARTS and n_top_billed >= p23.MIN_TOP_BILLED and st["round"] < office.max_rounds:
            v21._follow(office, pid, office.send_request(pid, {"kind": "targeted", "cpt": "99215", "n": p23.TARGETED_N}, deadline=30))
            rows = [r for c, r in st["usable"].items() if r.get("note_id")]
        if rows and st["round"] < office.max_rounds and p23.cloning_signs(rows, by_id):
            office.request_audit_trail(pid, [r["claim_id"] for r in rows][:p23.AUDIT_MAX])
        office.close_request(pid, "fixed v2.4 candidate policy")
