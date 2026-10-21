"""Fresh-seed evaluation of the v4/v5 line (issue 128): seeds 5555, 5656, ..., 6464 (step 101), data 4.0, code runs f4_<seed>. Never tuned on; the arms are frozen before this runs.

Workflow arms (free, API-free): the frozen workflow v2.5 on its own list (reference) and workflow v4.0 (`workflow_policy_40.FROZEN_V40`). Agent arms (PAID, run by eval/run_v5_fresh_agent.py after Simmy's
explicit OK and a posted estimate): the frozen agent v3.5 (reference) and agent v5.0. Scored with score 4.0 (eval/score_40.py), paired by seed.

Usage: python eval/run_v4_fresh.py build | workflow | report
"""
import json
import multiprocessing as mp
import os
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_release3 as dev  # noqa: E402
import make_v2_office_workflow_runs as ow  # noqa: E402
import make_v2_runs as mk  # noqa: E402
import run_release2 as r2  # noqa: E402
import score_40 as s4  # noqa: E402
import w_loop as wl  # noqa: E402
import workflow_policy_40 as wp40  # noqa: E402

SEEDS = [5555 + 101 * i for i in range(10)]
NOTE = "data 4.0 FRESH seed {s} (issue 128): 216 providers, 8 planted upcoders with habits, 8 hard negatives; never tuned on"
OUT = os.path.join(ROOT, "experiments", "v4_fresh_results.json")
WORKFLOW = {"W2.5 (frozen)": ("fr25", {"version": "2.5", "screen": "eb_ratio_t", "w40": None}), "W4.0": ("fr40", {"version": "4.0", **wp40.FROZEN_V40})}
AGENTS = {"A3.5 (frozen)": "fra35", "A5.0": "fra50"}


def build(seed):
    code = f"f4_{seed}"
    if not r2.done(code, "README.md"):
        mk.run((code, seed, 216, 8, 8, None, NOTE.format(s=seed)), data_version="4.0", screens=("eb_ratio",))
    return code


def run_workflow(job):
    label, seed = job
    pre, spec = WORKFLOW[label]
    code = f"f4_{seed}"
    scr = dev.write_flagged(code, spec["screen"], 10)
    rid = f"{pre}_{seed}"
    if not r2.done(rid, "case_summaries_checked.jsonl"):
        kw = {"w40": spec["w40"]} if spec["version"] == "4.0" else {}
        ow.run(rid, code, scr, f"{label} on fresh seed {seed} (issue 128)", version=spec["version"], tier1_n=11, no_model=True, **kw)
    c = s4.from_run(rid, code)
    return label, seed, {k: c[k] for k in wl.KEEP}


def report():
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for label, pre in AGENTS.items():
        for seed in SEEDS:
            rid = f"{pre}_{seed}"
            if os.path.exists(os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")) and os.path.exists(os.path.join(ROOT, "data", f"synthetic_v2_f4_{seed}", f"view_{rid}", "documentation.csv")):
                c = s4.from_run(rid, f"f4_{seed}")
                res.setdefault(label, {})[str(seed)] = {k: c[k] for k in wl.KEEP}
    json.dump(res, open(OUT, "w"), indent=0)
    return res


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        assert all(s >= 5555 for s in SEEDS)
        with mp.get_context("spawn").Pool(4) as pool:
            print(pool.map(build, SEEDS))
    elif cmd == "workflow":
        res = json.load(open(OUT)) if os.path.exists(OUT) else {}
        with mp.get_context("spawn").Pool(4) as pool:
            for label, seed, r in pool.map(run_workflow, [(l, s) for l in WORKFLOW for s in SEEDS], chunksize=1):
                res.setdefault(label, {})[str(seed)] = r
        json.dump(res, open(OUT, "w"), indent=0)
        for label in WORKFLOW:
            d = res[label]
            print(label, "score per seed", round(st.mean(v["score"] for v in d.values())), "found", sum(v["found"] for v in d.values()), "of", sum(v["upcoders"] for v in d.values()), "honest called", sum(v["honest_called"] for v in d.values()))
    elif cmd == "report":
        report()
