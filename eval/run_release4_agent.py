"""Release 4 fresh test, Phase B (issue 108): agent v3.4 on the fresh seeds 3535 to 4444 (data r4_<seed>, generated in Phase A). Opus 5.5, low effort, $1 cap per run, records for at
most 22 providers, starting screen eb_ratio_t top 10%. THIS SPENDS REAL MONEY; the plan and the batch cap ($4) were posted on issue 108 and the spend approved by Simmy.

Usage: python eval/run_release4_agent.py 3535
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import judge_agent_runs as jar  # noqa: E402
import run_agent  # noqa: E402
import run_release2 as r2  # noqa: E402

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, ".env"))
    seed = int(sys.argv[1])
    code, rid = f"r4_{seed}", f"r4a_{seed}"
    if not r2.done(rid, "results.json"):
        run_agent.main(rid, code, version="3.4", effort="low", screen_method="eb_ratio_t", top_pct=10, records_budget=run_agent.EVAL_RECORDS_BUDGET_33)
    if not os.path.isdir(os.path.join(ROOT, "data", f"synthetic_v2_{code}", f"view_{rid}")):
        jar.main(rid, code, "3.4")
    out = {**r2.score(rid, code), "effort": "low", "model": "claude-opus-5-5"}
    json.dump(out, open(os.path.join(ROOT, "experiments", f"r4a_results_{seed}.json"), "w"), indent=1)
    print(json.dumps(out))
