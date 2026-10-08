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
g.build(D, seed=11, n_normal=40, n_upcoders=3, n_hard_neg=3)
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


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
