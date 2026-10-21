"""Deterministic checks a summary must pass before the pipeline accepts it (and that the rule judge scores).

One definition, two uses: `eval/judge_rules.py` turns the same checks into a 1-to-5 score, and the agent's `submit_findings` and the v2.1
workflow's model step run `lint` and refuse or repair a summary that has a HARD defect. Hard defects are ones a reviewer should never see:
a figure the evidence does not support, a leaning the evidence does not support, text that contradicts its own facts, accusatory wording,
or a quoted overpayment estimate the tools marked unreliable. Soft defects (repeats, generic next steps, headline figures missing from the
body, understated signal) only lower the judge's score.
"""
import json
import re

import summary_numbers
import summary_rules as sr

FORBIDDEN = re.compile(r"\b(fraud\w*|guilty|criminal\w*|proves?|proven)\b", re.I)
UNDERSTATE = re.compile(r"\b(modest|mild|mildly|slight|weak signal|near peers?)\b", re.I)


def _doc_counts(packet):
    d = packet.get("documentation_review") or {}
    return d.get("claims_with_documentation", 0), d


def ratio_to_expected(packet):
    exp = packet["expected_share_given_patient_complexity"]
    return packet["share_99215"] / exp if exp else 0.0


def leaning_supported(leaning, packet, rules23=False, rules41=False):
    """Is the leaning one the evidence in the packet can support? (Inconclusive always is.) rules23: rules 2.3 (workflow v2.3, agent v3.3) also support an
    upcoding call from late-signature or audit-trail signs of cloned notes."""
    docs_n, d = _doc_counts(packet)
    ratio = ratio_to_expected(packet)
    if leaning == sr.INCONCLUSIVE:
        return True
    if leaning == sr.UPCODING:
        rows = [r for r in d.get("by_billed_level", []) if r["billed_cpt"] in ("99214", "99215")]
        n = sum(r["documented_claims"] for r in rows)
        k = sum(r["documentation_does_not_support_billed_level"] for r in rows)
        if rules41 and sr.rule_leaning_41(packet)[0] == sr.UPCODING:
            return True                                    # rules 4.1 also call from the time-padding and risk-inflation signs
        return (sr.rule_leaning_23 if rules23 else sr.rule_leaning)(packet)[0] == sr.UPCODING or (n >= 6 and k / n >= 0.25)
    if leaning == sr.HIGH_ACUITY:
        return ratio <= (2.5 if docs_n < 5 else 3.0)
    return True


def contradictions(summary, packet):
    docs_n, _ = _doc_counts(packet)
    text = " ".join([summary["headline"], summary["rationale"]]).lower()
    steps = " ".join(summary["next_steps"]).lower()
    both = text + " " + steps
    out = []
    if "documentation returned supports the level billed" in both and docs_n < 5:
        out.append("says returned documentation supports the level billed, but fewer than 5 documented claims exist")
    n215 = next((r["documented_claims"] for r in (packet.get("documentation_review") or {}).get("by_billed_level", []) if r["billed_cpt"] == "99215"), 0)
    if (docs_n >= 25 and re.search(r"re-screen|once the records arrive", both)) or (n215 >= 10 and re.search(r"too thin", both)):
        out.append("says records are thin or to wait for records, but many records came back")
    if re.search(r"not prioriti[sz]ed for records|no records requested", text) and re.search(r"request records|request (the )?(full )?records", steps):
        out.append("says no records were prioritized or requested, but the next steps request records")
    if "no action is recommended" in text and re.search(r"request", steps):
        out.append("says no action is recommended, but the next steps request records")
    return out


def unreliable_estimate_quoted(summary, evidence):
    """True when the text quotes dollars or 'valid for extrapolation' although the estimate tool marked its estimate unreliable."""
    if '"reliable": false' not in evidence:
        return False
    text = " ".join([summary["headline"], summary["rationale"]])
    return bool(re.search(r"\$\s?\d|valid for extrapolation|confidence interval|\bCI\b", text))


def _norm(sentence):
    return re.sub(r"\s+", " ", re.sub(r"[\d,.]+%?", "#", sentence.lower())).strip()


def style_defects(summary):
    """The two writing defects the rule judge deducts for in agent-written text (issue 116): a headline figure the rationale never states, and a repeated sentence.
    Same tests as eval/judge_rules_32.py, so a summary with none of them cannot lose points on these two checks. Returns a list of messages."""
    out = []
    head_nums = [lit for _, _, lit in summary_numbers.numbers_in(summary["headline"])]
    body = summary["rationale"].replace(",", "")
    missing = [x for x in head_nums if x.replace(",", "") not in body]
    if missing:
        out.append(f"headline figures the rationale never states: {', '.join(missing)}")
    sents = [_norm(x) for x in re.split(r"(?<=[.!?])\s+", summary["rationale"]) if len(x) > 25]
    if len(sents) != len(set(sents)):
        out.append("a sentence is repeated")
    return out


def style_repair(summary, packet, headline, interpretation, version="2.1"):
    """Fix the style defects with code and keep the leaning: a headline that fails is replaced by the code-written one; an interpretation that makes the rationale repeat itself is dropped."""
    leaning = summary["leaning"]
    fixed = sr.assemble(packet, leaning, headline, interpretation, version=version)
    defects = style_defects(fixed)
    if any(d.startswith("a sentence") for d in defects):
        fixed = sr.assemble(packet, leaning, headline, None, version=version)
        defects = style_defects(fixed)
    if any(d.startswith("headline") for d in defects):
        fixed = {**fixed, "headline": sr.assemble(packet, leaning, None, None, version=version)["headline"]}
    return fixed


def lint(summary, packet, evidence="", rules23=False, style=False, rules41=False):
    """Return {'hard': [messages], 'soft': [messages], 'unverified_numbers': [...]}."""
    hard, soft = [], []
    chk = summary_numbers.verify(summary, packet, evidence)
    if chk["unverified"]:
        hard.append(f"numbers not matched to the evidence or tool outputs: {', '.join(chk['unverified'])}")
    if not leaning_supported(summary["leaning"], packet, rules23, rules41):
        hard.append(f"leaning {summary['leaning'].replace('pattern_consistent_with_', '')} is not supported by the evidence "
                    f"(billed 99215 share is {ratio_to_expected(packet):.1f} times expected; {_doc_counts(packet)[0]} documented claims)")
    hard += contradictions(summary, packet)
    text = " ".join([summary["headline"], summary["rationale"], *summary["next_steps"]])
    if FORBIDDEN.search(text):
        hard.append("accusatory wording")
    if unreliable_estimate_quoted(summary, evidence):
        hard.append("quotes an overpayment estimate the estimate tool marked unreliable (too few reviewed charts in its stratum)")
    sents = [re.sub(r"\s+", " ", re.sub(r"[\d,.]+%?", "#", s.lower())).strip() for s in re.split(r"(?<=[.!?])\s+", summary["rationale"]) if len(s) > 25]
    if style:                                  # agent v5.0 (issue 116): the two judged writing defects are refused, not just noted
        hard += style_defects(summary)
    elif len(sents) != len(set(sents)):
        soft.append("a sentence is repeated")
    return {"hard": hard, "soft": soft, "unverified_numbers": chk["unverified"]}


def repair(summary, packet, leaning_fallback=sr.INCONCLUSIVE, rules23=False, rules41=False):
    """Deterministic fallback for a model-written summary that failed a hard check: drop the model's words and keep what code can state.
    The model's leaning is kept only if the evidence supports it."""
    leaning = summary["leaning"] if leaning_supported(summary["leaning"], packet, rules23, rules41) else leaning_fallback
    return sr.assemble(packet, leaning, version="2.1")


def estimate_json(evidence_text):
    """The last estimate_overpayment output found in a tool-evidence text, or None."""
    m = re.findall(r"estimate_overpayment output: (\{.*\})", evidence_text)
    if not m:
        return None
    try:
        return json.loads(m[-1])
    except ValueError:
        return None


def evidence_from(events, audit, pid):
    """Text of what the author's tools returned for one provider, from office transcript events and tool-call audit entries."""
    lines = []
    for e in events:
        if e.get("provider_id") != pid:
            continue
        if e.get("action") == "close_request":
            lines.append(f"Request closed ({e.get('end_state')}): {e.get('usable_charts')} usable charts of {e.get('requested')}; reason: {e.get('reason', '')}")
        elif e.get("action") == "audit_trail":
            lines.append(f"Audit-trail request (round {e['round']}): {e['status']}. {e.get('text', '')}")
        elif "status" in e:
            codes = ", ".join(d["code"] for d in e.get("deficiencies", [])) or "none"
            lines.append(f"Round {e['round']} ({e['action']}): response '{e['status']}' {e.get('text', '')} Deficiencies: {codes}. "
                         f"Usable charts {e['usable_total']} of {e['requested_total']}; sample kind {e['sample_kind']}; days elapsed {e['days_elapsed_total']}.")
    for a in audit:
        if a["tool"] not in ("estimate_overpayment", "hybrid_review", "draft_summary", "note_checks"):
            continue
        args = a["args"]
        if args.get("provider_id") == pid or pid in args.get("provider_ids", []):
            lines.append(f"{a['tool']} output: {a['result']}" if args.get("provider_id") == pid else f"{a['tool']} output (several providers): {a['result']}")
    return "\n".join(lines)
