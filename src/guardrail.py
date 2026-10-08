"""Citation guardrail: reject summaries that cite claims that don't exist for that provider.

Plain lookup, no model involved. For every summary it checks that:
  1. at least one claim ID is cited,
  2. every cited ID exists in claims.csv, and
  3. every cited ID belongs to the provider the summary is about.
Anything else is rejected with the reason. Reports citation accuracy overall.

Usage:
    python src/guardrail.py DATA_DIR SUMMARIES_JSONL OUT_JSONL
Exit code is 0 even when summaries are rejected (rejections are data, not errors).
"""
import argparse
import csv
import json
import os


def load_claim_owners(data_dir):
    owner = {}
    with open(os.path.join(data_dir, "claims.csv")) as f:
        for r in csv.DictReader(f):
            owner[r["claim_id"]] = r["provider_id"]
    return owner


def check(record, owner):
    """Return the record with a `citation_check` block. Does not mutate the input."""
    pid = record["provider_id"]
    cited = record.get("summary", {}).get("cited_claim_ids", [])
    missing = sorted({c for c in cited if c not in owner})
    wrong_provider = sorted({c for c in cited if c in owner and owner[c] != pid})
    reasons = []
    if not cited:
        reasons.append("no claims cited")
    if missing:
        reasons.append(f"{len(missing)} cited claim(s) do not exist")
    if wrong_provider:
        reasons.append(f"{len(wrong_provider)} cited claim(s) belong to another provider")
    out = dict(record)
    out["citations_checked"] = True
    out["citation_check"] = {
        "passed": not reasons,
        "n_cited": len(cited),
        "n_valid": sum(1 for c in cited if owner.get(c) == pid),
        "nonexistent_ids": missing,
        "other_provider_ids": wrong_provider,
        "reason": "; ".join(reasons),
    }
    return out


def run(data_dir, summaries_path, out_path):
    owner = load_claim_owners(data_dir)
    with open(summaries_path) as f:
        records = [json.loads(line) for line in f if line.strip()]
    checked = [check(r, owner) for r in records]
    with open(out_path, "w") as f:
        for r in checked:
            f.write(json.dumps(r) + "\n")
    cited = sum(r["citation_check"]["n_cited"] for r in checked)
    valid = sum(r["citation_check"]["n_valid"] for r in checked)
    passed = sum(r["citation_check"]["passed"] for r in checked)
    return {"summaries": len(checked), "passed": passed, "rejected": len(checked) - passed,
            "citations": cited, "valid_citations": valid,
            "citation_accuracy": (valid / cited) if cited else None}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir")
    ap.add_argument("summaries_jsonl")
    ap.add_argument("out_jsonl")
    a = ap.parse_args()
    s = run(a.data_dir, a.summaries_jsonl, a.out_jsonl)
    acc = "n/a" if s["citation_accuracy"] is None else f"{s['citation_accuracy']:.1%}"
    print(f"{s['summaries']} summaries: {s['passed']} passed, {s['rejected']} rejected; "
          f"citation accuracy {acc} ({s['valid_citations']}/{s['citations']})")
