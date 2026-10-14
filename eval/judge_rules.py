"""Judge v2.3 (v2.2 plus a fix: "too thin" about the 99215 charts is a contradiction only when 10 or more were documented; the check lives in src/summary_lint.py): a completely deterministic usefulness scorer (no model, free, identical every time).
v2.2 adds three checks taken from the LLM judge's most frequent complaints (generic next steps, headline not matching the body, understated
signal) and keeps the rest of v2.1 unchanged.

It scores a case summary 1 to 5 by counting auditable defects against the evidence the author had, instead of asking a model for a
holistic opinion. Start at 5 and subtract; the table is the whole definition, so a reviewer can see exactly why a summary lost points.
It measures defects a reviewer would hit (wrong or ungrounded numbers, a leaning the evidence does not support, next steps that
contradict the findings, thin disclosure of missing records), NOT writing quality or persuasion, so it will not agree exactly with the
LLM judge; compare them (eval/compare_judges.py) rather than assuming they are the same measure.

| Check | Deduction |
|---|---|
| Citation guardrail failed | score is 1 |
| Each number not matched to the evidence card or tool outputs (eval/numcheck.py) | 0.5 each, at most 1.5 |
| Leaning not supported by the evidence (rules below) | 1.5 |
| Inconclusive although the evidence rule says upcoding | 1.0 |
| Each contradiction between the text and the facts (rules below) | 1.0 each, at most 2.0 |
| A forbidden accusatory word (fraud, guilty, criminal, proves) | 1.0 |
| Upcoding leaning with no hedging language | 0.5 |
| Fewer than 2 cited claims | 0.5 |
| No next steps | 1.0 |
| Records thin or missing (fewer than 5 documented claims) and the text never says so | 0.5 |
| A repeated sentence (the same sentence twice, ignoring numbers) | 0.5 |
| No next step is specific (none names a claim, a count or a figure) | 1.0 |
| Each number in the headline that the rationale never states | 0.5 each, at most 1.0 |
| Words that understate the signal (modest, mild, slight, weak signal, near peers) while the billed 99215 share is 3 or more times expected and the leaning is not upcoding | 1.0 |

Score = max(1, min(5, floor(5 - total + 0.5))).

Leaning support: upcoding is supported when the evidence rule (src/summary_rules.rule_leaning) says upcoding, or at least 6 documented
claims show 25% or more below the billed level. High-acuity is supported when at least 5 documents came back and the billed 99215 share
is within 3 times the expected share; with no documents it is NOT supported when the billed share is more than 2.5 times expected.
Inconclusive is always supported.

Contradictions: (a) the text says returned documentation supports the level billed but fewer than 5 documented claims exist; (b) the text
says records are too thin or to re-screen when records are plentiful (25 or more); (c) the text says records are not prioritized or none
requested while the next steps request records; (d) the text says no action is recommended while the next steps request records.

Usage:
    python eval/judge_rules.py DATA_DIR FLAGGED_CSV CHECKED_SUMMARIES_JSONL OUT_JSONL [--run-dir RUN]
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
import numcheck  # noqa: E402
import summary_rules as sr  # noqa: E402

VERSION = "j2.3"
FORBIDDEN = re.compile(r"\b(fraud\w*|guilty|criminal\w*|proves?|proven)\b", re.I)
HEDGE = re.compile(r"consistent with|may |might|could|suggest|appears?|pattern|not a finding|needs? (a )?(coder|human|review)", re.I)


def _norm(sentence):
    return re.sub(r"\s+", " ", re.sub(r"[\d,.]+%?", "#", sentence.lower())).strip()


from summary_lint import _doc_counts, contradictions, leaning_supported, unreliable_estimate_quoted  # noqa: E402,F401


def score_summary(record, packet, evidence=""):
    """Return {score, problems, deductions} for one checked summary record."""
    sm = record["summary"]
    if not record["citation_check"]["passed"]:
        return {"score": 1, "problems": ["rejected by the citation guardrail"], "deductions": {"citation": 4}, "unverified_numbers": []}
    ded, prob = {}, []
    chk = numcheck.verify(sm, packet, evidence)
    if chk["unverified"]:
        ded["numbers"] = min(0.5 * len(chk["unverified"]), 1.5)
        prob.append(f"numbers not matched to the evidence: {', '.join(chk['unverified'])}")
    if not leaning_supported(sm["leaning"], packet):
        ded["leaning"] = 1.5
        prob.append(f"leaning {sm['leaning'].replace('pattern_consistent_with_', '')} is not supported by the evidence")
    if sm["leaning"] == sr.INCONCLUSIVE and sr.rule_leaning(packet)[0] == sr.UPCODING:
        ded["overcautious"] = 1.0
        prob.append("inconclusive although the evidence rule says upcoding")
    if unreliable_estimate_quoted(sm, evidence):
        ded["unreliable_estimate"] = 1.0
        prob.append("quotes an overpayment estimate the estimate tool marked unreliable")
    c = contradictions(sm, packet)
    if c:
        ded["contradictions"] = min(1.0 * len(c), 2.0)
        prob += c
    text = " ".join([sm["headline"], sm["rationale"], *sm["next_steps"]])
    if FORBIDDEN.search(text):
        ded["accusatory"] = 1.0
        prob.append("accusatory wording")
    if sm["leaning"] == sr.UPCODING and not HEDGE.search(text):
        ded["no_hedge"] = 0.5
        prob.append("upcoding leaning without hedging language")
    if len(sm["cited_claim_ids"]) < 2:
        ded["few_citations"] = 0.5
        prob.append("fewer than 2 cited claims")
    if not sm["next_steps"]:
        ded["no_next_steps"] = 1.0
        prob.append("no next steps")
    docs_n, _ = _doc_counts(packet)
    if docs_n < 5 and not re.search(r"no (documented|records)|records (came back|have not|were not)|too (thin|few)|not enough|no clinical|nothing here checks|unanswered|non-?respon", text, re.I):
        ded["undisclosed_gap"] = 0.5
        prob.append("records are thin or missing and the text never says so")
    sents = [_norm(s) for s in re.split(r"(?<=[.!?])\s+", sm["rationale"]) if len(s) > 25]
    if len(sents) != len(set(sents)):
        ded["repeated"] = 0.5
        prob.append("a sentence is repeated")
    steps = " ".join(sm["next_steps"])
    if sm["next_steps"] and not (re.search(r"\bC\d{7}\b", steps) or numcheck.numbers_in(steps)):
        ded["generic_next_steps"] = 1.0
        prob.append("no next step is specific (none names a claim, a count or a figure)")
    head_nums = [lit for _, _, lit in numcheck.numbers_in(sm["headline"])]
    body = sm["rationale"].replace(",", "")
    missing = [x for x in head_nums if x.replace(",", "") not in body]
    if missing:
        ded["headline_not_in_body"] = min(0.5 * len(missing), 1.0)
        prob.append(f"headline figures the rationale never states: {', '.join(missing)}")
    exp = packet["expected_share_given_patient_complexity"]
    ratio = packet["share_99215"] / exp if exp else 0
    if sm["leaning"] != sr.UPCODING and ratio >= 3 and re.search(r"\b(modest|mild|mildly|slight|weak signal|near peers?)\b", sm["headline"] + " " + sm["rationale"], re.I):
        ded["understates"] = 1.0
        prob.append(f"understates the signal (billed 99215 share is {ratio:.1f} times expected)")
    total = sum(ded.values())
    return {"score": int(max(1, min(5, math.floor(5 - total + 0.5)))), "problems": prob, "deductions": ded, "unverified_numbers": chk["unverified"]}


def run(data_dir, flagged_csv, checked_path, out_path, run_dir=None, with_docs=True):
    chronic, age, conditions, claims = cs.load(data_dir)
    rates = cs.peer_rates(claims, chronic)
    docs = cs.load_docs(data_dir) if with_docs else {}
    peer_doc = cs.doc_peer_rates(claims, docs, cs.control_providers(data_dir)) if docs else None
    facts = cs.load_doc_facts(data_dir) if with_docs else {}
    flags = {r["provider_id"]: r for r in csv.DictReader(open(flagged_csv))}
    out = []
    for line in open(checked_path):
        if not line.strip():
            continue
        r = json.loads(line)
        pid = r["provider_id"]
        packet = cs.build_packet(pid, flags[pid], chronic, age, conditions, claims, rates, docs or None, peer_doc, facts)
        res = score_summary(r, packet, ju.tool_evidence(run_dir, pid) if run_dir else "")
        out.append({"provider_id": pid, "score": res["score"], "justification": "; ".join(res["problems"]) or "no defects found",
                    "problems": res["problems"], "deductions": res["deductions"], "judge": "rules", "judge_version": VERSION,
                    "unverified_numbers": res["unverified_numbers"]})
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
    print(f"{len(rows)} summaries, mean {sum(sc) / len(sc):.2f}, distribution {[sc.count(k) for k in range(1, 6)]}")
