"""Tests for the simulated provider office. Run: python tests/test_provider_sim.py"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import derive  # noqa: E402
import generate_v2 as g  # noqa: E402
import provider_sim as ps  # noqa: E402
import records  # noqa: E402
import summary_rules as sr  # noqa: E402

D = tempfile.mkdtemp()
g.build(D, os.path.join(tempfile.mkdtemp(), "k.json"), seed=9, n_providers=25, n_upcoders=3, n_hard_neg=2)
VIEW = os.path.join(D, "view")
derive.build_view(D, VIEW)
PIDS = sorted({r["provider_id"] for r in __import__("csv").DictReader(open(os.path.join(VIEW, "claims.csv")))})
SAMPLE = {"kind": "random", "n": 20}


def office(seed=1, **kw):
    return ps.Office(D, VIEW, seed=seed, **kw)


def _force(o, pid, behavior):
    o._st(pid)["behavior"] = behavior


def test_deterministic_and_payer_visible_responses_hide_behavior_and_truth():
    a, b = office(3), office(3)
    ra = [a.send_request(p, SAMPLE) for p in PIDS[:6]]
    rb = [b.send_request(p, SAMPLE) for p in PIDS[:6]]
    assert ra == rb
    blob = json.dumps(ra)
    for leak in ("behavior", "cooperative", "evasive", "sloppy", "upcoder", "problems_level", "justified"):
        assert leak not in blob
    assert all(r["sample_kind"] == "random" for r in ra)


def test_module_does_not_read_the_answer_key():
    src = open(os.path.join(HERE, "..", "src", "provider_sim.py")).read().replace("answer key", "")
    assert "ground_truth" not in src and "answer_key" not in src


def test_caps_on_rounds_and_days():
    o = office()
    pid = PIDS[0]
    _force(o, pid, "evasive")
    r = o.send_request(pid, SAMPLE)
    for _ in range(ps.MAX_ROUNDS + 2):
        r = o.follow_up(pid, ["NO_RESPONSE"])
        if "error" in r:
            break
    assert "error" in r and o._st(pid)["round"] <= ps.MAX_ROUNDS
    assert o.send_request(pid, SAMPLE).get("error")                      # cannot open a second request


def test_cooperative_completes_and_evasive_can_end_non_responsive_without_usable_charts():
    o = office()
    _force(o, PIDS[0], "cooperative")
    r = o.send_request(PIDS[0], SAMPLE)
    if r["status"] != "complete":
        r = o.follow_up(PIDS[0], [d["code"] for d in r["deficiencies"]])
    assert o.close_request(PIDS[0])["end_state"] in ("complete", "partial") and o._st(PIDS[0])["usable"]
    # an evasive office that never answers ends non_responsive; the summary step then calls it inconclusive, not upcoding
    e = office()
    pid = PIDS[1]
    _force(e, pid, "evasive")
    e._round = lambda p, st, deadline, addressed, **kw: (st.update(round=st["round"] + 1), {"deficiencies": [], "status": "no_response"})[1]
    e.send_request(pid, SAMPLE)
    assert e.close_request(pid)["end_state"] == "non_responsive" and e.documentation_rows() == []
    packet = {"provider_id": pid, "documentation_review": {"claims_with_documentation": 0, "by_billed_level": []}}
    assert sr.rule_leaning(packet)[0] == sr.INCONCLUSIVE


def test_sample_kinds_are_labelled_and_only_random_supports_extrapolation():
    o = office()
    pid = PIDS[2]
    _force(o, pid, "cooperative")
    t = o.send_request(pid, {"kind": "targeted", "cpt": "99215", "n": 10})
    assert t["sample_kind"] == "targeted"
    assert o.documentation_rows(kinds=("random",)) == [] and len(o.documentation_rows(kinds=("targeted",))) == t["usable_total"]


def test_follow_up_releases_fixable_deficiencies_for_a_sloppy_office():
    for seed in range(40):
        o = office(seed)
        pid = PIDS[3]
        _force(o, pid, "sloppy")
        r = o.send_request(pid, SAMPLE)
        codes = [d["code"] for d in r["deficiencies"] if d["code"] in ps.FIXABLE_BY_FOLLOWUP]
        if codes and r["usable_total"] == 0:
            r2 = o.follow_up(pid, codes)
            if r2["usable_total"] > 0:
                return
    raise AssertionError("no seed produced a fixable deficiency that a follow-up resolved")


def test_correlation_knob_changes_upcoder_behaviour_only_when_set():
    roles = {p: "upcoder" for p in PIDS}
    base = [office(1, roles=roles)._behavior(p) for p in PIDS]
    same = [office(1)._behavior(p) for p in PIDS]
    corr = [office(1, correlation=1.0, roles=roles)._behavior(p) for p in PIDS]
    assert base == same
    assert sum(b in ("evasive", "sloppy") for b in corr) > sum(b in ("evasive", "sloppy") for b in base)


def _v21():
    d, key = tempfile.mkdtemp(), os.path.join(tempfile.mkdtemp(), "k.json")
    g.build(d, key, seed=9, n_providers=25, n_upcoders=3, n_hard_neg=2, data_version="2.1")
    view = os.path.join(d, "view")
    derive.build_view(d, view)
    return d, view


def test_office_v21_second_request_note_package_signatures_and_audit_trail():
    d, view = _v21()
    pids = sorted({r["provider_id"] for r in __import__("csv").DictReader(open(os.path.join(view, "claims.csv")))})
    old = ps.Office(d, view, seed=1)
    old.send_request(pids[0], SAMPLE)
    assert "already open" in old.send_request(pids[0], {"kind": "targeted", "cpt": "99215", "n": 10})["error"]       # frozen behaviour
    o = ps.Office(d, view, seed=1, version="2.1")
    pid = pids[1]
    o._st(pid)["behavior"] = "cooperative"
    r1 = o.send_request(pid, {"kind": "random", "n": 20})
    r2 = o.send_request(pid, {"kind": "targeted", "cpt": "99215", "n": 5})
    assert "error" not in r2 and r2["sample_kinds"] == ["random", "targeted"] and r2["requested_total"] >= r1["requested_total"]
    kinds = o._st(pid)["kinds"]
    assert set(o.random_claim_ids(pid)) == {c for c, k in kinds.items() if k == "random"}
    rows = o.documentation_rows()
    assert rows and all("note_text" in r and "auth_status" in r and "order_count" in r for r in rows)
    assert all(r["auth_status"] not in ("unsigned", "illegible") for r in rows)                    # those are held back until fixed
    assert {c for c in o._st(pid)["usable"]} <= set(kinds)
    ids = sorted(o._st(pid)["usable"])[:5]
    a = o.request_audit_trail(pid, ids)
    assert a["status"] in ("audit_trail_provided", "refused")
    if a["status"] == "audit_trail_provided":
        assert all(o._st(pid)["usable"][c]["created_ts"] for c in ids)
    assert "not available" in old.request_audit_trail(pids[0], ids)["error"]


def test_office_v21_unsigned_charts_are_held_back_then_attested_after_a_follow_up():
    d, view = _v21()
    notes = __import__("note_checks").load_notes(d)
    bad = {c for c, p in notes.items() if p["auth"]["status"] in ("unsigned", "illegible")}
    by = {}
    for r in __import__("csv").DictReader(open(os.path.join(view, "claims.csv"))):
        by.setdefault(r["provider_id"], []).append(r["claim_id"])
    pid = next(p for p, ids in by.items() if len(set(ids) & bad) >= 1)
    o = ps.Office(d, view, seed=1, version="2.1")
    o._st(pid)["behavior"] = "cooperative"
    target = sorted(set(by[pid]) & bad)[:1]
    r = o.send_request(pid, {"kind": "targeted", "claim_ids": target})
    if r["status"] not in ("complete", "partial"):
        return
    assert target[0] not in o._st(pid)["usable"] and any(x["code"] in ("MISSING_SIGNATURE", "ILLEGIBLE") for x in r["deficiencies"])
    for _ in range(4):
        r = o.follow_up(pid, ["MISSING_SIGNATURE", "ILLEGIBLE"]) if "error" not in r else r
        if target[0] in o._st(pid)["usable"]:
            assert o._st(pid)["usable"][target[0]]["auth_status"] == "attested"
            return


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
