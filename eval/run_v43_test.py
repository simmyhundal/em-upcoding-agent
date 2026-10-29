"""The true test of release 4.3 and 5.3 on data 4.3 test pool D4.3-TEST (seeds 6003 + 41j, j = 0 to 9; codes d43_<seed>). Run ONCE, after the freeze declaration (docs/w43_freeze.md) and the confirm read.

Free part (`workflow`): workflow v4.3 (H33), workflow v4.1, workflow v4.2, the ask-nobody control (H0) and the oracle ceiling, API-free, scored with score 4.3.
Paid part (`agent --model opus|sonnet`): agent v5.3, ONE run per seed per model, effort low: A5.3-O (Opus 5.5) and A5.3-S (Sonnet 5.5). It refuses without --approved and stops at the shared batch cap ($4 across both).
Usage: python eval/run_v43_test.py workflow
       python eval/run_v43_test.py agent --model opus --approved [--batch-cap 4.0]
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v43 as pool  # noqa: E402
import seed_registry as sreg  # noqa: E402

SEEDS = pool.TEST
OUT = os.path.join(ROOT, "experiments", "v43_test_results.json")
MODELS = {"opus": ("A5.3-O", "claude-opus-5-5", "fra53o"), "sonnet": ("A5.3-S", "claude-sonnet-5-5", "fra53s")}


def spent():
    return sum(json.load(open(f))["cost_usd"] for pre in ("fra53o", "fra53s") for f in glob.glob(os.path.join(ROOT, "experiments", f"{pre}_results_*.json")))


def build_seeds():
    import make_v2_runs as mk
    import run_release2 as r2
    for seed in SEEDS:
        code = f"d43_{seed}"
        if not r2.done(code, "README.md"):
            mk.run((code, seed, 216, 0, 0, None, f"data 4.3 test seed {seed} (release 4.3 and 5.3)"), data_version="4.3", screens=("eb_ratio",))


def workflow():
    import w_loop_43 as wl
    arms = {"W4.3": "H33", "W4.1": "W41", "W4.2": "W42", "H0": "H0"}
    for arm in arms.values():
        sreg.check_run("4.3", SEEDS, arm, "test")
    build_seeds()
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for seed in SEEDS:
        for arm, name in arms.items():
            res.setdefault(arm, {})[str(seed)] = wl._run((name, seed))[1]
        json.dump(res, open(OUT, "w"), indent=0)
        print(seed, {a: round(res[a][str(seed)]["score"]) for a in res}, flush=True)
    import oracle_s43
    orc = {}
    for seed in SEEDS:
        o = oracle_s43.oracle(f"d43_{seed}")
        orc[str(seed)] = round(o["score"], 2)
    res["oracle"] = orc
    json.dump(res, open(OUT, "w"), indent=0)
    print("oracle", orc, round(sum(orc.values())))


def agent():
    if "--approved" not in sys.argv:
        raise SystemExit("this run spends money: it needs --approved (Simmy's standing approval of /run-release paid cap=N, estimate logged in docs/decision_log.md)")
    import judge_agent_runs as jar
    import run_agent
    import run_release2 as r2
    import score_43 as s43
    import w_loop_43 as wl
    from dotenv import load_dotenv
    arm, model, pre = MODELS[sys.argv[sys.argv.index("--model") + 1]]
    cap = float(sys.argv[sys.argv.index("--batch-cap") + 1]) if "--batch-cap" in sys.argv else 4.0
    sreg.check_run("4.3", SEEDS, arm, "test")
    load_dotenv(os.path.join(ROOT, ".env"))
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for seed in SEEDS:
        if spent() >= cap:
            print(f"batch cap ${cap} reached after ${spent():.2f}; stopping")
            break
        code, rid = f"d43_{seed}", f"{pre}_{seed}"
        if not r2.done(rid, "results.json"):
            run_agent.main(rid, code, version="5.3", effort="low", model=model, screen_method="eb_upper_t", top_pct=10, records_budget=run_agent.EVAL_RECORDS_BUDGET_33)
        if not os.path.isdir(os.path.join(ROOT, "data", f"synthetic_v2_{code}", f"view_{rid}")):
            jar.main(rid, code, "5.3")
        r = json.load(open(os.path.join(ROOT, "experiments", rid, "results.json")))
        json.dump({"cost_usd": r["estimated_usd"], "effort": "low", "model": model, "version": "5.3"}, open(os.path.join(ROOT, "experiments", f"{pre}_results_{seed}.json"), "w"), indent=1)
        c, _ = s43.seed_result(rid, code)
        res.setdefault(arm, {})[str(seed)] = {k: c[k] for k in ("score", "collected", "staff_cost", "abrasion", "demands", "referrals", "rounds", "charts", "listed")}
        json.dump(res, open(OUT, "w"), indent=0)
        print(arm, seed, round(c["score"]), "spent", round(spent(), 3), flush=True)


if __name__ == "__main__":
    {"workflow": workflow, "agent": agent}[sys.argv[1]]()
