"""Release 4: the Stage 2 stop-or-escalate policy retrained on the DOLLAR reward, on the same 20 development seeds, leave-seeds-out (issue 108). Free.

Same setup as eval/rl_escalate_policy.py (every listed provider run under STOP, TARG, AUD and BOTH after the same first sample), but each provider-branch outcome is a number of
dollars (eval/dollar_reward.py): the extrapolated recovery if the provider is an upcoder called upcoding, minus the cost of the rounds sent, the burden on an honest practice, the chart
review, and the charge for an honest doctor called. The policy is a ridge regression per branch of that dollar outcome on the state after the first sample; it picks the branch with the
highest predicted dollars. Five folds of four seeds: each fold is scored with models fitted on the other sixteen seeds. Nothing is tuned after looking: the model class, the features
and the ridge penalty (1.0) are those of the points version.

Usage: python eval/rl_escalate_dollars.py     (writes docs/rl_escalate_dollars.md and experiments/rl_escalate_dollar_dataset.json)
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
import provider_sim  # noqa: E402
import rl_escalate_policy as r2  # noqa: E402
import summary_rules as sr  # noqa: E402

DATA = os.path.join(ROOT, "experiments", "rl_escalate_dollar_dataset.json")


def one(job):
    pre, seed = job
    src = f"{pre}_{seed}"
    name = dev3.write_flagged(src, "eb_ratio_t", 10)
    data = os.path.join(ROOT, "data", f"synthetic_v2_{src}")
    base = os.path.join(data, "view")
    flagged_file = os.path.join(ROOT, "experiments", src, f"flagged_{name}.csv")
    ids = [r["provider_id"] for r in csv.DictReader(open(flagged_file)) if r["flagged"] == "True"]
    claims = {}
    for r in csv.DictReader(open(os.path.join(base, "claims.csv"))):
        claims.setdefault(r["provider_id"], []).append(r)
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{src}.json")))["providers"]
    base_rows = {r["pid"]: r for r in json.load(open(r2.DATA)) if r["seed"] == seed}     # state features and ids from the points dataset
    out = {pid: dict(base_rows[pid]) for pid in ids}
    for branch in r2.BRANCHES:
        rid = f"rld{branch.lower()}_{seed}"
        view = os.path.join(data, f"view_{rid}")
        os.makedirs(view, exist_ok=True)
        for fn in ("claims.csv", "patients.csv", "providers.csv"):
            dst = os.path.join(view, fn)
            if not os.path.exists(dst):
                os.symlink(os.path.join(base, fn), dst)
        office = provider_sim.Office(data, base, seed=1, version="2.1")
        r2.run_branch(office, ids, claims, branch)
        import records
        owner = {r["claim_id"]: r["provider_id"] for rows in claims.values() for r in rows}
        req = list(csv.DictReader(open(os.path.join(base, "records_requests.csv"))))
        control = {r["provider_id"] for r in req if r["kind"] == "control"} - set(ids)
        docs = [r for r in csv.DictReader(open(os.path.join(base, "documentation.csv"))) if owner.get(r["claim_id"]) in control] + office.documentation_rows()
        records.write_docs(os.path.join(view, "documentation.csv"), docs)
        packets = cs.run(view, flagged_file, os.path.join("/tmp", f"{rid}.jsonl"), dry_run=True, rules="2.3")
        level = dr.level_of_rows([row for st in office.state.values() for row in st["usable"].values()])
        for o in packets:
            pid = o["provider_id"]
            called = sr.rule_leaning_23(o["packet"])[0] == sr.UPCODING
            up = key[pid]["role"] == "upcoder"
            st = office._st(pid)
            value = dr.point_estimate(pid, claims.get(pid, []), office.random_claim_ids(pid), level) if (called and up) else 0.0
            cost = dr.C_COPY * st["round"] + (0 if up else dr.C_BURDEN * st["round"]) + (dr.C_REVIEW if st["usable"] else 0) + (dr.C_FALSE if (called and not up) else 0)
            out[pid][branch] = {**out[pid][branch], "dollars": value - cost, "value": value}
    return list(out.values())


def cv(rows, folds=5):
    seeds = sorted({r["seed"] for r in rows})
    fold_of = {s: i % folds for i, s in enumerate(seeds)}
    f = np.array([fold_of[r["seed"]] for r in rows])
    X = r2.matrix(rows)
    pred = {b: np.zeros(len(rows)) for b in r2.BRANCHES}
    for k in range(folds):
        tr, te = f != k, f == k
        for b in r2.BRANCHES:
            y = np.array([r[b]["dollars"] for r in rows]) / 1000.0
            pred[b][te] = r2.linfit(X[tr], y[tr])(X[te]) * 1000.0
    return pred


def main():
    if not os.path.exists(DATA):
        with mp.Pool(4) as pool:
            rows = [r for part in pool.map(one, dev4.SEEDS) for r in part]
        json.dump(rows, open(DATA, "w"))
    rows = json.load(open(DATA))
    pred = cv(rows)
    choice = [max(r2.BRANCHES, key=lambda b: pred[b][i]) for i in range(len(rows))]
    total = lambda ch: sum(r[b]["dollars"] for r, b in zip(rows, ch))
    comp = lambda ch: (sum(r[b]["found"] for r, b in zip(rows, ch)), sum(r[b]["honest_called"] for r, b in zip(rows, ch)))
    res = json.load(open(os.path.join(ROOT, "experiments", "dollar_results.json")))
    w23 = [r for r in res if r["arm"] == "W2.3"]
    l_pts = [r for r in res if r["arm"] == "L"]
    nseeds = len({(r["set"], r["seed"]) for r in rows})
    L = ["# Release 4: the stop-or-escalate policy retrained on the dollar reward, 20 development seeds (issue 108)", "", "[Back to the README](../README.md)", "",
         "Generated by `python eval/rl_escalate_dollars.py`. Free. **Release 5 groundwork, not release 4.** Release 4 sticks to the points-based reinforcement learning (reward +1 per upcoder found, -1 per honest doctor flagged, -0.05 per extra round sent to an honest practice); the dollar reward and everything trained on it moves to release 5 (issue 109), where the value of a call becomes the 90% lower bound of the extrapolated estimate. Every listed provider is run under the four choices after the same first sample; the outcome of each choice is net dollars "
         "(`eval/dollar_reward.py`: extrapolated recovery on upcoders called, minus round costs, honest-practice burden, chart review, and the charge for an honest doctor called). "
         "The policy predicts the dollars of each choice from the state after the first sample and takes the best; **leave-seeds-out** (5 folds of 4 seeds). **In sample for the development "
         "seeds' history** (they shaped earlier decisions), so this is a development result, not a test.", "",
         "| Policy | Upcoders found | Honest doctors called | Net dollars (20 seeds) | Per seed |", "|---|---|---|---|---|",
         "| ask nobody | 0 | 0 | $0 | $0 |"]
    for b in r2.BRANCHES:
        f, h = comp([b] * len(rows))
        L.append(f"| always {b} (whole list) | {f} | {h} | ${total([b] * len(rows)):,.0f} | ${total([b] * len(rows)) / nseeds:,.0f} |")
    f, h = comp(choice)
    L.append(f"| **learned on dollars (cross-validated)** | {f} | {h} | **${total(choice):,.0f}** | **${total(choice) / nseeds:,.0f}** |")
    for name, xs in (("W2.3 hand-set rule (re-run)", w23), ("L: learned on points (cross-validated)", l_pts)):
        net = sum(dr.net(x) for x in xs)
        L.append(f"| {name} | {sum(x['found'] for x in xs)} | {sum(x['honest_called'] for x in xs)} | ${net:,.0f} | ${net / len(xs):,.0f} |")
    from collections import Counter
    c = Counter(choice)
    L += ["", f"Choices of the dollar policy: {dict(c)}.", "",
          "## Reading", "",
          "- **Ask nobody is the bar.** Most whole-list policies lose money at these prices and this scale; a policy is only worth running if it beats $0 (asking only where it pays is the point of the gate and of the ask-or-skip decision, Stage 1, which here is not yet trained on dollars).",
          "- **Training on dollars changes what escalation is worth:** a targeted request or audit trail costs rounds and a chart review, and pays only when it turns a provider into an upcoder with a documentable estimate.",
          "- **Small sample:** 440 providers and about 157 upcoders over 20 seeds; dollar outcomes are heavy-tailed, so the cross-validated number is noisy. A larger development pool (about 100 seeds) is the next step before any claim."]
    open(os.path.join(ROOT, "docs", "rl_escalate_dollars.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
