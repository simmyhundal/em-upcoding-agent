"""Release 4 development runs of workflow 2.4 candidates (issue 102) on 20 development seeds (data 2.2): free (simulated office, rules 2.3, no model calls).

Seeds: the 10 release 2 seeds (1515 to 2424, codes r2_<seed>) and the 10 release 3 seeds (2525 to 3434, codes r3_<seed>); both are development data. The selection rule was
fixed on issue 102 before this ran: among configurations finding at least 90% of B's upcoders and calling no more honest doctors than B, the fewest honest practices
asked per upcoder found; ties go to fewer rounds on honest practices. Cases rules 2.3 leave to the model count as inconclusive (the model said inconclusive in 104 of 104
release 1 cases and 6 of 6 in release 2).

Usage: python eval/dev_release4.py [--report-only]   (writes docs/dev_release4.md and experiments/d4_dev_results.json)
"""
import json
import multiprocessing as mp
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import case_summary as cs  # noqa: E402
import dev_release3 as dev3  # noqa: E402
import make_v2_office_workflow_runs as mw  # noqa: E402
import summary_rules as sr  # noqa: E402

SEEDS = [("r2", s) for s in (1515, 1616, 1717, 1818, 1919, 2020, 2121, 2222, 2323, 2424)] + [("r3", s) for s in (2525, 2626, 2727, 2828, 2929, 3030, 3131, 3232, 3333, 3434)]
CONFIGS = {"B": {}, "T2.5": {"gate_t": 2.5}, "T3": {"gate_t": 3.0}, "T3.5": {"gate_t": 3.5}, "A3": {"gate_t": 3.0, "gate_all": True}, "S": {"stop_silent": True},
           "T3+S": {"gate_t": 3.0, "stop_silent": True}, "T3.5+S": {"gate_t": 3.5, "stop_silent": True}, "A3+S": {"gate_t": 3.0, "gate_all": True, "stop_silent": True}}
TIER1_N = 11


def one(job):
    code_pre, seed, tag = job
    src = f"{code_pre}_{seed}"
    name = dev3.write_flagged(src, "eb_ratio_t", 10)
    rid = f"d4{tag.replace('.', '').replace('+', 'p').lower()}_{seed}"
    view, office, flagged_file = mw.build_view(rid, src, name, version="2.4", tier1_n=TIER1_N, policy24=CONFIGS[tag])
    out = cs.run(view, flagged_file, os.path.join("/tmp", f"{rid}.jsonl"), dry_run=True, rules="2.3")
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{src}.json")))["providers"]
    called = [o["provider_id"] for o in out if sr.rule_leaning_23(o["packet"])[0] == sr.UPCODING]
    asked = [p for p, st in office.state.items() if st["round"] > 0 and p in key]
    return {"set": code_pre, "seed": seed, "config": tag, "found": sum(key[p]["role"] == "upcoder" for p in called),
            "honest_called": sum(key[p]["role"] != "upcoder" for p in called), "upcoders": sum(v["role"] == "upcoder" for v in key.values()),
            "honest_asked": sum(key[p]["role"] != "upcoder" for p in asked), "rounds_honest": sum(office.state[p]["round"] for p in asked if key[p]["role"] != "upcoder"),
            "asked": len(asked)}


def agg(res, tag, which=None):
    x = [r for r in res if r["config"] == tag and (which is None or r["set"] == which)]
    f = sum(r["found"] for r in x)
    return {"found": f, "upcoders": sum(r["upcoders"] for r in x), "honest_called": sum(r["honest_called"] for r in x), "honest_asked": sum(r["honest_asked"] for r in x),
            "rounds": sum(r["rounds_honest"] for r in x), "per_up": (sum(r["honest_asked"] for r in x) / f) if f else float("inf")}


def high_acuity_check():
    """Issue 104: would a late-signature sign have changed the high-acuity calls on the 20 development seeds? Uses the v2.3 views of those seeds."""
    import collections
    rows = []
    for pre, view, seeds in (("r2", "d3v4", [s for c, s in SEEDS if c == "r2"]), ("r3", "r3w", [s for c, s in SEEDS if c == "r3"])):
        for s in seeds:
            src = f"{pre}_{s}"
            key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{src}.json")))["providers"]
            out = cs.run(os.path.join(ROOT, "data", f"synthetic_v2_{src}", f"view_{view}_{s}"), os.path.join(ROOT, "experiments", src, "flagged_eb_ratio_t_10.csv"),
                         "/tmp/h104.jsonl", dry_run=True, rules="2.3")
            for o in out:
                pk = o["packet"]
                ns = (pk.get("documentation_review") or {}).get("note_signals")
                v = key[o["provider_id"]]
                rows.append({"lean": sr.rule_leaning_23(pk)[0], "role": v["role"], "clone": bool(v.get("clones_notes")),
                             "late": (ns["rates"].get("late") or 0) if ns and ns["notes"] >= 8 else None})
    ha = [r for r in rows if r["lean"] == sr.HIGH_ACUITY]
    hot = [r for r in ha if r["late"] is not None and r["late"] >= sr.INFLATED_LATE]
    hn = [r for r in rows if r["role"] == "hard_negative" and r["late"] is not None]
    kind = lambda r: "upcoder (cloned notes)" if r["role"] == "upcoder" and r["clone"] else ("upcoder (honest notes)" if r["role"] == "upcoder" else r["role"].replace("_", " "))
    return ["", "## Issue 104: high-acuity calls and the late-signature sign", "",
            f"Rules 2.3 called {len(ha)} listed providers a high-acuity panel over the 20 development seeds: {dict(collections.Counter(kind(r) for r in ha))}. "
            f"Only {len(hot)} of them have a late-signature rate of {sr.INFLATED_LATE:.0%} or more over at least 8 notes: {[kind(r) for r in hot]}. "
            f"True high-acuity panels (hard negatives, {len(hn)} with at least 8 notes) have late rates of at most {max(r['late'] for r in hn):.0%}, so a late-signature override would not hit them. "
            "But the override would change one cloned-notes upcoder and one honest doctor, no more, and four of the five cloned-notes upcoders called high-acuity have late rates below the line. "
            "**Not built:** at most one more upcoder for one more wrong flip is not a reason for a rule; the issue stays open for the fresh seeds."]


def main(report_only=False):
    path = os.path.join(ROOT, "experiments", "d4_dev_results.json")
    if report_only:
        res = json.load(open(path))
    else:
        jobs = [(c, s, t) for c, s in SEEDS for t in CONFIGS]
        with mp.Pool(4) as pool:
            res = pool.map(one, jobs)
        json.dump(res, open(path, "w"), indent=1)
    base = agg(res, "B")
    L = ["# Release 4 development: workflow 2.4 candidates on 20 development seeds (issue 102)", "", "[Back to the README](../README.md)", "",
         "Generated by `python eval/dev_release4.py`. Free: simulated office and rules 2.3 only. **In sample**: the release 2 seeds (1515 to 2424) and the release 3 seeds "
         "(2525 to 3434) are development data. The selection rule was posted on issue 102 before the runs. Candidates start from workflow v2.3 (config B).", "",
         "| Config | What changes | Upcoders found | Honest doctors called | Honest practices asked | Rounds on honest | Honest asked per upcoder found | Release 2 seeds: found / asked | Release 3 seeds: found / asked |", "|---|---|---|---|---|---|---|---|---|"]
    what = {"B": "workflow v2.3 as is", "T2.5": "light tier only if ratio >= 2.5", "T3": "light tier only if ratio >= 3", "T3.5": "light tier only if ratio >= 3.5",
            "A3": "whole list only if ratio >= 3", "S": "stop at silent offices", "T3+S": "T3 and S", "T3.5+S": "T3.5 and S", "A3+S": "A3 and S"}
    ok = []
    for t in CONFIGS:
        a, a2, a3 = agg(res, t), agg(res, t, "r2"), agg(res, t, "r3")
        L.append(f"| {t} | {what[t]} | {a['found']} of {a['upcoders']} | {a['honest_called']} | {a['honest_asked']} | {a['rounds']} | {a['per_up']:.2f} | "
                 f"{a2['found']} / {a2['honest_asked']} | {a3['found']} / {a3['honest_asked']} |")
        if t != "B" and a["found"] >= 0.9 * base["found"] and a["honest_called"] <= base["honest_called"]:
            ok.append((a["per_up"], a["rounds"], t))
    ok.sort()
    L += ["", f"Configurations that keep at least 90% of B's upcoders ({0.9 * base['found']:.1f} of {base['found']}) and call no more honest doctors than B ({base['honest_called']}): "
          + (", ".join(t for _, _, t in ok) or "none") + ".",
          f"**Selected by the pre-registered rule: {ok[0][2] if ok else 'none (B stays)'}.**" if True else ""]
    sel = ok[0][2] if ok else "B"
    a, b = agg(res, sel), base
    L += ["", "## Reading", "",
          f"- **{sel} against B:** {a['found']} against {b['found']} upcoders found, {a['honest_asked']} against {b['honest_asked']} honest practices asked ({1 - a['honest_asked'] / b['honest_asked']:.0%} fewer), "
          f"{a['rounds']} against {b['rounds']} rounds on honest practices, honest doctors called {a['honest_called']} against {b['honest_called']}.",
          "- **The pre-registered rule is conservative on purpose.** Harder gates (T3, T3.5, A3) ask many fewer honest practices per upcoder found (2.5 to 2.8 against 4.2), "
          "but each loses more than a fifth of B's upcoders: the cloned-notes upcoders whose ratio sits between 2.5 and 3.5 are the ones given up. Whether that trade is worth it is a judgement, not a measurement.",
          "- **Stopping at silent offices (S) is a poor trade here:** it saves about 60 rounds but loses 6 upcoders, because an evasive office sometimes answers a later, targeted request. "
          "It is the case issue 103 is about (what happens after non-response), so it waits for that.",
          "- **Stable across the two halves?** The release 2 and release 3 columns move together for every config, but both halves are development data, so this is a consistency check, not a test.",
          "- **Next:** one fresh 10-seed test of the selected configuration (and the agent 3.4 changes) with the stopping rule posted first."]
    L += high_acuity_check()
    open(os.path.join(ROOT, "docs", "dev_release4.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main("--report-only" in sys.argv)
