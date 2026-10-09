"""Tests for the Payment Integrity packet and estimator. Run: python tests/test_pi.py"""
import csv
import json
import os
import sys
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import flagging  # noqa: E402
import generate_synthetic as g  # noqa: E402
import pi_estimate as pe  # noqa: E402
import pi_packet as pp  # noqa: E402

ALLOWED = {"99213": 80.0, "99214": 100.0, "99215": 150.0}


def test_sample_size_rule():
    assert pp.sample_size(30) == 30                       # small frame: review everything
    assert pp.sample_size(46) == 28                       # finite-population correction
    assert pp.sample_size(817) == 63 and pp.sample_size(100000) == 68
    assert pp.sample_size(46, margin=0.05) > pp.sample_size(46)
    assert pp.sample_size(1000, confidence=0.95) > pp.sample_size(1000, confidence=0.90)


def test_plan_is_reproducible_and_inside_the_frame():
    claims = [{"claim_id": f"C{i:04d}", "cpt": "99215" if i % 2 else "99214"} for i in range(400)]
    a = pp.make_plan("P0001", claims, ["99215", "99214"], 0.10, 0.90)
    b = pp.make_plan("P0001", claims, ["99215", "99214"], 0.10, 0.90)
    assert a == b and a != pp.make_plan("P0002", claims, ["99215", "99214"], 0.10, 0.90)
    frame = {c["claim_id"]: c["cpt"] for c in claims}
    assert all(frame[cid] == code for cid, code in a["sampled_claims"].items())
    assert sum(a["sample_sizes"].values()) == len(a["sampled_claims"])


def test_estimator_matches_hand_calculation():
    plan = {"provider_id": "P", "frame_sizes": {"99215": 100},
            "sampled_claims": {f"C{i}": "99215" for i in range(4)}}
    reviewed = {"C0": "99215", "C1": "99215", "C2": "99214", "C3": "99214"}   # overpayment 0, 0, 50, 50
    r = pe.estimate(plan, reviewed, ALLOWED, 0.90)
    assert abs(r["point_estimate"] - 2500) < 1e-9
    assert abs(r["standard_error"] - 1414.2136) < 1e-3     # 100 * sqrt(0.96 * 833.33 / 4)
    assert abs(r["ci_high"] - (2500 + 2.353 * 1414.2136)) < 1e-2 and r["ci_low"] == 0.0   # lower limit floored at 0
    assert r["response_rate"] == 1.0


def test_census_has_no_sampling_error_and_missing_records_are_handled():
    plan = {"provider_id": "P", "frame_sizes": {"99215": 4},
            "sampled_claims": {f"C{i}": "99215" for i in range(4)}}
    full = {"C0": "99215", "C1": "99214", "C2": "99214", "C3": "99213"}      # overpayment 0, 50, 50, 70
    r = pe.estimate(plan, full, ALLOWED, 0.90)
    assert r["standard_error"] == 0 and abs(r["point_estimate"] - 170) < 1e-9
    part = {"C0": "99214", "C1": "", "C2": "99214", "C3": ""}                 # two records missing
    ex = pe.estimate(plan, part, ALLOWED, 0.90, "exclude")
    assert ex["reviewed_claims"] == 2 and ex["response_rate"] == 0.5 and abs(ex["point_estimate"] - 200) < 1e-9
    un = pe.estimate(plan, part, ALLOWED, 0.90, "unsupported")                # blanks count as one level lower
    assert un["reviewed_claims"] == 4 and abs(un["point_estimate"] - 200) < 1e-9


def test_overpayment_ignores_underbilling():
    assert pe.overpay("99214", "99215", ALLOWED) == 0.0 and pe.overpay("99215", "99213", ALLOWED) == 70.0


def test_packet_files_are_written_without_ground_truth():
    d = tempfile.mkdtemp()
    g.build(d, os.path.join(tempfile.mkdtemp(), "gt.json"), seed=21, n_normal=40, n_upcoders=3, n_hard_neg=3)
    rows = flagging.flag(d, top_n=3)
    flagged = os.path.join(d, "f.csv")
    with open(flagged, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=flagging.COLUMNS)
        w.writeheader()
        w.writerows(rows)
    checked = os.path.join(d, "checked.jsonl")
    with open(checked, "w") as f:
        for r in rows[:2]:
            f.write(json.dumps({"provider_id": r["provider_id"], "citation_check": {"passed": True, "n_cited": 1, "n_valid": 1, "reason": ""},
                                "summary": {"headline": "h", "leaning": "pattern_consistent_with_upcoding", "rationale": "r",
                                            "cited_claim_ids": ["C0000001"], "next_steps": ["step"]}}) + "\n")
    allowed_path = os.path.join(d, "allowed.json")
    json.dump({"codes": {c: {"allowed_amount": a} for c, a in {"99211": 20.0, "99212": 50.0, "99213": 80.0, "99214": 120.0, "99215": 170.0}.items()}},
              open(allowed_path, "w"))
    out = os.path.join(d, "packets")
    done = pp.build(d, flagged, checked, os.path.join(d, "charts"), allowed_path, out, example=True)
    assert len(done) == 2
    for pid in done:
        for name in ("dossier.md", "record_request_list.csv", "sampling_plan.md", "plan.json", "reviewed_example.csv", "example_estimate.md"):
            assert os.path.exists(os.path.join(out, pid, name)), name
        blob = "".join(open(os.path.join(out, pid, n)).read() for n in os.listdir(os.path.join(out, pid)))
        for leak in ("hard_negative", "justified", "ground_truth", "upgrade_fraction"):
            assert leak not in blob
        cols = open(os.path.join(out, pid, "record_request_list.csv")).readline()
        assert "documented" not in cols and "supported" not in cols
    assert len(list(csv.DictReader(open(os.path.join(out, "tracker.csv"))))) == 2


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
