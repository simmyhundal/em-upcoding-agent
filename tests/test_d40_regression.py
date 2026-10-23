"""Hashes of what the data 4.0 generator writes, taken BEFORE data 4.2 existed (issue 173): seed 42 with the harness arguments (216 providers) and seed 7 (80 providers, defaults).
`python tests/test_d40_regression.py --write` records them (done once, on unmodified code); the test regenerates and compares, so data 4.0 provably reproduces byte for byte.
Run: python tests/test_d40_regression.py"""
import hashlib
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
import generate_v2  # noqa: E402

HASHES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generator_hashes_v40.json")
CASES = {"4.0_s42_harness": dict(seed=42, n_providers=216, n_upcoders=8, n_hard_neg=8, clone_share=0.125, data_version="4.0"),
         "4.0_s7_small": dict(seed=7, n_providers=80, n_upcoders=8, n_hard_neg=4, data_version="4.0")}


def digest(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build_case(kwargs):
    tmp = tempfile.mkdtemp()
    try:
        out, key = os.path.join(tmp, "data"), os.path.join(tmp, "key", "key.json")
        generate_v2.build(out, key, **kwargs)
        h = {}
        for dp, _, fs in os.walk(out):
            for f in sorted(fs):
                p = os.path.join(dp, f)
                h[os.path.relpath(p, out)] = digest(p)
        h["__answer_key__"] = digest(key)
        return h
    finally:
        shutil.rmtree(tmp)


def test_data_40_reproduces():
    want = json.load(open(HASHES))
    for name, kw in CASES.items():
        got = build_case(kw)
        assert got == want[name], (name, [k for k in set(got) | set(want[name]) if got.get(k) != want[name].get(k)])


if __name__ == "__main__":
    if "--write" in sys.argv:
        json.dump({name: build_case(kw) for name, kw in CASES.items()}, open(HASHES, "w"), indent=1, sort_keys=True)
        print("wrote", HASHES)
    else:
        test_data_40_reproduces()
        print("ok test_data_40_reproduces")
