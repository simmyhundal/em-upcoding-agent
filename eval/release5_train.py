"""Release 5, step 1 (issue 109): the workflow's ask-or-skip and stop-or-escalate decisions trained on the DOLLAR score (recovery model option 2, 90% lower bound) over the 30 development
seeds (release 2, 3 and 4 seeds: 1515 to 4444), leave-seeds-out. Free.

Per listed provider (top-10% eb_ratio_t list, 22 per seed): the state after the first sample and the outcome of each stop-or-escalate choice (STOP, TARG, AUD, BOTH) after the same first
sample, in net dollars (eval/dollar_reward.py: value of the call if it is an upcoder called, minus rounds, honest-practice burden, chart review, and the honest-call charge), plus the outcome
under workflow v2.3's hand-set rule (B). Models: a ridge regression of each choice's dollars on the state (stop-or-escalate), and of the dollars of asking on what the payer sees before asking
(ask-or-skip). Six folds of five seeds: each fold is scored with models fitted on the other 25 seeds. Reported with upcoders found, so the cost in recall is visible.

Usage: python eval/release5_train.py     (writes docs/release5_train.md and experiments/release5_dataset.json)
"""
import csv
import json
import multiprocessing as mp
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import case_summary as cs  # noqa: E402
import dev_release3 as dev3  # noqa: E402
import dev_release4 as dev4  # noqa: E402
import dollar_reward as dr  # noqa: E402
import make_v2_office_workflow_runs as mw  # noqa: E402
import provider_sim  # noqa: E402
import rl_ask_policy as rl1  # noqa: E402
import rl_escalate_policy as r2  # noqa: E402
import summary_rules as sr  # noqa: E402

FRESH = [3535, 3636, 3737, 3838, 3939, 4040, 4141, 4242, 4343, 4444]
SEEDS30 = dev4.SEEDS + [("r4", s) for s in FRESH]
DATA = os.path.join(ROOT, "experiments", "release5_dataset.json")
FOLDS = 6
STATE_KEYS = ["ratio", "charts", "docs99215", "unsupp99215", "notes", "late", "problems", "data", "silent", "first_rounds"]      # the rest of the state (rank) comes with the features


def provider_dollars(office, packets, key, claims):
    out = {}
    level = dr.level_of_rows([row for st in office.state.values() for row in st["usable"].values()])
    for o in packets:
        pid = o["provider_id"]
        called = sr.rule_leaning_23(o["packet"])[0] == sr.UPCODING
        up = key[pid]["role"] == "upcoder"
        st = office._st(pid)
        notes = {c: row for c, row in st["usable"].items()}
        value = dr.point_estimate(pid, claims.get(pid, []), office.random_claim_ids(pid), level, notes) if (called and up) else 0.0
        cost = dr.C_COPY * st["round"] + (0 if up else dr.C_BURDEN * st["round"]) + (dr.C_REVIEW if st["usable"] else 0) + (dr.C_FALSE if (called and not up) else 0)
        out[pid] = {"dollars": value - cost, "found": bool(called and up), "hc": bool(called and not up), "rounds": st["round"]}
    return out


def one(job):
    pre, seed = job
    src = f"{pre}_{seed}"
    base_rows = {r["pid"]: r for r in r2.one(job)}                     # state after the first sample and the points-era outcomes per branch (state features reused)
    feats = {r["pid"]: r for r in rl1.provider_rows(job)}              # features before asking, and the hand-set (B) outcomes in points
    name = dev3.write_flagged(src, "eb_ratio_t", 10)
    data = os.path.join(ROOT, "data", f"synthetic_v2_{src}")
    base = os.path.join(data, "view")
    flagged_file = os.path.join(ROOT, "experiments", src, f"flagged_{name}.csv")
    ids = [r["provider_id"] for r in csv.DictReader(open(flagged_file)) if r["flagged"] == "True"]
    claims = {}
    for r in csv.DictReader(open(os.path.join(base, "claims.csv"))):
        claims.setdefault(r["provider_id"], []).append(r)
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{src}.json")))["providers"]
    res = {pid: {**{k: feats[pid][k] for k in ("seed", "set", "pid", "rank", "ratio", "excess", "claims", "screen_score", "z_adj", "upcoder")},
                 **{k: base_rows[pid][k] for k in STATE_KEYS}} for pid in ids}
    import records
    for branch in r2.BRANCHES:
        rid = f"r5{branch.lower()}_{seed}"
        view = os.path.join(data, f"view_{rid}")
        os.makedirs(view, exist_ok=True)
        for fn in ("claims.csv", "patients.csv", "providers.csv"):
            dst = os.path.join(view, fn)
            if not os.path.exists(dst):
                os.symlink(os.path.join(base, fn), dst)
        office = provider_sim.Office(data, base, seed=1, version="2.1")
        r2.run_branch(office, ids, claims, branch)
        owner = {r["claim_id"]: r["provider_id"] for rows in claims.values() for r in rows}
        control = {r["provider_id"] for r in csv.DictReader(open(os.path.join(base, "records_requests.csv"))) if r["kind"] == "control"} - set(ids)
        docs = [r for r in csv.DictReader(open(os.path.join(base, "documentation.csv"))) if owner.get(r["claim_id"]) in control] + office.documentation_rows()
        records.write_docs(os.path.join(view, "documentation.csv"), docs)
        packets = cs.run(view, flagged_file, os.path.join("/tmp", f"{rid}.jsonl"), dry_run=True, rules="2.3")
        for pid, v in provider_dollars(office, packets, key, claims).items():
            res[pid][branch] = v
    rid = f"r5b_{seed}"
    view, office, flagged_file = mw.build_view(rid, src, name, version="2.3", tier1_n=dev4.TIER1_N)
    packets = cs.run(view, flagged_file, os.path.join("/tmp", f"{rid}.jsonl"), dry_run=True, rules="2.3")
    for pid, v in provider_dollars(office, packets, key, claims).items():
        res[pid]["B"] = v
    return list(res.values())


def folds(rows):
    seeds = sorted({r["seed"] for r in rows})
    fold_of = {s: i % FOLDS for i, s in enumerate(seeds)}
    return np.array([fold_of[r["seed"]] for r in rows])


def cv_escalation(rows):
    f = folds(rows)
    X = r2.matrix(rows)
    pred = {b: np.zeros(len(rows)) for b in r2.BRANCHES}
    for k in range(FOLDS):
        tr, te = f != k, f == k
        for b in r2.BRANCHES:
            y = np.array([r[b]["dollars"] for r in rows]) / 1000.0
            pred[b][te] = r2.linfit(X[tr], y[tr])(X[te]) * 1000.0
    return [max(r2.BRANCHES, key=lambda b: pred[b][i]) for i in range(len(rows))]


def cv_ask(rows, outcome):
    f = folds(rows)
    X = rl1.matrix(rows)
    y = np.array(outcome) / 1000.0
    p = np.zeros(len(rows))
    for k in range(FOLDS):
        tr, te = f != k, f == k
        p[te] = r2.linfit(X[tr], y[tr])(X[te]) * 1000.0
    return p > 0


def tot(rows, sel, key):
    xs = [(r, k) for r, s, k in zip(rows, sel, key) if s]
    return {"asked": len(xs), "found": sum(r[k]["found"] for r, k in xs), "hc": sum(r[k]["hc"] for r, k in xs), "dollars": sum(r[k]["dollars"] for r, k in xs),
            "honest_asked": sum(not r["upcoder"] for r, k in xs)}


def main():
    if not os.path.exists(DATA) or "--rerun" in sys.argv:
        with mp.Pool(4) as pool:
            rows = [r for part in pool.map(one, SEEDS30) for r in part]
        json.dump(rows, open(DATA, "w"))
    rows = json.load(open(DATA))
    n = len({(r["set"], r["seed"]) for r in rows})
    up = sum(r["upcoder"] for r in rows)
    esc = cv_escalation(rows)
    lkey = esc                                                          # the escalation choice made out-of-fold for each provider
    ask_b = cv_ask(rows, [r["B"]["dollars"] for r in rows])
    ask_l = cv_ask(rows, [r[b]["dollars"] for r, b in zip(rows, lkey)])
    allp = [True] * len(rows)
    gate = [(r["rank"] <= dev4.TIER1_N) or r["ratio"] >= 2.5 for r in rows]
    B = ["B"] * len(rows)
    lines = [("ask nobody", None, None), ("workflow v2.3 (ask everyone, hand-set escalation)", allp, B), ("G: gate 2.5, hand-set escalation", gate, B),
             ("L: ask everyone, learned escalation (dollars, cross-validated)", allp, lkey), ("GL: gate 2.5 and learned escalation", gate, lkey),
             ("learned ask-or-skip, hand-set escalation", list(ask_b), B), ("**learned ask-or-skip and learned escalation**", list(ask_l), lkey)]
    L = ["# Release 5, step 1: ask-or-skip and stop-or-escalate trained on dollars, 30 development seeds (issue 109)", "", "[Back to the README](../README.md)", "",
         "Generated by `python eval/release5_train.py`. Free. Score = net dollars (`eval/dollar_reward.py`: recovery model option 2, 90% lower bound, sourced costs). Six folds of five seeds, "
         f"**leave-seeds-out**. {n} development seeds (release 2, 3 and 4 seeds), {len(rows)} listed providers, {up} planted upcoders. Development data only; the fresh test comes later.", "",
         "| Policy | Providers asked | Honest practices asked | Upcoders found | Recall | Honest doctors called | Net dollars | Per seed |", "|---|---|---|---|---|---|---|---|"]
    for name, sel, key in lines:
        if sel is None:
            L.append("| ask nobody | 0 | 0 | 0 | 0% | 0 | $0 | $0 |")
            continue
        t = tot(rows, sel, key)
        L.append(f"| {name} | {t['asked']} | {t['honest_asked']} | {t['found']} | {t['found'] / up:.0%} | {t['hc']} | ${t['dollars']:,.0f} | ${t['dollars'] / n:,.0f} |")
    L += ["", "## Reading", "",
          "- Compare rows by net dollars, then look at recall: the learned policies may give up upcoders for dollars, and that cost is shown, not hidden.",
          "- Recovery model option 2 is the optimistic one (a flagged note is denied in full); options 1 and 3 change the values and would change what is worth asking. Not tested here.",
          "- Cross-validated on development data only; the pre-registered fresh test is the comparison that counts."]
    open(os.path.join(ROOT, "docs", "release5_train.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
