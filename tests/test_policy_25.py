"""Workflow v2.5's learned policy (issue 109): skipped practices get no request, asked ones get a branch from the file, and the answer key is not read."""
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import make_v2_office_workflow_runs as mw  # noqa: E402
import policy_25 as p25  # noqa: E402


def test_policy_file():
    p = p25.load()
    assert set(p["branches"]) == set(p25.BRANCHES) and len(p["ask"]["beta"]) == len(p25.ASK_FEATURES) + 1
    assert "role" not in open(p25.PATH).read() and len(p["fit_on_seeds"]) == 30


def test_run_on_one_seed():
    if not os.path.exists(os.path.join(ROOT, "data", "synthetic_v2_r2_1515", "view")):
        print("skip: data not built"); return
    view, office, flagged_file = mw.build_view("p25test_1515", "r2_1515", "eb_ratio_t_10", version="2.5", tier1_n=11)
    rows = list(csv.DictReader(open(flagged_file)))
    policy = p25.load()
    asked = {r["provider_id"] for r in rows if r["flagged"] == "True" and p25.ask(policy, p25.ask_vector(r))}
    sent = {pid for pid in office.policy_log} | {r["provider_id"] for r in csv.DictReader(open(os.path.join(view, "records_requests.csv"))) if r["kind"] == "flagged" and int(r["requested"]) > 0}
    assert sent == asked, (len(sent), len(asked))
    assert all(b in p25.BRANCHES for _, b in office.policy_log.values())


if __name__ == "__main__":
    test_policy_file()
    test_run_on_one_seed()
    print("ok")
