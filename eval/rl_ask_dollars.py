"""Release 4: the ask-or-skip decision trained on the DOLLAR reward, on the 20 development seeds, leave-seeds-out (issue 108). Free.

For every listed provider (22 per seed) the outcome of ASKING is net dollars (eval/dollar_reward.py), the outcome of skipping is 0. Asking is followed by one of two escalation rules:
the hand-set workflow v2.3 rule (B), or the stop-or-escalate policy trained on dollars (docs/rl_escalate_dollars.md, each provider's choice made by models that never saw its seed).
The ask-or-skip policy is a ridge regression of the dollars of asking on what the payer sees before asking (screen rank, ratio to expected, excess claims, claim count, screen score,
z_adj) and asks when the prediction is above zero. Five folds of four seeds, fitted on the other sixteen. Compared with asking everyone, asking nobody and the hand-set ratio gates.
The ask-or-skip outcomes under the learned escalation use choices that are themselves out-of-fold, so the nested leakage is small but not zero.

Usage: python eval/rl_ask_dollars.py      (writes docs/rl_ask_dollars.md and experiments/rl_ask_dollar_dataset.json)
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
import rl_ask_policy as rl1  # noqa: E402
import rl_escalate_dollars as rld  # noqa: E402
import rl_escalate_policy as r2  # noqa: E402
import summary_rules as sr  # noqa: E402

DATA = os.path.join(ROOT, "experiments", "rl_ask_dollar_dataset.json")


def hand_set(job):
    pre, seed = job
    src = f"{pre}_{seed}"
    name = dev3.write_flagged(src, "eb_ratio_t", 10)
    rid = f"rad_{seed}"
    view, office, flagged_file = mw.build_view(rid, src, name, version="2.3", tier1_n=dev4.TIER1_N)
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{src}.json")))["providers"]
    claims = {}
    for r in csv.DictReader(open(os.path.join(ROOT, "data", f"synthetic_v2_{src}", "view", "claims.csv"))):
        claims.setdefault(r["provider_id"], []).append(r)
    level = dr.level_of_rows([row for st in office.state.values() for row in st["usable"].values()])
    out = []
    for o in cs.run(view, flagged_file, os.path.join("/tmp", f"{rid}.jsonl"), dry_run=True, rules="2.3"):
        pid = o["provider_id"]
        called = sr.rule_leaning_23(o["packet"])[0] == sr.UPCODING
        up = key[pid]["role"] == "upcoder"
        st = office._st(pid)
        value = dr.point_estimate(pid, claims.get(pid, []), office.random_claim_ids(pid), level) if (called and up) else 0.0
        cost = dr.C_COPY * st["round"] + (0 if up else dr.C_BURDEN * st["round"]) + (dr.C_REVIEW if st["usable"] else 0) + (dr.C_FALSE if (called and not up) else 0)
        out.append({"seed": seed, "pid": pid, "B_dollars": value - cost, "B_found": bool(called and up), "B_hc": bool(called and not up)})
    return out


def main():
    if not os.path.exists(DATA):
        with mp.Pool(4) as pool:
            hs = [r for part in pool.map(hand_set, dev4.SEEDS) for r in part]
        feats = {(r["seed"], r["pid"]): r for r in json.load(open(rl1.DATA))}
        esc = json.load(open(rld.DATA))
        pred = rld.cv(esc)
        choice = {(r["seed"], r["pid"]): max(r2.BRANCHES, key=lambda b: pred[b][i]) for i, r in enumerate(esc)}
        escd = {(r["seed"], r["pid"]): r for r in esc}
        rows = []
        for h in hs:
            k = (h["seed"], h["pid"])
            f, e, b = feats[k], escd[k], choice[k]
            rows.append({**f, **h, "L_dollars": e[b]["dollars"], "L_found": bool(e[b]["found"]), "L_hc": bool(e[b]["honest_called"]), "L_choice": b})
        json.dump(rows, open(DATA, "w"))
    rows = json.load(open(DATA))
    X = rl1.matrix(rows)
    seeds = sorted({r["seed"] for r in rows})
    fold_of = {s: i % 5 for i, s in enumerate(seeds)}
    f = np.array([fold_of[r["seed"]] for r in rows])
    ask = {}
    for esc_name in ("B", "L"):
        y = np.array([r[esc_name + "_dollars"] for r in rows]) / 1000.0
        p = np.zeros(len(rows))
        for k in range(5):
            tr, te = f != k, f == k
            p[te] = r2.linfit(X[tr], y[tr])(X[te]) * 1000.0
        ask[esc_name] = p > 0
    n = len(seeds)
    def tot(esc_name, sel):
        return {"asked": int(sum(sel)), "found": int(sum(r[esc_name + "_found"] for r, s in zip(rows, sel) if s)), "hc": int(sum(r[esc_name + "_hc"] for r, s in zip(rows, sel) if s)),
                "honest_asked": int(sum((not r["upcoder"]) for r, s in zip(rows, sel) if s)), "dollars": sum(r[esc_name + "_dollars"] for r, s in zip(rows, sel) if s)}
    L = ["# Release 4: ask-or-skip trained on dollars, 20 development seeds (issue 108)", "", "[Back to the README](../README.md)", "",
         "Generated by `python eval/rl_ask_dollars.py`. Free. **Release 5 groundwork, not release 4.** Release 4 sticks to the points-based reinforcement learning (reward +1 per upcoder found, -1 per honest doctor flagged, -0.05 per extra round sent to an honest practice); the dollar reward and everything trained on it moves to release 5 (issue 109), where the value of a call becomes the 90% lower bound of the extrapolated estimate. Net dollars of asking each listed provider (`eval/dollar_reward.py`) under two escalation rules, B (workflow v2.3's hand-set rule) and L (the "
         "stop-or-escalate policy trained on dollars, out-of-fold); skipping is $0. The learned ask-or-skip is a ridge regression on what the payer sees before asking, **leave-seeds-out** (5 folds of 4 seeds). "
         "Development seeds only (they shaped earlier decisions), so this is not a test.", "",
         "| Ask-or-skip policy | Escalation | Providers asked | Honest practices asked | Upcoders found | Honest doctors called | Net dollars (20 seeds) | Per seed |", "|---|---|---|---|---|---|---|---|",
         "| ask nobody | – | 0 | 0 | 0 | 0 | $0 | $0 |"]
    for esc_name, label in (("B", "hand-set (B)"), ("L", "learned on dollars (L)")):
        sels = {"ask everyone": [True] * len(rows), "ratio >= 2.5 (light tier)": [(r["rank"] <= dev4.TIER1_N) or r["ratio"] >= 2.5 for r in rows],
                "ratio >= 3 (light tier)": [(r["rank"] <= dev4.TIER1_N) or r["ratio"] >= 3.0 for r in rows], "ratio >= 3 (whole list)": [r["ratio"] >= 3.0 for r in rows],
                "**learned on dollars (cross-validated)**": list(ask[esc_name])}
        for name, sel in sels.items():
            t = tot(esc_name, sel)
            L.append(f"| {name} | {label} | {t['asked']} | {t['honest_asked']} | {t['found']} | {t['hc']} | ${t['dollars']:,.0f} | ${t['dollars'] / n:,.0f} |")
    L += ["", "## Reading", "",
          "- **Asking nobody ($0) is the bar.** Any policy below it loses money at these prices and this synthetic scale.",
          "- Compare each row with the same escalation: whether the learned ask-or-skip beats the hand-set ratio gates, and whether pairing it with the learned escalation (L) helps more than either alone.",
          "- Everything here is cross-validated on development data and noisy (440 providers, about 157 upcoders, heavy-tailed dollars); the next step is a larger development pool, then one fresh test."]
    open(os.path.join(ROOT, "docs", "rl_ask_dollars.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
