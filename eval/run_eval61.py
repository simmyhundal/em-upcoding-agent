"""Issue 61: the multi-seed paired evaluation of all four arms, and the smoke run that precedes it (issue 84).

Every dataset is generated once as data 2.1 (claims and records universe identical to data 2.0 for the same seed; 2.1 adds the note
package). Four arms run on it, paired by seed:
  W2.0  frozen workflow v2.0 on the provider office 2.0 (screen suspicion >= 5, fixed office policy)  eval/make_v2_office_workflow_runs.py
  W2.1  workflow v2.1: office 2.1, the fixed v2.1 policy, v2.1 summaries                                same script, version "2.1"
  A3.0  frozen agent v3.0 (office 2.0)                                                                 eval/run_agent.py
  A3.1  agent v3.1 (office 2.1, note tools, lint)                                                      eval/run_agent.py --version 3.1
The frozen arms read only the data 2.0 part of the folder. Each step is skipped when its output already exists, so the script resumes.
This SPENDS REAL MONEY (about $0.25 to $0.45 per arm plus about $0.05 per agent judge); the user approved it in the issue.

Usage:
    python eval/run_eval61.py smoke            # development seed 42, arms W2.1 and A3.1 only (not counted)
    python eval/run_eval61.py eval [--only-datasets e404 ...] [--arms W2.0 W2.1 A3.0 A3.1]
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import judge_agent_runs as jar  # noqa: E402
import judge_rules  # noqa: E402
import make_v2_office_workflow_runs as ow  # noqa: E402
import make_v2_runs as mk  # noqa: E402
import run_agent  # noqa: E402

DATE = "261015"
ARMS = ["W2.0", "W2.1", "A3.0", "A3.1"]
# key, seed, providers, upcoders, hard negatives, clone share, note, seed status
SMOKE = [("x1_s42", 42, 216, 8, 8, 0.5, "smoke run: development seed 42, 3.7% upcoders, half clone notes", "development")]
EVAL = [(f"e{s}", s, 216, 8, 8, 0.5, f"issue 61: fresh seed {s}, 3.7% upcoders, half clone notes", "reserved")
        for s in (404, 505, 606, 707, 808, 909, 1010, 1111, 1212, 1313)]
EVAL += [("e1414_r05", 1414, 600, 3, 18, 0.5, "issue 61: fresh seed 1414, 0.5% upcoders (3 of 600), half clone notes", "reserved"),
         ("e1414_r1", 1414, 600, 6, 18, 0.5, "issue 61: fresh seed 1414, 1% upcoders (6 of 600), half clone notes", "reserved"),
         ("e1414_r2", 1414, 600, 12, 18, 0.5, "issue 61: fresh seed 1414, 2% upcoders (12 of 600), half clone notes", "reserved")]
DATA_DESC = ("Version 2.1 synthetic data: the version 2 plan-shaped tables (claims and records universe identical to 2.0 for the same "
             "seed) plus the note package a records request returns (note text, signatures, orders and results, an EHR audit trail).")


def run_ids(key, smoke):
    """Stable run ids: one code run and one run per arm, numbered in a fixed order so a resumed run reuses them."""
    keys = [d[0] for d in (SMOKE if smoke else SMOKE + EVAL)]
    base = 1 + keys.index(key) * 5
    ids = {"code": f"{DATE}_{base}_code"}
    for k, arm in enumerate(ARMS):
        ids[arm] = f"{DATE}_{base + 1 + k}_api"
    return ids


def done(rid, name):
    return os.path.exists(os.path.join(ROOT, "experiments", rid, name))


def rules_judge(rid, view, flagged):
    out = os.path.join(ROOT, "experiments", rid, "usefulness_rules.jsonl")
    judge_rules.run(view, flagged, os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl"), out,
                    run_dir=os.path.join(ROOT, "experiments", rid), with_docs=True)


def register(reg, spec, ids, arms):
    key, seed, n, n_up, n_hn, clone, note, status = spec
    code = ids["code"]
    reg["data_descriptions"].setdefault("v2.1", DATA_DESC)
    reg["datasets"][key] = {"label": f"seed {seed}", "seed": seed, "flagged": f"experiments/{code}/flagged.csv",
                            "truth": f"eval/answer_key/ground_truth_v2_{code}.json", "view": f"data/synthetic_v2_{code}/view",
                            "data_version": "v2.1", "seed_status": status}
    have = {r["run"] for r in reg["runs"]}
    for arm in arms:
        rid = ids[arm]
        if rid in have or not done(rid, "case_summaries_checked.jsonl"):
            continue
        tag = "smoke run, not counted" if status == "development" else "issue 61"
        if arm.startswith("W"):
            reg["runs"].append({"run": rid, "dataset": key, "kind": "v2", "version": "v" + arm[1:], "source": "api",
                                "notes": f"{tag}: workflow {arm[1:]} with the provider office, screen suspicion >= 5",
                                "ai": {"checked": f"experiments/{rid}/case_summaries_checked.jsonl",
                                       "usefulness": f"experiments/{rid}/usefulness.jsonl",
                                       "transcript": f"experiments/{rid}/office_transcript.jsonl",
                                       "usefulness_rules": f"experiments/{rid}/usefulness_rules.jsonl"},
                                "sent": f"experiments/{rid}/flagged_threshold.csv", "min_suspicion": 5})
        else:
            reg["runs"].append({"run": rid, "dataset": key, "kind": "agent", "source": "api", "version": "v" + arm[1:],
                                "tuning": "Agent with the screen tool", "notes": f"{tag}: investigator agent {arm[1:]}", "records": True,
                                "checked": f"experiments/{rid}/case_summaries_checked.jsonl",
                                "transcript": f"experiments/{rid}/office_transcript.jsonl",
                                "usefulness": f"experiments/{rid}/usefulness.jsonl",
                                "usefulness_rules": f"experiments/{rid}/usefulness_rules.jsonl"})


def run_dataset(spec, arms, smoke):
    key, seed, n, n_up, n_hn, clone, note, status = spec
    ids = run_ids(key, smoke)
    code = ids["code"]
    if not done(code, "README.md"):
        mk.run((code, seed, n, n_up, n_hn, clone, note), data_version="2.1")
        print("built", code, flush=True)
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    for arm in arms:
        rid = ids[arm]
        if done(rid, "usefulness_rules.jsonl"):
            print("skip", arm, rid, flush=True)
            continue
        print("start", arm, rid, flush=True)
        if arm.startswith("W"):
            ver = arm[1:]
            if not done(rid, "usefulness.jsonl"):
                ow.run(rid, code, "threshold", f"{note}; workflow {ver} on the provider office", version=ver)
            rules_judge(rid, os.path.join(data, f"view_{rid}"), os.path.join(ROOT, "experiments", code, "flagged.csv"))
        else:
            ver = arm[1:]
            if not done(rid, "results.json"):
                run_agent.main(rid, code, version=ver)
            if not done(rid, "usefulness.jsonl"):
                jar.main(rid, code, ver)
            rules_judge(rid, os.path.join(data, f"view_{rid}"), os.path.join(ROOT, "experiments", code, "flagged.csv"))
        print("done", arm, rid, flush=True)
    path = os.path.join(ROOT, "experiments", "runs.json")
    reg = json.load(open(path))
    register(reg, spec, ids, arms)
    json.dump(reg, open(path, "w"), indent=1)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, ".env"))
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["smoke", "eval"])
    ap.add_argument("--only-datasets", nargs="*")
    ap.add_argument("--arms", nargs="*", default=None)
    a = ap.parse_args()
    smoke = a.mode == "smoke"
    specs = SMOKE if smoke else EVAL
    arms = a.arms or (["W2.1", "A3.1"] if smoke else ARMS)
    for spec in specs:
        if not a.only_datasets or spec[0] in a.only_datasets:
            run_dataset(spec, arms, smoke)
