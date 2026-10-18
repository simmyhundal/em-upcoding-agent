"""Release 3 development runs of workflow v2.3 on the ten release 2 seeds (data 2.2): free (simulated office, rules only, no model calls).

Those seeds are now DEVELOPMENT data for release 3 (the analysis of release 2 suggested the changes), so every number here is in sample; the test is a fresh
10-seed batch posted in advance. The variants add one change at a time so each step's gain and cost can be read separately:

  V0  workflow v2.2 as run in release 2 (stored)                                   eb_ratio top 5%,   policy 2.1,  rules 2.2
  V1  + rules 2.3 (late-signature / audit-trail signs)                             eb_ratio top 5%,   policy 2.1,  rules 2.3
  V2  + the test-line covariate in the screen                                      eb_ratio_t top 5%, policy 2.1,  rules 2.3
  V3  + audit-trail request also on late signatures (policy 2.3 tier 1 only)       eb_ratio_t top 5%, policy 2.3,  rules 2.3
  V4  + a wider list with a light tier for ranks 12 to 22                          eb_ratio_t top 10%, policy 2.3 tiers, rules 2.3 (the full W2.3)
  V5  V4 with the list taken straight from eb_ratio (no test-line covariate)       eb_ratio top 10%,  policy 2.3 tiers, rules 2.3

Where rules 2.3 leave a case to the model (notes claim data review the claims do not show, no late sign), the model said inconclusive in 104 of 104 release 1 cases
and 6 of 6 in release 2, so this free run counts those as inconclusive and reports how many there were.

Usage: python eval/dev_release3.py   (writes docs/dev_release3.md)
"""
import csv
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import case_summary as cs  # noqa: E402
import flagging  # noqa: E402
import make_v2_office_workflow_runs as mw  # noqa: E402
import summary_rules as sr  # noqa: E402

SEEDS = [1515, 1616, 1717, 1818, 1919, 2020, 2121, 2222, 2323, 2424]
NO_CHART_TEST = 1.0           # ALPHA_CHART_23 = 1: the chart-test step of rules 2.3 always passes (rules 2.3 as first built)
VARIANTS = [("V1", "eb_ratio", 5, "2.2", "2.3", NO_CHART_TEST), ("V1c", "eb_ratio", 5, "2.2", "2.3", None),
            ("V2", "eb_ratio_t", 5, "2.2", "2.3", None), ("V3", "eb_ratio_t", 5, "2.3", "2.3", None),
            ("V4n", "eb_ratio_t", 10, "2.3", "2.3", NO_CHART_TEST), ("V4", "eb_ratio_t", 10, "2.3", "2.3", None), ("V5", "eb_ratio", 10, "2.3", "2.3", None)]
TAGS = ("V0", "V1", "V1c", "V2", "V3", "V4n", "V4", "V5")


def write_flagged(src, method, pct):
    name = f"{method}_{pct}"
    path = os.path.join(ROOT, "experiments", src, f"flagged_{name}.csv")
    if not os.path.exists(path):
        rows = flagging.flag(os.path.join(ROOT, "data", f"synthetic_v2_{src}", "view"), method=method, top_pct=pct)
        cols = flagging.COLUMNS + ["screen_method", "screen_score"]
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
    return name


def run_variant(seed, tag, method, pct, policy, rules, alpha=None):
    saved = sr.ALPHA_CHART_23
    if alpha is not None:
        sr.ALPHA_CHART_23 = alpha
    try:
        return _run_variant(seed, tag, method, pct, policy, rules)
    finally:
        sr.ALPHA_CHART_23 = saved


def _run_variant(seed, tag, method, pct, policy, rules):
    src = f"r2_{seed}"
    name = write_flagged(src, method, pct)
    rid = f"d3{tag.lower()}_{seed}"
    tier1 = flagging.top_n_from_pct(216, 5)
    view, office, flagged_file = mw.build_view(rid, src, name, version=policy, tier1_n=tier1)
    out = cs.run(view, flagged_file, os.path.join("/tmp", f"{rid}.jsonl"), dry_run=True, rules=rules)
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{src}.json")))["providers"]
    called, asked_model = [], 0
    lean = sr.rule_leaning_23 if rules == "2.3" else sr.rule_leaning_22
    for o in out:
        l, _ = lean(o["packet"])
        asked_model += l is None
        if l == sr.UPCODING:
            called.append(o["provider_id"])
    asked = set(office.state)
    return {"seed": seed, "variant": tag, "found": sum(key[p]["role"] == "upcoder" for p in called), "honest_called": sum(key[p]["role"] != "upcoder" for p in called),
            "upcoders": sum(v["role"] == "upcoder" for v in key.values()), "honest_asked": sum(key[p]["role"] != "upcoder" for p in asked if p in key),
            "rounds_honest": sum(office.state[p]["round"] for p in asked if p in key and key[p]["role"] != "upcoder"), "model_cases": asked_model}


def stored_v0(seed):
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_r2_{seed}.json")))["providers"]
    called = [x["provider_id"] for x in map(json.loads, open(os.path.join(ROOT, "experiments", f"r2w_{seed}", "case_summaries_checked.jsonl")))
              if x["summary"]["leaning"] == "pattern_consistent_with_upcoding"]
    per = Counter()
    for line in open(os.path.join(ROOT, "experiments", f"r2w_{seed}", "office_transcript.jsonl")):
        e = json.loads(line)
        if e.get("action") in ("send_request", "follow_up") and "error" not in e:
            per[e["provider_id"]] += 1
    return {"seed": seed, "variant": "V0", "found": sum(key[p]["role"] == "upcoder" for p in called), "honest_called": sum(key[p]["role"] != "upcoder" for p in called),
            "upcoders": sum(v["role"] == "upcoder" for v in key.values()), "honest_asked": sum(key[p]["role"] != "upcoder" for p in per),
            "rounds_honest": sum(n for p, n in per.items() if key[p]["role"] != "upcoder"), "model_cases": 0}


def main(report_only=False):
    path = os.path.join(ROOT, "experiments", "d3_dev_results.json")
    if report_only:
        res = json.load(open(path))
    else:
        res = [stored_v0(s) for s in SEEDS]
        for s in SEEDS:
            for v in VARIANTS:
                print("seed", s, v[0], flush=True)
                res.append(run_variant(s, *v))
        json.dump(res, open(path, "w"), indent=1)
    L = ["# Release 3 development: workflow v2.3 on the release 2 seeds (data 2.2)", "", "[Back to the README](../README.md)", "",
         "Generated by `python eval/dev_release3.py`. Free: simulated office and rules only. **In sample**: these ten seeds (1515 to 2424) suggested the changes and are development data "
         "for release 3; a fresh 10-seed batch is the test. Each row adds one change to the row above it (V1c, V4n and V5 are side branches: V1c adds the chart test to V1, V4n is V4 without it, V5 swaps the screen).", "",
         "| Variant | What changes | Upcoders found (of 78) | Honest doctors called | Honest practices sent requests | Request rounds on honest | Cases left to the model |", "|---|---|---|---|---|---|---|"]
    what = {"V0": "workflow v2.2 as run in release 2", "V1": "+ rules 2.3 as first built (late-signature and audit-trail signs)",
            "V1c": "+ the chart test (an upcoding call from charts must beat the real peer rate, one-sided exact binomial 0.05)",
            "V2": "+ test-line covariate in the screen (`eb_ratio_t`)",
            "V3": "+ audit-trail request also on late signatures (policy 2.3)", "V4n": "V3 + top 10% list with a light tier for ranks 12 to 22, no chart test",
            "V4": "V3 + top 10% list with a light tier for ranks 12 to 22, with the chart test (**full W2.3**)",
            "V5": "V4 with plain `eb_ratio` as the screen"}
    for tag in TAGS:
        x = [r for r in res if r["variant"] == tag]
        L.append(f"| {tag} | {what[tag]} | {sum(r['found'] for r in x)} | {sum(r['honest_called'] for r in x)} | {sum(r['honest_asked'] for r in x)} | "
                 f"{sum(r['rounds_honest'] for r in x)} | {sum(r['model_cases'] for r in x) if tag != 'V0' else '–'} |")
    L += ["", "## Per seed (upcoders found / honest doctors called)", "", "| Seed | " + " | ".join(TAGS) + " |", "|---" * (len(TAGS) + 1) + "|"]
    for s in SEEDS:
        cells = []
        for tag in TAGS:
            r = next(r for r in res if r["seed"] == s and r["variant"] == tag)
            cells.append(f"{r['found']} / {r['honest_called']}")
        L.append(f"| {s} | " + " | ".join(cells) + " |")
    v = {t: [r for r in res if r["variant"] == t] for t in TAGS}
    tot = lambda t, k: sum(r[k] for r in v[t])
    L += ["", "## Reading the table", "",
          f"- **Rules 2.3 do most of the work:** {tot('V0', 'found')} to {tot('V1', 'found')} upcoders found on the same list, almost all cloned-notes upcoders (see `replay_rules_23.md`).",
          f"- **The chart test trades recall for precision:** V1c finds {tot('V1c', 'found')} against {tot('V1', 'found')} and calls {tot('V1c', 'honest_called')} honest doctors against {tot('V1', 'honest_called')}. "
          f"It matters more with the wider list: without it V4n calls {tot('V4n', 'honest_called')} honest doctors, with it V4 calls {tot('V4', 'honest_called')}. The 15% peer cap of rules 2.2 let honest doctors through on small samples.",
          f"- **The test-line covariate** adds {tot('V2', 'found') - tot('V1c', 'found')} upcoders on the narrow list and {tot('V4', 'found') - tot('V5', 'found')} on the wide one (V4 against V5). In sample, and the test-line signal is generated, so probably easier than real claims.",
          f"- **The audit-trail request on late signatures adds nothing** here (V3 against V2: {tot('V3', 'found')} against {tot('V2', 'found')}): once rules 2.3 read the late rate, the audit trail does not change a decision.",
          f"- **The wider list is a real trade.** V4 finds {tot('V4', 'found') - tot('V3', 'found')} more upcoders than V3 ({tot('V4', 'found')} against {tot('V3', 'found')}) and calls {tot('V4', 'honest_called') - tot('V3', 'honest_called')} more honest doctors, "
          f"but sends requests to {tot('V4', 'honest_asked')} honest practices against {tot('V3', 'honest_asked')} ({tot('V4', 'rounds_honest')} request rounds against {tot('V3', 'rounds_honest')}), roughly "
          f"{(tot('V4', 'honest_asked') - tot('V3', 'honest_asked')) / max(tot('V4', 'found') - tot('V3', 'found'), 1):.0f} extra honest practices bothered per extra upcoder found. That cost is the thing to decide on (issue 87).",
          "",
          "## Steps from the plan that were checked and not built", "",
          "- **Follow up on providers who sent nothing:** the four screened upcoders with no records on the release 2 runs were all evasive offices that had already been asked in rounds 1 to 4 (objection or no response each time). The simulated office never answers them; more asking changes nothing. What follows non-response is issue 68.",
          "- **A sample-size-aware test for the 'between the cutoffs' cases, against the 15% line:** adds 1 upcoder and 2 honest doctors. Rejected. The version that matters is the chart test above, against the real peer rate.",
          "- **Never let a 'high-acuity' call override a late signature:** one case in ten seeds (the other six high-acuity calls have late rates under 7%). Too little to separate from luck; not built.",
          "- **Other ways to use the same list size** (claims-only, in sample): mixing the top of `priority` or a 99214-and-up score into the list gave 44 to 46 of 78 against 47 for `eb_ratio_t` alone; an expected-level model for 99214 and 99215 together listed only 15 of 78 in the top 5%. Diagnosis counts and chronic-condition flags added nothing beyond the test-line covariate.", "",
          "## Not covered", "",
          "- Agent v3.3 is not built; the changes here are workflow v2.3 only (one-sided in the parity table, to be mirrored).",
          "- Model calls: 1 case of 220 was left to the model; the free run counts it as inconclusive.",
          "- Everything is in sample on data 2.2; the test is a fresh 10-seed batch."]
    open(os.path.join(ROOT, "docs", "dev_release3.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main("--report-only" in sys.argv)
