"""Reference arms on data 4.2 development seeds (issue 173): the frozen workflow v2.5 (R0, its own list), workflow v4.0 (H8) and the W4.1 candidate (H23 at N = 4), free (no model, API-free),
on office 4.2, scored with score 4.0 through the adapter and with the data 4.2 metrics (eval/metrics_d42.py). Own code d42_<seed> and run ids d42wl<name>_<seed>, so a data 4.0 run with the same seed number is never read.
Usage: python eval/run_d42_reference.py [N_SEEDS]       (default 20: the first 20 development seeds)"""
import json
import multiprocessing as mp
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v42 as pool  # noqa: E402
import dev_release3 as dev  # noqa: E402
import make_v2_office_workflow_runs as ow  # noqa: E402
import metrics_d42 as md  # noqa: E402
import run_release2 as r2  # noqa: E402
import seed_registry as sreg  # noqa: E402
import w_loop  # noqa: E402

ARMS = {"W2.5": "R0", "W4.0": "H8", "W4.1": "H23_n4"}         # arm name -> the hypothesis in eval/w_loop.py VERSIONS (used exactly as it is)
OUT = os.path.join(ROOT, "experiments", "d42_reference_arms.json")


def _run(job):
    arm, seed = job
    spec = w_loop.VERSIONS[ARMS[arm]]
    code = f"d42_{seed}"
    scr = dev.write_flagged(code, spec["screen"], 10)
    if spec.get("list_k"):
        scr = w_loop.write_flagged_topk(code, scr, spec["list_k"])
    rid = f"d42wl{ARMS[arm].lower()}_{seed}"
    if not r2.done(rid, "case_summaries_checked.jsonl"):
        kw = {"w40": spec["w40"]} if spec["version"] == "4.0" else {}
        ow.run(rid, code, scr, f"reference arm {arm} ({ARMS[arm]}) on data 4.2 development seed {seed} (issue 173)", version=spec["version"], tier1_n=11, no_model=True, office_version="4.2", **kw)
    return arm, seed, md.run_metrics(rid, code)


def main(n=20):
    seeds = pool.DEV[:n]
    sreg.check_development("4.2", seeds)
    for arm in ARMS:
        sreg.check_run("4.2", seeds, arm, "select")
    jobs = [(a, s) for a in ARMS for s in seeds]
    res = {a: {} for a in ARMS}
    with mp.get_context("spawn").Pool(4) as p:
        for arm, seed, m in p.imap_unordered(_run, jobs, chunksize=1):
            res[arm][str(seed)] = m
    json.dump(res, open(OUT, "w"), indent=0, default=float)
    return res


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20)
