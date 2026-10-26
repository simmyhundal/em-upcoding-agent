"""Hashes of what the data 4.2 generator writes and of what offices 2.0, 2.1 and 4.2 answer on a data 4.2 dataset, taken BEFORE data 4.3 existed (issue 197).
Cases: seed 42 with 216 providers (defaults), seed 7 with 60 providers (defaults), and seed 3 with 40 providers where every provider commits every fraud kind (the phantom-claim and unbundling paths).
The office case runs a fixed script of requests, follow-ups and an audit-trail request under each office version and hashes the transcript and the returned chart rows.
`python tests/test_d42_regression.py --write` records them (done once, on unmodified code); the test regenerates and compares, so data 4.2 and the frozen offices provably reproduce.
Run: python tests/test_d42_regression.py"""
import csv
import hashlib
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
import derive  # noqa: E402
import generate_v2  # noqa: E402
import provider_sim  # noqa: E402

HASHES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generator_hashes_v42.json")
CASES = {"4.2_s42_harness": dict(seed=42, n_providers=216, data_version="4.2"),
         "4.2_s7_small": dict(seed=7, n_providers=60, data_version="4.2"),
         "4.2_s3_allfwa": dict(seed=3, n_providers=40, data_version="4.2", nr_prob=1.0, imp_prob=1.0, unb_prob=1.0)}


def digest(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def _tree(out):
    h = {}
    for dp, _, fs in os.walk(out):
        for f in sorted(fs):
            p = os.path.join(dp, f)
            h[os.path.relpath(p, out)] = digest(p)
    return h


def build_case(kwargs):
    tmp = tempfile.mkdtemp()
    try:
        out, key = os.path.join(tmp, "data"), os.path.join(tmp, "key", "key.json")
        generate_v2.build(out, key, **kwargs)
        h = _tree(out)
        h["__answer_key__"] = digest(key)
        return h
    finally:
        shutil.rmtree(tmp)


def office_script(out, version):
    """A fixed sequence of plan-side actions on the first eight providers; returns a hash of the transcript and of the usable chart rows."""
    base = os.path.join(out, "view")
    office = provider_sim.Office(out, base, seed=1, version=version)
    pids = sorted(office.claims)[:8]
    for i, pid in enumerate(pids):
        r = office.send_request(pid, {"kind": "random", "n": 25})
        for _ in range(3):
            if r.get("error") or not r.get("deficiencies") or r.get("rounds_left", 0) <= 0:
                break
            r = office.follow_up(pid, [d["code"] for d in r["deficiencies"]])
        if version != "2.0" and i % 2 == 0 and office.state[pid]["usable"]:
            office.request_audit_trail(pid, sorted(office.state[pid]["usable"])[:5])
        if version != "2.0" and i % 3 == 0:
            office.send_request(pid, {"kind": "targeted", "cpt": "99214", "n": 5})
        office.close_request(pid, "regression script")
    blob = json.dumps(office.transcript, sort_keys=True) + json.dumps(sorted(office.documentation_rows(), key=lambda r: r["claim_id"]), sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


def office_case():
    tmp = tempfile.mkdtemp()
    try:
        out, key = os.path.join(tmp, "data"), os.path.join(tmp, "key", "key.json")
        generate_v2.build(out, key, **CASES["4.2_s3_allfwa"])
        derive.build_view(out, os.path.join(out, "view"))
        return {v: office_script(out, v) for v in ("2.0", "2.1", "4.2")}
    finally:
        shutil.rmtree(tmp)


def test_data_42_reproduces():
    want = json.load(open(HASHES))
    for name, kw in CASES.items():
        got = build_case(kw)
        assert got == want[name], (name, [k for k in set(got) | set(want[name]) if got.get(k) != want[name].get(k)])


def test_offices_20_21_42_reproduce():
    want = json.load(open(HASHES))["__offices__"]
    got = office_case()
    assert got == want, [v for v in want if got.get(v) != want[v]]


if __name__ == "__main__":
    if "--write" in sys.argv:
        res = {name: build_case(kw) for name, kw in CASES.items()}
        res["__offices__"] = office_case()
        json.dump(res, open(HASHES, "w"), indent=1, sort_keys=True)
        print("wrote", HASHES)
    else:
        test_data_42_reproduces()
        print("ok test_data_42_reproduces")
        test_offices_20_21_42_reproduce()
        print("ok test_offices_20_21_42_reproduce")
