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
        assert "RUBRIC" in u and "EVIDENCE CARD" in u and "SUMMARY TO GRADE" in u and "number check" in u
        for leak in ("hard_negative", "upgrade_fraction", "ground_truth"):
            assert leak not in u


def test_rejected_summaries_score_one_without_a_model_call():
    calls = []

    def fake(system, user):
        calls.append(1)
        return json.dumps({"score": 5, "justification": "ok", "problems": []})
    out = ju.run(D, FLAGGED, _checked([True, False, True]), os.path.join(D, "o2.jsonl"), llm=fake)
    assert [r["score"] for r in out] == [5, 1, 5] and len(calls) == 2 and out[1]["judge"] is None


def test_unverified_numbers_are_reported_to_the_judge_and_in_the_output():
    path = os.path.join(D, "checked_bad.jsonl")
    with open(path, "w") as f:
        f.write(json.dumps({"provider_id": ROWS[0]["provider_id"], "citation_check": {"passed": True, "n_cited": 1, "n_valid": 1, "reason": ""},
                            "summary": {"headline": "h", "leaning": "inconclusive", "rationale": "Billed 987654.32 of everything.",
                                        "cited_claim_ids": ["C0000001"], "next_steps": []}}) + "\n")
    seen = []

    def fake(system, user):
        seen.append(user)
        return json.dumps({"score": 3, "justification": "ok", "problems": []})
    out = ju.run(D, FLAGGED, path, os.path.join(D, "o3.jsonl"), llm=fake)
    assert out[0]["unverified_numbers"] == ["987654.32"] and "987654.32" in seen[0]
    assert ju.summarize(out)["summaries_with_all_numbers_verified"] == 0.0


def test_judge_v2_adds_tool_outputs_and_v1_prompt_is_unchanged():
    run_dir = tempfile.mkdtemp()
    pid = ROWS[0]["provider_id"]
    with open(os.path.join(run_dir, "office_transcript.jsonl"), "w") as f:
        f.write(json.dumps({"action": "send_request", "provider_id": pid, "round": 1, "status": "extension", "text": "We need more time.",
                            "deficiencies": [{"code": "EXTENSION"}], "usable_total": 0, "requested_total": 30, "sample_kind": "random",
                            "days_elapsed_total": 41}) + "\n")
    with open(os.path.join(run_dir, "audit.jsonl"), "w") as f:
        f.write(json.dumps({"tool": "estimate_overpayment", "args": {"provider_id": pid}, "result": '{"point_estimate": 98765}'}) + "\n")
    ev = ju.tool_evidence(run_dir, pid)
    assert "extension" in ev and "98765" in ev and "days elapsed 41" in ev
    path = os.path.join(D, "checked_v2.jsonl")
    with open(path, "w") as f:
        f.write(json.dumps({"provider_id": pid, "citation_check": {"passed": True, "n_cited": 1, "n_valid": 1, "reason": ""},
                            "summary": {"headline": "h", "leaning": "inconclusive", "rationale": "The estimate is 98765 dollars.",
                                        "cited_claim_ids": ["C0000001"], "next_steps": []}}) + "\n")
    seen = {}

    def fake(system, user):
        seen["system"], seen["user"] = system, user
        return json.dumps({"score": 3, "justification": "ok", "problems": []})
    out = ju.run(D, FLAGGED, path, os.path.join(D, "o_v2.jsonl"), llm=fake, run_dir=run_dir, version="j2")
    assert "TOOL OUTPUTS THE AUTHOR SAW" in seen["user"] and "98765" in seen["user"] and "output of tools" in seen["system"]
    assert out[0]["judge_version"] == "j2" and out[0]["unverified_numbers"] == []          # the estimate's number is matched through the tool output
    ju.run(D, FLAGGED, path, os.path.join(D, "o_v1.jsonl"), llm=fake, run_dir=run_dir, version="j1")
    assert "TOOL OUTPUTS" not in seen["user"] and seen["system"] == ju.SYSTEM               # j1 is exactly the original prompt


def test_summarize():
    s = ju.summarize([{"score": 5}, {"score": 3}, {"score": 4}])
    assert s["mean"] == 4.0 and s["distribution"][3] == 1 and s["n"] == 3


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
