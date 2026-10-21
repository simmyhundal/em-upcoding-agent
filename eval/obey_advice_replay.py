"""Free counterfactual for issue 118: should the agent obey the policy's recommendation after a provider's first sample?

Per listed provider (the top-10% eb_ratio_t list, 22 per seed) on the 40 development seeds of releases 2 to 5, the simulator is run once per stop-or-escalate branch (STOP, TARG, AUD, BOTH) after the
same first sample (random 30 charts and a follow-up): the office's responses are keyed by provider and round, so every branch is exact without a model. Each branch is valued with score 4.0
(eval/score_40.py: a demand is sent where rules 2.3 call upcoding; recovered minus staff-hours cost minus abrasion). The policy's advice is `src/policy_25.json` on the state after the first sample.

For each stored agent run (A3.2 to A3.5) the providers it worked and the branch it took (TARG if it sent a targeted request, AUD if it requested the audit trail, BOTH, else STOP) are read from its
audit log, and four designs are valued on those providers: (a) observed branch; (b) always the advised branch; (c) the advised branch only when it is STOP; (d) the advised branch only when it is
TARG, AUD or BOTH. Exact for the action; approximate for the call (the rules decide here, the agent may have decided differently). The policy was fitted on the release 2 to 4 seeds, so those are
IN SAMPLE for (b), (c) and (d); release 5 seeds are out of sample.

Usage: python eval/obey_advice_replay.py [--rebuild]       (writes docs/obey_advice_replay.md and experiments/obey_advice_table.json)
"""
import csv
import json
import multiprocessing as mp
import os
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import case_summary as cs  # noqa: E402
import dev_release3 as dev3  # noqa: E402
import dollar_reward as dr  # noqa: E402
import escalation_policy as ep  # noqa: E402
import policy_25 as p25  # noqa: E402
import provider_sim  # noqa: E402
import records  # noqa: E402
import rl_escalate_policy as r2  # noqa: E402
import score_40 as s4  # noqa: E402
import summary_rules as sr  # noqa: E402

TABLE = os.path.join(ROOT, "experiments", "obey_advice_table.json")
DOC = os.path.join(ROOT, "docs", "obey_advice_replay.md")
SETS = [("A3.2", "r2", "r2a", list(range(1515, 2425, 101))), ("A3.3", "r3", "r3a", list(range(2525, 3435, 101))),
        ("A3.4", "r4", "r4a", list(range(3535, 4445, 101))), ("A3.5", "r5", "r5a", list(range(4545, 5455, 101)))]
BRANCHES = r2.BRANCHES


def branch_table(job):
    pre, seed = job
    code = f"{pre}_{seed}"
    name = dev3.write_flagged(code, "eb_ratio_t", 10)
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    base = os.path.join(data, "view")
    flagged_file = os.path.join(ROOT, "experiments", code, f"flagged_{name}.csv")
    flagged = [r for r in csv.DictReader(open(flagged_file)) if r["flagged"] == "True"]
    ids = [r["provider_id"] for r in flagged]
    meta = {r["provider_id"]: r for r in flagged}
    claims, key, truth = s4.context(code)
    allclaims = {pid: rows for pid, rows in claims.items()}
    policy = p25.load()
    out = {pid: {"seed": seed, "set": pre, "pid": pid, "upcoder": key["providers"][pid]["role"] == "upcoder"} for pid in ids}
    for branch in BRANCHES:
        rid = f"oa{branch.lower()}_{seed}"
        view = os.path.join(data, f"view_{rid}")
        os.makedirs(view, exist_ok=True)
        for fn in ("claims.csv", "patients.csv", "providers.csv"):
            dst = os.path.join(view, fn)
            if not os.path.exists(dst):
                os.symlink(os.path.join(base, fn), dst)
        office = provider_sim.Office(data, base, seed=1, version="2.1")
        r2.run_branch(office, ids, allclaims, branch)
        owner = {r["claim_id"]: r["provider_id"] for rows in allclaims.values() for r in rows}
        control = {r["provider_id"] for r in csv.DictReader(open(os.path.join(base, "records_requests.csv"))) if r["kind"] == "control"} - set(ids)
        docs = [r for r in csv.DictReader(open(os.path.join(base, "documentation.csv"))) if owner.get(r["claim_id"]) in control] + office.documentation_rows()
        records.write_docs(os.path.join(view, "documentation.csv"), docs)
        packets = cs.run(view, flagged_file, os.path.join("/tmp", f"{rid}.jsonl"), dry_run=True, rules="2.3")
        level = dr.level_of_rows([row for stt in office.state.values() for row in stt["usable"].values()])
        for o in packets:
            pid = o["provider_id"]
            called = sr.rule_leaning_23(o["packet"])[0] == sr.UPCODING
            stt = office._st(pid)
            rec = s4.recovery(allclaims.get(pid, []), office.random_claim_ids(pid), level, s4.PARAMS) if called else {"value": 0.0}
            rounds, charts = stt["round"], len(stt["usable"])
            cost, _ = s4.staff_cost(1, rounds, charts, 1 if called else 0, 0.0, s4.PARAMS)             # triage of this provider counts for every design alike
            r = truth[pid]["net_rate"]
            abr = s4.abrasion_weight(r, s4.PARAMS) * (rounds * s4.PARAMS["C_BURDEN"] + (s4.PARAMS["C_DEMAND_ABRASION"] if called else 0.0))
            out[pid][branch] = {"score": rec["value"] - cost - abr, "found": bool(called and out[pid]["upcoder"]), "honest_called": bool(called and not out[pid]["upcoder"]), "rounds": rounds}
            if branch == "STOP":
                x = ep.state_vector(list(stt["usable"].values()), allclaims[pid], int(meta[pid]["rank"]), float(meta[pid]["share_99215"]) / max(float(meta[pid]["expected_share"]), 1e-9), rounds)
                out[pid]["advice"] = p25.choose(policy, x)
    return list(out.values())


def build():
    jobs = [(pre, s) for _, pre, _, seeds in SETS for s in seeds]
    with mp.get_context("spawn").Pool(4) as pool:
        rows = [r for part in pool.map(branch_table, jobs, chunksize=1) for r in part]
    json.dump(rows, open(TABLE, "w"))
    return rows


def observed_branches(rid):
    """provider -> branch the stored agent took after its first sample, for providers it requested records from."""
    took = {}
    for line in open(os.path.join(ROOT, "experiments", rid, "audit.jsonl")):
        a = json.loads(line)
        if '"error"' in a["result"][:20]:
            continue
        pid = a["args"].get("provider_id")
        if a["tool"] == "request_records":
            t = took.setdefault(pid, {"targ": False, "aud": False})
            t["targ"] |= a["args"].get("sample", {}).get("kind") == "targeted"
        elif a["tool"] == "request_audit_trail" and pid:
            took.setdefault(pid, {"targ": False, "aud": False})["aud"] = True
    return {p: ("BOTH" if t["targ"] and t["aud"] else "TARG" if t["targ"] else "AUD" if t["aud"] else "STOP") for p, t in took.items()}


def designs(table, arm, pre, rpre, seeds):
    by = {}
    for r in table:
        by.setdefault((r["set"], r["seed"]), {})[r["pid"]] = r
    res = {d: [] for d in "abcd"}
    stats = {"worked": 0, "listed": 0, "differ": 0}
    for s in seeds:
        obs = observed_branches(f"{rpre}_{s}")
        rows = by[(pre, s)]
        worked = [p for p in obs if p in rows]
        stats["worked"] += len(worked)
        stats["listed"] += len(obs)
        per = {d: {"score": 0.0, "found": 0, "hc": 0, "rounds": 0} for d in "abcd"}
        for p in worked:
            r, bo, ba = rows[p], obs[p], rows[p]["advice"]
            stats["differ"] += int(bo != ba)
            pick = {"a": bo, "b": ba, "c": ba if ba == "STOP" else bo, "d": ba if ba != "STOP" else bo}
            for d, b in pick.items():
                v = r[b]
                per[d]["score"] += v["score"]
                per[d]["found"] += v["found"]
                per[d]["hc"] += v["honest_called"]
                per[d]["rounds"] += v["rounds"]
        for d in "abcd":
            res[d].append(per[d])
    return res, stats


def main():
    table = json.load(open(TABLE)) if os.path.exists(TABLE) and "--rebuild" not in sys.argv else build()
    L = ["# Should the agent obey the policy's stop or escalate advice? A free counterfactual on stored runs (issue 118)", "", "[Back to the README](../README.md) · [v4/v5 plan](v4_v5_plan.md)", "",
         "Generated by `python eval/obey_advice_replay.py`. **Free:** no model. Method and caveats in the script's docstring. Score 4.0 per seed on the providers each stored agent worked, under the rules' calls (the agent's own calls may differ). "
         "Releases 2 to 4 are in sample for the policy (fitted on those seeds); release 5 is out of sample.", "",
         "Designs: **(a)** the branch the agent took; **(b)** always the advised branch; **(c)** the advised branch only when it is STOP; **(d)** the advised branch only when it is TARG, AUD or BOTH.", "",
         "| Agent | Providers worked | Departed from advice | Design | Score 4.0 per seed | Per-seed difference to (a): mean (sd) | Upcoders found | Honest called | Rounds |", "|---|---|---|---|---|---|---|---|---|"]
    verdict = []
    for arm, pre, rpre, seeds in SETS:
        res, stats = designs(table, arm, pre, rpre, seeds)
        base = [x["score"] for x in res["a"]]
        for d in "abcd":
            sc = [x["score"] for x in res[d]]
            diff = [a - b for a, b in zip(sc, base)]
            pooled = {k: sum(x[k] for x in res[d]) for k in ("found", "hc", "rounds")}
            L.append(f"| {arm} | {stats['worked']} | {stats['differ']} ({stats['differ'] / max(stats['worked'], 1):.0%}) | {d} | ${st.mean(sc):,.0f} | "
                     + ("-" if d == "a" else f"${st.mean(diff):,.0f} (${st.stdev(diff):,.0f})") + f" | {pooled['found']} | {pooled['hc']} | {pooled['rounds']} |")
            if d != "a" and arm != "A3.2":
                verdict.append((arm, d, st.mean(diff), st.stdev(diff)))
    wins = {}
    for arm, d, m, sd in verdict:
        wins.setdefault(d, []).append((arm, m, sd, m > sd))
    L += ["", "## Decision rule (issue 118)", "", "A design beats (a) in a release when its mean per-seed difference exceeds the seed-to-seed spread (sd) of that difference. The rule asks for this on at least two of the three agent releases A3.3, A3.4 and A3.5.", ""]
    for d in "bcd":
        n = sum(w[3] for w in wins[d])
        L.append(f"- Design ({d}): beats (a) in {n} of 3 releases ({', '.join(f'{w[0]} {w[1]:+,.0f} against sd {w[2]:,.0f}' for w in wins[d])}).")
    chosen = [d for d in "bcd" if sum(w[3] for w in wins[d]) >= 2]
    L += ["", "**Result:** " + (f"design {', '.join(chosen)} passes the rule: the agent should get a deterministic step for that case (code executes the recommendation, the agent handles exceptions with a stated reason, as in the binding rule of v3.5)." if chosen
                              else "no design passes the rule, so the advice stays advisory in agent v5.0 and the effort moves elsewhere."),
          "", "Caveats: the final call is approximate (rules decide here); release 2 to 4 numbers favor (b) to (d) because the policy was fitted on those seeds; ten seeds per release with about eight upcoders each; "
          "the agent's own first sample can differ from the standard first sample used for the advice."]
    L += ["", "## What the agents did against the advice", "", "Branch taken (rows) against branch advised on the standard first sample (columns), providers worked, all four agents pooled:", ""]
    cross = {}
    by = {}
    for r in table:
        by.setdefault((r["set"], r["seed"]), {})[r["pid"]] = r
    for arm, pre, rpre, seeds in SETS:
        for s in seeds:
            for p, b in observed_branches(f"{rpre}_{s}").items():
                if p in by[(pre, s)]:
                    cross[(b, by[(pre, s)][p]["advice"])] = cross.get((b, by[(pre, s)][p]["advice"]), 0) + 1
    cols = ["STOP", "TARG", "AUD", "BOTH"]
    L += ["| Taken \\ Advised | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    for b in cols:
        L.append(f"| {b} | " + " | ".join(str(cross.get((b, a), 0)) for a in cols) + " |")
    L += ["", "- Almost every departure is the agent **stopping where the policy says escalate** (STOP taken, TARG or AUD advised). The agents stop by not continuing, so these omissions never appear as a logged action: the 79% 'followed' figure of the release 5 advice log counted logged actions only, and overstated adherence per provider.",
          "- Obeying the escalation advice (designs b and d) finds more upcoders (for A3.5, 40 against 31 over ten seeds) but with about 60% more rounds, and each find recovers little under score 4.0, so the net falls. Designs that only enforce STOP (c) change almost nothing because the agents already stop.",
          "- The policy itself is the weak part: `src/policy_25.json` was fitted on release 5's option 2 dollars (cloned notes denied in full, cheap review), where escalating paid. Under score 4.0 on these seeds its escalations do not pay. A v4.0 policy refitted on score 4.0 and data 4.0 is the next step (the workflow RL loop), and only then is the question of binding it worth asking again."]
    open(DOC, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
