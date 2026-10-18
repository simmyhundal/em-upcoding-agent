"""Issue 61: analyse the multi-seed paired evaluation with the decision rules fixed before any run (posted on the issue).

Reads experiments/runs.json and experiments/results.csv (run `python eval/scoreboard.py --write` first) and writes docs/eval61.md.

Primary metric: upcoders found per seed on the ten 3.7% datasets. Comparisons are paired by seed: mean difference with a 95% percentile
bootstrap interval over seeds (10,000 resamples, random seed 61). A gap is "confirmed" when the interval excludes zero.
Decision (fixed in advance):
- The agent (v3.1) becomes the main line if A3.1 - W2.1 is confirmed above zero, A3.1 accuses at most one more honest doctor than W2.1
  in total over the ten seeds, and A3.1's precision over the ten seeds is at least 80%. Otherwise the workflow (v2.1) is the main line.
  The agent stays in development either way.
- An upgrade (W2.1 over W2.0, A3.1 over A3.0) "helped" if its gap is confirmed above zero with at most one more false accusation in total,
  "hurt" if confirmed below zero, and otherwise "no detectable change".
The low-base-rate datasets (one seed each) are descriptive only.

Usage:
    python eval/analyze_eval61.py
"""
import csv
import glob
import json
import os
import random
import sys

import eval61_recovery as rec61

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "eval"))
ARMS = ["W2.0", "W2.1", "A3.0", "A3.1"]
PAIRS = [("A3.1", "W2.1", "agent v3.1 vs workflow v2.1 (which stream is the main line)"),
         ("W2.1", "W2.0", "workflow upgrade: v2.1 vs v2.0"),
         ("A3.1", "A3.0", "agent upgrade: v3.1 vs v3.0"),
         ("A3.0", "W2.0", "replication of the Milestone 6 comparison: v3.0 vs v2.0")]


def arm_of(run, row):
    v = run.get("version") or ("v3.0" if run["kind"] == "agent" else "v2.0")
    return ("A" if run["kind"] == "agent" else "W") + v[1:]


def cost(rid):
    d = os.path.join(ROOT, "experiments", rid)
    usd = sum(json.loads(line).get("estimated_usd", 0) for f in glob.glob(os.path.join(d, "usage_*.jsonl")) for line in open(f) if line.strip())
    p = os.path.join(d, "agent_run.json")
    if os.path.exists(p):
        a = json.load(open(p))
        usd += a.get("estimated_usd", 0) + a.get("model_spend_in_tools_usd", 0)
    return usd


def load():
    reg = json.load(open(os.path.join(ROOT, "experiments", "runs.json")))
    rows = {(r["run_id"], r["stage"]): r for r in csv.DictReader(open(os.path.join(ROOT, "experiments", "results.csv")))}
    out = {}
    for run in reg["runs"]:
        key = run["dataset"]
        if not key.startswith("e"):
            continue
        row = rows.get((run["run"], "Agent" if run["kind"] == "agent" else "AI"))
        if not row:
            continue
        arm = arm_of(run, row)
        found = int(row["fn_total"]) - int(row["fn_missed"])
        out[(key, arm)] = {"run": run["run"], "code": reg["datasets"][key]["flagged"].split("/")[1], "overpaid": int(row["overpaid_usd"] or 0), "reached": int(row["reached_usd"] or 0), "found": found, "upcoders": int(row["fn_total"]),
                           "accused": int(row["fp_count"] or 0), "precision": row["precision"],
                           "honest_requested": int(row["honest_requested"] or 0), "rounds_honest": int(row["request_rounds_honest"] or 0),
                           "usefulness": row["usefulness"], "usefulness_rules": row["usefulness_rules"], "cost": cost(run["run"])}
    return out


def bootstrap(diffs, n=10000, seed=61):
    rng = random.Random(seed)
    means = sorted(sum(rng.choice(diffs) for _ in diffs) / len(diffs) for _ in range(n))
    return sum(diffs) / len(diffs), means[int(0.025 * n)], means[int(0.975 * n) - 1]


R2_SEEDS = [1515, 1616, 1717, 1818, 1919, 2020, 2121, 2222, 2323, 2424]
R2_ARMS = [("W2.2", "r2w", "Opus 5.5 (Batch API), only where the rules were silent; no effort setting"),
           ("A3.2", "r2a", "Opus 5.5, low effort")]


def release2_lines():
    """Release 2 (data 2.2) arms, ten seeds, in the same columns as the release 1 table. Free: stored runs only. Data 2.2 differs from 2.1
    (honest coding noise, group billing, payer-based upcoder definition), so these rows are NOT directly comparable to the release 1 rows."""
    import csv as _csv
    rows = []
    for arm, pre, how in R2_ARMS:
        f = up = acc = hr = rh = 0
        usd = est = total = 0.0
        unrel = estd = 0
        for seed in R2_SEEDS:
            rid, code = f"{pre}_{seed}", f"r2_{seed}"
            d = os.path.join(ROOT, "experiments", rid)
            if not os.path.exists(os.path.join(d, "case_summaries_checked.jsonl")):
                break
            key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))
            roles = key["providers"]
            called = {x["provider_id"] for x in map(json.loads, open(os.path.join(d, "case_summaries_checked.jsonl")))
                      if x["summary"]["leaning"] == "pattern_consistent_with_upcoding"}
            f += sum(roles[p]["role"] == "upcoder" for p in called)
            acc += sum(roles[p]["role"] != "upcoder" for p in called)
            up += sum(v["role"] == "upcoder" for v in roles.values())
            per = {}
            for line in open(os.path.join(d, "office_transcript.jsonl")) if os.path.exists(os.path.join(d, "office_transcript.jsonl")) else []:
                e = json.loads(line)
                if e.get("action") in ("send_request", "follow_up") and "error" not in e:
                    per[e["provider_id"]] = per.get(e["provider_id"], 0) + 1
            hr += sum(roles[p]["role"] != "upcoder" for p in per)
            rh += sum(n for p, n in per.items() if roles[p]["role"] != "upcoder")
            usd += cost(rid)
            r = rec61.recover(rid, code)
            est += r["est"]
            unrel += r["unreliable"]
            estd += r["estimated"]
            just = key["justified_cpt_by_claim"]
            fees = rec61.allowed()
            for c in _csv.DictReader(open(os.path.join(ROOT, "data", f"synthetic_v2_{code}", "view", "claims.csv"))):
                j = just.get(c["claim_id"])
                if j and c["cpt"] > j and roles[c["provider_id"]]["role"] == "upcoder":
                    a, pd = float(c["allowed_amount"]), float(c["paid_amount"])
                    total += max(a - fees[j], 0.0) * (pd / a if a else 0.8)
        else:
            n = len(R2_SEEDS)
            prec = f"{f / (f + acc):.0%}" if f + acc else "–"
            rows.append(f"| {arm} | {how} | {f} of {up} | {f / up:.0%} | {acc} | {prec} | {hr} | {rh} | {hr / f:.1f} | ${usd:.2f} | ${usd / n:.2f} | "
                        f"${est:,.0f} | ${total:,.0f} | {est / total:.0%} | {unrel}/{estd} |")
    if not rows:
        return []
    return ["", "## Release 2 arms on data 2.2 (ten seeds, 1515 to 2424)", "",
            "Same columns as the table above. **Data 2.2 is harder and different** (honest coding noise of about 8%, an upcoder defined by true rate above the honest 95th percentile "
            "and at least 6 points over the honest mean, group billing, 8 planted upcoders and 8 hard negatives per seed), so compare arms within this table, not across to release 1. "
            "Screen: `eb_ratio`, top 5% of 216 doctors. Judge: rule judge j3.2 only (no LLM judge, so no usefulness columns). Seeds 1515 and 2424 each have one honest doctor called.", "",
            "| Arm | Model and effort | Upcoders found | Recall | Honest doctors accused | Precision | Honest practices sent requests | Request rounds on honest | "
            "Requests to honest per upcoder found | Cost | Cost per run | Estimated recovery from accused providers | Total recoverable from all upcoders | Share recovered | "
            "Unreliable estimates |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"] + rows + [
            "", "Paired result on these ten seeds: workflow found 10 upcoders the agent missed and the agent 1 the workflow missed (exact McNemar p = 0.012; with the design effect of 1.5 for "
            "seed clusters, p = 0.027). This was an unplanned look at 10 seeds (the pre-registered looks were 22 and 44 seeds, alpha 0.0294); Simmy chose to stop at 10 and conclude "
            "the workflow is stronger, to save cost. Full table and the rule: `docs/release2_results.md`."]


def main():
    res = load()
    main_keys = sorted({k for k, _ in res if "_r" not in k}, key=lambda k: int(k[1:]))
    low_keys = sorted({k for k, _ in res if "_r" in k})
    complete = [k for k in main_keys if all((k, a) in res for a in ARMS)]
    lines = ["# Issue 61: multi-seed paired evaluation", "",
             "Generated by `python eval/analyze_eval61.py`. Decision rules were fixed and posted on issue 61 before any evaluation run. "
             f"Seeds with all four arms: {len(complete)} of {len(main_keys)}.", "",
             "Arms: **W2.0** frozen workflow (provider office 2.0, screen suspicion >= 5, fixed office policy), **W2.1** workflow v2.1, "
             "**A3.0** frozen agent, **A3.1** agent v3.1. Data 2.1 for every seed (the frozen arms read only the 2.0 part, which is identical).", "",
             "## Per arm, ten seeds at 3.7% upcoders (8 of 216 each)", "",
             "| Arm | Upcoders found | Recall | Honest doctors accused | Precision | Honest practices sent requests | Request rounds on honest | "
             "Requests to honest per upcoder found | Usefulness (LLM judge) | Usefulness (rule judge) | Cost | Cost per run | "
             "Estimated recovery from accused providers | Total recoverable from all upcoders | Share recovered |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    tot, unrel, chk = {}, {}, {}
    for a in ARMS:
        rs = [res[(k, a)] for k in complete]
        if not rs:
            continue
        f, up, acc = sum(r["found"] for r in rs), sum(r["upcoders"] for r in rs), sum(r["accused"] for r in rs)
        hr, rh = sum(r["honest_requested"] for r in rs), sum(r["rounds_honest"] for r in rs)
        prec = f / (f + acc) if f + acc else None
        vals = lambda key: [float(r[key]) for r in rs if r[key] not in ("", None)]
        mean = lambda key: f"{sum(vals(key)) / len(vals(key)):.2f}" if vals(key) else "–"      # "–": no run had that judge (release 2: no LLM judge)
        tot[a] = {"found": f, "accused": acc, "precision": prec}
        rc = [rec61.recover(r["run"], r["code"]) for r in rs]
        est, total = sum(x["est"] for x in rc), sum(r["overpaid"] for r in rs)
        money = (f"{sum(x['unreliable'] for x in rc)}/{sum(x['estimated'] for x in rc)}", f"${est:,.0f}", f"${total:,.0f}", f"{est / total:.0%}")
        cost_tot = sum(r["cost"] for r in rs)
        lines.append(f"| {a} | {f} of {up} | {f / up:.0%} | {acc} | {'–' if prec is None else f'{prec:.0%}'} | {hr} | {rh} | "
                     f"{hr / f:.1f} | {mean('usefulness')} | {mean('usefulness_rules')} | ${cost_tot:.2f} | ${cost_tot / len(rs):.2f} | "
                     f"{money[1]} | {money[2]} | {money[3]} |"
                     if f else f"| {a} | 0 of {up} | 0% | {acc} | – | {hr} | {rh} | – | – | – | ${cost_tot:.2f} | ${cost_tot / len(rs):.2f} | {money[1]} | {money[2]} | {money[3]} |")
        unrel[a] = money[0]
        chk[a] = est / sum(r["reached"] for r in rs) if sum(r["reached"] for r in rs) else None
    lines += ["", "**Recall** is upcoders found divided by upcoders planted. **Cost per run** is the arm's total cost divided by its ten runs. "
              "**Estimated recovery** is what the extrapolation tool (`src/pi_estimate.py`, the arithmetic behind the agent's `estimate_overpayment`) would estimate if run on every provider "
              "the arm accused, using the random charts the office returned for that provider (point estimate, negative estimates count as zero; honest doctors the arm accused are included). "
              "**Total recoverable** is what upcoders were paid above the justified levels (answer key), the same for every arm because the data is the same; **Share recovered** divides the two. "
              "Read these as upper-bound arithmetic, not recovered money: charts are read by a simulated reviewer with coder noise, a provider with no random charts adds nothing, and estimates "
              "from few charts are unreliable (accused providers with fewer than 8 charts in the main stratum, as the agent tool counts: "
              + ", ".join(f"{a} {unrel[a]}" for a in ARMS if a in unrel) + "). Check against the truth: the estimate is "
              + ", ".join(f"{chk[a]:.0%} ({a})" for a in ARMS if chk.get(a)) + " of the dollars actually sitting with the upcoders each arm called, so the extrapolation tends to fall short rather than overshoot. "
              "Method and code: `eval/eval61_recovery.py`.",
              "", "## Paired comparisons (upcoders found per seed)", "",
              "| Comparison | Mean difference per seed | 95% interval | Verdict | Extra honest doctors accused (total) |", "|---|---|---|---|---|"]
    verdicts = {}
    for a, b, label in PAIRS:
        ks = [k for k in complete]
        if not ks:
            continue
        diffs = [res[(k, a)]["found"] - res[(k, b)]["found"] for k in ks]
        m, lo, hi = bootstrap(diffs)
        extra = tot[a]["accused"] - tot[b]["accused"]
        if lo > 0 and extra <= 1:
            v = "helped" if b != "W2.1" else "agent ahead"
        elif hi < 0:
            v = "hurt" if b != "W2.1" else "workflow ahead"
        else:
            v = "no detectable change" if b != "W2.1" else "no confirmed gap"
        if a == "A3.1" and b == "W2.1" and lo > 0 and extra > 1:
            v = "agent finds more but accuses more: not confirmed"
        verdicts[(a, b)] = (lo, hi, extra)
        lines.append(f"| {label} | {m:+.2f} | {lo:+.2f} to {hi:+.2f} | {v} | {extra:+d} |")
    if ("A3.1", "W2.1") in verdicts and "A3.1" in tot:
        lo, hi, extra = verdicts[("A3.1", "W2.1")]
        p = tot["A3.1"]["precision"]
        agent_main = lo > 0 and extra <= 1 and p is not None and p >= 0.8
        lines += ["", f"**Decision (rule fixed in advance):** {'the agent (v3.1) becomes the main line' if agent_main else 'the workflow (v2.1) stays the main line'}; "
                  "the agent stays in development either way."]
    lines += ["", "## Upcoders found by kind of notes (ten seeds, 40 of each)", "",
              "Half the planted upcoders clone their notes so the charts match the bill; the data 2.1 note package plants signals of that "
              "(generated, so easier than real notes).", "", "| Arm | Cloned-notes upcoders found | Honest-notes upcoders found |", "|---|---|---|"]
    reg = json.load(open(os.path.join(ROOT, "experiments", "runs.json")))
    for a in ARMS:
        cf = ca = hf = ha = 0
        for k in complete:
            rid = res[(k, a)]["run"]
            key = json.load(open(os.path.join(ROOT, reg["datasets"][k]["truth"])))["providers"]
            called = {x["provider_id"] for x in map(json.loads, open(os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")))
                      if x["summary"]["leaning"] == "pattern_consistent_with_upcoding"}
            for p, v in key.items():
                if v["role"] == "upcoder":
                    if v.get("clones_notes"):
                        ca, cf = ca + 1, cf + (p in called)
                    else:
                        ha, hf = ha + 1, hf + (p in called)
        lines.append(f"| {a} | {cf} of {ca} | {hf} of {ha} |")
    if low_keys:
        lines += ["", "## Low base rates (one seed each, descriptive only)", "",
                  "| Dataset | Arm | Upcoders found | Honest doctors accused | Precision | Cost |", "|---|---|---|---|---|---|"]
        for k in low_keys:
            for a in ARMS:
                r = res.get((k, a))
                if r:
                    lines.append(f"| {k} | {a} | {r['found']} of {r['upcoders']} | {r['accused']} | {r['precision'] or '–'} | ${r['cost']:.2f} |")
    lines += ["", f"Total estimated cost of these runs: ${sum(r['cost'] for r in res.values()):.2f}.", "",
              "Per-seed rows are in `experiments/results.csv` and `docs/results.md`; run folders under `experiments/`."]
    lines += release2_lines()
    out = os.path.join(ROOT, "docs", "eval61.md")
    open(out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
