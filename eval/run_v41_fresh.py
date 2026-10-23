"""W4.1 on the ten test seeds of workflow v4.0 (5555 to 6464): the run declared in docs/w41_freeze.md. Free (API-free workflow). Never used by the development loop (eval/w_loop.py refuses these seeds on purpose).
Runs two arms once each: W4.1 (H23, N = 4) and the control W4.0 with the same 4-provider list (H8_n4). Writes experiments/v41_fresh_results.json and prints the paired comparisons. Usage: python eval/run_v41_fresh.py [run|report]"""
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
import run_release2 as r2  # noqa: E402
import score_40 as s4  # noqa: E402
import w_loop as wl  # noqa: E402

SEEDS = [5555 + 101 * i for i in range(10)]
ARMS = {"W4.1 (H23, list 4)": ("fr41", "H23_n4"), "W4.0 with list 4 (control)": ("fr40n4", "H8_n4")}
OUT = os.path.join(ROOT, "experiments", "v41_fresh_results.json")


def _run(job):
    label, seed = job
    pre, name = ARMS[label]
    spec = wl.VERSIONS[name]
    code = f"f4_{seed}"
    scr = dev.write_flagged(code, spec["screen"], 10)
    if spec.get("list_k"):
        scr = wl.write_flagged_topk(code, scr, spec["list_k"])
    rid = f"{pre}_{seed}"
    if not r2.done(rid, "case_summaries_checked.jsonl"):
        ow.run(rid, code, scr, f"{label} on test seed {seed} (docs/w41_freeze.md)", version=spec["version"], tier1_n=11, no_model=True, w40=spec["w40"])
    c = s4.from_run(rid, code)
    return label, seed, {k: c[k] for k in wl.KEEP}


def run():
    assert all(s >= 5555 for s in SEEDS)
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    with mp.get_context("spawn").Pool(4) as pool:
        for label, seed, r in pool.map(_run, [(a, s) for a in ARMS for s in SEEDS], chunksize=1):
            res.setdefault(label, {})[str(seed)] = r
    json.dump(res, open(OUT, "w"), indent=0)


def report():
    new = json.load(open(OUT))
    old = json.load(open(os.path.join(ROOT, "experiments", "v4_fresh_results.json")))
    pairs = [("W4.1 (H23, list 4)", "W4.0", old["W4.0"]), ("W4.1 (H23, list 4)", "W4.0 with list 4 (control)", new["W4.0 with list 4 (control)"]), ("W4.1 (H23, list 4)", "frozen W2.5", old["W2.5 (frozen)"]),
             ("W4.0 with list 4 (control)", "W4.0", old["W4.0"])]
    for lab in new:
        d = new[lab]
        print(f"{lab}: score per seed {st.mean(v['score'] for v in d.values()):,.0f}; found {sum(v['found'] for v in d.values())} of {sum(v['upcoders'] for v in d.values())}; honest called {sum(v['honest_called'] for v in d.values())}; "
              f"rounds {sum(v['rounds'] for v in d.values())}; recovered {sum(v['recovered'] for v in d.values()):,.0f}; staff {sum(v['staff_cost'] for v in d.values()):,.0f}")
    for a, b, ref in pairs:
        A = new[a] if a in new else None
        d = [A[str(s)]["score"] - ref[str(s)]["score"] for s in SEEDS]
        print(f"{a} minus {b}: mean {st.mean(d):+,.0f} per seed (sd {st.stdev(d):,.0f}), better on {sum(x > 0 for x in d)}, worse on {sum(x < 0 for x in d)}, same {sum(x == 0 for x in d)}; one-sided exact p = {wl.perm_p(d):.4f}")
    for lab in new:
        d = [new[lab][str(s)]["score"] for s in SEEDS]
        print(f"{lab} against zero: mean {st.mean(d):+,.0f}; one-sided exact p = {wl.perm_p(d):.4f}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "run":
        run()
    report()
