"""Agent v5.1 (A5.1) on the ten test seeds of workflow v4.0, agent v5.0 and workflow v4.1 (5555 to 6464, step 101; data f4_<seed>). THIS SPENDS REAL MONEY: it refuses to run without --approved, which stands
for Simmy's explicit OK after the cost estimate in docs/agent_v51.md. Nothing in A5.1 was chosen on these seeds (second use of them for the agent line; the second fresh pool 6565 to 7474 is not touched).

Runs once per seed: Opus 5.5, low effort, $1 cap per run (EVAL_MAX_USD_32), records for at most 22 providers (as A5.0), screen eb_upper_t at the top 10%, and a batch cap ($4 by default) checked
before every run. Writes experiments/fra51_<seed>/ (the run), experiments/fra51_results_<seed>.json (as A5.0's), and experiments/v51_fresh_results.json (score 4.0 per seed, the keys of
experiments/v4_fresh_results.json).

Usage: python3 eval/run_v51_fresh_agent.py --approved [--batch-cap 4.0] [SEED ...]
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))

PRE, VERSION, SCREEN = "fra51", "5.1", "eb_upper_t"
OUT = os.path.join(ROOT, "experiments", "v51_fresh_results.json")


def spent():
    return sum(json.load(open(f))["cost_usd"] for f in glob.glob(os.path.join(ROOT, "experiments", f"{PRE}_results_*.json")))


if __name__ == "__main__":
    if "--approved" not in sys.argv:
        raise SystemExit("this run spends money: it needs --approved (Simmy's explicit OK after the cost estimate in docs/agent_v51.md)")
    import judge_agent_runs as jar
    import run_agent
    import run_release2 as r2
    import run_v4_fresh as fresh
    import score_40 as s4
    import w_loop as wl
    cap = float(sys.argv[sys.argv.index("--batch-cap") + 1]) if "--batch-cap" in sys.argv else 4.0
    seeds = [int(a) for a in sys.argv[1:] if a.isdigit()] or fresh.SEEDS
    assert all(s in fresh.SEEDS for s in seeds), "only the ten test seeds 5555 to 6464"
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, ".env"))
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for seed in seeds:
        if spent() >= cap:
            print(f"batch cap ${cap} reached after ${spent():.2f}; stopping")
            break
        code, rid = f"f4_{seed}", f"{PRE}_{seed}"
        if not r2.done(rid, "results.json"):
            run_agent.main(rid, code, version=VERSION, effort="low", screen_method=SCREEN, top_pct=10, records_budget=run_agent.EVAL_RECORDS_BUDGET_33)
        if not os.path.isdir(os.path.join(ROOT, "data", f"synthetic_v2_{code}", f"view_{rid}")):
            jar.main(rid, code, VERSION)
        out = {**r2.score(rid, code), "effort": "low", "model": "claude-opus-5-5", "version": VERSION}
        json.dump(out, open(os.path.join(ROOT, "experiments", f"{PRE}_results_{seed}.json"), "w"), indent=1)
        c = s4.from_run(rid, code)
        res.setdefault("A5.1", {})[str(seed)] = {k: c[k] for k in wl.KEEP}
        json.dump(res, open(OUT, "w"), indent=0)
        print(json.dumps(out))
