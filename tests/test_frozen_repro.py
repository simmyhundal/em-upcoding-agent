"""The frozen versions still reproduce after the v4/v5 changes to shared code (provider_sim, case_summary, summary_rules, summary_lint, the workflow runners, agent_tools).
(a) workflow v2.5: rerun a stored API-free run under a new id and diff its checked summaries and office transcript with the stored copies.
(b) agent v3.5: replay a stored run's audit log through Environment(version="3.5") and compare every hybrid_review leaning and every advice with what was logged.
Run: python tests/test_frozen_repro.py   (needs the release 5 development data; skipped otherwise)"""
import json
import os
import re
import shutil
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))

CODE, SEED = "r5_4545", 4545
DATA = os.path.join(ROOT, "data", f"synthetic_v2_{CODE}")


def test_workflow_v25_reproduces_a_stored_run():
    if not os.path.isdir(os.path.join(DATA, "view_r5w25n_4545")):
        print("skipped (no release 5 data)")
        return
    import dev_release3 as dev
    import make_v2_office_workflow_runs as ow
    rid = "repro25_4545"
    shutil.rmtree(os.path.join(ROOT, "experiments", rid), ignore_errors=True)
    try:
        ow.run(rid, CODE, dev.write_flagged(CODE, "eb_ratio_t", 10), "reproduction of the frozen workflow v2.5", version="2.5", tier1_n=11)
        for name in ("case_summaries_checked.jsonl", "office_transcript.jsonl"):
            assert open(os.path.join(ROOT, "experiments", rid, name)).read() == open(os.path.join(ROOT, "experiments", "r5w25n_4545", name)).read(), name
    finally:
        shutil.rmtree(os.path.join(ROOT, "experiments", rid), ignore_errors=True)
        shutil.rmtree(os.path.join(DATA, f"view_{rid}"), ignore_errors=True)


def test_agent_v35_replays_a_stored_run():
    run = os.path.join(ROOT, "experiments", "r5a_4545")
    if not (os.path.isdir(DATA) and os.path.exists(os.path.join(run, "audit.jsonl"))):
        print("skipped (no release 5 data)")
        return
    import agent_tools as at
    env = at.Environment(DATA, os.path.join(DATA, "view"), seed=1, records_budget=22, version="3.5")
    logged_review = {}
    checked = 0
    for line in open(os.path.join(run, "audit.jsonl")):
        a = json.loads(line)
        if a["tool"] in ("request_records", "follow_up_records", "close_records", "request_audit_trail", "hybrid_review", "screen_providers", "advise_next_step", "note_checks", "provider_profile", "peer_comparison",
                         "estimate_overpayment", "data_quality"):
            out = env.call(a["tool"], a["args"])
            if a["tool"] == "hybrid_review":
                want = dict(re.findall(r'"provider": "(\d+)", "leaning": "([^"]*)"', a["result"]))
                got = {x["provider"]: x["leaning"] for x in out.get("results", [])}
                for pid, lean in want.items():
                    assert got.get(pid) == lean, (pid, got.get(pid), lean)
                    checked += 1
    adv = json.load(open(os.path.join(run, "advice_log.json")))["log"]
    assert [x["advised"] for x in env.advice_log if x["advised"] is not None] == [x["advised"] for x in adv if x["advised"] is not None]
    assert checked > 0


if __name__ == "__main__":
    test_workflow_v25_reproduces_a_stored_run()
    print("ok workflow")
    test_agent_v35_replays_a_stored_run()
    print("ok agent")
