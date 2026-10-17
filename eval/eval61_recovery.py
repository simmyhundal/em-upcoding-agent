"""Hypothetical recovery for the issue 61 arms: what the extrapolation tool (src/pi_estimate.py) would estimate if it were run on every provider an arm
accused, against the dollars that could be recovered from all upcoders.

For each run, every provider the final summaries call upcoding ("accused") gets the same arithmetic the agent's estimate_overpayment tool uses: the
RANDOM charts the office returned for that provider (transcript `sample_kind` random), the level each chart supports (documentation rows: MDM level or
minutes, whichever is higher), stratified by billed level and extrapolated to the provider's claims with a point estimate (90% interval, t critical values).
A provider with no random charts gets 0 (nothing to extrapolate from). A negative point estimate counts as 0 (nothing to recover). Honest doctors the arm
accused are included: a payer running the tool on them would recover little or nothing, and any positive estimate is a false recovery.

Total recoverable = dollars paid above what the justified levels would have paid, for all upcoders (answer key; evaluation only), the same number as the
`overpaid_usd` column of experiments/results.csv.

Caveats: charts are read by a simulated reviewer with coder noise; estimates are draft arithmetic, not recovery; many estimates rest on few charts in the
main stratum (counted as unreliable, as the agent tool does when fewer than 8). Free: stored runs only.
"""
import csv
import json
import os
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import pi_estimate as pe  # noqa: E402
import records  # noqa: E402

CODES = records.CODES
MIN_MAIN = 8
_ALLOWED = None


def allowed():
    global _ALLOWED
    if _ALLOWED is None:
        _ALLOWED = {c: v["allowed_amount"] for c, v in json.load(open(os.path.join(ROOT, "data", "baselines", "allowed_amounts_ga_fp.json")))["codes"].items()}
    return _ALLOWED


def _supported_level(row):
    mins = row["documented_minutes"]
    return max(records.MDM_LEVELS.index(row["documented_mdm_level"]), records.level_from_minutes(mins))


def random_ids(rid):
    """provider -> set of claim ids returned from RANDOM requests (transcript entries whose own sample kind is random)."""
    out = {}
    path = os.path.join(ROOT, "experiments", rid, "office_transcript.jsonl")
    if not os.path.exists(path):
        return out
    for line in open(path):
        e = json.loads(line)
        if e.get("action") in ("send_request", "follow_up") and e.get("sample_kind") == "random" and "error" not in e:
            out.setdefault(e["provider_id"], set()).update(e.get("usable_claim_ids", []))
    return out


def recover(rid, code):
    """Estimated recovery for one run: {"est": dollars, "accused": n, "estimated": n, "unreliable": n, "false_recovery": dollars}."""
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
    truth = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))["providers"]
    claims = {}
    for r in csv.DictReader(open(os.path.join(data, "view", "claims.csv"))):
        claims.setdefault(r["provider_id"], []).append(r)
    docs = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(data, f"view_{rid}", "documentation.csv")))}
    accused = [x["provider_id"] for x in map(json.loads, open(os.path.join(ROOT, "experiments", rid, "case_summaries_checked.jsonl")))
               if x["summary"]["leaning"] == "pattern_consistent_with_upcoding"]
    rnd = random_ids(rid)
    est = false_rec = 0.0
    n_est = n_unrel = 0
    for pid in accused:
        rows = claims.get(pid, [])
        by = {r["claim_id"]: r for r in rows}
        ids = [c for c in sorted(rnd.get(pid, ())) if c in by and c in docs]
        if not ids:
            continue
        plan = {"provider_id": pid, "frame_sizes": dict(Counter(r["cpt"] for r in rows)), "sampled_claims": {c: by[c]["cpt"] for c in ids}}
        reviewed = {c: CODES[_supported_level(docs[c])] for c in ids}
        amounts = {r["claim_id"]: (float(r["allowed_amount"]), float(r["paid_amount"])) for r in rows if r.get("allowed_amount")}
        res = pe.estimate(plan, reviewed, allowed(), 0.90, claim_amounts=amounts)
        strata = {c: d for c, d in res["strata"].items() if d.get("n_reviewed")}
        main = max(strata, key=lambda c: strata[c]["N"] * strata[c].get("mean_overpayment", 0), default=None)
        n_main = strata[main]["n_reviewed"] if main else 0
        pt = max(res["point_estimate"], 0.0)
        est += pt
        n_est += 1
        n_unrel += n_main < MIN_MAIN
        if truth[pid]["role"] != "upcoder":
            false_rec += pt
    return {"est": est, "accused": len(accused), "estimated": n_est, "unreliable": n_unrel, "false_recovery": false_rec}


if __name__ == "__main__":
    print(json.dumps(recover(sys.argv[1], sys.argv[2]), indent=1))
