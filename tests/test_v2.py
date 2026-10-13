"""Tests for the v2 data model: generator, derived risk, detector view, records requests, claim-based pricing.
Run: python tests/test_v2.py"""
import csv
import json
import os
import random
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import derive  # noqa: E402
import generate_v2 as g  # noqa: E402
import pi_estimate as pe  # noqa: E402
import records  # noqa: E402

_CACHE = {}


def _build(seed=3, **kw):
    key = (seed, tuple(sorted(kw.items())))
    if key not in _CACHE:
        d, k = tempfile.mkdtemp(), os.path.join(tempfile.mkdtemp(), "key.json")
        g.build(d, k, seed=seed, n_providers=30, n_upcoders=4, n_hard_neg=3, **kw)
        view = os.path.join(d, "view")
        derive.build_view(d, view)
        _CACHE[key] = (d, k, view)
    return _CACHE[key]


def _rows(d, name):
    with open(os.path.join(d, name)) as f:
        return list(csv.DictReader(f))


def test_deterministic_and_answer_key_outside_data():
    a, b = _build(3), _build(3)
    assert _rows(a[0], "claims_header.csv")[:50] == _rows(b[0], "claims_header.csv")[:50]
    assert _rows(a[0], "claims_header.csv")[:50] != _rows(_build(4)[0], "claims_header.csv")[:50]
    try:
        g.build(os.path.join(a[0], "x"), os.path.join(a[0], "x", "key.json"), n_providers=10)
        raise AssertionError("answer key inside data folder must be refused")
    except ValueError:
        pass


def test_plan_tables_and_view_leak_no_truth_or_conditions():
    d, _, view = _build()
    for path in ("members.csv", "providers.csv", "claims_header.csv", "claim_lines.csv", "remittance.csv"):
        head = " ".join(_rows(d, path)[0].keys()).lower()
        for banned in ("role", "justified", "upcod", "clone", "condition", "risk"):
            assert banned not in head, (path, banned)
    assert "justified" not in " ".join(_rows(view, "claims.csv")[0].keys())


def test_counts_roles_and_configurable_base_rate():
    _, key, _ = _build()
    roles = Counter(v["role"] for v in json.load(open(key))["providers"].values())
    assert roles == {"normal": 23, "upcoder": 4, "hard_negative": 3}
    d, k = tempfile.mkdtemp(), os.path.join(tempfile.mkdtemp(), "key.json")
    g.build(d, k, seed=1, n_providers=40, upcoder_rate=0.05, hard_neg_rate=0.05)
    assert Counter(v["role"] for v in json.load(open(k))["providers"].values())["upcoder"] == 2


def test_only_upcoders_bill_above_justified_level():
    d, key, _ = _build()
    truth = json.load(open(key))
    role = {p: v["role"] for p, v in truth["providers"].items()}
    just = truth["justified_cpt_by_claim"]
    up_seen = False
    for h in _rows(d, "claims_header.csv"):
        if h["claim_frequency"] != "1" or h["claim_id"] not in just:
            continue
    lines = {r["claim_id"]: r for r in _rows(d, "claim_lines.csv") if r["line_no"] == "1"}
    rend = {h["claim_id"]: h["rendering_npi"] for h in _rows(d, "claims_header.csv") if h["claim_frequency"] == "1"}
    for cid, j in just.items():
        billed = lines[cid]["cpt"]
        if role[rend[cid]] != "upcoder":
            assert billed == j
        elif billed != j:
            up_seen = True
            assert int(billed) == int(j) + 1
    assert up_seen


def test_view_handles_replacements_voids_and_denials_and_derives_conditions_from_claims_only():
    d, _, view = _build()
    header = {h["claim_id"]: h for h in _rows(d, "claims_header.csv")}
    status = {r["claim_id"]: r["status"] for r in _rows(d, "remittance.csv")}
    assert any(h["claim_frequency"] == "7" for h in header.values()) and any(h["claim_frequency"] == "8" for h in header.values())
    assert any(s == "denied" for s in status.values())
    ids = [r["claim_id"] for r in _rows(view, "claims.csv")]
    assert len(ids) == len(set(ids))                                   # one row per visit
    voided = {h["original_claim_id"] for h in header.values() if h["claim_frequency"] == "8"}
    assert not (set(ids) & voided)
    assert not {c for c, s in status.items() if s == "denied"} & set(ids)
    # derived conditions are exactly the mapped diagnosis codes on the member's accepted visits
    visits = derive.accepted_visits(d)
    expect = {}
    for v in visits.values():
        for code in v["diagnosis_codes"].split(";"):
            if code in derive.CONDITION_MAP:
                expect.setdefault(v["member_id"], set()).add(code)
    for r in _rows(view, "patients.csv"):
        assert int(r["chronic_condition_count"]) == len(expect.get(r["patient_id"], ()))
    assert "chronic_condition_count" not in _rows(d, "members.csv")[0]


def test_documented_level_rule():
    assert records.mdm_level(0, 4, 2) == 2 and records.mdm_level(3, 3, 0) == 3 and records.mdm_level(4, 4, 4) == 4
    assert records.supported_level(2, "35") == 3 and records.supported_level(3, "") == 3 and records.supported_level(1, "15") == 1
    assert records.level_from_minutes("") == -1 and records.level_from_minutes("55") == 4


def test_records_request_limits_late_and_missing():
    d, _, view = _build()
    provs = sorted({r["provider_id"] for r in _rows(view, "claims.csv")})[:5]
    docs, status = records.request_records(d, view, provs, 20, random.Random(1))
    assert all(s["requested"] <= 20 for s in status)
    assert all(s["received"] + s["late"] + s["no_response"] == s["requested"] for s in status)
    assert any(s["late"] or s["no_response"] for s in status) and len(docs) == sum(s["received"] for s in status)
    none, st0 = records.request_records(d, view, provs, 20, random.Random(1), response_rate=0.0)
    assert none == [] and all(s["received"] == 0 for s in st0)
    again, _ = records.request_records(d, view, provs, 20, random.Random(1))
    assert again == docs


def test_cloned_documentation_inflates_notes_but_not_claim_facts():
    d, key, view = _build(5, clone_share=1.0)
    truth = json.load(open(key))
    cloners = {p for p, v in truth["providers"].items() if v["clones_notes"]}
    assert len(cloners) == 4
    uni = {r["claim_id"]: r for r in _rows(d, "records/records_universe.csv")}
    just = truth["justified_cpt_by_claim"]
    seen = 0
    for r in _rows(view, "claims.csv"):
        if r["provider_id"] in cloners and r["cpt"] != just[r["claim_id"]]:
            u = uni[r["claim_id"]]
            assert (int(u["problems_level"]), int(u["data_level"]), int(u["risk_level"])) == (int(r["cpt"]) - 99211,) * 3
            seen += 1
    assert seen > 0
    d0, k0, v0 = _build(5, clone_share=0.0)
    assert not any(v["clones_notes"] for v in json.load(open(k0))["providers"].values())


def test_overpayment_uses_claim_amounts_and_paid_share():
    allowed = {"99213": 84.02, "99214": 120.21, "99215": 170.18}
    flat = pe.overpay("99215", "99214", allowed)
    assert abs(flat - 49.97) < 0.01
    own = pe.overpay("99215", "99214", allowed, (170.18, 136.14))      # plan paid 80%
    assert abs(own - 49.97 * 0.8) < 0.01
    assert pe.overpay("99214", "99215", allowed, (120.21, 96.17)) == 0.0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
