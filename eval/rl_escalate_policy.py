"""Release 4, Stage 2 of the learning plan (issue 108): after the first sample, choose stop, a targeted request, an audit trail, or both. Free (simulated office, rules 2.3).

Every listed provider (top-10% eb_ratio_t list, 22 per seed, 20 development seeds, data 2.2) gets the same first sample (a random request for 30 charts and a follow-up on any
deficiency). The office draws each provider's responses from a stream keyed by provider and round, so what each later action would have returned is well defined and independent
of the other providers: we run the whole list under four fixed branches and observe the outcome of every choice for every provider.
  STOP   nothing more.          TARG  a targeted request for 15 charts of the top code, with a follow-up on any deficiency.
  AUD    an audit-trail request for up to 20 notes.          BOTH  TARG, then AUD.
Outcome per branch: the upcoder is found by rules 2.3 (or an honest doctor is called) and the rounds the practice was sent (all of them, from the office state).
State (what the payer sees after the first sample): charts returned, documented 99215 claims and their unsupported share, notes returned and the late, problems and data
signal rates, whether the office was silent, rounds used, the screen rank and ratio. The answer key supplies outcomes only.

Policy: pick the branch b maximizing  P_b(found|x) - kappa P_b(honest called|x) - lambda P(honest|x) E[extra rounds_b|x]   (kappa = 1, lambda on a grid fixed here), with logistic
and linear models fitted on other seeds only (leave-seeds-out cross-validation, 5 folds of 4 seeds). Compared with the four fixed branches and with workflow v2.3's hand-set rule
(targeted request only in the first 5% and when fewer than 6 usable 99215 charts came back; audit trail when the notes show cloning), taken from the Stage 1 run.

Usage: python eval/rl_escalate_policy.py     (writes docs/rl_escalate_policy.md and experiments/rl_escalate_dataset.json)
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
import make_v2_office_workflow_runs as mw  # noqa: E402
import provider_sim  # noqa: E402
import rl_ask_policy as rl1  # noqa: E402
import summary_rules as sr  # noqa: E402
import workflow_policy_23 as p23  # noqa: E402
import workflow_policy_v21 as v21  # noqa: E402

BRANCHES = ("STOP", "TARG", "AUD", "BOTH")
LAMBDAS = [0.0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5]
KAPPA = 1.0
DATA = os.path.join(ROOT, "experiments", "rl_escalate_dataset.json")
STATE = ["rank", "log_ratio", "charts", "docs99215", "unsupp99215", "notes", "late", "problems", "data", "silent", "first_rounds"]


def run_branch(office, ids, claims_by_provider, branch):
    for pid in ids:
        resp = v21._follow(office, pid, office.send_request(pid, {"kind": "random", "n": p23.RANDOM_N}, deadline=30))
        if "error" in resp:
            continue
        st = office.state[pid]
        if branch in ("TARG", "BOTH") and st["round"] < office.max_rounds:
            v21._follow(office, pid, office.send_request(pid, {"kind": "targeted", "cpt": "99215", "n": p23.TARGETED_N}, deadline=30))
        rows = [r for c, r in st["usable"].items() if r.get("note_id")]
        if branch in ("AUD", "BOTH") and rows and st["round"] < office.max_rounds:
            office.request_audit_trail(pid, [r["claim_id"] for r in rows][:p23.AUDIT_MAX])
        office.close_request(pid, f"stage 2 branch {branch}")


def one(job):
    pre, seed = job
    src = f"{pre}_{seed}"
    name = dev3.write_flagged(src, "eb_ratio_t", 10)
    data = os.path.join(ROOT, "data", f"synthetic_v2_{src}")
    base = os.path.join(data, "view")
    flagged_file = os.path.join(ROOT, "experiments", src, f"flagged_{name}.csv")
    flagged = [r for r in csv.DictReader(open(flagged_file)) if r["flagged"] == "True"]
    ids = [r["provider_id"] for r in flagged]
    meta = {r["provider_id"]: r for r in flagged}
    by_provider = {}
    for r in csv.DictReader(open(os.path.join(base, "claims.csv"))):
        by_provider.setdefault(r["provider_id"], []).append(r)
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{src}.json")))["providers"]
    out = {}
    for branch in BRANCHES:
        rid = f"rl2{branch.lower()}_{seed}"
        view = os.path.join(data, f"view_{rid}")
        os.makedirs(view, exist_ok=True)
        for fn in ("claims.csv", "patients.csv", "providers.csv"):
            dst = os.path.join(view, fn)
            if not os.path.exists(dst):
                os.symlink(os.path.join(base, fn), dst)
        office = provider_sim.Office(data, base, seed=1, version="2.1")
        run_branch(office, ids, by_provider, branch)
        req = list(csv.DictReader(open(os.path.join(base, "records_requests.csv"))))
        control = {r["provider_id"] for r in req if r["kind"] == "control"} - set(ids)
        owner = {r["claim_id"]: r["provider_id"] for r in by_provider_flat(by_provider)}
        import records
        docs = [r for r in csv.DictReader(open(os.path.join(base, "documentation.csv"))) if owner.get(r["claim_id"]) in control] + office.documentation_rows()
        records.write_docs(os.path.join(view, "documentation.csv"), docs)
        packets = cs.run(view, flagged_file, os.path.join("/tmp", f"{rid}.jsonl"), dry_run=True, rules="2.3")
        for o in packets:
            pid, pk = o["provider_id"], o["packet"]
            called = sr.rule_leaning_23(pk)[0] == sr.UPCODING
            up = key[pid]["role"] == "upcoder"
            d = pk.get("documentation_review") or {}
            ns = d.get("note_signals")
            row99 = next((r for r in d.get("by_billed_level", []) if r["billed_cpt"] == "99215"), None)
            rec = out.setdefault(pid, {"seed": seed, "set": pre, "pid": pid, "upcoder": up, "rank": int(meta[pid]["rank"]),
                                       "ratio": float(meta[pid]["share_99215"]) / max(float(meta[pid]["expected_share"]), 1e-9)})
            rec[branch] = {"found": up and called, "honest_called": (not up) and called, "rounds": office._st(pid)["round"]}
            if branch == "STOP":
                rate = lambda k: ((ns["rates"].get(k) or 0.0) if ns and ns["notes"] >= 8 else 0.0)
                rec.update({"charts": d.get("claims_with_documentation", 0), "docs99215": row99["documented_claims"] if row99 else 0,
                            "unsupp99215": (row99["unsupported_rate"] if row99 else 0.0), "notes": ns["notes"] if ns else 0, "late": rate("late"),
                            "problems": rate("problems"), "data": rate("data"), "silent": d.get("claims_with_documentation", 0) == 0, "first_rounds": office._st(pid)["round"]})
    return list(out.values())


def by_provider_flat(by_provider):
    return [r for rows in by_provider.values() for r in rows]


def matrix(rows):
    return np.array([[r["rank"], np.log(max(r["ratio"], 0.05)), r["charts"], r["docs99215"], r["unsupp99215"], r["notes"], r["late"], r["problems"], r["data"],
                      float(r["silent"]), r["first_rounds"]] for r in rows], float)


def linfit(X, y):
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    beta = np.linalg.solve(Z.T @ Z + 1.0 * np.eye(Z.shape[1]), Z.T @ y)
    return lambda Xn: np.column_stack([np.ones(len(Xn)), (Xn - mu) / sd]) @ beta


def cv_predict(rows, folds=5):
    seeds = sorted({r["seed"] for r in rows})
    fold_of = {s: i % folds for i, s in enumerate(seeds)}
    f = np.array([fold_of[r["seed"]] for r in rows])
    X = matrix(rows)
    P = {b: {k: np.zeros(len(rows)) for k in ("found", "hc", "extra")} for b in BRANCHES}
    honest = np.zeros(len(rows))
    for k in range(folds):
        tr, te = f != k, f == k
        honest[te] = rl1.fit(X[tr], np.array([not r["upcoder"] for r in rows])[tr])(X[te])
        for b in BRANCHES:
            P[b]["found"][te] = rl1.fit(X[tr], np.array([r[b]["found"] for r in rows])[tr])(X[te])
            P[b]["hc"][te] = rl1.fit(X[tr], np.array([r[b]["honest_called"] for r in rows])[tr])(X[te])
            extra = np.array([r[b]["rounds"] - r["STOP"]["rounds"] for r in rows], float)
            P[b]["extra"][te] = np.maximum(linfit(X[tr], extra[tr])(X[te]), 0)
    return P, honest


def evaluate(rows, choice):
    f = hc = rounds = 0
    for r, b in zip(rows, choice):
        f += r[b]["found"]
        hc += r[b]["honest_called"]
        rounds += r[b]["rounds"] if not r["upcoder"] else 0
    return {"found": int(f), "honest_called": int(hc), "honest_rounds": int(rounds)}


def main():
    if not os.path.exists(DATA):
        with mp.Pool(4) as pool:
            rows = [r for part in pool.map(one, dev4.SEEDS) for r in part]
        json.dump(rows, open(DATA, "w"))
    rows = json.load(open(DATA))
    P, honest = cv_predict(rows)
    fixed = {b: evaluate(rows, [b] * len(rows)) for b in BRANCHES}
    stage1 = json.load(open(rl1.DATA))
    hand = {"found": sum(r["found"] for r in stage1), "honest_called": sum(r["honest_called"] for r in stage1),
            "honest_rounds": sum(r["rounds"] for r in stage1 if not r["upcoder"])}
    L = ["# Release 4, Stage 2: a learned stop-or-escalate policy against fixed branches and the hand-set rule (issue 108)", "", "[Back to the README](../README.md)", "",
         "Generated by `python eval/rl_escalate_policy.py`. Free. 20 development seeds, 440 listed providers, data 2.2. Every provider is run under all four branches (the office's "
         "responses are keyed by provider and round, so each branch is observed for each provider); the learned policy picks a branch from the state after the first sample, "
         "**leave-seeds-out cross-validated** (5 folds of 4 seeds). Features are payer-visible only; the answer key gives outcomes.", "",
         "| Policy | Upcoders found | Honest doctors called | Rounds sent to honest practices |", "|---|---|---|---|"]
    L.append(f"| workflow v2.3 hand-set rule (Stage 1 run) | {hand['found']} | {hand['honest_called']} | {hand['honest_rounds']} |")
    for b in BRANCHES:
        L.append(f"| always {b} | {fixed[b]['found']} | {fixed[b]['honest_called']} | {fixed[b]['honest_rounds']} |")
    results = {}
    for lam in LAMBDAS:
        choice = []
        for i in range(len(rows)):
            sc = {b: P[b]["found"][i] - KAPPA * P[b]["hc"][i] - lam * honest[i] * P[b]["extra"][i] for b in BRANCHES}
            choice.append(max(sc, key=sc.get))
        results[lam] = (evaluate(rows, choice), {b: choice.count(b) for b in BRANCHES})
        e, c = results[lam]
        L.append(f"| learned, lambda = {lam:g} (STOP {c['STOP']}, TARG {c['TARG']}, AUD {c['AUD']}, BOTH {c['BOTH']}) | {e['found']} | {e['honest_called']} | {e['honest_rounds']} |")
    best_same = [(e["found"], lam) for lam, (e, _) in results.items() if e["honest_rounds"] <= hand["honest_rounds"]]
    L += ["", "## Reading", "",
          f"- **Against the hand-set rule at no more honest rounds:** the best learned setting finds {max(best_same)[0] if best_same else 'none'} upcoders (lambda = {max(best_same)[1] if best_same else '-'}) "
          f"against {hand['found']} for the hand-set rule, which sent {hand['honest_rounds']} rounds to honest practices.",
          "- The branches tell what each extra step buys on its own: compare always STOP with always TARG, AUD and BOTH above.",
          "- Cross-validation is by seed inside development data; the fresh 10-seed test is the only unbiased comparison. A policy that cannot beat the hand-set rule here should not go forward."]
    open(os.path.join(ROOT, "docs", "rl_escalate_policy.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
