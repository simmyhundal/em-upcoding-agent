"""The workflow's RL loop on data 4.3 (release 4.3 and 5.3), scored with score 4.3 (signed off 2026-10-27); `score42` and the lane diagnostics come from score 4.2. Free: every version is API-free. Same machinery as eval/w_loop.py (which stays untouched), run on the data 4.2 development pool
(eval/dev_pool_v42.py: code d42_<seed>, run ids d42wl<name>_<seed>, the ones the reference arms already wrote are reused) and scored with score 4.2 (eval/score_42.py) beside the score 4.0 adapter.

Usage: python eval/w_loop_42.py run NAME BATCHES        BATCHES like 1,2,3,4 (ten seeds each)
       python eval/w_loop_42.py compare NAME REF BATCHES
"""
import json
import multiprocessing as mp
import os
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import d42_truth as dt  # noqa: E402
import dev_pool_v43 as pool  # noqa: E402
import dev_release3 as dev  # noqa: E402
import make_v2_office_workflow_runs as ow  # noqa: E402
import run_release2 as r2  # noqa: E402
import score_42 as s42  # noqa: E402
import score_43 as s43  # noqa: E402
import seed_registry as sreg  # noqa: E402
import w_loop  # noqa: E402

CACHE_DIR = os.path.join(ROOT, "experiments", "w_loop_43")
W41 = w_loop.VERSIONS["H23_n4"]
LANE = {"day_max": 30, "n": 30, "persist": 3, "office_version": "4.3"}    # workflow v4.2 (H28) with the lane on office 4.3
def _v(base, fwa=None, floor=None, **top):
    w = {**base["w40"]}
    if fwa is not None:
        w["fwa"] = {**LANE, **fwa} if fwa else None
        if not fwa:
            w.pop("fwa")
    if floor:
        w["demand_floor"] = floor
    return {**base, **top, "w40": w}


NOLANE = {}                                                                         # an empty lane option removes the lane
VERSIONS = {
    "W41": w_loop.VERSIONS["H23_n4"],                                                                                                   # workflow v4.1, the level review only
    "W42": {**W41, "w40": {**W41["w40"], "fwa": dict(LANE)}},                                                                           # workflow v4.2 (H28) with office 4.3 for the lane: the reference of this release
    # hypotheses of workflow v4.3 (docs/w_loop_v43.md), each against the current best on development batches 1 to 4
    "D7": {"version": "4.0", "screen": "eb_upper_t", "w40": {"ask": "all", "escalate": "stop", "demand_floor": "cost43", "rules": "4.1"}},                  # diagnostic, not a hypothesis: every listed provider asked (the data the ask model of H33 is fitted on)
    "H33": {**W41, "w40": {**W41["w40"], "ask_model": os.path.join(ROOT, "experiments", "w_loop_43", "ask_model43_b1to4.json"), "demand_floor": "cost43"}},   # the ask-or-skip model refitted under score 4.3 prices on data 4.3 development batches 1 to 4 (eval/fit_ask_43.py); level demands use the score 4.3 floor
    "H0": {**W41, "w40": {**W41["w40"], "ask_model": os.path.join(ROOT, "experiments", "w_loop_43", "ask_model43_none.json"), "demand_floor": "cost43"}},      # control, not a hypothesis: list the same providers and ask none of them (what a short-list saving alone buys)
    "H34": {**W41, "w40": {**W41["w40"], "ask_model": os.path.join(ROOT, "experiments", "w_loop_43", "ask_model43_v43_b1to4.json"), "demand_floor": "cost43"}},  # H33 with the paid-dollar features added to the ask model (the money is in rare large providers)
    "H29": _v(W41, floor="cost43"),                                                                                                     # level demands: the break-even rule uses score 4.3's collected value (no lane)
    "H30": _v(W41, fwa={"break_even": "s43"}, floor="cost43"),                                                                          # the lane too: a referral only when its collected lower bound covers the referral cost
    "H31": _v(W41, fwa={"break_even": "s43", "probe": {"n": 10, "k": 3, "more": 20}}, floor="cost43"),                                  # H30 with a probe of 10 claims first; 20 more only if at least 3 had no record
    "H32": _v(W41, fwa={"break_even": "s43", "max_flagged": 3}, floor="cost43"),                                                        # H30 but at most 3 providers go through the lane (the busiest days)
}
KEEP = ("score", "recovered", "recovered_level", "recovered_fwa", "staff_cost", "abrasion", "demands", "lane_flagged", "lane_demands", "lane_true", "lane_false", "impossible_providers",
        "justified_called", "justified", "rounds", "charts", "listed")


def _run(job):
    name, seed = job
    spec = VERSIONS[name]
    code = f"d43_{seed}"
    scr = dev.write_flagged(code, spec["screen"], 10)
    if spec.get("list_k"):
        scr = w_loop.write_flagged_topk(code, scr, spec["list_k"])
    rid = f"d43wl{name.lower()}_{seed}"
    if not r2.done(rid, "case_summaries_checked.jsonl"):
        kw = {"w40": spec["w40"]} if spec["version"] == "4.0" else {}
        ow.run(rid, code, scr, f"workflow loop version {name} on data 4.3 development seed {seed}", version=spec["version"], tier1_n=11, no_model=True, office_version="4.3", **kw)
    c, _ = s42.seed_result(rid, code)
    c3, _ = s43.seed_result(rid, code)
    out = {k: c[k] for k in KEEP}
    out.update({"score42": c["score"], "score": c3["score"], "collected": c3["collected"], "referrals": c3["referrals"], "demands43": c3["demands"]})       # the loop's score is score 4.3; the lane diagnostics are score 4.2's
    return seed, out


def evaluate(name, seeds, workers=1):
    sreg.check_development("4.3", seeds)
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{name}_s43.json")
    have = json.load(open(path)) if os.path.exists(path) else {}
    todo = [s for s in seeds if str(s) not in have]
    if todo:
        if workers <= 1:                                                            # serial by default: the spawn pool deadlocked once and a crash in a worker hid behind it
            results = [_run((name, s)) for s in todo]
        else:
            with mp.get_context("spawn").Pool(workers) as p:
                results = p.map(_run, [(name, s) for s in todo], chunksize=1)
        for seed, res in results:
            have[str(seed)] = res
        json.dump(have, open(path, "w"), indent=0)
    return {s: have[str(s)] for s in seeds}


def compare(name, ref, seeds):
    a, b = evaluate(name, seeds), evaluate(ref, seeds)
    diffs = [a[s]["score"] - b[s]["score"] for s in seeds]
    return {"mean_a": st.mean(a[s]["score"] for s in seeds), "mean_b": st.mean(b[s]["score"] for s in seeds), "median_a": st.median(a[s]["score"] for s in seeds),
            "mean_diff": st.mean(diffs), "sd_diff": st.stdev(diffs) if len(diffs) > 1 else 0.0, "p": w_loop.perm_p(diffs), "n": len(seeds), "wins": sum(d > 0 for d in diffs),
            "above_zero": sum(a[s]["score"] > 0 for s in seeds), "lane_true": sum(a[s]["lane_true"] for s in seeds), "lane_false": sum(a[s]["lane_false"] for s in seeds),
            "impossible": sum(a[s]["impossible_providers"] for s in seeds), "recovered_fwa": st.mean(a[s]["recovered_fwa"] for s in seeds)}


def line(c, name, ref):
    return (f"{name} vs {ref} on {c['n']} seeds: S4.3 per seed {c['mean_a']:,.0f} (median {c['median_a']:,.0f}) vs {c['mean_b']:,.0f} (difference {c['mean_diff']:+,.0f}, sd {c['sd_diff']:,.0f}, better on {c['wins']} of {c['n']}, "
            f"one-sided p = {c['p']:.4f}); seeds above zero {c['above_zero']}; lane providers right {c['lane_true']} of {c['impossible']} impossible-day providers, wrong {c['lane_false']}; lane recovery per seed {c['recovered_fwa']:,.0f}")


if __name__ == "__main__":
    cmd, name = sys.argv[1], sys.argv[2]
    if cmd == "run":
        seeds = sum([pool.BATCHES[int(b) - 1] for b in sys.argv[3].split(",")], [])
        res = evaluate(name, seeds)
        print(name, "S4.3 per seed:", round(st.mean(r["score"] for r in res.values())), "median", round(st.median(r["score"] for r in res.values())))
    elif cmd == "compare":
        ref = sys.argv[3]
        seeds = sum([pool.BATCHES[int(b) - 1] for b in sys.argv[4].split(",")], [])
        print(line(compare(name, ref, seeds), name, ref))
