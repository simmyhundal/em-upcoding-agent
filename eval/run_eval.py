"""Eval harness: score each detector against ground truth and write a side-by-side report.

Detectors compared (all use the same top-N cutoff): plain z-score, risk-adjusted, combined list.
Reads reports/flagged.csv (from flagging.py) and the answer key (eval/answer_key/ground_truth.json; eval only).
Optionally reads guardrail output files (one per summary run) for citation accuracy and for
scoring the LLM's leanings against the true roles.

Usage:
    python eval/run_eval.py FLAGGED_CSV GROUND_TRUTH_JSON OUT_MD [--top-n 25]
        [--checked-summaries [LABEL=]FILE ...]
"""
import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from score import score  # noqa: E402

DETECTORS = [("Plain z-score", "rank_zscore"), ("Risk-adjusted", "rank_riskadj"), ("Combined list", "rank")]
LEANINGS = [("upcoding", "pattern_consistent_with_upcoding"),
            ("high-acuity panel", "pattern_consistent_with_high_acuity_panel"),
            ("inconclusive", "inconclusive")]
ROLES = [("upcoder", "Upcoder"), ("hard_negative", "Hard negative"), ("normal", "Normal")]


def evaluate(flagged_rows, truth, top_n=25):
    roles = {p: v["role"] for p, v in truth["providers"].items()}
    out = {}
    for name, col in DETECTORS:
        ranks = {r["provider_id"]: int(float(r[col])) for r in flagged_rows}
        flagged = [p for p, k in ranks.items() if k <= top_n]
        s = score(flagged, truth)
        out[name] = {
            "upcoders_found": s["upcoder"]["flagged"], "upcoders_total": s["upcoder"]["total"],
            "hard_neg_flagged": s["hard_negative"]["flagged"], "hard_neg_total": s["hard_negative"]["total"],
            "normal_flagged": s["normal"]["flagged"], "normal_total": s["normal"]["total"],
            "upcoder_ranks": sorted(ranks[p] for p in roles if roles[p] == "upcoder"),
            "hard_neg_ranks": sorted(ranks[p] for p in roles if roles[p] == "hard_negative"),
            "precision": s["upcoder"]["flagged"] / top_n,
        }
    return out


def load_checked(path):
    return [json.loads(line) for line in open(path) if line.strip()]


def citation_stats(records):
    cited = sum(r["citation_check"]["n_cited"] for r in records)
    valid = sum(r["citation_check"]["n_valid"] for r in records)
    return {"summaries": len(records), "passed": sum(r["citation_check"]["passed"] for r in records),
            "accuracy": (valid / cited) if cited else None, "cited": cited, "valid": valid}


def leaning_stats(records, truth):
    """Score the LLM's leanings against the true roles. Only summaries that passed the guardrail count."""
    roles = {p: v["role"] for p, v in truth["providers"].items()}
    kept = [r for r in records if r["citation_check"]["passed"]]
    table = {role: {lean: 0 for lean, _ in LEANINGS} for role, _ in ROLES}
    for r in kept:
        lean = next((k for k, v in LEANINGS if v == r["summary"]["leaning"]), None)
        if lean:
            table[roles[r["provider_id"]]][lean] += 1
    n_role = {role: sum(table[role].values()) for role, _ in ROLES}
    called_up = sum(table[role]["upcoding"] for role, _ in ROLES)
    tp = table["upcoder"]["upcoding"]
    honest_n = n_role["hard_negative"] + n_role["normal"]
    honest_up = table["hard_negative"]["upcoding"] + table["normal"]["upcoding"]
    return {"table": table, "n_role": n_role, "scored": len(kept), "rejected": len(records) - len(kept),
            "upcoding_calls": called_up, "true_upcoders_called": tp,
            "precision": (tp / called_up) if called_up else None,
            "recall": (tp / n_role["upcoder"]) if n_role["upcoder"] else None,
            "honest_called_upcoding": honest_up, "honest_total": honest_n}


def render(res, top_n, runs=None, truth=None):
    z, ra, comb = (res[n] for n, _ in DETECTORS)
    lines = [f"# Eval report (top {top_n} flagged)", "",
             "| Metric | Plain z-score | Risk-adjusted | Combined list | Target |", "|---|---|---|---|---|"]

    def row(label, f, target):
        lines.append(f"| {label} | " + " | ".join(f(res[n]) for n, _ in DETECTORS) + f" | {target} |")
    row("Upcoders found", lambda r: f"{r['upcoders_found']} / {r['upcoders_total']}", ">= 7 / 8")
    row("Hard negatives falsely flagged", lambda r: f"{r['hard_neg_flagged']} / {r['hard_neg_total']}",
        "lower than plain z-score")
    row("Normal providers falsely flagged", lambda r: f"{r['normal_flagged']} / {r['normal_total']}", "-")
    row("Precision (upcoders / flagged)", lambda r: f"{r['precision']:.0%}", "-")
    row("Upcoder ranks", lambda r: ",".join(map(str, r["upcoder_ranks"])), "-")
    row("Hard-negative ranks", lambda r: ",".join(map(str, r["hard_neg_ranks"])), "-")
    lines += ["", "## LLM summary metrics"]
    if not runs:
        lines += ["- Citation accuracy: pending (needs a summary run). Target: 100%.",
                  "- Leaning vs true role: pending."]
    for label, records in (runs or []):
        c = citation_stats(records)
        acc = "n/a" if c["accuracy"] is None else f"{c['accuracy']:.1%}"
        lines += ["", f"### {label}",
                  f"- Citation accuracy: {acc} ({c['valid']}/{c['cited']}); {c['passed']}/{c['summaries']} "
                  f"summaries passed the guardrail. Target: 100%."]
        if truth:
            L = leaning_stats(records, truth)
            lines += ["", "| Actual role (summaries scored) | " + " | ".join(n for n, _ in LEANINGS) + " |",
                      "|---|" + "---|" * len(LEANINGS)]
            for role, name in ROLES:
                lines.append(f"| {name} ({L['n_role'][role]}) | " +
                             " | ".join(str(L["table"][role][k]) for k, _ in LEANINGS) + " |")
            prec = "n/a" if L["precision"] is None else f"{L['precision']:.0%}"
            rec = "n/a" if L["recall"] is None else f"{L['recall']:.0%}"
            lines += ["", f"- \"Upcoding\" calls: {L['upcoding_calls']}; precision {prec}, recall {rec} "
                          f"({L['true_upcoders_called']} of {L['n_role']['upcoder']} upcoders).",
                      f"- Honest providers labeled upcoding: {L['honest_called_upcoding']} of {L['honest_total']}.",
                      f"- Summaries rejected by the guardrail and not scored: {L['rejected']}."]
    lines += ["- Summary usefulness (1-5, see eval/rubric.md): pending. Target: average >= 4.", "",
              "## Target check"]
    lines += [f"- Recall >= 7/8: {'met' if comb['upcoders_found'] >= 7 else 'NOT met'} (combined list)"]
    better = comb["hard_neg_flagged"] < z["hard_neg_flagged"]
    lines += [f"- Hard-negative false flags lower than plain z-score: {'met' if better else 'NOT met'} "
              f"({comb['hard_neg_flagged']} vs {z['hard_neg_flagged']})", "",
              "## Caveats",
              "- Synthetic data. Billed level depends on patient complexity by construction, so the risk-adjusted "
              "detector is helped by how the data was built; results do not transfer directly to real claims.",
              "- One seed, 8 upcoders and 8 hard negatives: small counts, so one provider moves a rate a lot.",
              "- The CMS file hides small cells; the synthetic data is calibrated to it only in the upper tail "
              "(see docs/synthetic_data.md).",
              "- Summary runs listed here come from in-session agents, not the API step, unless labeled otherwise; "
              "see each experiment's README for what it is and is not."]
    return "\n".join(lines) + "\n"


def parse_runs(items):
    runs = []
    for it in items or []:
        label, _, path = it.partition("=") if "=" in it else ("summaries", "", it)
        runs.append((label, load_checked(path)))
    return runs


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("flagged_csv")
    ap.add_argument("truth_json")
    ap.add_argument("out_md")
    ap.add_argument("--top-n", type=int, default=25)
    ap.add_argument("--checked-summaries", nargs="*", metavar="[LABEL=]FILE")
    a = ap.parse_args()
    with open(a.flagged_csv) as f:
        rows = list(csv.DictReader(f))
    truth = json.load(open(a.truth_json))
    md = render(evaluate(rows, truth, a.top_n), a.top_n, parse_runs(a.checked_summaries), truth)
    os.makedirs(os.path.dirname(os.path.abspath(a.out_md)), exist_ok=True)
    open(a.out_md, "w").write(md)
    print(md)
