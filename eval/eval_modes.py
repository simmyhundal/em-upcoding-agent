"""Evaluation modes (issue 207; docs/evaluation_modes.md): the stage a run covers and the people at the two ends of it, as parameters of the harness, not of the arms.

Stages: `screen` (score the shortlist from the screen alone), `records` (start from a given list and run the records stage), `full` (both, with the gates between).
Gate 1 (a PI team reviews the shortlist and sends the requests): accept all (the setting of every number reported so far), keep the top k, or a person vetoes a seeded random fraction (level list and
volume-lane providers alike). Gate 2 (a PI team signs off each demand): accept all, accept only demands whose conservative estimate is at least a figure, or reject a seeded random fraction.
The gates are a MODEL of a person, an assumption, not evidence of how teams decide; every results row carries the settings.
Usage: python eval/eval_modes.py table NAME SEEDS...      one row per preset, free (data 4.2 codes d42_<seed>)
"""
import csv
import hashlib
import json
import os
import random
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_release3 as dev  # noqa: E402
import make_v2_office_workflow_runs as ow  # noqa: E402
import metrics_d42 as md  # noqa: E402
import run_release2 as r2  # noqa: E402
import score_42 as s42  # noqa: E402
import w_loop  # noqa: E402
import w_loop_42 as wl  # noqa: E402

PRESETS = {
    "accept_all": {"stage": "full", "gate1": {"kind": "accept_all"}, "gate2": {"kind": "accept_all"}},                                  # every number reported so far
    "veto_30": {"stage": "full", "gate1": {"kind": "veto", "fraction": 0.3, "seed": 1}, "gate2": {"kind": "accept_all"}},              # a person drops 30% of the list at random
    "top_2_and_signoff": {"stage": "full", "gate1": {"kind": "top_k", "k": 2}, "gate2": {"kind": "min_estimate", "usd": 1000.0}},    # keep the top 2 of the level list, sign off demands of $1,000 or more
}


def _list_path(code, name):
    return os.path.join(ROOT, "experiments", code, f"flagged_{name}.csv")


def write_list(code, base_name, tag, keep_ids=None, veto_fraction=0.0, veto_seed=1, top_k=None):
    """A flagged file derived from `base_name` for the records stage: only `keep_ids` (when given) stay flagged, a seeded fraction is vetoed, or only the first k stay. Returns the new screen name."""
    new = f"{base_name}_{tag}"
    path = _list_path(code, new)
    rows = list(csv.DictReader(open(_list_path(code, base_name))))
    rng = random.Random(f"{veto_seed}:{code}:gate1")
    left = top_k
    for r in rows:
        if keep_ids is not None:
            r["flagged"] = "True" if r["provider_id"] in keep_ids else "False"
        elif r["flagged"] == "True":
            if veto_fraction and rng.random() < veto_fraction:
                r["flagged"] = "False"
            elif left is not None:
                if left > 0:
                    left -= 1
                else:
                    r["flagged"] = "False"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return new


def gate2_fn(spec):
    kind = spec["kind"]
    if kind == "accept_all":
        return None
    if kind == "min_estimate":
        return lambda pid, v: v >= spec["usd"]
    if kind == "reject_fraction":
        rng = random.Random(spec.get("seed", 1))
        return lambda pid, v: rng.random() >= spec["fraction"]
    raise ValueError(kind)


def run_full(name, seed, preset, code_prefix="d42", office_version="4.2", list_ids=None):
    """One workflow version on one seed under a preset. Returns the score components plus the preset. `list_ids` starts the records stage from a given list (stage 'records')."""
    spec = wl.VERSIONS[name]
    cfg = PRESETS[preset] if isinstance(preset, str) else preset
    code = f"{code_prefix}_{seed}"
    scr = dev.write_flagged(code, spec["screen"], 10)
    if spec.get("list_k"):
        scr = w_loop.write_flagged_topk(code, scr, spec["list_k"])
    g1 = cfg["gate1"]
    w40 = json.loads(json.dumps(spec["w40"]))
    if list_ids is not None:
        scr = write_list(code, scr, "given", keep_ids=set(list_ids))
    elif g1["kind"] == "veto":
        scr = write_list(code, scr, f"veto{int(100 * g1['fraction'])}s{g1.get('seed', 1)}", veto_fraction=g1["fraction"], veto_seed=g1.get("seed", 1))
    elif g1["kind"] == "top_k":
        scr = write_list(code, scr, f"top{g1['k']}", top_k=g1["k"])
    if g1["kind"] == "veto" and w40.get("fwa") is not None:
        w40["fwa"]["veto_fraction"], w40["fwa"]["veto_seed"] = g1["fraction"], g1.get("seed", 1)
    if g1["kind"] == "top_k" and w40.get("fwa") is not None:
        w40["fwa"]["max_flagged"] = min(w40["fwa"].get("max_flagged", 10), g1["k"])
    rid = f"em_{name.lower()}_{scr}_{seed}"
    if w40.get("fwa") is not None:
        rid += "_" + hashlib.md5(json.dumps(w40["fwa"], sort_keys=True).encode()).hexdigest()[:6]
    if not r2.done(rid, "case_summaries_checked.jsonl"):
        ow.run(rid, code, scr, f"evaluation mode run, version {name}, preset {preset}", version=spec["version"], tier1_n=11, no_model=True, office_version=office_version, w40=w40)
    c, _ = s42.seed_result(rid, code, gate2=gate2_fn(cfg["gate2"]))
    return {k: c[k] for k in wl.KEEP + ("rejected_demands",)} | {"stage": cfg["stage"], "gate1": cfg["gate1"], "gate2": cfg["gate2"]}


def screen_only(name, seed, code_prefix="d42", ks=(4, 10, 22)):
    """Stage 'screen': score the shortlist itself (no records requested): dollars of true overpayment in the first k and ranking quality, free."""
    spec = wl.VERSIONS[name]
    code = f"{code_prefix}_{seed}"
    scr = dev.write_flagged(code, spec["screen"], 10)
    return md.screen_metrics(code, _list_path(code, scr), ks=ks)


def table(name, seeds, presets=tuple(PRESETS)):
    out = {}
    for pr in presets:
        res = [run_full(name, s, pr) for s in seeds]
        sc = [r["score"] for r in res]
        out[pr] = {"mean": st.mean(sc), "median": st.median(sc), "above_zero": sum(x > 0 for x in sc), "demands": sum(r["demands"] for r in res), "rejected": sum(r["rejected_demands"] for r in res), "n": len(sc)}
    return out


if __name__ == "__main__":
    if sys.argv[1] == "table":
        print(json.dumps(table(sys.argv[2], [int(x) for x in sys.argv[3:]]), indent=1))
