"""Correction rates and directions by clinician on a data 2.2 dataset (issue 79): context for a reviewer, not evidence of upcoding.

Shows the spread of correction rates, the direction split, and whether the clinicians who correct most are penalized by the screen
(their rank under the frozen risk-adjusted screen). Needs the dataset and answer key (evaluation only for the roles).

Usage:
    python eval/correction_peers.py [DATA_DIR] [ANSWER_KEY] [--write]
"""
import json
import os
import re
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import baseline_riskadj as ra  # noqa: E402
import derive  # noqa: E402

DATA = os.path.join(ROOT, "data", "synthetic_v2_261016_1_code")
KEY = os.path.join(ROOT, "eval", "answer_key", "ground_truth_v2_261016_1_code.json")


def report(data=DATA, key=KEY):
    st = derive.correction_stats(data)
    truth = json.load(open(key))["providers"]
    rows, _, _ = ra.rank(os.path.join(data, "view"), 25)
    rank = {r["provider_id"]: r["rank"] for r in rows}
    rate = {p: v["corrections"] / v["visits"] for p, v in st.items() if v["visits"] >= 100}
    tot = {k: sum(v[k] for v in st.values()) for k in ("visits", "corrections", "level_up", "level_down")}
    r = sorted(rate.values())
    lines = [f"- {tot['visits']:,} visits and {tot['corrections']:,} corrected claims ({tot['corrections'] / tot['visits']:.1%}); "
             f"{tot['level_up'] + tot['level_down']:,} corrections changed the level ({tot['level_up']:,} up, {tot['level_down']:,} down).",
             f"- Correction rate per clinician with at least 100 visits: median {statistics.median(r):.1%}, 5th to 95th percentile {r[int(.05 * len(r))]:.1%} to {r[int(.95 * len(r))]:.1%}, maximum {r[-1]:.1%}."]
    top = sorted(st, key=lambda p: -(st[p]["level_down"]))[:5]
    lines += ["", "The five clinicians with the most downward corrections:", "", "| Clinician | Visits | Corrections | Down | Up | Role | Screen rank (of %d) |" % len(rank), "|---|---|---|---|---|---|---|"]
    for p in top:
        v = st[p]
        lines.append(f"| {p} | {v['visits']} | {v['corrections']} | {v['level_down']} | {v['level_up']} | {truth[p]['role']} | {rank[p]} |")
    return "\n".join(lines)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    t = report(*args)
    print(t)
    if "--write" in sys.argv:
        path = os.path.join(ROOT, "docs", "data_v2_2.md")
        text = open(path).read()
        text = re.sub(r"(<!-- corr:start -->).*?(<!-- corr:end -->)", lambda m: m.group(1) + "\n" + t + "\n" + m.group(2), text, flags=re.S)
        open(path, "w").write(text)
