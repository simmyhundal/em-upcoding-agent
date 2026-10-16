"""Score every run's summaries with judge v2.1 (deterministic, free) and record the files in experiments/runs.json.

Writes experiments/<run>/usefulness_rules.jsonl for each run that has summaries and sets `usefulness_rules` on its registry entry.
Needs the data folders (gitignored) and, for agent runs, replays the office to rebuild the charts the agent saw.

Usage:
    python eval/rejudge_rules_all.py
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "eval"))
sys.path.insert(0, os.path.join(ROOT, "src"))
import judge_agent_runs as jar  # noqa: E402
import judge_rules  # noqa: E402

NO_DOCS = {"261008_2_cc", "261008_3_cc"}          # these chat runs were given no records evidence


def run_view(r, ds):
    rid = r["run"]
    code = os.path.basename(os.path.dirname(ds["flagged"])) if r["kind"] in ("v2", "agent") else None
    if r["kind"] == "agent":
        return jar.build_view(rid, code, "3.1" if r.get("version") == "v3.1" else "3.0")
    if r["kind"] == "v2":
        v = os.path.join(ROOT, ds["view"].rsplit("/view", 1)[0], f"view_{rid}")
        return v if os.path.isdir(v) else os.path.join(ROOT, ds["view"])
    return os.path.join(ROOT, ds["view"])


def main():
    path = os.path.join(ROOT, "experiments", "runs.json")
    reg = json.load(open(path))
    for r in reg["runs"]:
        if r["kind"] == "screen":
            continue
        ds = reg["datasets"][r["dataset"]]
        checked = (r.get("ai") or {}).get("checked") or r.get("checked")
        if not checked:
            continue
        rid = r["run"]
        out = os.path.join(ROOT, "experiments", rid, "usefulness_rules.jsonl")
        view = run_view(r, ds)
        rows = judge_rules.run(view, os.path.join(ROOT, ds["flagged"]), os.path.join(ROOT, checked), out,
                               run_dir=os.path.join(ROOT, "experiments", rid), with_docs=rid not in NO_DOCS)
        (r.get("ai") or r)["usefulness_rules"] = f"experiments/{rid}/usefulness_rules.jsonl"
        print(rid, f"{len(rows)} summaries, mean {sum(x['score'] for x in rows) / len(rows):.2f}")
    json.dump(reg, open(path, "w"), indent=1)


if __name__ == "__main__":
    main()
