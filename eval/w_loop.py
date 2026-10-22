"""The workflow's RL loop on data 4.0 and score 4.0 (issue 131). Free: every workflow version here is API-free.

`VERSIONS` names each version as options of the workflow runner (screen, rules, policy options). `evaluate` runs a version on development seeds (code runs d4_<seed> built by eval/dev_pool_v4.py),
scores each run with score 4.0 (eval/score_40.py) and caches the components per seed in experiments/w_loop/<name>.json. `compare` gives the paired per-seed difference of two versions with an exact
(or, past 16 seeds, Monte Carlo) one-sided sign-flip permutation test. Fresh seeds (5555 and above) are refused.

Usage: python eval/w_loop.py run NAME BATCHES          e.g.  python eval/w_loop.py run R0 1
       python eval/w_loop.py compare NAME REF BATCHES      e.g.  python eval/w_loop.py compare H1 R0 1
"""
import itertools
import json
import multiprocessing as mp
import os
import random
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v4 as pool  # noqa: E402
import dev_release3 as dev  # noqa: E402
import make_v2_office_workflow_runs as ow  # noqa: E402
import workflow_policy_40 as wp40  # noqa: E402
import run_release2 as r2  # noqa: E402
import score_40 as s4  # noqa: E402

CACHE_DIR = os.path.join(ROOT, "experiments", "w_loop")
KEEP = ("score", "recovered", "staff_cost", "abrasion", "found", "upcoders", "demands", "honest_called", "rounds", "charts")
HI = ["99214", "99215"]
VERSIONS = {
    "R0": {"version": "2.5", "screen": "eb_ratio_t", "w40": None},                                                 # the frozen workflow v2.5 on its own list
    "R0u": {"version": "2.5", "screen": "eb_upper_t", "w40": None},                                               # frozen v2.5 with the chosen screen
    "H1": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "policy25", "escalate": "policy25"}},         # the chosen screen and rules 4.0 (chart test pooled over 99214 and 99215)
    "H2": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "policy25", "escalate": "policy25", "sample_cpts": HI}},   # H1 with the first sample drawn within the 99214 and 99215 claims
    "H4": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "policy25", "escalate": "stop"}},                           # H1 without escalation (no frame change)
    "H5": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "all", "escalate": "policy25"}},                            # H1 asking every listed provider
    "H6": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "policy25", "escalate": "stop", "demand_floor": "cost"}},      # H4 and a demand only when the estimated recovery covers its cost
    "H7": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "policy25", "escalate": "stop", "demand_floor": "cost", "rules": "4.1"}},      # H6 with rules 4.1 (time padding and risk inflation)
    "D7": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "all", "escalate": "stop", "demand_floor": "cost", "rules": "4.1"}},          # diagnostic only (not a hypothesis): rules 4.1 with every listed provider asked
    "H8h": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "ask_model": os.path.join(ROOT, "experiments", "w_loop", "ask_model_b123.json"), "escalate": "stop", "demand_floor": "cost"}},   # H6 with the ask model fitted on batches 1 to 3 (held-out check on batch 4)
    "H8": {"version": "4.0", **wp40.FROZEN_V40},                                                                             # H6 with the ask model fitted on batches 1 to 4 (src/policy_40_ask.json): the frozen workflow v4.0
    "H9": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "escalate": "stop", "demand_floor": "cost2"}},                # H8 with the demand floor at twice the demand cost
    "H10": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "escalate": "stop", "demand_floor": "cost", "n": 20}},      # H8 with a first sample of 20 charts
    "H11": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "escalate": "stop", "demand_floor": "cost", "n": 45}},      # H8 with a first sample of 45 charts
    "H12": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "ask_model": os.path.join(ROOT, "experiments", "w_loop", "ask_model_b1to6.json"), "escalate": "stop", "demand_floor": "cost"}},   # H8 with the ask model refitted on batches 1 to 6
    "H13": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "ask_model": os.path.join(ROOT, "experiments", "w_loop", "ask_model41_b1to4.json"), "escalate": "stop", "demand_floor": "cost"}},   # H8 with the ask model on features built from the eb_upper_t screen (workflow v4.1 candidate, issue 132); fitted on batches 1 to 4
    "H14": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "ask_model": os.path.join(ROOT, "experiments", "w_loop", "ask_model_margin.json"), "escalate": "stop", "demand_floor": "cost"}},   # H8 asking only when the predicted value exceeds a margin of $50 (stop-loss at the ask step, workflow v4.1 candidate, issue 132); margin chosen by leave-one-batch-out CV on batches 1 to 4
    # workflow v4.1 hypotheses on top of H8 (issue 132; docs/w_loop_v41.md): H15 probe then extend (10 charts, then 20 more when at least k documented 99214 and 99215 charts are unsupported)
    **{f"H15k{k}": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "escalate": "stop", "demand_floor": "cost", "n": 10, "probe": {"k": k, "more": 20}}} for k in (2, 3, 4)},
    "H15": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "escalate": "stop", "demand_floor": "cost", "n": 10, "probe": {"k": 3, "more": 20}}},   # H15 at the k chosen on batches 1 to 4
    # H16 near-miss extension: after the rules call, a second random request of 30 charts for providers whose estimate is at least c times the demand cost but whose lower bound is below it
    **{f"H16c{c}": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "escalate": "stop", "demand_floor": "cost", "extend": {"c": c, "more": 30}}} for c in (1, 1.5, 2)},
    "H8chk": {"version": "4.0", **wp40.FROZEN_V40},                                                                         # H8 rerun after the v4.1 refactors: must reproduce H8 exactly
    "H16": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "escalate": "stop", "demand_floor": "cost", "extend": {"c": 2, "more": 30}}},   # H16 at the c chosen on batches 1 to 4 (all three c gave the same result; ties go to the setting closest to H8)
    # H17 let the money decide: a loosened pooled chart test of rules 4.0 (min documented charts, min unsupported share, alpha), the demand floor kept. H8 is (10, 0.25, 0.05).
    **{f"H17{t}": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "escalate": "stop", "demand_floor": "cost", "rules40_opts": {"min": m, "up": u, "alpha": a}}}
       for t, (m, u, a) in {"L1": (8, 0.20, 0.05), "L2": (6, 0.15, 0.10), "L3": (5, 0.10, 0.20)}.items()},
    "H17": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "linear", "escalate": "stop", "demand_floor": "cost", "rules40_opts": {"min": 5, "up": 0.10, "alpha": 0.20}}},   # H17 at L3, chosen on batches 1 to 4
    "H3": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "policy25", "escalate": "stop", "sample_cpts": HI}},       # H2 without escalation (the first sample decides)
}


def _run(job):
    name, seed = job
    spec = VERSIONS[name]
    code = f"d4_{seed}"
    scr = dev.write_flagged(code, spec["screen"], 10)
    rid = f"wl{name.lower()}_{seed}"
    if not r2.done(rid, "case_summaries_checked.jsonl"):
        kw = {"w40": spec["w40"]} if spec["version"] == "4.0" else {}
        ow.run(rid, code, scr, f"workflow loop version {name} on data 4.0 development seed {seed} (issue 131)", version=spec["version"], tier1_n=11, no_model=True, **kw)
    c = s4.from_run(rid, code)
    return seed, {k: c[k] for k in KEEP}


def evaluate(name, seeds):
    assert all(s < 5555 for s in seeds), "fresh seeds (5555 and above) are never run in the development loop"
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{name}.json")
    have = json.load(open(path)) if os.path.exists(path) else {}
    todo = [s for s in seeds if str(s) not in have]
    if todo:
        with mp.get_context("spawn").Pool(4) as p:
            for seed, res in p.map(_run, [(name, s) for s in todo], chunksize=1):
                have[str(seed)] = res
        json.dump(have, open(path, "w"), indent=0)
    return {s: have[str(s)] for s in seeds}


def perm_p(diffs, n_mc=40000):
    """One-sided exact sign-flip permutation p-value that the mean difference is positive (Monte Carlo when more than 16 pairs)."""
    n, obs = len(diffs), sum(diffs)
    if n <= 16:
        flips = list(itertools.product((1, -1), repeat=n))
        return sum(sum(s * d for s, d in zip(f, diffs)) >= obs - 1e-9 for f in flips) / len(flips)
    rnd = random.Random(20261021)
    return sum(sum(rnd.choice((1, -1)) * d for d in diffs) >= obs - 1e-9 for _ in range(n_mc)) / n_mc


def compare(name, ref, seeds):
    a, b = evaluate(name, seeds), evaluate(ref, seeds)
    diffs = [a[s]["score"] - b[s]["score"] for s in seeds]
    return {"mean_a": st.mean(a[s]["score"] for s in seeds), "mean_b": st.mean(b[s]["score"] for s in seeds), "mean_diff": st.mean(diffs), "sd_diff": st.stdev(diffs) if len(diffs) > 1 else 0.0,
            "p": perm_p(diffs), "n": len(seeds), "wins": sum(d > 0 for d in diffs),
            "found_a": sum(a[s]["found"] for s in seeds), "found_b": sum(b[s]["found"] for s in seeds), "hc_a": sum(a[s]["honest_called"] for s in seeds), "hc_b": sum(b[s]["honest_called"] for s in seeds),
            "rounds_a": sum(a[s]["rounds"] for s in seeds), "rounds_b": sum(b[s]["rounds"] for s in seeds), "above_zero": st.mean(a[s]["score"] for s in seeds) > 0}


def line(c, name, ref):
    return (f"{name} vs {ref} on {c['n']} seeds: score 4.0 per seed {c['mean_a']:,.0f} vs {c['mean_b']:,.0f} (difference {c['mean_diff']:+,.0f}, sd {c['sd_diff']:,.0f}, better on {c['wins']} of {c['n']}, "
            f"one-sided p = {c['p']:.4f}); found {c['found_a']} vs {c['found_b']}, honest called {c['hc_a']} vs {c['hc_b']}, rounds {c['rounds_a']} vs {c['rounds_b']}; above zero: {c['above_zero']}")


if __name__ == "__main__":
    cmd, name = sys.argv[1], sys.argv[2]
    if cmd == "run":
        seeds = sum([pool.BATCHES[int(b) - 1] for b in sys.argv[3].split(",")], [])
        res = evaluate(name, seeds)
        print(name, "per seed score:", round(st.mean(r["score"] for r in res.values())), "found", sum(r["found"] for r in res.values()), "of", sum(r["upcoders"] for r in res.values()))
    elif cmd == "compare":
        ref = sys.argv[3]
        seeds = sum([pool.BATCHES[int(b) - 1] for b in sys.argv[4].split(",")], [])
        print(line(compare(name, ref, seeds), name, ref))
