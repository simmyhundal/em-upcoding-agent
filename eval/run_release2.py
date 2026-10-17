"""Release 2 evaluation harness (issue 90): workflow v2.2 and agent v3.2 on the same fresh seed, same screen (eb_ratio, top 5%), rule judge j3.2 only.

Per seed (216 doctors, 8 planted upcoders, 8 high-acuity doctors, half the upcoders clone notes, data 2.2 defaults; seeds 1515, 1616, ...):
  1. the code-only run `r2_<seed>` (data, derived view, screens; free);
  2. workflow v2.2 arm `r2w_<seed>`: office 2.1, the fixed v2.1 policy on the top-5% eb_ratio list, rules 2.2 summaries (a model only where the rules leave a
     real question, Batch API), data-quality pre-flight and hold, then judge j3.2 (about $0.015);
  3. agent v3.2 arm `r2a_<seed>`: the agent with the data-quality tools, a $1 cap, the starting screen named in the task, then judge j3.2 (about $0.2 to $0.45).
Each step is skipped when its output exists, so the script resumes. THIS SPENDS REAL MONEY; the cap and the seeds are posted on issue 90 and every run needs
Simmy's OK. Results are printed and written to experiments/r2_results.json; registering runs in experiments/runs.json and the paired analysis come later.

Usage:
    python eval/run_release2.py 1515 [--arms W A] [--effort low|medium] [--model claude-sonnet-5-5]
"""
import argparse
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import judge_agent_runs as jar  # noqa: E402
import judge_rules_32  # noqa: E402
import make_v2_office_workflow_runs as ow  # noqa: E402
import make_v2_runs as mk  # noqa: E402
import run_agent  # noqa: E402

SCREEN, TOP_PCT = "eb_ratio", 5
NOTE = "release 2 evaluation (issue 90): seed {s}, 216 doctors, 8 planted upcoders, half clone notes, data 2.2 defaults"


def done(rid, name):
    return os.path.exists(os.path.join(ROOT, "experiments", rid, name))


def cost(rid):
    d = os.path.join(ROOT, "experiments", rid)
    usd = 0.0
    for f in os.listdir(d):
        if f.startswith("usage_") and f.endswith(".jsonl"):
            usd += sum(json.loads(x).get("estimated_usd", 0) for x in open(os.path.join(d, f)) if x.strip())
    p = os.path.join(d, "agent_run.json")
    if os.path.exists(p):
        usd += json.load(open(p)).get("estimated_usd", 0)
    return round(usd, 4)


def score(rid, code):
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))["providers"]
    called = [x["provider_id"] for x in map(json.loads, open(os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")))
              if x["summary"]["leaning"] == "pattern_consistent_with_upcoding"]
    up = sum(v["role"] == "upcoder" for v in key.values())
    return {"run": rid, "upcoders_found": sum(key[p]["role"] == "upcoder" for p in called), "upcoders": up,
            "honest_accused": sum(key[p]["role"] != "upcoder" for p in called), "called": len(called), "cost_usd": cost(rid)}


def rule_judge(rid, code):
    out = os.path.join(ROOT, "experiments", rid, "usefulness_rules.jsonl")
    if done(rid, "usefulness_rules.jsonl"):
        return
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    judge_rules_32.run(os.path.join(data, f"view_{rid}"), os.path.join(ROOT, "experiments", code, "flagged.csv"),
                       os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl"), out, run_dir=os.path.join(ROOT, "experiments", rid))


def run_seed(seed, arms=("W", "A"), effort="medium", model=None):
    code, w, a = f"r2_{seed}", f"r2w_{seed}", f"r2a_{seed}"
    if not done(code, "README.md"):
        mk.run((code, seed, 216, 8, 8, 0.5, NOTE.format(s=seed)), data_version="2.2", screens=("eb_ratio", "priority"))
        print("built", code, flush=True)
    out = {"seed": seed}
    if "W" in arms:
        if not done(w, "case_summaries_checked.jsonl"):
            ow.run(w, code, f"{SCREEN}_top{TOP_PCT}pct", NOTE.format(s=seed) + "; workflow v2.2, eb_ratio top 5%", version="2.2")
        rule_judge(w, code)
        out["workflow"] = score(w, code)
    if "A" in arms:
        if not done(a, "results.json"):
            run_agent.main(a, code, version="3.2", effort=effort, model=model, screen_method=SCREEN, top_pct=TOP_PCT)
        if not os.path.isdir(os.path.join(ROOT, "data", f"synthetic_v2_{code}", f"view_{a}")):
            jar.main(a, code, "3.2")
        rule_judge(a, code)
        out["agent"] = score(a, code)
        out["agent"].update({"effort": effort, "model": model or "claude-opus-5-5"})
    return out


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, ".env"))
    ap = argparse.ArgumentParser()
    ap.add_argument("seed", type=int)
    ap.add_argument("--arms", nargs="*", default=["W", "A"], choices=["W", "A"])
    ap.add_argument("--effort", default="medium", choices=["low", "medium", "high"])
    ap.add_argument("--model")
    a = ap.parse_args()
    res = run_seed(a.seed, tuple(a.arms), a.effort, a.model)
    path = os.path.join(ROOT, "experiments", "r2_results.json")
    allres = json.load(open(path)) if os.path.exists(path) else {}
    allres[str(a.seed)] = {**allres.get(str(a.seed), {}), **res}
    json.dump(allres, open(path, "w"), indent=1)
    print(json.dumps(res, indent=1))
