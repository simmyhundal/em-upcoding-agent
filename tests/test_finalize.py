"""Test that finalize_run writes self-contained reviewer materials. Run: python tests/test_finalize.py"""
import csv
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import finalize_run  # noqa: E402
import flagging  # noqa: E402
import generate_synthetic as g  # noqa: E402


def test_run_folder_is_self_contained():
    d = tempfile.mkdtemp()
    g.build(d, os.path.join(tempfile.mkdtemp(), "gt.json"), seed=23, n_normal=40, n_upcoders=3, n_hard_neg=3)
    rows = flagging.flag(d, top_n=4)
    flagged = os.path.join(d, "f.csv")
    with open(flagged, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=flagging.COLUMNS)
        w.writeheader()
        w.writerows(rows)
    checked = os.path.join(d, "checked.jsonl")
    with open(checked, "w") as f:
        for r in rows[:4]:
            f.write(json.dumps({"provider_id": r["provider_id"], "citation_check": {"passed": True, "n_cited": 1, "n_valid": 1, "reason": ""},
                                "summary": {"headline": "h", "leaning": "pattern_consistent_with_upcoding", "rationale": "r",
                                            "cited_claim_ids": ["C0000001"], "next_steps": ["s"]}}) + "\n")
    allowed = os.path.join(d, "allowed.json")
    json.dump({"codes": {c: {"allowed_amount": a} for c, a in zip(["99211", "99212", "99213", "99214", "99215"], [20, 50, 80, 120, 170])}}, open(allowed, "w"))
    run = os.path.join(d, "run")
    n_cases, packets = finalize_run.finalize(run, d, flagged, checked, allowed)
    assert n_cases == 4 and len(packets) == 4
    for sub in ("charts", "cases", "pi_packets"):
        assert os.path.isdir(os.path.join(run, sub))
    for md in [os.path.join(run, "cases", f) for f in os.listdir(os.path.join(run, "cases")) if f.startswith("P")] + \
              [os.path.join(run, "pi_packets", p, "dossier.md") for p in packets]:
        for link in re.findall(r"!\[[^\]]*\]\(([^)]+\.svg)\)", open(md).read()):
            assert os.path.exists(os.path.normpath(os.path.join(os.path.dirname(md), link))), (md, link)   # chart link resolves inside the run folder
            assert os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(md), link))).startswith(os.path.abspath(run))


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
