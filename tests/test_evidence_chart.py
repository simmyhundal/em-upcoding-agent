"""Tests for the evidence chart and case report. Run: python tests/test_evidence_chart.py"""
import json
import os
import sys
import tempfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import case_report  # noqa: E402
import case_summary as cs  # noqa: E402
import evidence_chart as ec  # noqa: E402
import flagging  # noqa: E402
import generate_synthetic as g  # noqa: E402

D = tempfile.mkdtemp()
g.build(D, os.path.join(tempfile.mkdtemp(), "gt.json"), seed=9, n_normal=40, n_upcoders=3, n_hard_neg=3)
COUNTS = ec.load_counts(D)


def test_wilson_interval_matches_known_values():
    lo, hi = ec.wilson(50, 100)
    assert abs(lo - 0.4038) < 1e-3 and abs(hi - 0.5962) < 1e-3
    lo, hi = ec.wilson(0, 10)
    assert lo == 0.0 and abs(hi - 0.2775) < 1e-3
    assert ec.wilson(0, 0) == (0.0, 0.0)


def test_chart_counts_match_the_packet_table():
    flagged = os.path.join(D, "f.csv")
    import csv
    rows = flagging.flag(D, top_n=3)
    with open(flagged, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=flagging.COLUMNS)
        w.writeheader()
        w.writerows(rows)
    packets = [r["packet"] for r in cs.run(D, flagged, os.path.join(D, "p.jsonl"), dry_run=True)]
    for p in packets:
        table = {t["chronic_conditions"]: t for t in p["99215_share_by_patient_complexity"]}
        for d in ec.chart_data(COUNTS, p["provider_id"]):
            if d["visits"]:
                assert d["visits"] == table[d["bucket"]]["visits"] and d["n_99215"] == table[d["bucket"]]["n_99215"]
            else:
                assert d["bucket"] not in table


def test_peer_boxes_exclude_the_provider_and_thin_levels_are_marked():
    pid = sorted(COUNTS)[0]
    data = ec.chart_data(COUNTS, pid)
    for d in data:
        assert d["thin"] == (d["visits"] < ec.MIN_SHOWN_VISITS)
        if d["peer"]:
            n_peers = sum(1 for p, c in COUNTS.items() if p != pid and c[d["bucket"]][0] >= ec.MIN_PEER_VISITS)
            assert d["peer"]["n"] == n_peers
    svg = ec.render_svg(pid, data)
    ET.fromstring(svg)                                    # well-formed XML
    assert svg.count("thin (under") == sum(d["thin"] for d in data)


def test_case_report_embeds_chart_and_flags_rejected():
    rec = {"provider_id": "P0001", "summary": {"headline": "h", "leaning": "inconclusive", "rationale": "r",
                                               "cited_claim_ids": ["C0000001"], "next_steps": ["step"]},
           "citation_check": {"passed": False, "n_cited": 1, "n_valid": 0, "reason": "1 cited claim(s) do not exist"}}
    md = case_report.render(rec, "../charts/P0001.svg")
    assert "![99215 share by patient complexity](../charts/P0001.svg)" in md and "Rejected by the citation guardrail" in md
    rec["citation_check"] = {"passed": True, "n_cited": 1, "n_valid": 1, "reason": ""}
    assert "Rejected" not in case_report.render(rec, "x.svg")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
