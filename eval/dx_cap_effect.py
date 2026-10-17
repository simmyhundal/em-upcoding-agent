"""Effect of diagnosis-code truncation (data 2.2 --dx-cap, issue 77) on the screen, development seed 42 only. Free (no model).

Truncation lowers the derived condition counts, so sick panels look healthier and honest high-acuity doctors can look like upcoders.
Reports, per cap: the mean derived condition count, the 99215 expectation error for high-acuity doctors, and the screen's top 25.

Usage:
    python eval/dx_cap_effect.py [--write]      # --write puts the table into docs/data_v2_2.md between the dxcap markers
"""
import csv
import json
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import baseline_riskadj as ra  # noqa: E402
import derive  # noqa: E402
import generate_v2  # noqa: E402
import screen_methods as sm  # noqa: E402
import screen_metrics as mt  # noqa: E402

CAPS = [0, 4, 3, 2]
SEED = 42


def one(cap):
    tmp = tempfile.mkdtemp()
    data, key = os.path.join(tmp, "d"), os.path.join(tmp, "k", "key.json")
    generate_v2.build(data, key, seed=SEED, n_providers=216, n_upcoders=8, n_hard_neg=8, clone_share=0.5, data_version="2.2", dx_cap=cap)
    view = os.path.join(data, "view")
    derive.build_view(data, view)
    truth = json.load(open(key))
    roles = {p: v["role"] for p, v in truth["providers"].items()}
    counts = [int(r["chronic_condition_count"]) for r in csv.DictReader(open(os.path.join(view, "patients.csv")))]
    rows, _, _ = ra.rank(view, 25)
    S = sm.score_all(view)
    ids = sorted(S["riskadj"])
    labels = [1 if roles[p] == "upcoder" else 0 for p in ids]
    out = {"cap": cap, "mean_count": sum(counts) / len(counts), "claims_shortened": truth["defects"].get("dx_truncation", {}).get("claims_shortened", 0)}
    hn_over = [r["share_99215"] / r["expected_share"] for r in rows if roles[r["provider_id"]] == "hard_negative" and r["expected_share"]]
    out["hn_ratio"] = sum(hn_over) / len(hn_over)
    for m in ("riskadj", "eb_ratio"):
        top = sorted(S[m], key=lambda p: (-S[m][p], p))[:25]
        out[m] = (sum(roles[p] == "upcoder" for p in top), sum(roles[p] == "hard_negative" for p in top), sum(roles[p] == "normal" for p in top))
        out[m + "_auprc"] = mt.average_precision([S[m][p] for p in ids], labels)
    out["n_up"] = sum(labels)
    out["z5"] = sum(1 for r in rows if r["z_adj"] >= 5)
    return out


def table(res):
    lines = ["| Diagnosis positions kept | Claims shortened | Mean derived conditions per patient | High-acuity doctors: 99215 share / expected | Doctors with suspicion >= 5 | `riskadj` top 25: upcoders / high-acuity / ordinary | `riskadj` AUPRC | `eb_ratio` top 25: upcoders / high-acuity / ordinary | `eb_ratio` AUPRC |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        lines.append(f"| {'6 (no cap)' if not r['cap'] else r['cap']} | {r['claims_shortened']:,} | {r['mean_count']:.2f} | {r['hn_ratio']:.2f} | {r['z5']} "
                     f"| {r['riskadj'][0]} / {r['riskadj'][1]} / {r['riskadj'][2]} | {r['riskadj_auprc']:.3f} "
                     f"| {r['eb_ratio'][0]} / {r['eb_ratio'][1]} / {r['eb_ratio'][2]} | {r['eb_ratio_auprc']:.3f} |")
    return "\n".join(lines)


if __name__ == "__main__":
    res = [one(c) for c in CAPS]
    t = table(res)
    print(t)
    if "--write" in sys.argv:
        path = os.path.join(ROOT, "docs", "data_v2_2.md")
        text = open(path).read()
        text = re.sub(r"(<!-- dxcap:start -->).*?(<!-- dxcap:end -->)", lambda m: m.group(1) + "\n" + t + "\n" + m.group(2), text, flags=re.S)
        open(path, "w").write(text)
