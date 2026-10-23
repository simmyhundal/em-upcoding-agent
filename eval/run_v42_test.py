"""The true test of release 4.2 and 5.2 on data 4.2 test pool D4.2-TEST-1 (seeds 4700 + 37j, j = 0 to 9; codes d42_<seed>). Run ONCE, after the freeze declaration (docs/w42_freeze.md) and the confirm read.

Free part (`workflow`): workflow v4.2 (H28), workflow v4.1 (H23 at N = 4, re-run), the do-nothing arm and the oracle ceiling, API-free, scored with score 4.2.
Paid part (`agent`): agent v5.2, ONE run per seed, effort low, Opus 5.5. It refuses without --approved and stops at the batch cap. The earlier agent (v5.1) is not re-run: it is compared indirectly, through workflow v4.1 on the same seeds.
Usage: python eval/run_v42_test.py workflow
       python eval/run_v42_test.py agent --approved [--batch-cap 4.0]
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v42 as pool  # noqa: E402
import seed_registry as sreg  # noqa: E402

SEEDS = pool.TEST
OUT = os.path.join(ROOT, "experiments", "v42_test_results.json")
PRE = "fra52"


def spent():
    return sum(json.load(open(f))["cost_usd"] for f in glob.glob(os.path.join(ROOT, "experiments", f"{PRE}_results_*.json")))


def workflow():
    import make_v2_runs as mk
    import run_release2 as r2
    import w_loop
    import w_loop_42 as wl
    import dev_release3 as dev
    import make_v2_office_workflow_runs as ow
    import score_42 as s42
    for arm in ("W4.2", "W4.1"):
        sreg.check_run("4.2", SEEDS, arm, "test")
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for seed in SEEDS:
        code = f"d42_{seed}"
        if not r2.done(code, "README.md"):
            mk.run((code, seed, 216, 0, 0, None, f"data 4.2 test seed {seed} (release 4.2 and 5.2)"), data_version="4.2", screens=("eb_ratio",))
        for arm, name in (("W4.2", "H28"), ("W4.1", "H23_n4")):
            spec = wl.VERSIONS[name]
            scr = dev.write_flagged(code, spec["screen"], 10)
            if spec.get("list_k"):
                scr = w_loop.write_flagged_topk(code, scr, spec["list_k"])
            rid = f"d42t_{name.lower()}_{seed}"
            if not r2.done(rid, "case_summaries_checked.jsonl"):
                ow.run(rid, code, scr, f"{arm} on data 4.2 test seed {seed}", version="4.0", tier1_n=11, no_model=True, office_version="4.2", w40=spec["w40"])
            c, _ = s42.seed_result(rid, code)
            res.setdefault(arm, {})[str(seed)] = {k: c[k] for k in wl.KEEP}
        json.dump(res, open(OUT, "w"), indent=0)
        print(seed, {a: round(res[a][str(seed)]["score"]) for a in res if str(seed) in res[a]}, flush=True)


def agent():
    if "--approved" not in sys.argv:
        raise SystemExit("this run spends money: it needs --approved (Simmy's standing approval of /run-release paid cap=N, or an explicit OK after the cost estimate in docs/agent_v52.md)")
    import judge_agent_runs as jar
    import run_agent
    import run_release2 as r2
    import score_42 as s42
    import w_loop_42 as wl
    from dotenv import load_dotenv
    cap = float(sys.argv[sys.argv.index("--batch-cap") + 1]) if "--batch-cap" in sys.argv else 4.0
    sreg.check_run("4.2", SEEDS, "A5.2", "test")
    load_dotenv(os.path.join(ROOT, ".env"))
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for seed in SEEDS:
        if spent() >= cap:
            print(f"batch cap ${cap} reached after ${spent():.2f}; stopping")
            break
        code, rid = f"d42_{seed}", f"{PRE}_{seed}"
        if not r2.done(rid, "results.json"):
            run_agent.main(rid, code, version="5.2", effort="low", screen_method="eb_upper_t", top_pct=10, records_budget=run_agent.EVAL_RECORDS_BUDGET_33)
        if not os.path.isdir(os.path.join(ROOT, "data", f"synthetic_v2_{code}", f"view_{rid}")):
            jar.main(rid, code, "5.2")
        r = json.load(open(os.path.join(ROOT, "experiments", rid, "results.json")))
        json.dump({"cost_usd": r["estimated_usd"], "effort": "low", "model": "claude-opus-5-5", "version": "5.2"}, open(os.path.join(ROOT, "experiments", f"{PRE}_results_{seed}.json"), "w"), indent=1)
        c, _ = s42.seed_result(rid, code)
        res.setdefault("A5.2", {})[str(seed)] = {k: c[k] for k in wl.KEEP}
        json.dump(res, open(OUT, "w"), indent=0)
        print(seed, round(c["score"]), "spent", round(spent(), 3), flush=True)


if __name__ == "__main__":
    {"workflow": workflow, "agent": agent}[sys.argv[1]]()
