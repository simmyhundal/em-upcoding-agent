"""Tests for the usefulness judge with a fake LLM (no API call). Run: python tests/test_judge.py"""
import csv
import json
import os
import sys
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "eval"))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import flagging  # noqa: E402
import generate_synthetic as g  # noqa: E402
import judge_usefulness as ju  # noqa: E402

D = tempfile.mkdtemp()
g.build(D, os.path.join(tempfile.mkdtemp(), "gt.json"), seed=13, n_normal=30, n_upcoders=2, n_hard_neg=2)
FLAGGED = os.path.join(D, "f.csv")
ROWS = flagging.flag(D, top_n=3)
with open(FLAGGED, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=flagging.COLUMNS)
    w.writeheader()
    w.writerows(ROWS)


def _checked(passed_flags):
    path = os.path.join(D, "checked.jsonl")
    with open(path, "w") as f:
        for r, ok in zip(ROWS[:3], passed_flags):
            f.write(json.dumps({"provider_id": r["provider_id"], "citation_check": {"passed": ok, "n_cited": 1, "n_valid": int(ok), "reason": ""},
                                "summary": {"headline": "h", "leaning": "inconclusive", "rationale": "r",
                                            "cited_claim_ids": ["C0000001"], "next_steps": []}}) + "\n")
    return path


def test_judge_prompt_has_rubric_packet_and_summary_but_no_answer_key():
    seen = []

    def fake(system, user):
        seen.append(user)
        return json.dumps({"score": 4, "justification": "ok", "problems": []})
    out = ju.run(D, FLAGGED, _checked([True, True, True]), os.path.join(D, "o.jsonl"), llm=fake)
    assert len(out) == 3 and all(r["score"] == 4 for r in out)
    for u in seen:
        assert "RUBRIC" in u and "EVIDENCE PACKET" in u and "SUMMARY TO GRADE" in u
        for leak in ("hard_negative", "upgrade_fraction", "ground_truth"):
            assert leak not in u


def test_rejected_summaries_score_one_without_a_model_call():
    calls = []

    def fake(system, user):
        calls.append(1)
        return json.dumps({"score": 5, "justification": "ok", "problems": []})
    out = ju.run(D, FLAGGED, _checked([True, False, True]), os.path.join(D, "o2.jsonl"), llm=fake)
    assert [r["score"] for r in out] == [5, 1, 5] and len(calls) == 2 and out[1]["judge"] is None


def test_summarize():
    s = ju.summarize([{"score": 5}, {"score": 3}, {"score": 4}])
    assert s["mean"] == 4.0 and s["distribution"][3] == 1 and s["n"] == 3


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
