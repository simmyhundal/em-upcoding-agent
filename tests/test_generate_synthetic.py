"""Smoke tests for the synthetic data generator. Run: python tests/test_generate_synthetic.py
(or `pytest` if installed)."""
import csv
import hashlib
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import generate_synthetic as g  # noqa: E402

SMALL = dict(n_normal=20, n_upcoders=3, n_hard_neg=3)


def _build(seed=42):
    d = tempfile.mkdtemp()
    key = os.path.join(tempfile.mkdtemp(), "ground_truth.json")
    g.build(d, key, seed=seed, **SMALL)
    return d, key


def _rows(d, name):
    with open(os.path.join(d, name)) as f:
        return list(csv.DictReader(f))


def _digest(built):
    d, key = built
    h = hashlib.sha256()
    for path in [os.path.join(d, n) for n in ("providers.csv", "patients.csv", "claims.csv")] + [key]:
        with open(path, "rb") as f:
            h.update(f.read())
    return h.hexdigest()


def test_same_seed_is_identical_and_different_seed_differs():
    assert _digest(_build(1)) == _digest(_build(1))
    assert _digest(_build(1)) != _digest(_build(2))


def test_role_counts_and_ids():
    d, key = _build()
    gt = json.load(open(key))
    roles = [v["role"] for v in gt["providers"].values()]
    assert roles.count("normal") == 20 and roles.count("upcoder") == 3 and roles.count("hard_negative") == 3
    claims = _rows(d, "claims.csv")
    ids = [c["claim_id"] for c in claims]
    assert len(ids) == len(set(ids))
    assert set(c["cpt"] for c in claims) <= set(g.CODES)
    assert set(ids) == set(gt["justified_cpt_by_claim"])


def test_answer_key_is_outside_the_data_folder():
    d, key = _build()
    assert os.path.exists(key) and not os.path.abspath(key).startswith(os.path.abspath(d))
    assert not any("truth" in n or "answer" in n for n in os.listdir(d))
    try:
        g.build(d, os.path.join(d, "ground_truth.json"), **SMALL)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_agent_visible_files_do_not_leak_ground_truth():
    d, key = _build()
    for name in ("providers.csv", "patients.csv", "claims.csv", "documentation.csv"):
        cols = set(_rows(d, name)[0])
        assert not {c for c in cols if "role" in c or "justified" in c or "upgrade" in c or c.startswith("_")}


def test_only_upcoders_bill_above_justified():
    d, key = _build()
    gt = json.load(open(key))
    role = {k: v["role"] for k, v in gt["providers"].items()}
    just = gt["justified_cpt_by_claim"]
    over = {"normal": 0, "hard_negative": 0, "upcoder": 0}
    for c in _rows(d, "claims.csv"):
        j, b = just[c["claim_id"]], c["cpt"]
        assert b >= j  # nobody bills below what is justified
        if b > j:
            over[role[c["provider_id"]]] += 1
    assert over["normal"] == 0 and over["hard_negative"] == 0 and over["upcoder"] > 0


def test_documentation_sample_coverage_and_signal():
    d, key = _build()
    gt = json.load(open(key))
    role = {k: v["role"] for k, v in gt["providers"].items()}
    claims = {c["claim_id"]: c for c in _rows(d, "claims.csv")}
    docs = _rows(d, "documentation.csv")
    assert 0.2 < len(docs) / len(claims) < 0.4
    lv = {n: i for i, n in enumerate(g.MDM_LEVELS)}
    code = {c: i for i, c in enumerate(g.CODES)}
    rate = {"upcoder": [0, 0], "other": [0, 0]}
    for r in docs:
        c = claims[r["claim_id"]]
        if c["cpt"] == "99215":
            k = "upcoder" if role[c["provider_id"]] == "upcoder" else "other"
            rate[k][0] += 1
            rate[k][1] += lv[r["documented_mdm_level"]] < code[c["cpt"]]
    up, other = rate["upcoder"][1] / rate["upcoder"][0], rate["other"][1] / rate["other"][0]
    assert up > 0.4 and other < 0.2 and up > 2 * other


def test_documentation_does_not_change_claims():
    import csv as _csv
    a, _ = _build(5)
    b = tempfile.mkdtemp()
    g.DOC_COVERAGE, old = 0.0, g.DOC_COVERAGE      # documentation uses its own random stream
    try:
        g.build(b, os.path.join(tempfile.mkdtemp(), "k.json"), seed=5, **SMALL)
    finally:
        g.DOC_COVERAGE = old
    assert open(os.path.join(a, "claims.csv")).read() == open(os.path.join(b, "claims.csv")).read()


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
