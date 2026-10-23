"""Workflow disposition table (issue 66; eval/dispositions_w.py): a synthetic run folder gives one row per listed provider with a stated reason for each of the three dispositions,
a short-list run marks the rest `not listed`, and the module never reads the answer key. A stored run is checked too when present. Run: python tests/test_dispositions.py"""
import csv
import json
import os
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dispositions_w as dw  # noqa: E402

UP = "pattern_consistent_with_upcoding"
HEAD = ["rank", "provider_id", "flagged", "screen_score", "share_99215", "expected_share", "z_adj"]


def _run_folder(d, n_listed=3, short_of=None):
    """Providers A (asked, called, kept), B (asked, called, withdrawn by the floor), C (skipped by an integer-K ask rule), D (beyond a short list)."""
    ids = ["A", "B", "C", "D"]
    name = "flagged_s_10.csv" if short_of is None else "flagged_s_10_top3.csv"
    with open(os.path.join(d, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEAD)
        for i, p in enumerate(ids):
            w.writerow([i + 1, p, "True" if (short_of is None or i < 3) else "False", 2.0 - i * 0.1, 0.1, 0.05, 1.0])
    with open(os.path.join(d, "case_summaries_checked.jsonl"), "w") as f:
        for p, lean, why in (("A", UP, "40% of 30 charts below billed"), ("B", UP, "35% of 30 charts below billed"), ("C", "inconclusive", "only 0 documented claims came back")):
            f.write(json.dumps({"provider_id": p, "summary": {"leaning": "inconclusive" if p == "B" else lean}, "rule_leaning": lean, "rule_reason": why}) + "\n")
    with open(os.path.join(d, "office_transcript.jsonl"), "w") as f:
        for p in ("A", "B"):
            f.write(json.dumps({"action": "send_request", "provider_id": p, "round": 1, "requested_total": 30, "usable_total": 28}) + "\n")
    json.dump({"floor": 276.0, "withdrawn": {"B": 12.5}}, open(os.path.join(d, "demand_floor.json"), "w"))
    return d


def test_synthetic_run_has_a_reason_for_every_listed_provider():
    with tempfile.TemporaryDirectory() as d:
        rows = {r["provider_id"]: r for r in dw.build(_run_folder(d), spec={"w40": {"ask": 2}})}
        assert [r["on_list"] for r in rows.values()] == ["yes"] * 4
        assert rows["A"]["disposition"] == "demanded" and rows["A"]["charts_usable"] == 28
        assert rows["B"]["disposition"] == "examined and set aside" and rows["B"]["demand_floor_withdrawn"] == "yes" and rows["B"]["floor_estimate"] == 12.5 and rows["B"]["floor_cost"] == 276.0
        assert "below the staff cost" in rows["B"]["disposition_reason"]
        assert rows["C"]["ask_decision"] == "skipped" and rows["C"]["disposition"] == "not examined" and "outside the first 2 asked" in rows["C"]["disposition_reason"]
        assert all(r["reason_stated"] == "yes" for r in rows.values()) and dw.share(list(rows.values()))[:2] == (4, 4)
        assert dw.share(list(rows.values())) == (4, 4, 0)             # D is beyond K = 2 and was not asked: consistent with the rule


def test_short_list_marks_the_rest_not_listed():
    with tempfile.TemporaryDirectory() as d:
        _run_folder(d, short_of=True)
        full = os.path.join(d, "full.csv")
        with open(full, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(HEAD)
            for i, p in enumerate("ABCD"):
                w.writerow([i + 1, p, "True", 2.0 - i * 0.1, 0.1, 0.05, 1.0])
        rows = {r["provider_id"]: r for r in dw.build(d, spec={"w40": {"ask": 2}}, full_list_file=full)}
        assert list(rows) == ["A", "B", "C", "D"] and rows["D"]["on_list"] == "no" and rows["D"]["disposition"] == "not examined" and rows["D"]["ask_reason"].startswith("not listed")
        assert rows["D"]["reason_stated"] == "yes" and dw.share(list(rows.values()))[0] == 3


def test_module_never_reads_the_answer_key():
    src = open(os.path.join(ROOT, "eval", "dispositions_w.py")).read()
    assert "answer_key" not in src and "ground_truth" not in src
    assert not [c for c in dw.COLUMNS if c in ("role", "planted", "habit", "true_rate")]


def test_stored_runs_reach_every_listed_provider():
    for rid in ("wlh8_1616", "fr40_5555"):
        run = os.path.join(ROOT, "experiments", rid)
        if not os.path.exists(os.path.join(run, "case_summaries_checked.jsonl")):
            continue
        rows = dw.build(run, dw.run_spec(rid))
        n, ok, bad = dw.share(rows)
        assert n > 0 and ok == n and bad == 0
        assert {r["disposition"] for r in rows} <= {"demanded", "examined and set aside", "not examined"}


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
