"""Case summaries: an LLM writes an investigator-facing note for each flagged provider.

The statistics decide who is flagged (see flagging.py). The LLM does not set the
flag; it explains the numbers, cites specific claims from an evidence packet, and
gives an advisory leaning plus next steps. Citations are checked separately by
the guardrail (Issue 6): this module only records what the model cited.

Reads only agent-visible files plus the flagging output. Never touches ground truth.

Usage:
    python src/case_summary.py DATA_DIR FLAGGED_CSV OUT_JSONL [--limit N] [--dry-run]
Needs ANTHROPIC_API_KEY (environment or .env) unless --dry-run.
"""
import argparse
import csv
import json
import os
from collections import Counter, defaultdict

MODEL = os.environ.get("CASE_SUMMARY_MODEL", "claude-opus-5-5")
FALLBACK_BETA = "server-side-fallback-2026-07-01"
LOW_COMPLEXITY_SAMPLE = 25    # 99215 claims on the least complex patients
HIGH_COMPLEXITY_SAMPLE = 10   # 99215 claims on the most complex patients

SCHEMA = {
    "type": "object",
    "properties": {
        "headline": {"type": "string"},
        "leaning": {"type": "string", "enum": [
            "pattern_consistent_with_upcoding",
            "pattern_consistent_with_high_acuity_panel",
            "inconclusive"]},
        "rationale": {"type": "string"},
        "cited_claim_ids": {"type": "array", "items": {"type": "string"}},
        "next_steps": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["headline", "leaning", "rationale", "cited_claim_ids", "next_steps"],
    "additionalProperties": False,
}

SYSTEM = """You assist a Special Investigations Unit reviewing outpatient E/M billing (CPT 99211-99215).
All data is synthetic. A statistical screen has already flagged this provider; you do not decide that.
Your job is to explain, for an investigator, whether the billing pattern looks like upcoding or like a
legitimately sicker patient panel, using only the evidence packet you are given.

Rules:
- Ground every factual statement in the packet. Cite claim IDs only from the packet's claim lists, and never invent one.
- Compare billed level to patient complexity: a high 99215 share on complex patients is expected; the same share
  on low-complexity patients is the concern.
- Use cautious language ("pattern consistent with"). You are not asserting fraud.
- Say what is missing (for example clinical documentation) and what a reviewer should check next.
- Keep the rationale to a short paragraph a busy reviewer can read in under a minute."""


def load(data_dir):
    chronic, age, conditions = {}, {}, {}
    with open(os.path.join(data_dir, "patients.csv")) as f:
        for r in csv.DictReader(f):
            chronic[r["patient_id"]] = int(r["chronic_condition_count"])
            age[r["patient_id"]] = int(r["age"])
            conditions[r["patient_id"]] = r["conditions"]
    claims = defaultdict(list)
    with open(os.path.join(data_dir, "claims.csv")) as f:
        for r in csv.DictReader(f):
            claims[r["provider_id"]].append(r)
    return chronic, age, conditions, claims


def bucket(c):
    return "5+" if c >= 5 else str(c)


def build_packet(pid, flag_row, chronic, age, conditions, claims, peer_rate):
    rows = claims[pid]
    mix = Counter(r["cpt"] for r in rows)
    by_bucket = defaultdict(lambda: [0, 0])
    for r in rows:
        b = bucket(chronic[r["patient_id"]])
        by_bucket[b][0] += 1
        by_bucket[b][1] += r["cpt"] == "99215"
    table = []
    for b in ["0", "1", "2", "3", "4", "5+"]:
        n, k = by_bucket.get(b, [0, 0])
        if n:
            table.append({"chronic_conditions": b, "visits": n, "n_99215": k,
                          "provider_99215_share": round(k / n, 3),
                          "all_provider_99215_share": round(peer_rate.get(b, 0.0), 3)})

    def card(r):
        p = r["patient_id"]
        return {"claim_id": r["claim_id"], "date": r["service_date"], "patient_id": p, "age": age[p],
                "chronic_conditions": chronic[p], "conditions": conditions[p],
                "diagnosis_codes": r["diagnosis_codes"]}

    top = sorted((r for r in rows if r["cpt"] == "99215"),
                 key=lambda r: (chronic[r["patient_id"]], r["claim_id"]))
    low = [card(r) for r in top if chronic[r["patient_id"]] <= 1][:LOW_COMPLEXITY_SAMPLE]
    high = [card(r) for r in reversed(top) if chronic[r["patient_id"]] >= 4][:HIGH_COMPLEXITY_SAMPLE]
    return {
        "provider_id": pid, "specialty": "Family Practice", "state": "GA",
        "n_claims": len(rows), "n_patients": len({r["patient_id"] for r in rows}),
        "billed_mix": {c: mix.get(c, 0) for c in ["99211", "99212", "99213", "99214", "99215"]},
        "share_99215": float(flag_row["share_99215"]),
        "expected_share_given_patient_complexity": float(flag_row["expected_share"]),
        "z_vs_peers": float(flag_row["z"]), "risk_adjusted_score": float(flag_row["z_adj"]),
        "flagged_by": flag_row["flagged_by"],
        "99215_share_by_patient_complexity": table,
        "99215_claims_on_low_complexity_patients_0_or_1_conditions": low,
        "99215_claims_on_high_complexity_patients_4_plus_conditions": high,
    }


def make_prompt(packet):
    return ("Evidence packet (JSON):\n" + json.dumps(packet, indent=1) +
            "\n\nWrite the case summary as JSON matching the schema.")


def call_anthropic(system, user):
    """Real call. Returns the model's JSON text. Raises on refusal."""
    import anthropic
    client = anthropic.Anthropic()
    resp = client.beta.messages.create(
        model=MODEL, max_tokens=4000,
        betas=[FALLBACK_BETA], fallbacks="default",
        output_config={"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
        system=system, messages=[{"role": "user", "content": user}],
    )
    if resp.stop_reason == "refusal":
        raise RuntimeError(f"model refused: {getattr(resp, 'stop_details', None)}")
    return next(b.text for b in resp.content if b.type == "text")


def peer_rates(claims, chronic):
    tot, hit = Counter(), Counter()
    for rows in claims.values():
        for r in rows:
            b = bucket(chronic[r["patient_id"]])
            tot[b] += 1
            hit[b] += r["cpt"] == "99215"
    return {b: hit[b] / tot[b] for b in tot}


def run(data_dir, flagged_csv, out_path, limit=None, dry_run=False, llm=call_anthropic):
    chronic, age, conditions, claims = load(data_dir)
    rates = peer_rates(claims, chronic)
    with open(flagged_csv) as f:
        flagged = [r for r in csv.DictReader(f) if r["flagged"] == "True"]
    if limit:
        flagged = flagged[:limit]
    out = []
    for fr in flagged:
        packet = build_packet(fr["provider_id"], fr, chronic, age, conditions, claims, rates)
        if dry_run:
            out.append({"provider_id": fr["provider_id"], "prompt_chars": len(make_prompt(packet)), "packet": packet})
            continue
        summary = json.loads(llm(SYSTEM, make_prompt(packet)))
        out.append({"provider_id": fr["provider_id"], "model": MODEL, "summary": summary,
                    "citations_checked": False})
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w") as f:
        for row in out:
            f.write(json.dumps(row) + "\n")
    return out


if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir")
    ap.add_argument("flagged_csv")
    ap.add_argument("out_jsonl")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--dry-run", action="store_true", help="build packets only; no API call")
    a = ap.parse_args()
    res = run(a.data_dir, a.flagged_csv, a.out_jsonl, a.limit, a.dry_run)
    print(f"{len(res)} {'packets' if a.dry_run else 'summaries'} -> {a.out_jsonl}")
