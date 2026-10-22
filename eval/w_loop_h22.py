"""H22 = H16 + H17 (workflow v4.1 loop), declared before it was run.

The two leads of the first v4.1 batch were each directionally positive and each limited by a different thing: H17 (loosened chart test: min 5 documented charts, unsupported share >= 10%, alpha 0.20) calls more upcoders but
most of its extra calls are withdrawn by the demand floor; H16 (a second random request of 30 charts for a rules-called provider whose point estimate is at least 2 times the demand cost while its 90% lower bound is below it)
tightens the bound that the floor reads. Together: more calls reach the floor, and near-misses get the extra charts that can lift the bound over it. Both options already exist in workflow_policy_40 / make_v2_office_workflow_runs
(`rules40_opts` and `extend`) and compose without new code. NO new parameter: H17's L3 and H16's c = 2 are the settings chosen on batches 1 to 4 earlier.

Test (declared in advance): ONE run on development batches 7 to 10 (40 seeds, untouched by the selection of either lead and out of sample for the ask model), paired against H8 (workflow v4.0) with eval/w_loop.py `compare`;
also H16 alone on the same seeds. Report the paired difference, wins/losses/ties, one-sided p, honest providers called. No re-tuning, no extra seeds added after looking. H22 is the tenth hypothesis tried (H13 to H20, H20c, H22),
so the bar named for it is alpha = 0.05 / 10 = 0.005; it is also reported against 0.05.

This module exists so the combination can run without editing eval/w_loop.py while another run edits it. Usage: python eval/w_loop_h22.py BATCH[,BATCH...]
"""
import json
import multiprocessing as mp
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v4 as pool  # noqa: E402
import dev_release3 as dev  # noqa: E402
import make_v2_office_workflow_runs as ow  # noqa: E402
import run_release2 as r2  # noqa: E402
import score_40 as s4  # noqa: E402
import w_loop as wl  # noqa: E402

SPEC = {"version": "4.0", "screen": "eb_upper_t",
        "w40": {"ask": "linear", "escalate": "stop", "demand_floor": "cost", "rules40_opts": {"min": 5, "up": 0.10, "alpha": 0.20}, "extend": {"c": 2, "more": 30}}}


def _run(job):
    name, seed = job
    code = f"d4_{seed}"
    scr = dev.write_flagged(code, SPEC["screen"], 10)
    rid = f"wl{name.lower()}_{seed}"
    if not r2.done(rid, "case_summaries_checked.jsonl"):
        ow.run(rid, code, scr, f"workflow loop version {name} (H16 + H17) on data 4.0 development seed {seed} (issue 132)", version="4.0", tier1_n=11, no_model=True, w40=SPEC["w40"])
    c = s4.from_run(rid, code)
    return seed, {k: c[k] for k in wl.KEEP}


def evaluate(name, seeds):
    assert all(s < 5555 for s in seeds), "fresh seeds are never run in the development loop"
    path = os.path.join(wl.CACHE_DIR, f"{name}.json")
    have = json.load(open(path)) if os.path.exists(path) else {}
    todo = [s for s in seeds if str(s) not in have]
    if todo:
        with mp.get_context("spawn").Pool(4) as p:
            for seed, res in p.map(_run, [(name, s) for s in todo], chunksize=1):
                have[str(seed)] = res
        json.dump(have, open(path, "w"), indent=0)
    return {s: have[str(s)] for s in seeds}


if __name__ == "__main__":
    seeds = sum([pool.BATCHES[int(b) - 1] for b in sys.argv[1].split(",")], [])
    res = evaluate("H22", seeds)
    print("H22 per seed score:", round(sum(r["score"] for r in res.values()) / len(res)), "found", sum(r["found"] for r in res.values()), "of", sum(r["upcoders"] for r in res.values()))
