"""Judge j3.2: the deterministic rule judge of release 2 (issue 93). No model, free, identical on every rerun.

j2.3 (`eval/judge_rules.py`, frozen and still runnable) counts auditable defects. j3.2 keeps that 1-to-5 defect score with four changes and adds a
checklist of what a reviewer acts on, reported as pass/fail beside the score (the release 2 decision rules do not need a single number).

What changed from j2.3:
1. **Evidence-strength match replaces "leaning supported" and "no hedging".** j2.3 asked the writer's own rule (`summary_rules.rule_leaning`) whether
   a leaning was supported, so a rule-written summary was graded by the rule that wrote it. j3.2 sorts the evidence into tiers with its own
   thresholds (below) and checks that the leaning and the strength of the wording fit the tier.
2. **Citation support.** The guardrail checks that cited claims exist and belong to the provider, not that they support the sentence. j3.2 reads
   each stated fact about a cited claim (billed code, patient age, number of chronic conditions, documented MDM level, documented minutes) and
   checks it against the claim, patient and chart rows.
3. **Dollar honesty.** Any dollar figure or extrapolation needs a reliable estimate from a random sample in the author's tool outputs.
4. **Note package in the packet.** j2.3 built the packet without the returned notes, so every note-check percentage in a v2.1 summary counted as an
   unmatched number. j3.2 builds it the way the writer did.

| Check | Deduction | Code |
|---|---|---|
| Citation guardrail failed | score is 1 | shared (guardrail) |
| Each number not matched to the evidence or tool outputs | 0.5 each, at most 1.5 | shared (summary_numbers) |
| Upcoding leaning although the charts support the billed level, or with no charts and a ratio under 3 | 1.5 | own |
| Upcoding leaning on claims alone (no charts, ratio 3 or more) or on mixed chart evidence | 1.0 | own |
| Upcoding leaning on upcoding-tier evidence with no hedging language | 0.5 | own |
| High-acuity leaning although charts or notes point to upcoding, or with no charts and a ratio above 2.5 | 1.5 | own |
| High-acuity leaning on claims alone, on mixed charts, or with charts that support billing but a ratio above 3 | 0.5 | own |
| Inconclusive although the charts show upcoding | 1.0 | own |
| Certainty words (clearly, definitely, confirms, demonstrates, ...) unless the charts show upcoding | 0.5 | own |
| Each stated fact about a cited claim that its rows contradict | 0.5 each, at most 1.0 | own |
| A dollar figure or extrapolation without a reliable estimate from a random sample | 1.0 | own (extends the shared unreliable-estimate check) |
| Each contradiction between the text and the facts | 1.0 each, at most 2.0 | shared (summary_lint) |
| A forbidden accusatory word | 1.0 | shared |
| Fewer than 2 cited claims | 0.5 | as j2.3 |
| No next steps / no next step is specific | 1.0 / 1.0 | as j2.3 |
| Next steps do not fit the leaning | 0.5 | own |
| Records thin or missing and the text never says so | 0.5 | as j2.3 |
| A repeated sentence | 0.5 | as j2.3 |
| Each headline figure the rationale never states | 0.5 each, at most 1.0 | as j2.3 |
| Words that understate the signal while the billed 99215 share is 3 or more times expected and the leaning is not upcoding | 1.0 | as j2.3 |

Score = max(1, min(5, floor(5 - total + 0.5))).

Evidence tiers (own thresholds, written for a reviewer, not the writer's): **no charts** (fewer than 5 documented claims); **charts show upcoding**
(at least 8 documented 99214/99215 claims, at least 30% below the billed level and at least twice the peer rate); **notes look inflated** (at
least 8 returned notes, 35% or more addressing fewer problems than the level implies, plus late signatures at 12% or more or, with an audit trail,
bulk-created or paste-heavy notes at 8% or more; these are the same thresholds as the writer's note rule, so this tier is not independent of it);
**charts support billing** (at least 8 documented 99215 claims, at most 15% below the billed level); otherwise **mixed**.

Checklist (pass, fail, or n/a): leaning explained in words; observed and expected 99215 share both stated; the size of the excess stated (ratio to
expected or excess claims); the chart evidence state (how many charts and what they showed, or that none came back); the data caveat when the
pre-flight flagged the provider; a specific next step that fits the leaning; valid citations (guardrail passed, at least 2).

Usage:
    python eval/judge_rules_32.py DATA_DIR FLAGGED_CSV CHECKED_SUMMARIES_JSONL OUT_JSONL [--run-dir RUN]
"""
import argparse
import csv
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import case_summary as cs  # noqa: E402
import judge_usefulness as ju  # noqa: E402
import summary_lint  # noqa: E402
import summary_numbers  # noqa: E402
import summary_rules as sr  # noqa: E402

VERSION = "j3.2"
HEDGE = re.compile(r"consistent with|may |might|could|suggest|appears?|pattern|not a finding|needs? (a )?(coder|human|review)", re.I)
CERTAIN = re.compile(r"\b(clearly|definitely|certainly|undeniabl\w*|conclusive(ly)?|confirms?|confirmed|demonstrates?|establish(es|ed))\b", re.I)
DOLLAR = re.compile(r"\$\s?\d|\bextrapolat\w*|projected overpayment|overpaid by", re.I)
CLAIM = re.compile(r"\bC\d{7}\b")
MDM = "(minimal|straightforward|low|moderate|high)"
TIERS = ("no_charts", "charts_show_upcoding", "notes_look_inflated", "charts_support_billing", "mixed")
CHECKLIST = ("leaning_explained", "observed_vs_expected", "excess_stated", "chart_state", "data_caveat", "next_step_fits_leaning", "citations_valid")


# ---- evidence -----------------------------------------------------------------------------------------------------

def _rows(packet, codes):
    d = packet.get("documentation_review") or {}
    return [r for r in d.get("by_billed_level", []) if r["billed_cpt"] in codes]


def ratio(packet):
    exp = packet["expected_share_given_patient_complexity"]
    return packet["share_99215"] / exp if exp else 0.0


def evidence_tier(packet):
    d = packet.get("documentation_review") or {}
    if d.get("claims_with_documentation", 0) < 5:
        return "no_charts"
    rows = _rows(packet, ("99214", "99215"))
    n = sum(r["documented_claims"] for r in rows)
    k = sum(r["documentation_does_not_support_billed_level"] for r in rows)
    peer = (sum(r["documented_claims"] * (r.get("all_provider_unsupported_rate") or 0.10) for r in rows) / n) if n else 0.10
    if n >= 8 and k / n >= 0.30 and k / n >= 2 * peer:
        return "charts_show_upcoding"
    ns = d.get("note_signals")
    if ns and ns["notes"] >= 8:
        r = ns["rates"]
        second = (r.get("late") or 0) >= 0.12 or (ns["audit_trail_received"] and ((r.get("bulk_created") or 0) >= 0.08 or (r.get("paste_heavy") or 0) >= 0.08))
        if (r.get("problems") or 0) >= 0.35 and second:
            return "notes_look_inflated"
    r215 = _rows(packet, ("99215",))
    if r215 and r215[0]["documented_claims"] >= 8 and r215[0]["unsupported_rate"] <= 0.15:
        return "charts_support_billing"
    return "mixed"


def strength_problems(sm, packet):
    """[(key, deduction, problem)] for a leaning or wording that does not fit the evidence tier."""
    tier, x, lean = evidence_tier(packet), ratio(packet), sm["leaning"]
    text = " ".join([sm["headline"], sm["rationale"]])
    out = []
    if lean == sr.UPCODING:
        if tier == "charts_support_billing" or (tier == "no_charts" and x < 3):
            out.append(("overstated", 1.5, f"upcoding leaning on {tier.replace('_', ' ')} (ratio {x:.1f})"))
        elif tier in ("no_charts", "mixed"):
            out.append(("weak_basis", 1.0, f"upcoding leaning on {'claims alone' if tier == 'no_charts' else 'mixed chart evidence'}"))
        elif not HEDGE.search(text + " " + " ".join(sm["next_steps"])):
            out.append(("no_hedge", 0.5, "upcoding leaning without hedging language"))
    elif lean == sr.HIGH_ACUITY:
        if tier in ("charts_show_upcoding", "notes_look_inflated") or (tier == "no_charts" and x > 2.5):
            out.append(("overstated", 1.5, f"high-acuity leaning on {tier.replace('_', ' ')} (ratio {x:.1f})"))
        elif tier in ("no_charts", "mixed") or (tier == "charts_support_billing" and x > 3):
            out.append(("weak_basis", 0.5, f"high-acuity leaning on {tier.replace('_', ' ')} (ratio {x:.1f})"))
    elif lean == sr.INCONCLUSIVE and tier == "charts_show_upcoding":
        out.append(("understated_leaning", 1.0, "inconclusive although the charts show upcoding"))
    if tier != "charts_show_upcoding" and CERTAIN.search(text):
        out.append(("certainty", 0.5, f"certainty wording ('{CERTAIN.search(text).group(0)}') on {tier.replace('_', ' ')}"))
    return out


# ---- citation support ---------------------------------------------------------------------------------------------

def load_claim_facts(data_dir):
    """claim_id -> billed code, patient age, chronic condition count, documented MDM level and minutes (raw, as the chart says)."""
    pts = {r["patient_id"]: r for r in csv.DictReader(open(os.path.join(data_dir, "patients.csv")))}
    out = {}
    for r in csv.DictReader(open(os.path.join(data_dir, "claims.csv"))):
        p = pts.get(r["patient_id"], {})
        out[r["claim_id"]] = {"cpt": r["cpt"], "age": p.get("age"), "chronic": p.get("chronic_condition_count")}
    doc = os.path.join(data_dir, "documentation.csv")
    if os.path.exists(doc):
        for r in csv.DictReader(open(doc)):
            if r["claim_id"] in out:
                out[r["claim_id"]].update({"mdm": r["documented_mdm_level"], "minutes": r["documented_minutes"]})
    return out


def _pieces(rationale):
    """Text pieces that state facts about specific claims: the code-written examples one claim at a time, prose one sentence at a time."""
    body, _, examples = rationale.partition(" Examples: ")
    pieces = [p.strip() for p in re.split(r"(?=\bC\d{7}: )", examples) if CLAIM.search(p)] if examples else []
    pieces += [s for s in re.split(r"(?<=[.!?])\s+", body) if 0 < len(CLAIM.findall(s)) <= 2]
    return pieces


def citation_support(sm, facts):
    """(facts checked, [mismatch descriptions]) for stated facts about cited claims."""
    checked, bad = 0, []
    for piece in _pieces(sm["rationale"]):
        ids = [c for c in dict.fromkeys(CLAIM.findall(piece)) if c in facts]
        if not ids:
            continue
        stated = []
        m = re.search(r"\bbilled (992\d\d)\b", piece)
        if m:
            stated.append(("cpt", m.group(1)))
        m = re.search(r"\baged (\d+)\b|\b(\d+)-year-old\b", piece)
        if m:
            stated.append(("age", m.group(1) or m.group(2)))
        m = re.search(r"\bwith (\d+) chronic condition", piece)
        if m:
            stated.append(("chronic", m.group(1)))
        m = re.search(rf"MDM level {MDM}\b|\b(?:at|documented at|documented) {MDM} MDM\b|\b{MDM} medical decision", piece, re.I)
        if m:
            stated.append(("mdm", next(g for g in m.groups() if g).lower()))
        m = re.search(r"\b(\d+) minutes\b", piece)
        if m:
            stated.append(("minutes", m.group(1)))
        for key, val in stated:
            for c in ids:
                have = facts[c].get(key)
                if have in (None, ""):
                    continue
                checked += 1
                if str(have).lower() != val:
                    bad.append(f"{c}: text says {key} {val}, the record says {have}")
    return checked, bad


# ---- dollars ------------------------------------------------------------------------------------------------------

def dollars_unsupported(sm, evidence):
    text = " ".join([sm["headline"], sm["rationale"]])
    if not DOLLAR.search(text):
        return False
    est = summary_lint.estimate_json(evidence or "")
    return not (est and est.get("valid_for_extrapolation") and est.get("reliable", True) is not False)


# ---- checklist ----------------------------------------------------------------------------------------------------

def _has_number(text, value, tol):
    return any(abs(v - value) <= tol for v, _, _ in summary_numbers.numbers_in(text))


LEANING_WORDS = {sr.UPCODING: r"upcod|below the billed|not support|above what|higher than (the )?(documented|supported)",
                 sr.HIGH_ACUITY: r"sicker|complex|acuity|chronic|legitimate",
                 sr.INCONCLUSIVE: r"inconclusive|cannot (tell|say|judge|decide)|not enough|too (few|thin)|mixed|unclear|ambigu|until|undetermined|no (clear|firm)"}
STEP_WORDS = {sr.UPCODING: r"coder|re-?scor|recover|sampl|audit",
              sr.HIGH_ACUITY: r"close|monitor|no further|re-?screen|watch|routine",
              sr.INCONCLUSIVE: r"request|follow|records|charts|re-?screen|review"}


def checklist(record, packet, dq_flagged=None):
    sm = record["summary"]
    text = " ".join([sm["headline"], sm["rationale"]])
    steps = " ".join(sm["next_steps"])
    d = packet.get("documentation_review") or {}
    n_docs = d.get("claims_with_documentation", 0)
    share, exp, n = packet["share_99215"], packet["expected_share_given_patient_complexity"], packet["n_claims"]
    excess = (share - exp) * n
    r215 = _rows(packet, ("99215",))
    out = {"leaning_explained": bool(re.search(LEANING_WORDS[sm["leaning"]], text, re.I)),
           "observed_vs_expected": _has_number(text, share * 100, 0.06) and _has_number(text, exp * 100, 0.06),
           "excess_stated": bool(re.search(rf"\b{ratio(packet):.0f}(\.\d)?\s*(times|x|×)", text)) or (excess >= 1 and _has_number(text, excess, max(1.0, 0.02 * excess)))
                            or bool(re.search(r"\b(two|three|four|five|six|seven|eight|nine|ten)(fold| times)\b", text, re.I)),
           "chart_state": (bool(re.search(r"no (documented|records|charts)|records? (have not|were not|did not|never)|did not (respond|return)|no response|unanswered", text, re.I))
                           if n_docs == 0 else _has_number(text, n_docs, 0) and (not r215 or _has_number(text, r215[0]["documentation_does_not_support_billed_level"], 0)
                                                                                 or bool(re.search(r"below the billed|support(s|ed)? the (level|billed)", text, re.I)))),
           "data_caveat": None if not dq_flagged else ("Data caveat" in sm["rationale"]),
           "next_step_fits_leaning": bool(sm["next_steps"]) and bool(CLAIM.search(steps) or summary_numbers.numbers_in(steps))
                                     and bool(re.search(STEP_WORDS[sm["leaning"]], steps, re.I)),
           "citations_valid": bool(record.get("citation_check", {}).get("passed")) and len(sm["cited_claim_ids"]) >= 2}
    return out


# ---- the score ----------------------------------------------------------------------------------------------------

def _norm(sentence):
    return re.sub(r"\s+", " ", re.sub(r"[\d,.]+%?", "#", sentence.lower())).strip()


def score_summary(record, packet, evidence="", facts=None, dq_flagged=None):
    """Return {score, problems, deductions, unverified_numbers, checklist, evidence_tier, citation_facts_checked}."""
    sm = record["summary"]
    cl = checklist(record, packet, dq_flagged)
    base = {"checklist": cl, "evidence_tier": evidence_tier(packet)}
    if not record["citation_check"]["passed"]:
        return {"score": 1, "problems": ["rejected by the citation guardrail"], "deductions": {"citation": 4}, "unverified_numbers": [],
                "citation_facts_checked": 0, **base}
    ded, prob = {}, []
    chk = summary_numbers.verify(sm, packet, evidence)
    if chk["unverified"]:
        ded["numbers"] = min(0.5 * len(chk["unverified"]), 1.5)
        prob.append(f"numbers not matched to the evidence: {', '.join(chk['unverified'])}")
    for key, d, p in strength_problems(sm, packet):
        ded[key] = ded.get(key, 0) + d
        prob.append(p)
    n_checked, bad = citation_support(sm, facts or {})
    if bad:
        ded["citation_support"] = min(0.5 * len(bad), 1.0)
        prob += bad
    if dollars_unsupported(sm, evidence):
        ded["dollars"] = 1.0
        prob.append("states dollars or an extrapolation without a reliable estimate from a random sample")
    c = summary_lint.contradictions(sm, packet)
    if c:
        ded["contradictions"] = min(1.0 * len(c), 2.0)
        prob += c
    text = " ".join([sm["headline"], sm["rationale"], *sm["next_steps"]])
    if summary_lint.FORBIDDEN.search(text):
        ded["accusatory"] = 1.0
        prob.append("accusatory wording")
    if len(sm["cited_claim_ids"]) < 2:
        ded["few_citations"] = 0.5
        prob.append("fewer than 2 cited claims")
    steps = " ".join(sm["next_steps"])
    if not sm["next_steps"]:
        ded["no_next_steps"] = 1.0
        prob.append("no next steps")
    elif not (CLAIM.search(steps) or summary_numbers.numbers_in(steps)):
        ded["generic_next_steps"] = 1.0
        prob.append("no next step is specific (none names a claim, a count or a figure)")
    elif not re.search(STEP_WORDS[sm["leaning"]], steps, re.I):
        ded["steps_do_not_fit"] = 0.5
        prob.append("the next steps do not fit the leaning")
    docs_n = (packet.get("documentation_review") or {}).get("claims_with_documentation", 0)
    if docs_n < 5 and not re.search(r"no (documented|records)|records (came back|have not|were not)|too (thin|few)|not enough|no clinical|nothing here checks|unanswered|non-?respon", text, re.I):
        ded["undisclosed_gap"] = 0.5
        prob.append("records are thin or missing and the text never says so")
    sents = [_norm(s) for s in re.split(r"(?<=[.!?])\s+", sm["rationale"]) if len(s) > 25]
    if len(sents) != len(set(sents)):
        ded["repeated"] = 0.5
        prob.append("a sentence is repeated")
    head_nums = [lit for _, _, lit in summary_numbers.numbers_in(sm["headline"])]
    body = sm["rationale"].replace(",", "")
    missing = [x for x in head_nums if x.replace(",", "") not in body]
    if missing:
        ded["headline_not_in_body"] = min(0.5 * len(missing), 1.0)
        prob.append(f"headline figures the rationale never states: {', '.join(missing)}")
    if sm["leaning"] != sr.UPCODING and ratio(packet) >= 3 and summary_lint.UNDERSTATE.search(sm["headline"] + " " + sm["rationale"]):
        ded["understates"] = 1.0
        prob.append(f"understates the signal (billed 99215 share is {ratio(packet):.1f} times expected)")
    total = sum(ded.values())
    return {"score": int(max(1, min(5, math.floor(5 - total + 0.5)))), "problems": prob, "deductions": ded,
            "unverified_numbers": chk["unverified"], "citation_facts_checked": n_checked, **base}


def packets(data_dir, flagged_csv, with_docs=True):
    """pid -> packet, built the way the writer built it (with the note package when the charts carry notes)."""
    chronic, age, conditions, claims = cs.load(data_dir)
    rates = cs.peer_rates(claims, chronic)
    docs = cs.load_docs(data_dir) if with_docs else {}
    peer_doc = cs.doc_peer_rates(claims, docs, cs.control_providers(data_dir)) if docs else None
    facts = cs.load_doc_facts(data_dir) if with_docs else {}
    notes = cs.load_note_rows(data_dir) if with_docs else {}
    flags = {r["provider_id"]: r for r in csv.DictReader(open(flagged_csv))}
    return lambda pid: cs.build_packet(pid, flags[pid], chronic, age, conditions, claims, rates, docs or None, peer_doc, facts, notes or None)


def dq_flagged_providers(run_dir):
    p = os.path.join(run_dir or "", "data_quality.json")
    return set(json.load(open(p)).get("per_provider", {})) if run_dir and os.path.exists(p) else set()


def run(data_dir, flagged_csv, checked_path, out_path, run_dir=None, with_docs=True):
    packet_of = packets(data_dir, flagged_csv, with_docs)
    facts = load_claim_facts(data_dir)
    flagged_dq = dq_flagged_providers(run_dir)
    out = []
    for line in open(checked_path):
        if not line.strip():
            continue
        r = json.loads(line)
        pid = r["provider_id"]
        res = score_summary(r, packet_of(pid), ju.tool_evidence(run_dir, pid) if run_dir else "", facts, pid in flagged_dq)
        out.append({"provider_id": pid, "score": res["score"], "justification": "; ".join(res["problems"]) or "no defects found",
                    "problems": res["problems"], "deductions": res["deductions"], "checklist": res["checklist"],
                    "evidence_tier": res["evidence_tier"], "citation_facts_checked": res["citation_facts_checked"],
                    "judge": "rules", "judge_version": VERSION, "unverified_numbers": res["unverified_numbers"]})
    with open(out_path, "w") as f:
        for row in out:
            f.write(json.dumps(row) + "\n")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for n in ("data_dir", "flagged_csv", "checked_summaries", "out_jsonl"):
        ap.add_argument(n)
    ap.add_argument("--run-dir")
    ap.add_argument("--no-docs", action="store_true")
    a = ap.parse_args()
    rows = run(a.data_dir, a.flagged_csv, a.checked_summaries, a.out_jsonl, a.run_dir, not a.no_docs)
    sc = [r["score"] for r in rows]
    passed = {k: sum(1 for r in rows if r["checklist"][k]) for k in CHECKLIST}
    print(f"{len(rows)} summaries, mean {sum(sc) / len(sc):.2f}, distribution {[sc.count(k) for k in range(1, 6)]}; checklist passes {passed}")
