"""Release 3 evaluation harness (issue 99): workflow v2.2, workflow v2.3 and agent v3.3 on the same fresh seed (data 2.2, 216 doctors, 8 planted upcoders,
8 hard negatives, half clone notes; seeds 2525, 2626, ... in steps of 101). Rule judge is NOT run (the j3.2 judge predates rules 2.3; a j3.3 is future work).

  1. code-only run `r3_<seed>` (data, derived view, eb_ratio top-5% list for W2.2; free);
  2. `r3w2_<seed>`: workflow v2.2 exactly as release 2 ran it (eb_ratio top 5%, policy 2.1, rules 2.2), the reference arm (about $0.01);
  3. `r3w_<seed>`: workflow v2.3 (eb_ratio_t top 10%, two-tier policy 2.3, rules 2.3; about $0.01);
  4. `r3a_<seed>`: agent v3.3 (Opus 5.5, low effort, $1 cap, records for at most 22 providers; about $0.2).
Each step is skipped when its output exists. THIS SPENDS REAL MONEY; the seeds, arms and cap were posted on issue 99 before the first run.

Usage: python eval/run_release3.py 2525 [--arms W2 W A] [--effort low]
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_release3 as dev  # noqa: E402
import judge_agent_runs as jar  # noqa: E402
import make_v2_office_workflow_runs as ow  # noqa: E402
import make_v2_runs as mk  # noqa: E402
import run_agent  # noqa: E402
import run_release2 as r2  # noqa: E402

NOTE = "release 3 evaluation (issue 99): seed {s}, 216 doctors, 8 planted upcoders, half clone notes, data 2.2 defaults"
TIER1_N = 11                        # the first 5% of 216 providers get the full policy in workflow v2.3
EFFORT = "low"


def run_seed(seed, arms=("W2", "W", "A"), effort=EFFORT, model=None):
    code = f"r3_{seed}"
    if not r2.done(code, "README.md"):
        mk.run((code, seed, 216, 8, 8, 0.5, NOTE.format(s=seed)), data_version="2.2", screens=("eb_ratio",))
        print("built", code, flush=True)
    out = {"seed": seed}
    if "W2" in arms:
        rid = f"r3w2_{seed}"
        if not r2.done(rid, "case_summaries_checked.jsonl"):
            ow.run(rid, code, "eb_ratio_top5pct", NOTE.format(s=seed) + "; workflow v2.2, eb_ratio top 5%", version="2.2")
        out["workflow_v22"] = r2.score(rid, code)
    if "W" in arms:
        rid = f"r3w_{seed}"
        name = dev.write_flagged(code, "eb_ratio_t", 10)
        if not r2.done(rid, "case_summaries_checked.jsonl"):
            ow.run(rid, code, name, NOTE.format(s=seed) + "; workflow v2.3, eb_ratio_t top 10%, two-tier policy", version="2.3", tier1_n=TIER1_N)
        out["workflow_v23"] = r2.score(rid, code)
    if "A" in arms:
        rid = f"r3a_{seed}"
        if not r2.done(rid, "results.json"):
            run_agent.main(rid, code, version="3.3", effort=effort, model=model, screen_method="eb_ratio_t", top_pct=10, records_budget=run_agent.EVAL_RECORDS_BUDGET_33)
        if not os.path.isdir(os.path.join(ROOT, "data", f"synthetic_v2_{code}", f"view_{rid}")):
            jar.main(rid, code, "3.3")
        out["agent_v33"] = {**r2.score(rid, code), "effort": effort, "model": model or "claude-opus-5-5"}
    return out


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, ".env"))
    ap = argparse.ArgumentParser()
    ap.add_argument("seed", type=int)
    ap.add_argument("--arms", nargs="*", default=["W2", "W", "A"], choices=["W2", "W", "A"])
    ap.add_argument("--effort", default=EFFORT, choices=["low", "medium", "high"])
    ap.add_argument("--model")
    a = ap.parse_args()
    res = run_seed(a.seed, tuple(a.arms), a.effort, a.model)
    path = os.path.join(ROOT, "experiments", f"r3_results_{a.seed}.json")      # one file per seed: parallel runs do not race
    json.dump(res, open(path, "w"), indent=1)
    print(json.dumps(res, indent=1))
