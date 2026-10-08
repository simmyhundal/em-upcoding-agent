"""Tests for the citation guardrail. Run: python tests/test_guardrail.py"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import generate_synthetic as g  # noqa: E402
import guardrail  # noqa: E402

D = tempfile.mkdtemp()
g.build(D, seed=3, n_normal=6, n_upcoders=1, n_hard_neg=1)
OWNER = guardrail.load_claim_owners(D)
P1 = "P0001"
P2 = "P0002"
own = [c for c, p in OWNER.items() if p == P1]
other = [c for c, p in OWNER.items() if p == P2]


def rec(ids):
    return {"provider_id": P1, "summary": {"cited_claim_ids": ids}}


def test_valid_citations_pass():
    r = guardrail.check(rec(own[:3]), OWNER)["citation_check"]
    assert r["passed"] and r["n_valid"] == 3 and r["reason"] == ""


def test_nonexistent_id_rejected():
    r = guardrail.check(rec(own[:1] + ["C9999999"]), OWNER)["citation_check"]
    assert not r["passed"] and r["nonexistent_ids"] == ["C9999999"] and r["n_valid"] == 1


def test_other_providers_real_claim_rejected():
    r = guardrail.check(rec(own[:1] + other[:1]), OWNER)["citation_check"]
    assert not r["passed"] and r["other_provider_ids"] == other[:1]


def test_no_citations_rejected():
    assert not guardrail.check(rec([]), OWNER)["citation_check"]["passed"]


def test_input_not_mutated_and_file_roundtrip():
    original = rec(own[:2])
    guardrail.check(original, OWNER)
    assert "citation_check" not in original
    src, dst = os.path.join(D, "in.jsonl"), os.path.join(D, "out.jsonl")
    with open(src, "w") as f:
        f.write(json.dumps(rec(own[:2])) + "\n" + json.dumps(rec(["nope"])) + "\n")
    s = guardrail.run(D, src, dst)
    assert s["passed"] == 1 and s["rejected"] == 1 and s["citations"] == 3 and s["valid_citations"] == 2
    assert abs(s["citation_accuracy"] - 2 / 3) < 1e-9


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
