"""Fresh-seed evaluation, agent arms (issue 128). THIS SPENDS REAL MONEY: it refuses to run without --approved, which stands for Simmy's explicit OK after the estimate posted on issue 128.

Runs agent v3.5 (frozen reference; screen eb_ratio_t) or agent v5.0 (screen eb_upper_t) on the fresh seeds 5555 to 6464 (step 101; data f4_<seed> from eval/run_v4_fresh.py): Opus 5.5, low effort,
$1 cap per run, records for at most 22 providers, a batch cap checked after every run.

Usage: python eval/run_v5_fresh_agent.py {3.5|5.0} --approved [--batch-cap 4.0] [SEED ...]
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import judge_agent_runs as jar  # noqa: E402
import run_agent  # noqa: E402
import run_release2 as r2  # noqa: E402
import run_v4_fresh as fresh  # noqa: E402

PRE = {"3.5": "fra35", "5.0": "fra50"}
SCREEN = {"3.5": "eb_ratio_t", "5.0": "eb_upper_t"}


def spent(pre):
    return sum(json.load(open(f))["cost_usd"] for f in glob.glob(os.path.join(ROOT, "experiments", f"{pre}_results_*.json")))


if __name__ == "__main__":
    version = sys.argv[1]
    if "--approved" not in sys.argv:
        raise SystemExit("this run spends money: it needs --approved (Simmy's explicit OK after the cost estimate on issue 128)")
    cap = float(sys.argv[sys.argv.index("--batch-cap") + 1]) if "--batch-cap" in sys.argv else 4.0
    seeds = [int(a) for a in sys.argv[2:] if a.isdigit()] or fresh.SEEDS
    assert all(s in fresh.SEEDS for s in seeds)
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, ".env"))
    pre = PRE[version]
    for seed in seeds:
        if spent(pre) >= cap:
            print(f"batch cap ${cap} reached after ${spent(pre):.2f}; stopping")
            break
        code, rid = f"f4_{seed}", f"{pre}_{seed}"
        if not r2.done(rid, "results.json"):
            run_agent.main(rid, code, version=version, effort="low", screen_method=SCREEN[version], top_pct=10, records_budget=run_agent.EVAL_RECORDS_BUDGET_33)
        if not os.path.isdir(os.path.join(ROOT, "data", f"synthetic_v2_{code}", f"view_{rid}")):
            jar.main(rid, code, version)
        out = {**r2.score(rid, code), "effort": "low", "model": "claude-opus-5-5", "version": version}
        json.dump(out, open(os.path.join(ROOT, "experiments", f"{pre}_results_{seed}.json"), "w"), indent=1)
        print(json.dumps(out))
