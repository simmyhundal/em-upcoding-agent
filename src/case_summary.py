"""Case summaries: an investigator-facing note for each flagged provider.

The statistics decide who is flagged (see flagging.py). The numeric facts, the cited claims and the next steps are written by
code (summary_rules.py). Where the evidence is lopsided, a rule also sets the advisory leaning and the whole summary is written
by code; where it is ambiguous (or with --llm-all), the model reads a compact evidence card and returns a headline, a leaning and
a short interpretation. The model is called through the Batch API by default (half price) with a response cache, and its token
usage and estimated cost are logged. Citations are checked separately by the guardrail: this module only records what was cited.

Reads only agent-visible files plus the flagging output. Never touches ground truth.

Usage:
    python src/case_summary.py DATA_DIR FLAGGED_CSV OUT_JSONL [--limit N] [--dry-run] [--estimate] [--llm-all] [--sync]
                               [--cache-dir DIR] [--usage-jsonl FILE]
Needs ANTHROPIC_API_KEY (environment or .env) unless --dry-run or --estimate is replaced by a cache hit.
"""
import argparse
import csv
import json
import os
import random
from collections import Counter, defaultdict

import llm as llm_mod
import summary_lint
import summary_rules as sr
from records import level_from_minutes

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

LLM_SCHEMA = {
    "type": "object",
    "properties": {
        "headline": {"type": "string"},
        "leaning": {"type": "string", "enum": [sr.UPCODING, sr.HIGH_ACUITY, sr.INCONCLUSIVE]},
        "interpretation": {"type": "string"},
    },
    "required": ["headline", "leaning", "interpretation"],
    "additionalProperties": False,
}

SYSTEM = """You assist a Special Investigations Unit reviewing outpatient E/M billing (CPT 99211-99215).
All data is synthetic. A statistical screen has already flagged this provider; you do not decide that.
Your job is to explain, for an investigator, whether the billing pattern looks like upcoding or like a
legitimately sicker patient panel, using only the evidence packet you are given.

Code has already written the numeric facts, will cite the example claims and will add standard next steps. You write only:
a one-sentence headline, the advisory leaning, and an interpretation of 3 to 5 sentences that weighs the evidence, says what is
ambiguous and what a reviewer should look at first. Do not repeat the numbers code already states; refer to them.
The evidence card is compact JSON: each table is {"cols": [...], "rows": [[...]]}.

Rules:
- The claim lists in the packet are random samples, not every claim. Do not generalize from them beyond what the tables show.
- For some claims the packet includes documentation facts from a records review (documented MDM level and minutes). Records exist for only a sample of each provider's claims (a records request can return few, late or no charts), and the documentation is itself noisy, so a small share of honest claims will show a mismatch. A billed level above the documented level is unsupported. A high unsupported rate among documented 99215 claims, well above the all-provider rate, is strong evidence of upcoding; a high 99215 share whose documented claims support the billed level is consistent with a legitimately complex panel. Without enough documented claims, say the documentation is too thin to judge. Documentation can also be cloned or inflated to match the billed level; when the packet shows documented data reviewed at moderate or higher on claims that have no lab or test line, treat that as weak evidence the note does not match what happened, not as proof.
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
                mins = r["documented_minutes"]
                # the supported level is the MDM level or the level the minutes support, whichever is higher
                lvl = max(MDM_LEVELS.index(r["documented_mdm_level"]), level_from_minutes(mins))
                docs[r["claim_id"]] = (lvl, int(mins) if mins != "" else None)
    return docs


def load_note_rows(data_dir):
    """claim_id -> full returned-chart row, when documentation.csv carries the data v2.1 note columns (else {})."""
    path = os.path.join(data_dir, "documentation.csv")
    out = {}
    if os.path.exists(path):
        with open(path) as f:
            for r in csv.DictReader(f):
                if r.get("note_id"):
                    out[r["claim_id"]] = r
    return out


def load_doc_facts(data_dir):
    """claim_id -> documented data-reviewed level (0-4), when the documentation file carries it (v2 records requests)."""
    path = os.path.join(data_dir, "documentation.csv")
    facts = {}
    if os.path.exists(path):
        with open(path) as f:
            for r in csv.DictReader(f):
                if r.get("documented_data_level") not in (None, ""):
                    facts[r["claim_id"]] = int(r["documented_data_level"])
    return facts


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


def control_providers(data_dir):
    """Providers whose records stand in for prior reviews (v2 records requests); None when not applicable."""
    path = os.path.join(data_dir, "records_requests.csv")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return {r["provider_id"] for r in csv.DictReader(f) if r["kind"] == "control"}


def doc_peer_rates(claims, docs, only=None):
    """Share of documented claims whose documentation does not support the billed level, by billed code.
    `only` limits it to a set of providers (the control sample in v2, so flagged providers do not set their own baseline)."""
    tot, bad = Counter(), Counter()
    for pid, rows in claims.items():
        if only is not None and pid not in only:
            continue
        for r in rows:
            if r["claim_id"] in docs:
                tot[r["cpt"]] += 1
                bad[r["cpt"]] += docs[r["claim_id"]][0] < BILLED_LEVEL[r["cpt"]]
    return {c: (bad[c] / tot[c] if tot[c] else None) for c in tot}


MIN_FLOOR = [0, 10, 20, 30, 40]       # minutes at which each level is supported (src/records.py)


def cutoff_counts(rows, docs, note_rows):
    """Rules 4.1 (data 4.0 habits): over the returned charts billed 99214 or 99215, how many carry documented minutes 0 to 2 over the billed level's floor (time padding), and how many carry
    a risk element at the billed level while the problems and data elements stay below it (risk inflation). {"time": (charts with minutes, padded), "risk": (charts with the elements, inflated)}."""
    t_n = t_k = r_n = r_k = 0
    for r in rows:
        if r["cpt"] not in ("99214", "99215") or r["claim_id"] not in docs:
            continue
        lvl = BILLED_LEVEL[r["cpt"]]
        mins = docs[r["claim_id"]][1]
        if mins is not None:
            t_n += 1
            t_k += 0 <= mins - MIN_FLOOR[lvl] <= 2
        nr = (note_rows or {}).get(r["claim_id"])
        if nr and nr.get("documented_risk_level", "") != "":
            r_n += 1
            r_k += int(nr["documented_risk_level"]) >= lvl and int(nr["documented_problems_level"]) < lvl and int(nr["documented_data_level"]) < lvl
    return {"time": (t_n, t_k), "risk": (r_n, r_k)}


def load_doc_elements(data_dir):
    """claim_id -> returned-chart row for EVERY returned chart (the control sample's charts carry the MDM element levels but no note columns)."""
    path = os.path.join(data_dir, "documentation.csv")
    out = {}
    if os.path.exists(path):
        with open(path) as f:
            for r in csv.DictReader(f):
                out[r["claim_id"]] = r
    return out


def peer_cutoff_rates(claims, docs, note_rows, only=None):
    """The same two shares over the control sample (providers whose records stand in for prior reviews): the peer rates the provider is tested against."""
    tot = {"time": [0, 0], "risk": [0, 0]}
    for pid, rows in claims.items():
        if only is not None and pid not in only:
            continue
        for k, (n, x) in cutoff_counts(rows, docs, note_rows).items():
            tot[k][0] += n
            tot[k][1] += x
    return {k: (v[1] / v[0] if v[0] else None) for k, v in tot.items()}


def doc_section(rows, docs, rng, peer_doc, facts=None, note_rows=None):
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
                "documented_minutes": mins if mins is not None else "not recorded"}
    unsup = [r for r in got if docs[r["claim_id"]][0] < BILLED_LEVEL[r["cpt"]]]
    sup = [r for r in got if r["cpt"] == "99215" and docs[r["claim_id"]][0] >= 4]
    extra = {}
    if facts and any("has_test_line" in r for r in got):
        high = [r for r in got if facts.get(r["claim_id"], 0) >= 3]
        extra = {"documented_data_reviewed_moderate_or_higher": len(high),
                 "of_those_with_no_lab_or_test_line_on_the_claim": sum(r.get("has_test_line") == "0" for r in high)}
    if note_rows:
        import note_checks
        by_id = {r["claim_id"]: r for r in rows}
        mine = [note_rows[r["claim_id"]] for r in got if r["claim_id"] in note_rows]
        audit = any(x.get("created_ts") for x in mine)
        sig = note_checks.signals_from_docs(mine, by_id, with_audit=audit)
        extra["note_signals"] = {"notes": sig["notes"], "audit_trail_received": audit,
                                 "rates": {k: (round(v, 3) if v is not None else None) for k, v in sig.items() if k in note_checks.SIGNALS},
                                 "examples": {k: note_checks.flagged_claims(mine, by_id, k, 3, audit) for k in ("problems", "late", "unsigned", "data", "bulk_created", "paste_heavy")
                                              if sig.get(k)}}
    return {"claims_with_documentation": len(got), "share_of_claims_documented": round(len(got) / len(rows), 3),
            **extra, "by_billed_level": table,
            "examples_documentation_below_billed_level": [card(r) for r in sample_claims(rng, unsup, DOC_UNSUPPORTED_SAMPLE, lambda r: r["cpt"])],
            "examples_99215_documentation_supports": [card(r) for r in sample_claims(rng, sup, DOC_SUPPORTED_SAMPLE, lambda r: 0)]}


def build_packet(pid, flag_row, chronic, age, conditions, claims, peer_rate, docs=None, peer_doc=None, facts=None, note_rows=None, cutoff_peer=None, elements=None):
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
        **({"documentation_review": doc_section(rows, docs, rng, peer_doc or {}, facts, note_rows)} if docs else {}),
        **({"cutoff_signs": {k: {"n": n, "k": x, "peer": cutoff_peer.get(k)} for k, (n, x) in cutoff_counts(rows, docs, elements).items()}} if (docs and cutoff_peer) else {}),
    }


def make_prompt(packet, rule_reason=""):
    note = f"\nRule check: {rule_reason}." if rule_reason else ""
    return ("Evidence card (compact JSON):\n" + sr.card_json(packet) +
            "\n\nFacts already stated by code:\n" + "\n".join(sr.facts(packet)) + note +
            "\n\nReturn the headline, leaning and interpretation as JSON matching the schema.")


def call_anthropic(system, user):
    """One synchronous call (used by tests' injection point and --sync). Returns the model's JSON text."""
    return llm_mod.sync_call(MODEL, system, user, LLM_SCHEMA)[0]


def peer_rates(claims, chronic):
    tot, hit = Counter(), Counter()
    for rows in claims.values():
        for r in rows:
            b = bucket(chronic[r["patient_id"]])
            tot[b] += 1
            hit[b] += r["cpt"] == "99215"
    return {b: hit[b] / tot[b] for b in tot}


def run(data_dir, flagged_csv, out_path, limit=None, dry_run=False, llm=None, batch=False, llm_all=False,
        cache_dir=None, usage_path=None, estimate=False, assume_output_tokens=1000, log=print, version="2.0", lint=False, rules="2.0", no_model=False):
    """version "2.1": next steps depend on the records state and name claims and counts (issue 63). lint=True: a model-written summary that fails a
    hard check (unsupported figure or leaning, contradiction, accusatory wording) is replaced by the code-written one (summary_lint.repair).
    rules "2.2" (workflow v2.2, issue 91): summary_rules.rule_leaning_22 decides more ambiguous cases by rule, so fewer need the model.
    rules "2.3" (workflow v2.3, issue 99): rule_leaning_23 adds late-signature and audit-trail signs of cloned notes.
    no_model=True (workflow v2.5 onward): never call the model; where the rules are silent the summary is written by code as inconclusive. The run is then fully deterministic."""
    chronic, age, conditions, claims = load(data_dir)
    rates = peer_rates(claims, chronic)
    docs = load_docs(data_dir)
    peer_doc = doc_peer_rates(claims, docs, control_providers(data_dir)) if docs else None
    facts = load_doc_facts(data_dir)
    note_rows = load_note_rows(data_dir)
    elements = load_doc_elements(data_dir) if rules == "4.1" else None
    cutoff_peer = peer_cutoff_rates(claims, docs, elements, control_providers(data_dir)) if (docs and rules == "4.1") else None      # rules 4.1 only: frozen packets keep their keys
    with open(flagged_csv) as f:
        flagged = [r for r in csv.DictReader(f) if r["flagged"] == "True"]
    if limit:
        flagged = flagged[:limit]
    packets, plan = {}, []
    for fr in flagged:
        pid = fr["provider_id"]
        packets[pid] = build_packet(pid, fr, chronic, age, conditions, claims, rates, docs, peer_doc, facts, note_rows, cutoff_peer, elements)
        lean, reason = {"4.1": sr.rule_leaning_41, "4.0": sr.rule_leaning_40, "2.3": sr.rule_leaning_23, "2.2": sr.rule_leaning_22}.get(rules, sr.rule_leaning)(packets[pid])
        if no_model and lean is None:
            lean, reason = sr.INCONCLUSIVE, "the rules are silent on this provider and no model is used; left for a person to read"
        plan.append((pid, lean, reason, (lean is None or llm_all) and not no_model))
    if dry_run:
        out = [{"provider_id": pid, "prompt_chars": len(make_prompt(packets[pid], reason)), "packet": packets[pid],
                "will_call_llm": call, "rule_leaning": lean} for pid, lean, reason, call in plan]
        _write(out_path, out)
        return out
    items = [(pid, SYSTEM, make_prompt(packets[pid], reason)) for pid, lean, reason, call in plan if call]
    if estimate:
        n_in = [llm_mod.count_tokens(MODEL, s, u) for _, s, u in items]
        usd = llm_mod.cost(MODEL, sum(n_in), assume_output_tokens * len(items), batch=True)
        log(f"{len(items)} of {len(plan)} providers need the model; input {sum(n_in):,} tokens "
            f"(mean {sum(n_in) // max(len(n_in), 1):,}); estimated ${usd:.2f} at batch price assuming {assume_output_tokens} output tokens each")
        return {"calls": len(items), "providers": len(plan), "input_tokens": sum(n_in), "estimated_usd": usd}
    got = {}
    if items:
        if llm is not None:                                  # injected function (tests): one call at a time, no cache
            got = {pid: (llm(s, u), {"input_tokens": 0, "output_tokens": 0}, "sync") for pid, s, u in items}
        else:
            got = llm_mod.run_requests(items, MODEL, LLM_SCHEMA, cache_dir, batch=batch, log=log)
    out = []
    for pid, lean, reason, call in plan:
        if call:
            m = json.loads(got[pid][0])
            summary = sr.assemble(packets[pid], m["leaning"], m["headline"], m["interpretation"], version=version)
            rec = {"provider_id": pid, "model": MODEL, "summary": summary, "citations_checked": False,
                   "source": "llm", "rule_leaning": lean, "rule_reason": reason}
            if lint:
                found = summary_lint.lint(summary, packets[pid], rules23=rules in ("2.3", "4.0", "4.1"), rules41=rules == "4.1")
                if found["hard"]:
                    rec.update({"summary": summary_lint.repair(summary, packets[pid], rules23=rules in ("2.3", "4.0", "4.1"), rules41=rules == "4.1"), "lint_repaired": True, "lint_problems": found["hard"], "source": "llm+repair"})
            out.append(rec)
        else:
            out.append({"provider_id": pid, "model": "rules", "summary": sr.assemble(packets[pid], lean, version=version),
                        "citations_checked": False, "source": "rules", "rule_leaning": lean, "rule_reason": reason})
    _write(out_path, out)
    if usage_path and got:
        total = llm_mod.write_usage(usage_path, MODEL, [(pid, u, via) for pid, (_, u, via) in got.items()])
        log(f"estimated writer spend: ${total:.2f} ({len(got)} model calls; usage in {usage_path})")
    return out


def _write(out_path, rows):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


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
    ap.add_argument("--estimate", action="store_true", help="count tokens (free) and print the estimated cost; no billed call")
    ap.add_argument("--llm-all", action="store_true", help="call the model for every provider, even where a rule decides")
    ap.add_argument("--sync", action="store_true", help="one request at a time instead of the Batch API")
    ap.add_argument("--v21", action="store_true", help="version 2.1 summaries: conditional next steps and the lint-and-repair check")
    ap.add_argument("--v22", action="store_true", help="workflow v2.2: the 2.1 summaries with rules 2.2 (more cases decided by rule; implies --v21)")
    ap.add_argument("--v41", action="store_true", help="workflow v4.0 with rules 4.1: rules 4.0 plus the time-padding and risk-inflation signs of data 4.0 (implies --v40)")
    ap.add_argument("--v40", action="store_true", help="workflow v4.0: the 2.3 summaries with rules 4.0 (the chart test pooled over 99214 and 99215; implies --v23)")
    ap.add_argument("--v23", action="store_true", help="workflow v2.3: the 2.2 summaries with rules 2.3 (cloned-notes signs decide by rule; implies --v22)")
    ap.add_argument("--no-model", action="store_true", help="never call the model: where the rules are silent the summary is code-written and inconclusive (deterministic; workflow v2.5 onward)")
    ap.add_argument("--cache-dir", help="response cache folder (default: llm_cache next to the output)")
    ap.add_argument("--usage-jsonl", help="where to write token usage and estimated cost (default: next to the output)")
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.out_jsonl))
    res = run(a.data_dir, a.flagged_csv, a.out_jsonl, a.limit, a.dry_run, batch=not a.sync, llm_all=a.llm_all,
              cache_dir=a.cache_dir or os.path.join(base, "llm_cache"),
              usage_path=a.usage_jsonl or os.path.join(base, "usage_writer.jsonl"), estimate=a.estimate,
              version="2.1" if (a.v21 or a.v22 or a.v23 or a.v40 or a.v41) else "2.0", lint=a.v21 or a.v22 or a.v23 or a.v40 or a.v41,
              rules="4.1" if a.v41 else "4.0" if a.v40 else "2.3" if a.v23 else "2.2" if a.v22 else "2.0", no_model=a.no_model)
    if not a.estimate:
        calls = sum(1 for r in res if r.get("source") == "llm" or r.get("will_call_llm"))
        print(f"{len(res)} {'packets' if a.dry_run else 'summaries'} ({calls} via the model) -> {a.out_jsonl}")
