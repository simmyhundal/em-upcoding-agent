"""Score the usefulness of an agent run's summaries with the same judge as the workflow (issue 42).

The judge must see the charts the agent itself obtained. The office is deterministic, so this replays the agent's records requests
(from audit.jsonl) against a fresh office to rebuild exactly those charts, checks the replay matches the logged transcript, writes a
view folder for the run, then calls eval/judge_usefulness.py (Batch API, cached). Costs real money (about $0.05 a run).

Usage:
    python eval/judge_agent_runs.py RUN_ID CODE_RUN
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import judge_usefulness as ju  # noqa: E402
import provider_sim  # noqa: E402
import records  # noqa: E402


def replay(run_id, code_run):
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code_run}")
    base = os.path.join(data, "view")
    out = os.path.join(ROOT, "experiments", run_id)
    office = provider_sim.Office(data, base, seed=1)
    for line in open(os.path.join(out, "audit.jsonl")):
        a = json.loads(line)
        args = a["args"]
        if a["tool"] == "request_records":
            office.send_request(args["provider_id"], args["sample"], args.get("deadline_days", provider_sim.DEFAULT_DEADLINE))
        elif a["tool"] == "follow_up_records":
            office.follow_up(args["provider_id"], args["addressed_codes"], claim_ids=args.get("claim_ids"))
        elif a["tool"] == "close_records":
            office.close_request(args["provider_id"], args.get("reason", ""))
    logged = {}
    for line in open(os.path.join(out, "office_transcript.jsonl")):
        e = json.loads(line)
        if "usable_total" in e:
            logged[e["provider_id"]] = e["usable_total"]
    for pid, n in logged.items():
        assert len(office.state[pid]["usable"]) == n, f"replay does not match the logged transcript for {pid}"
    return data, base, office


def main(run_id, code_run):
    data, base, office = replay(run_id, code_run)
    view = os.path.join(data, f"view_{run_id}")
    os.makedirs(view, exist_ok=True)
    for name in ("claims.csv", "patients.csv", "providers.csv"):
        dst = os.path.join(view, name)
        if not os.path.exists(dst):
            os.symlink(os.path.join(base, name), dst)
    req = list(csv.DictReader(open(os.path.join(base, "records_requests.csv"))))
    control = {r["provider_id"] for r in req if r["kind"] == "control"} - set(office.state)
    owner = {r["claim_id"]: r["provider_id"] for r in csv.DictReader(open(os.path.join(base, "claims.csv")))}
    docs = [r for r in csv.DictReader(open(os.path.join(base, "documentation.csv"))) if owner.get(r["claim_id"]) in control]
    docs += office.documentation_rows()
    with open(os.path.join(view, "documentation.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=records.DOC_COLS)
        w.writeheader()
        w.writerows(docs)
    with open(os.path.join(view, "records_requests.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["provider_id", "kind", "requested", "received", "late", "no_response"])
        for p in sorted(control):
            w.writerow([p, "control", 0, 0, 0, 0])
    out = os.path.join(ROOT, "experiments", run_id)
    rows = ju.run(view, os.path.join(ROOT, "experiments", code_run, "flagged.csv"), os.path.join(out, "case_summaries_checked.jsonl"),
                  os.path.join(out, "usefulness.jsonl"), batch=True, cache_dir=os.path.join(out, "llm_cache_judge"),
                  usage_path=os.path.join(out, "usage_judge.jsonl"), run_dir=out)
    print(run_id, ju.summarize(rows))


if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    main(sys.argv[1], sys.argv[2])
