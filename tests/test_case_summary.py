"""Tests for the case-summary step, using a fake LLM (no API call). Run: python tests/test_case_summary.py"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import case_summary as cs  # noqa: E402
import flagging  # noqa: E402
import generate_synthetic as g  # noqa: E402

D = tempfile.mkdtemp()
g.build(D, os.path.join(tempfile.mkdtemp(), "gt.json"), seed=11, n_normal=40, n_upcoders=3, n_hard_neg=3)
FLAGGED = os.path.join(D, "flagged.csv")
import csv  # noqa: E402
rows = flagging.flag(D, top_n=5)
with open(FLAGGED, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=flagging.COLUMNS)
    w.writeheader()
    w.writerows(rows)


def test_packet_has_evidence_and_no_ground_truth():
    out = cs.run(D, FLAGGED, os.path.join(D, "p.jsonl"), dry_run=True)
    assert len(out) == 5
    blob = json.dumps(out)
    for leak in ("upcoder", "hard_negative", "justified", "upgrade_fraction", "_role"):
        assert leak not in blob
    pkt = out[0]["packet"]
    assert pkt["n_claims"] > 0 and pkt["99215_share_by_patient_complexity"]


def test_fake_llm_roundtrip_records_citations_unchecked():
    def fake(system, user):
        pkt = json.loads(user.split("Evidence packet (JSON):\n")[1].split("\n\nWrite the case")[0])
        ids = [c["claim_id"] for c in pkt["99215_claims_on_low_complexity_patients_0_or_1_conditions"][:2]]
        return json.dumps({"headline": "h", "leaning": "inconclusive", "rationale": "r",
                           "cited_claim_ids": ids, "next_steps": ["review notes"]})
    out = cs.run(D, FLAGGED, os.path.join(D, "s.jsonl"), limit=2, llm=fake)
    assert len(out) == 2 and all(r["citations_checked"] is False for r in out)
    assert set(out[0]["summary"]) == set(cs.SCHEMA["properties"])


def _packets():
    return [r["packet"] for r in cs.run(D, FLAGGED, os.path.join(D, "p2.jsonl"), dry_run=True)]


def test_sampler_is_deterministic():
    a = json.dumps(_packets(), sort_keys=True)
    b = json.dumps(_packets(), sort_keys=True)
    assert a == b


def test_sampler_sizes_and_distinct_patients_when_possible():
    LOW = "99215_claims_on_low_complexity_patients_0_or_1_conditions"
    HIGH = "99215_claims_on_high_complexity_patients_4_plus_conditions"
    for p in _packets():
        for key, cap in ((LOW, cs.LOW_COMPLEXITY_SAMPLE), (HIGH, cs.HIGH_COMPLEXITY_SAMPLE)):
            lst = p[key]
            assert len(lst) <= cap
            assert len({c["patient_id"] for c in lst}) >= min(len(lst), 3) or len(lst) <= 3
        cmp_ = p["comparison_claims_other_than_99215_random_sample"]
        assert len(cmp_) <= cs.COMPARISON_SAMPLE and all(c["cpt"] != "99215" for c in cmp_)


def test_sample_claims_stratifies_and_prefers_distinct_patients():
    import random
    rows = [{"claim_id": f"C{i:03d}", "patient_id": f"A{i % 2}", "g": "x"} for i in range(20)]       # 2 patients
    rows += [{"claim_id": f"D{i:03d}", "patient_id": f"B{i}", "g": "y"} for i in range(20)]           # 20 patients
    out = cs.sample_claims(random.Random(1), rows, 6, lambda r: r["g"])
    assert len(out) == 6 and {r["g"] for r in out} == {"x", "y"}
    ys = [r for r in out if r["g"] == "y"]
    assert len({r["patient_id"] for r in ys}) == len(ys)           # distinct where possible
    # falls back to repeats only when patients run out
    only_two = cs.sample_claims(random.Random(1), rows[:20], 5, lambda r: r["g"])
    assert len(only_two) == 5 and len({r["patient_id"] for r in only_two}) == 2


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
