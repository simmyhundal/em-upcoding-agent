"""Hashes of what the data 2.x generator writes (issue 124): data 2.0, 2.1 and 2.2 on seed 42 and data 2.2 on the release 5 seed 4545 with the harness's arguments.
`python tests/test_generator_regression.py --write` records the hashes (done BEFORE data 4.0 touched generate_v2); the test regenerates and compares, so 2.x provably reproduces.
Run: python tests/test_generator_regression.py"""
import hashlib
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
import generate_v2  # noqa: E402

HASHES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generator_hashes.json")
CASES = {"2.0_s42": dict(seed=42, data_version="2.0"), "2.1_s42": dict(seed=42, data_version="2.1"), "2.2_s42": dict(seed=42, data_version="2.2"),
         "2.2_s4545_harness": dict(seed=4545, n_providers=216, n_upcoders=8, n_hard_neg=8, clone_share=0.5, data_version="2.2")}


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


def test_data_2x_reproduces():
    want = json.load(open(HASHES))
    for name, kw in CASES.items():
        got = build_case(kw)
        assert got == want[name], (name, [k for k in set(got) | set(want[name]) if got.get(k) != want[name].get(k)])


if __name__ == "__main__":
    if "--write" in sys.argv:
        json.dump({name: build_case(kw) for name, kw in CASES.items()}, open(HASHES, "w"), indent=1, sort_keys=True)
        print("wrote", HASHES)
    else:
        test_data_2x_reproduces()
        print("ok test_data_2x_reproduces")
