"""Records-request budget sweep, offline and free (issue 48). No model: records come from the simulated office with the fixed policy
(a random request for 30 charts, one follow-up), and a provider is "called" when the deterministic rules say upcoding (the chart rule or the
summary rules). For each ordering of providers (the screen's z_adj, the workflow's combined rank, the claims-only priority score) and each
budget B (5, 10, 15, 25 providers asked), report recall, precision and the area under the precision-recall curve as B grows.

The ordering is chosen on the development seed (42); the other datasets validate. Writes docs/budget_sweep.md.

Usage:
    python eval/budget_sweep_offline.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent_tools as at  # noqa: E402
import priority_analysis as pa  # noqa: E402
import summary_rules as sr  # noqa: E402

BUDGETS = [5, 10, 15, 25]
ORDERINGS = {"z_adj (the screen's score)": "z_adj (the screen's score)", "combined rank (workflow top 25)": "combined rank (workflow top 25)",
             "priority (rank average of ratio and excess claims)": "priority: rank average of ratio and excess claims"}


def decide(env, pid):
    """The deterministic decision after the fixed records policy: True when the rules say upcoding."""
    r = env.request_records(pid, {"kind": "random", "n": 30}, 30)
    if r.get("deficiencies") and r.get("rounds_left", 0) > 0:
        env.follow_up_records(pid, [d["code"] for d in r["deficiencies"]])
    env.close_records(pid, "offline sweep")
    return bool(env._chart_rule(pid)["triggered"] or sr.rule_leaning(env._packet(pid))[0] == sr.UPCODING)


def aurc(recalls):
    """Area under the recall-versus-budget curve (mean recall over budgets 1..25): rewards finding upcoders early, which AUPRC cannot see
    when every call is correct."""
    return sum(recalls) / len(recalls)


def ap_of(order, up):
    tp, s = 0, 0.0
    for k, p in enumerate(order, 1):
        if p in up:
            tp += 1
            s += tp / k
    return s / len(up)


def evidence_scores(env, order, prior_rank):
    """Continuous deterministic scores for providers already examined: the claims prior, the shrunk chart rate, and a rank average of both."""
    chart = {}
    for p in order:
        c = env._chart_rule(p)
        n, below = c["charts"], c["below_billed"]
        chart[p] = (below + 0.06 * 8) / (n + 8)                 # shrink toward the typical rate so a few charts cannot dominate
    def ranks(sc):
        o = sorted(order, key=lambda p: -sc[p])
        return {p: i for i, p in enumerate(o)}
    rp, rc = ranks({p: -prior_rank[p] for p in order}), ranks(chart)
    return {"claims prior": {p: -prior_rank[p] for p in order}, "chart evidence (shrunk rate)": chart,
            "prior + chart evidence (rank average)": {p: -(rp[p] + rc[p]) / 2 for p in order}}


def auprc(points):
    """Sum over budgets of (recall gained) x (precision), the average-precision form of the area under the precision-recall curve."""
    area, prev = 0.0, 0.0
    for rec, prec in points:
        area += (rec - prev) * prec
        prev = rec
    return area


def main():
    rows, evrows = [], []
    for label, code, dev in pa.DATASETS:
        feats = pa.features(code)
        truth = {p: v["role"] == "upcoder" for p, v in json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))["providers"].items()}
        up = {p for p, v in truth.items() if v}
        data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
        orders = {name: sorted(pa.SCORES[key](feats), key=lambda p: -pa.SCORES[key](feats)[p])[:25] for name, key in ORDERINGS.items()}
        env = at.Environment(data, os.path.join(data, "view"), seed=1, records_budget=100)
        called = {p: decide(env, p) for p in sorted({p for o in orders.values() for p in o})}
        prio = pa.SCORES["priority: rank average of ratio and excess claims"](feats)
        pr_order = orders["priority (rank average of ratio and excess claims)"]
        ev = evidence_scores(env, pr_order, {p: i for i, p in enumerate(pr_order)})
        for ename, esc in ev.items():
            evrows.append((label, ename, ap_of(sorted(pr_order, key=lambda p: -esc[p]), up)))
        for name, order in orders.items():
            pts, cells, recs = [], {}, []
            for B in range(1, 26):
                sel = [p for p in order[:B] if called[p]]
                tp = sum(p in up for p in sel)
                rec, prec = tp / len(up), (tp / len(sel) if sel else 1.0)
                pts.append((rec, prec))
                recs.append(rec)
                if B in BUDGETS:
                    cells[B] = (rec, tp / len(sel) if sel else float("nan"), len(sel))
            rows.append((label, name, auprc(pts), cells, aurc(recs)))
    out = ["# Records budget sweep (offline, no model)", "",
           "Generated by `python eval/budget_sweep_offline.py`. Each provider is asked for charts with the fixed policy and called when the deterministic rules say upcoding. "
           "**AUPRC** is the area under the precision-recall curve as the budget grows from 1 to 25 providers asked (higher is better). Cells: `recall / precision (calls)` "
           "at a budget of 5, 10, 15, 25. The ordering was chosen on seed 42; other datasets validate. 8 upcoders per 216 providers (3 to 12 in the 600-provider sets).", ""]
    for label, _, _ in pa.DATASETS:
        out += [f"## {label}", "", "| Ordering | AURC | AUPRC | budget 5 | budget 10 | budget 15 | budget 25 |", "|---|---|---|---|---|---|---|"]
        for l, name, a, cells, ar in rows:
            if l == label:
                out.append(f"| {name} | {ar:.2f} | {a:.2f} | " + " | ".join(f"{cells[b][0]:.2f} / {cells[b][1]:.2f} ({cells[b][2]})" for b in BUDGETS) + " |")
        out.append("")
    out += ["## Mean AURC (recall found early) and AUPRC", "", "| Ordering | AURC seed 42 (chosen on) | AURC mean of the other six | AUPRC seed 42 | AUPRC mean of the other six |", "|---|---|---|---|---|"]
    for name in ORDERINGS:
        d0 = [(a, ar) for l, n, a, _, ar in rows if n == name and l == pa.DATASETS[0][0]][0]
        oth = [(a, ar) for l, n, a, _, ar in rows if n == name and l != pa.DATASETS[0][0]]
        out.append(f"| {name} | {d0[1]:.2f} | {sum(x[1] for x in oth) / len(oth):.2f} | {d0[0]:.2f} | {sum(x[0] for x in oth) / len(oth):.2f} |")
    out += ["", "AUPRC cannot tell the orderings apart here because every call the deterministic rules make is correct (precision 1.0), so the area equals the final recall; "
            "AURC (mean recall over budgets 1 to 25) shows which ordering finds upcoders earlier.", "",
            "## Ranking the providers already asked: which evidence ranks upcoders best (average precision over the 25 asked, priority ordering)", "",
            "| Score used to decide whom to call | AP seed 42 | mean AP, other six |", "|---|---|---|"]
    for ename in dict.fromkeys(n for _, n, _ in evrows):
        d0 = [a for l, n, a in evrows if n == ename and l == pa.DATASETS[0][0]][0]
        oth = [a for l, n, a in evrows if n == ename and l != pa.DATASETS[0][0]]
        out.append(f"| {ename} | {d0:.2f} | {sum(oth) / len(oth):.2f} |")
    open(os.path.join(ROOT, "docs", "budget_sweep.md"), "w").write("\n".join(out) + "\n")
    print("\n".join(out[-6:]))


if __name__ == "__main__":
    main()
