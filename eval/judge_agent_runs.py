"""Score the usefulness of an agent run's summaries with the same judge as the workflow (issue 42).

The judge must see the charts the agent itself obtained. The office is deterministic, so this replays the agent's records requests
(from audit.jsonl) against a fresh office to rebuild exactly those charts, checks the replay matches the logged transcript, writes a
view folder for the run, then calls eval/judge_usefulness.py (Batch API, cached). Costs real money (about $0.05 a run).

Usage:
    python eval/judge_agent_runs.py RUN_ID CODE_RUN [3.0|3.1|3.2|3.3]      (3.2 and 3.3: rebuild the view only; no LLM judge)
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent_tools  # noqa: E402
import judge_usefulness as ju  # noqa: E402
import provider_sim  # noqa: E402
import records  # noqa: E402


def replay(run_id, code_run, version="3.0"):
    """version "3.1" and "3.2": the agent ran against office 2.1 (second requests, audit-trail requests, the note package)."""
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code_run}")
    base = os.path.join(data, "view")
    out = os.path.join(ROOT, "experiments", run_id)
    office = agent_tools.make_office(data, base, version, seed=1)
    for line in open(os.path.join(out, "audit.jsonl")):
        a = json.loads(line)
        args = a["args"]
        if version == "5.1" and a["tool"] == "request_records" and a.get("result", "").startswith('{"error"'):
            continue                                # agent v5.1 refuses some requests itself (extension gate, budget); those never reached the office, so they are not replayed
        if a["tool"] == "request_records":
            office.send_request(args["provider_id"], args["sample"], args.get("deadline_days", provider_sim.DEFAULT_DEADLINE))
        elif a["tool"] == "follow_up_records":
            office.follow_up(args["provider_id"], args["addressed_codes"], claim_ids=args.get("claim_ids"))
        elif a["tool"] == "close_records":
            office.close_request(args["provider_id"], args.get("reason", ""))
        elif a["tool"] == "request_audit_trail":
            office.request_audit_trail(args["provider_id"], args.get("claim_ids", []))
    logged = {}
    for line in open(os.path.join(out, "office_transcript.jsonl")):
        e = json.loads(line)
        if "usable_total" in e:
            logged[e["provider_id"]] = e["usable_total"]
    for pid, n in logged.items():
        assert len(office.state[pid]["usable"]) == n, f"replay does not match the logged transcript for {pid}"
    return data, base, office


def build_view(run_id, code_run, version="3.0"):
    """Replay the agent's records requests and write the run's view folder (claims, patients, providers, the charts it obtained)."""
    data, base, office = replay(run_id, code_run, version)
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
    records.write_docs(os.path.join(view, "documentation.csv"), docs)
    with open(os.path.join(view, "records_requests.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["provider_id", "kind", "requested", "received", "late", "no_response"])
        for p in sorted(control):
            w.writerow([p, "control", 0, 0, 0, 0])
    return view


def main(run_id, code_run, version="3.0", llm_judge=None):
    """llm_judge None: the LLM judge for 3.0 and 3.1 (as run); 3.2 skips it and only builds the view the rule judge reads (issues 92 and 93)."""
    view = build_view(run_id, code_run, version)
    if llm_judge is None:
        llm_judge = version not in ("3.2", "3.3", "3.4", "3.5", "5.0", "5.1")
    if not llm_judge:
        print(run_id, "view rebuilt; no LLM judge")
        return
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
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "3.0")
