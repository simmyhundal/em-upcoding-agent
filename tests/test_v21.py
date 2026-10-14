"""Tests for data v2.1 (note package) and the claim-versus-note checks. Run: python tests/test_v21.py"""
import csv
import hashlib
import json
import os
import sys
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import derive  # noqa: E402
import generate_v2 as g  # noqa: E402
import note_checks as nc  # noqa: E402

KW = dict(seed=5, n_providers=30, n_upcoders=4, n_hard_neg=2)
_C = {}


def build(version="2.1", strength=0.7):
    k = (version, strength)
    if k not in _C:
        d, key = tempfile.mkdtemp(), os.path.join(tempfile.mkdtemp(), "k.json")
        g.build(d, key, data_version=version, clone_signal_strength=strength, **KW)
        derive.build_view(d, os.path.join(d, "view"))
        _C[k] = (d, key)
    return _C[k]


def digest(d):
    h = hashlib.sha256()
    for f in ("claims_header.csv", "claim_lines.csv", "remittance.csv", "records/records_universe.csv"):
        h.update(open(os.path.join(d, f), "rb").read())
    return h.hexdigest()


def test_v21_keeps_claims_and_universe_identical_to_v20_and_is_deterministic():
    assert digest(build("2.0")[0]) == digest(build("2.1")[0])
    d, key = tempfile.mkdtemp(), os.path.join(tempfile.mkdtemp(), "k.json")
    g.build(d, key, data_version="2.1", **KW)
    assert open(os.path.join(d, "records", "visit_notes.csv")).read() == open(os.path.join(build()[0], "records", "visit_notes.csv")).read()


def test_every_visit_has_a_note_and_signature_and_orders_match_claim_lab_lines():
    d, _ = build()
    notes = nc.load_notes(d)
    lines = list(csv.DictReader(open(os.path.join(d, "claim_lines.csv"))))
    labs = {r["claim_id"] for r in lines if r["line_no"] == "2"}
    headers = {r["claim_id"] for r in csv.DictReader(open(os.path.join(d, "claims_header.csv"))) if r["claim_frequency"] == "1"}
    assert set(notes) == headers
    assert all("auth" in p and "audit" in p for p in notes.values())
    assert {c for c, p in notes.items() if p["orders"]} == (labs & headers)                 # an order exists exactly where the claim shows a lab


def test_cloned_notes_do_not_gain_orders_or_diagnoses_and_signals_follow_strength():
    d, key = build(strength=1.0)
    truth = json.load(open(key))
    cloned = {c["claim_id"] for c in truth["cloned_visits"]}
    assert cloned and truth["clone_signal_strength"] == 1.0
    notes = nc.load_notes(d)
    hi = sum("multiple active chronic conditions" in notes[c]["note"]["note_text"] for c in cloned)
    assert hi == len(cloned)                                                     # at strength 1 every cloned note carries the cloned text
    d0, key0 = build(strength=0.0)
    notes0 = nc.load_notes(d0)
    assert not any("multiple active chronic conditions" in notes0[c]["note"]["note_text"] for c in cloned)
    claims = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(d, "view", "claims.csv")))}
    for c in [x for x in cloned if x in claims][:50]:
        assert set(notes[c]["note"]["problems_addressed"].split(";")) <= set(claims[c]["diagnosis_codes"].split(";"))


def test_checks_flag_what_they_should_and_are_rates_not_proof():
    d, key = build(strength=1.0)
    truth = json.load(open(key))["providers"]
    notes = nc.load_notes(d)
    claims = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(d, "view", "claims.csv")))}
    by = {}
    for c, r in claims.items():
        by.setdefault(r["provider_id"], []).append(c)
    cl = [p for p, t in truth.items() if t["clones_notes"] and len(by.get(p, [])) >= 40]
    ho = [p for p, t in truth.items() if t["role"] == "normal" and not t.get("uses_template") and len(by.get(p, [])) >= 40][:15]
    assert cl and ho

    def rate(p, sig):
        return nc.provider_signals([(notes[c], claims[c]) for c in sorted(by[p])[:40]], with_audit=True)[sig]
    for sig in ("paste_heavy", "bulk_created"):
        assert sum(rate(p, sig) for p in cl) / len(cl) > sum(rate(p, sig) for p in ho) / len(ho) + 0.05, sig


def test_module_never_reads_the_answer_key():
    src = open(os.path.join(HERE, "..", "src", "note_checks.py")).read()
    assert "ground_truth" not in src and "answer_key" not in src


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
