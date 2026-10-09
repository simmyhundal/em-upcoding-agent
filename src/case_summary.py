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
import random
from collections import Counter, defaultdict

MODEL = os.environ.get("CASE_SUMMARY_MODEL", "claude-opus-5-5")
FALLBACK_BETA = "server-side-fallback-2026-07-01"
LOW_COMPLEXITY_SAMPLE = 25    # 99215 claims on the least complex patients
HIGH_COMPLEXITY_SAMPLE = 10   # 99215 claims on the most complex patients
COMPARISON_SAMPLE = 10        # non-99215 claims, stratified by complexity, for comparison
SAMPLER_SEED = "case-summary-v1"
MDM_LEVELS = ["minimal", "straightforward", "low", "moderate", "high"]
BILLED_LEVEL = {"99211": 0, "99212": 1, "99213": 2, "99214": 3, "99215": 4}
DOC_UNSUPPORTED_SAMPLE = 8
DOC_SUPPORTED_SAMPLE = 4

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
- The claim lists in the packet are random samples, not every claim. Do not generalize from them beyond what the tables show.
- For some claims the packet includes documentation facts from a records review (documented MDM level and minutes). Records exist for only a sample of each provider's claims, and the documentation is itself noisy, so a small share of honest claims will show a mismatch. A billed level above the documented level is unsupported. A high unsupported rate among documented 99215 claims, well above the all-provider rate, is strong evidence of upcoding; a high 99215 share whose documented claims support the billed level is consistent with a legitimately complex panel. Without enough documented claims, say the documentation is too thin to judge.
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


def load_docs(data_dir):
    """claim_id -> (documented level index 0-4, minutes); empty if no documentation file."""
    path = os.path.join(data_dir, "documentation.csv")
    docs = {}
    if os.path.exists(path):
        with open(path) as f:
            for r in csv.DictReader(f):
                docs[r["claim_id"]] = (MDM_LEVELS.index(r["documented_mdm_level"]), int(r["documented_minutes"]))
    return docs


def bucket(c):
    return "5+" if c >= 5 else str(c)


def sample_claims(rng, rows, k, stratum):
    """Random, stratified sample of up to k claims, at most one per patient where possible.

    Strata are filled round-robin so each level present is represented. A second claim from the same
    patient is used only when there are not enough distinct patients to reach k.
    """
    groups = defaultdict(list)
    for r in rows:
        groups[stratum(r)].append(r)
    firsts, seconds = {}, {}
    for key, items in groups.items():
        by_patient = defaultdict(list)
        for r in items:
            by_patient[r["patient_id"]].append(r)
        pats = sorted(by_patient)
        rng.shuffle(pats)
        first, rest = [], []
        for p in pats:
            claims = by_patient[p][:]
            rng.shuffle(claims)
            first.append(claims[0])
            rest.extend(claims[1:])
        rng.shuffle(rest)
        firsts[key], seconds[key] = first, rest
    picked = []
    for pool in (firsts, seconds):
        keys = sorted(pool)
        while len(picked) < k and any(pool[x] for x in keys):
            for x in keys:
                if pool[x] and len(picked) < k:
                    picked.append(pool[x].pop())
    return sorted(picked, key=lambda r: r["claim_id"])


def doc_peer_rates(claims, docs):
    tot, bad = Counter(), Counter()
    for rows in claims.values():
        for r in rows:
            if r["claim_id"] in docs:
                tot[r["cpt"]] += 1
                bad[r["cpt"]] += docs[r["claim_id"]][0] < BILLED_LEVEL[r["cpt"]]
    return {c: (bad[c] / tot[c] if tot[c] else None) for c in tot}


def doc_section(rows, docs, rng, peer_doc):
    got = [r for r in rows if r["claim_id"] in docs]
    table = []
    for cpt in ["99213", "99214", "99215"]:
        d = [r for r in got if r["cpt"] == cpt]
        if d:
            bad = sum(docs[r["claim_id"]][0] < BILLED_LEVEL[cpt] for r in d)
            table.append({"billed_cpt": cpt, "documented_claims": len(d), "documentation_does_not_support_billed_level": bad,
                          "unsupported_rate": round(bad / len(d), 3),
                          "all_provider_unsupported_rate": round(peer_doc[cpt], 3) if peer_doc.get(cpt) is not None else None})

    def card(r):
        lvl, mins = docs[r["claim_id"]]
        return {"claim_id": r["claim_id"], "billed_cpt": r["cpt"], "documented_mdm_level": MDM_LEVELS[lvl],
                "documented_minutes": mins}
    unsup = [r for r in got if docs[r["claim_id"]][0] < BILLED_LEVEL[r["cpt"]]]
    sup = [r for r in got if r["cpt"] == "99215" and docs[r["claim_id"]][0] >= 4]
    return {"claims_with_documentation": len(got), "share_of_claims_documented": round(len(got) / len(rows), 3),
            "by_billed_level": table,
            "examples_documentation_below_billed_level": [card(r) for r in sample_claims(rng, unsup, DOC_UNSUPPORTED_SAMPLE, lambda r: r["cpt"])],
            "examples_99215_documentation_supports": [card(r) for r in sample_claims(rng, sup, DOC_SUPPORTED_SAMPLE, lambda r: 0)]}


def build_packet(pid, flag_row, chronic, age, conditions, claims, peer_rate, docs=None, peer_doc=None):
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
        return {"claim_id": r["claim_id"], "cpt": r["cpt"], "date": r["service_date"], "patient_id": p,
                "age": age[p], "chronic_conditions": chronic[p], "conditions": conditions[p],
                "diagnosis_codes": r["diagnosis_codes"]}

    rng = random.Random(f"{SAMPLER_SEED}:{pid}")
    n215 = [r for r in rows if r["cpt"] == "99215"]
    low = [card(r) for r in sample_claims(rng, [r for r in n215 if chronic[r["patient_id"]] <= 1],
                                          LOW_COMPLEXITY_SAMPLE, lambda r: chronic[r["patient_id"]])]
    high = [card(r) for r in sample_claims(rng, [r for r in n215 if chronic[r["patient_id"]] >= 4],
                                           HIGH_COMPLEXITY_SAMPLE, lambda r: min(chronic[r["patient_id"]], 5))]
    comparison = [card(r) for r in sample_claims(rng, [r for r in rows if r["cpt"] != "99215"],
                                                 COMPARISON_SAMPLE, lambda r: bucket(chronic[r["patient_id"]]))]
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
        "comparison_claims_other_than_99215_random_sample": comparison,
        **({"documentation_review": doc_section(rows, docs, rng, peer_doc or {})} if docs else {}),
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
        betas=[FALLBACK_BETA], extra_body={"fallbacks": "default"},
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
    docs = load_docs(data_dir)
    peer_doc = doc_peer_rates(claims, docs) if docs else None
    with open(flagged_csv) as f:
        flagged = [r for r in csv.DictReader(f) if r["flagged"] == "True"]
    if limit:
        flagged = flagged[:limit]
    out = []
    for fr in flagged:
        packet = build_packet(fr["provider_id"], fr, chronic, age, conditions, claims, rates, docs, peer_doc)
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
