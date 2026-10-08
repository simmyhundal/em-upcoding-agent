"""Score a flagged list against ground truth (eval only; detectors never import this).

Usage:
    python eval/score.py FLAGS_CSV GROUND_TRUTH_JSON
FLAGS_CSV needs columns: provider_id, flagged (True/False).
"""
import csv
import json
import sys


def score(flagged_ids, truth):
    roles = {p: v["role"] for p, v in truth["providers"].items()}
    flagged = set(flagged_ids)
    out = {}
    for role in ("upcoder", "hard_negative", "normal"):
        members = [p for p, r in roles.items() if r == role]
        out[role] = {"total": len(members), "flagged": sum(p in flagged for p in members)}
    return out


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        flagged = [r["provider_id"] for r in csv.DictReader(f) if r["flagged"] == "True"]
    res = score(flagged, json.load(open(sys.argv[2])))
    u, h, n = res["upcoder"], res["hard_negative"], res["normal"]
    print(f"Recall on upcoders:         {u['flagged']}/{u['total']}")
    print(f"False flags, hard negatives: {h['flagged']}/{h['total']}")
    print(f"False flags, normal:         {n['flagged']}/{n['total']}")
