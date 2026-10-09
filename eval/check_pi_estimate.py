"""Eval-only check: does the simulated PI estimate land near the true overpayment, and do its intervals cover it?

Compares each packet's example estimate (built from the synthetic documentation sample) with the true overpayment on that
provider's 99215 frame, computed from the answer key. This uses the answer key, so it lives under eval/ and is never run
by the packet builder.

Usage:
    python eval/check_pi_estimate.py DATA_DIR PACKETS_DIR ALLOWED_JSON GROUND_TRUTH_JSON
"""
import csv
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pi_estimate as pe  # noqa: E402


def check(data_dir, packets_dir, allowed_path, truth_path, confidence=0.90):
    truth = json.load(open(truth_path))["justified_cpt_by_claim"]
    allowed = {c: v["allowed_amount"] for c, v in json.load(open(allowed_path))["codes"].items()}
    claims = list(csv.DictReader(open(os.path.join(data_dir, "claims.csv"))))
    rows = []
    for pid in sorted(d for d in os.listdir(packets_dir) if os.path.isdir(os.path.join(packets_dir, d))):
        plan = json.load(open(os.path.join(packets_dir, pid, "plan.json")))
        reviewed = pe.load_reviewed(os.path.join(packets_dir, pid, "reviewed_example.csv"))
        est = pe.estimate(plan, reviewed, allowed, confidence)
        frame = set(plan["frame_sizes"])
        true = sum(pe.overpay(r["cpt"], truth[r["claim_id"]], allowed)
                   for r in claims if r["provider_id"] == pid and r["cpt"] in frame)
        rows.append({"provider_id": pid, "true": true, "estimate": est["point_estimate"], "low": est["ci_low"],
                     "high": est["ci_high"], "covered": est["ci_low"] <= true <= est["ci_high"],
                     "reviewed": est["reviewed_claims"], "sampled": est["sampled_claims"]})
    return rows


if __name__ == "__main__":
    rows = check(*sys.argv[1:5])
    print("| Provider | True overpayment | Estimate | 90% CI | Covered | Reviewed / sampled |\n|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['provider_id']} | ${r['true']:,.0f} | ${r['estimate']:,.0f} | ${r['low']:,.0f} to ${r['high']:,.0f} | "
              f"{'yes' if r['covered'] else 'no'} | {r['reviewed']} / {r['sampled']} |")
    print(f"\nIntervals covering the true value: {sum(r['covered'] for r in rows)} of {len(rows)}")
