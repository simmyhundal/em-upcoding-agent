"""Tests for data 2.2 (issues 74 and later). Run: python tests/test_v22.py"""
import filecmp
import json
import os
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
import generate_v2  # noqa: E402


def build(version, seed=5, **opts):
    tmp = tempfile.mkdtemp()
    out, key = os.path.join(tmp, "d"), os.path.join(tmp, "k", "key.json")
    generate_v2.build(out, key, seed=seed, n_providers=40, n_upcoders=4, n_hard_neg=4, clone_share=0.5, data_version=version, **opts)
    return out, json.load(open(key))


def same_files(a, b):
    bad = []
    for root, _, files in os.walk(a):
        for f in files:
            pa = os.path.join(root, f)
            pb = os.path.join(b, os.path.relpath(pa, a))
            if not os.path.exists(pb) or not filecmp.cmp(pa, pb, shallow=False):
                bad.append(os.path.relpath(pa, a))
    return bad


def test_zero_noise_reproduces_data_2_1_exactly():
    a, ka = build("2.1")
    b, kb = build("2.2", honest_miscode_rate=0.0, subtle_upcoder_share=0.0)
    assert same_files(a, b) == []
    assert ka["justified_cpt_by_claim"] == kb["justified_cpt_by_claim"]
    assert {p: v["role"] for p, v in ka["providers"].items()} == {p: v["role"] for p, v in kb["providers"].items()}


def test_options_are_refused_on_frozen_versions():
    for version in ("2.0", "2.1"):
        try:
            build(version, honest_miscode_rate=0.1)
        except ValueError:
            continue
        raise AssertionError("frozen data versions must not accept data 2.2 options")


def test_noise_bills_honest_visits_off_level_and_roles_follow_the_margin():
    out, key = build("2.2", seed=6, honest_miscode_rate=0.12, subtle_upcoder_share=0.5)
    P = key["providers"]
    honest = [v for v in P.values() if v["planted"] != "upcoder"]
    assert sum(v["upcode_rate"] for v in honest) / len(honest) > 0.02 and sum(v["downcode_rate"] for v in honest) / len(honest) > 0.02
    base, margin = key["honest_baseline_upcode_rate"], key["upcoder_margin"]
    for v in P.values():
        assert (v["role"] == "upcoder") == (v["upcode_rate"] - base >= margin), v
    assert all("planted" in v and "honest_miscode_rate" in v for v in P.values())


def test_frozen_keys_carry_no_data_22_fields():
    _, key = build("2.1")
    assert "honest_baseline_upcode_rate" not in key
    assert all("planted" not in v for v in key["providers"].values())


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
