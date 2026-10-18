"""Deterministic parts of a case summary: facts, rule-based leaning, citations, next steps, and the compact evidence card.

Why this exists (Cost issues 22 and 28): most of a case summary is a function of numbers already in the evidence packet. Code
writes those parts for free and reproducibly; the model is called only where judgment is needed.

  * `facts`          the numeric sentences (shares, expected share, documentation rates), stated by code so they cannot be misread
  * `rule_leaning`   upcoding / high-acuity panel / inconclusive when the evidence is lopsided, else None (ambiguous)
  * `pick_citations` the claims cited, chosen by code from the packet's own sample lists
  * `next_steps`     standard next steps for each leaning
  * `to_card`        a compact, derived-numbers-first version of the packet for the model (no repeated keys, no whitespace)
  * `assemble`       puts it together; rule-decided cases are written entirely by code, ambiguous ones get the model's headline,
                     leaning and interpretation paragraph

Thresholds are set by reasoning about the data, written here, and not tuned on held-out seeds. Rules read only the packet.
"""
import json

UPCODING = "pattern_consistent_with_upcoding"
HIGH_ACUITY = "pattern_consistent_with_high_acuity_panel"
INCONCLUSIVE = "inconclusive"

MIN_DOCS_ANY = 5            # fewer returned records than this: too thin to judge
MIN_DOCS_99215 = 6          # documented 99215 claims needed before a rule leans either way
UP_RATE, UP_VS_PEER = 0.40, 3.0          # unsupported share at least this AND this many times the peer rate: upcoding
LOW_RATE, LOW_VS_PEER = 0.15, 1.5        # unsupported share at most this OR this close to the peer rate: documentation supports billing
PEER_FALLBACK = 0.10        # peer unsupported rate used when the packet has none
MAX_EXCESS_FOR_ACUITY = 3.0  # a high-acuity call also needs the 99215 share within this multiple of the expected share
POOL_MIN_DOCS, POOL_UP_RATE = 12, 0.25   # fallback on documented 99214 and 99215 claims pooled, when 99215 alone is too thin
NO_TEST_RATE = 0.25         # note claims moderate+ data reviewed with no lab on the claim this often: leave it to the model

LOW_KEY = "99215_claims_on_low_complexity_patients_0_or_1_conditions"
HIGH_KEY = "99215_claims_on_high_complexity_patients_4_plus_conditions"
COMPARE_KEY = "comparison_claims_other_than_99215_random_sample"


def _row_99215(packet):
    d = packet.get("documentation_review") or {}
    for r in d.get("by_billed_level", []):
        if r["billed_cpt"] == "99215":
            return r
    return None


def doc_total(packet):
    return (packet.get("documentation_review") or {}).get("claims_with_documentation", 0)


def low_complexity_share_of_99215(packet):
    rows = packet["99215_share_by_patient_complexity"]
    tot = sum(r["n_99215"] for r in rows)
    low = sum(r["n_99215"] for r in rows if r["chronic_conditions"] in ("0", "1"))
    return (low / tot) if tot else None


INFLATED_PROBLEMS, INFLATED_LATE, INFLATED_AUDIT = 0.35, 0.12, 0.08      # data v2.1 note signals; set on the development seed only
MIN_NOTES_SIGNALS = 8


def inflated_notes(packet):
    """True when the returned notes look inflated: they address fewer problems than their claimed level implies AND show a second signal
    (late signatures, or with an audit trail bulk creation or paste-heavy notes). Rates, not proof: honest providers show each at a baseline."""
    ns = (packet.get("documentation_review") or {}).get("note_signals")
    if not ns or ns["notes"] < MIN_NOTES_SIGNALS:
        return False
    r = ns["rates"]
    second = (r.get("late") or 0) >= INFLATED_LATE or (ns["audit_trail_received"] and ((r.get("bulk_created") or 0) >= INFLATED_AUDIT
                                                                                       or (r.get("paste_heavy") or 0) >= INFLATED_AUDIT))
    return (r.get("problems") or 0) >= INFLATED_PROBLEMS and bool(second)


def rule_leaning(packet):
    """Return (leaning or None, reason). None means ambiguous: ask the model."""
    if doc_total(packet) < MIN_DOCS_ANY:
        return INCONCLUSIVE, f"only {doc_total(packet)} documented claims came back"
    row = _row_99215(packet)
    d = packet["documentation_review"]
    if not row or row["documented_claims"] < MIN_DOCS_99215:
        return _pooled(packet, d)
    n, u = row["documented_claims"], row["unsupported_rate"]
    peer = row.get("all_provider_unsupported_rate")
    peer = PEER_FALLBACK if peer is None else peer
    if d.get("documented_data_reviewed_moderate_or_higher", 0) >= MIN_DOCS_99215:
        no_test = d["of_those_with_no_lab_or_test_line_on_the_claim"] / d["documented_data_reviewed_moderate_or_higher"]
        if no_test > NO_TEST_RATE:
            return None, "notes claim data reviewed that the claims do not show"
    if u >= UP_RATE and u >= UP_VS_PEER * peer:
        return UPCODING, f"{u:.0%} of {n} documented 99215 claims are below the billed level (peer rate {peer:.0%})"
    if inflated_notes(packet):
        return UPCODING, "the notes look inflated: they address fewer problems than their claimed level implies and show late signatures or audit-trail signs"
    if u <= max(LOW_RATE, LOW_VS_PEER * peer):
        exp = packet["expected_share_given_patient_complexity"]
        if exp and packet["share_99215"] <= MAX_EXCESS_FOR_ACUITY * exp:
            return HIGH_ACUITY, f"documentation supports the level billed ({u:.0%} below, peer rate {peer:.0%})"
        return None, "documentation supports billing but the 99215 share is far above the expected share"
    return None, "documentation result sits between the rule's cutoffs"


# Rules 2.2 (workflow v2.2, issue 91): in the release 1 runs the model, asked about these ambiguous cases, answered inconclusive every
# time (workflow v2.1: 104 of 104; docs/workflow_cost.md). Rules 2.2 decide them inconclusive without a model call. The model is still
# asked when notes claim data review the claims do not show, the one case where it leaned upcoding (correctly). rule_leaning itself is
# frozen (workflow v2.0 and v2.1, agent v3.0 and v3.1, the lint and the rule judge all call it); only rule_leaning_22 changes.
RULES_22_INCONCLUSIVE = ("documentation supports billing but the 99215 share is far above the expected share",
                         "documented 99215 claims are too few and the pooled result is not lopsided",
                         "documentation result sits between the rule's cutoffs",
                         "too few documented 99214 and 99215 claims to lean either way")


PEER_CAP_22 = LOW_RATE      # rules 2.2: the peer unsupported rate never counts as higher than the "documentation supports billing" line (0.15)


def _cap_peer(packet):
    """Copy of the packet with the peer unsupported rates capped at PEER_CAP_22, and whether anything was capped. Honest coding errors lift the peer rate
    on 99215 charts (to 54% on data 2.2, from 10% on data 2.1): the control sample's 99215 claims come mostly from low-volume billers, where a third are
    honest up-slips from 99214. A provider billing 99215 at several times its expected share is mostly billing true 99215s, so its charts should look
    cleaner than that peer rate, and a clause such as "3 times the peer rate" can never be met. Below the cap (every release 1 run) nothing changes."""
    import copy
    d = (packet.get("documentation_review") or {})
    rows = d.get("by_billed_level") or []
    if not any((r.get("all_provider_unsupported_rate") or 0) > PEER_CAP_22 for r in rows):
        return packet, False
    pk = copy.deepcopy(packet)
    for r in pk["documentation_review"]["by_billed_level"]:
        if (r.get("all_provider_unsupported_rate") or 0) > PEER_CAP_22:
            r["all_provider_unsupported_rate"] = PEER_CAP_22
    return pk, True


def rule_leaning_22(packet):
    """rule_leaning with the peer rate capped (rules 2.2, issue 91 and the data 2.2 diagnosis), and the ambiguous cases in RULES_22_INCONCLUSIVE decided
    inconclusive by rule."""
    pk, capped = _cap_peer(packet)
    lean, reason = rule_leaning(pk)
    if capped and lean in (UPCODING, HIGH_ACUITY):
        reason += f"; the peer baseline is capped at {PEER_CAP_22:.0%} because honest coding errors inflate the control sample's rate"
    if lean is None and reason in RULES_22_INCONCLUSIVE:
        return INCONCLUSIVE, reason + "; rules 2.2 leave it inconclusive without a model call"
    return lean, reason


# Rules 2.3 (workflow v2.3, issue 99, data stays 2.2): cloned notes make the charts match the bill, so rules 2.2 end at "inconclusive" for an upcoder whose
# 99215 share is far above expected. Late signatures are the clean sign in the returned notes: rule_leaning's own "inflated notes" test needs the problems
# signal at 35% as well, a seed-42 cutoff that honest doctors on data 2.2 nearly reach (27% on average). Rules 2.3 lean upcoding when rules 2.2 would say
# inconclusive (or still ask the model) and (a) at least MIN_NOTES_SIGNALS notes came back, (b) the late-signature rate is at least INFLATED_LATE, or an audit trail came back with bulk-created or paste-heavy notes at INFLATED_AUDIT (existing constants, not refit) and
# (c) the 99215 share is more than MAX_EXCESS_FOR_ACUITY times the expected share (the existing "far above expected" line). The thresholds are existing constants, not refit; the idea of the rule came from reading the release 2 evaluation seeds, which are development data from now on.
ALPHA_CHART_23 = 0.05        # rules 2.3: a chart-based upcoding call must beat the peer unsupported rate at this one-sided exact binomial level


def _binom_sf(x, n, p):
    """P(X >= x) for X ~ Binomial(n, p), exact."""
    from math import comb
    return sum(comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(x, n + 1))


def _chart_test_23(packet):
    """(documented 99215 claims, unsupported, peer rate, one-sided p) for the 99215 row; the peer rate is the packet's own, NOT capped."""
    row = _row_99215(packet)
    n, x = row["documented_claims"], row["documentation_does_not_support_billed_level"]
    peer = row.get("all_provider_unsupported_rate")
    peer = PEER_FALLBACK if peer is None else peer
    return n, x, peer, _binom_sf(x, n, peer)


def rule_leaning_23(packet):
    lean, reason = rule_leaning_22(packet)
    if lean == UPCODING and "documented 99215 claims are below the billed level" in reason:
        # rules 2.2 cap the peer rate at 15% so that noisy honest peers (40% unsupported on data 2.2) do not blind the chart rule. With a wider list that cap lets
        # honest doctors through on small samples, so rules 2.3 also ask whether the provider's unsupported share beats the real peer rate by more than chance.
        n, x, peer, p = _chart_test_23(packet)
        if p > ALPHA_CHART_23:
            return INCONCLUSIVE, (f"{x} of {n} documented 99215 claims are below the billed level, but that does not beat the peer rate of {peer:.0%} "
                                  f"by more than chance (one-sided p = {p:.2f}, rules 2.3)")
        return lean, reason + f"; it beats the uncapped peer rate (one-sided p = {p:.3f}, rules 2.3)"
    if lean not in (INCONCLUSIVE, None):          # None: the one case rules 2.2 still send to the model (notes claim data review the claims do not show)
        return lean, reason
    ns = (packet.get("documentation_review") or {}).get("note_signals")
    exp = packet.get("expected_share_given_patient_complexity")
    if not (ns and ns["notes"] >= MIN_NOTES_SIGNALS and exp and packet["share_99215"] > MAX_EXCESS_FOR_ACUITY * exp):
        return lean, reason
    r = ns["rates"]
    if (r.get("late") or 0) >= INFLATED_LATE:
        sign = f"{r['late']:.0%} of {ns['notes']} returned notes were signed late"
    elif ns.get("audit_trail_received") and ((r.get("bulk_created") or 0) >= INFLATED_AUDIT or (r.get("paste_heavy") or 0) >= INFLATED_AUDIT):
        sign = "the audit trail shows bulk-created or paste-heavy notes"      # an audit trail came back and shows the cloning directly
    else:
        return lean, reason
    return UPCODING, (f"documentation supports the billed level, but {sign} and the 99215 share is more than {MAX_EXCESS_FOR_ACUITY:g} times the expected share "
                      "(rules 2.3)")



def _pooled(packet, d):
    rows = [r for r in d["by_billed_level"] if r["billed_cpt"] in ("99214", "99215")]
    n = sum(r["documented_claims"] for r in rows)
    if n < POOL_MIN_DOCS:
        return None, "too few documented 99214 and 99215 claims to lean either way"
    k = sum(r["documentation_does_not_support_billed_level"] for r in rows)
    peer = sum(r["documented_claims"] * (r.get("all_provider_unsupported_rate") or PEER_FALLBACK) for r in rows) / n
    u = k / n
    if u >= POOL_UP_RATE and u >= UP_VS_PEER * peer:
        return UPCODING, f"{u:.0%} of {n} documented 99214 and 99215 claims are below the billed level (peer rate {peer:.0%})"
    if inflated_notes(packet):
        return UPCODING, "the notes look inflated: they address fewer problems than their claimed level implies and show late signatures or audit-trail signs"
    return None, "documented 99215 claims are too few and the pooled result is not lopsided"


def facts(packet):
    """Numeric sentences, written by code."""
    pid, n = packet["provider_id"], packet["n_claims"]
    exp = packet["expected_share_given_patient_complexity"]
    out = [f"{pid} billed 99215 on {packet['share_99215']:.1%} of {n:,} claims against an expected {exp:.1%} given patient "
           f"complexity (risk-adjusted score {packet['risk_adjusted_score']:.2f}; plain z-score vs peers {packet['z_vs_peers']:.2f})."]
    low = low_complexity_share_of_99215(packet)
    if low is not None:
        out.append(f"{low:.0%} of this provider's 99215 claims were on patients with 0 or 1 chronic conditions.")
    d = packet.get("documentation_review")
    if d:
        out.append(f"Records came back for {d['claims_with_documentation']:,} claims.")
        row = _row_99215(packet)
        if row:
            peer = row.get("all_provider_unsupported_rate")
            out.append(f"Of {row['documented_claims']} documented 99215 claims, {row['documentation_does_not_support_billed_level']} "
                       f"({row['unsupported_rate']:.0%}) were documented below the billed level"
                       + (f", against {peer:.0%} for the comparison providers." if peer is not None else "."))
        else:
            out.append("No documented 99215 claims came back.")
        ns = d.get("note_signals")
        if ns and ns["notes"] >= MIN_NOTES_SIGNALS:
            r = ns["rates"]
            bits = [f"{k.replace('_', ' ')} {r[k]:.0%}" for k in ("problems", "late", "unsigned", "data", "bulk_created", "paste_heavy") if r.get(k) is not None]
            out.append(f"Note checks on {ns['notes']} returned notes (share showing each sign): " + ", ".join(bits) + "."
                       + ("" if ns["audit_trail_received"] else " No audit trail was received."))
        if d.get("documented_data_reviewed_moderate_or_higher"):
            out.append(f"{d['of_those_with_no_lab_or_test_line_on_the_claim']} of {d['documented_data_reviewed_moderate_or_higher']} "
                       "notes claiming moderate-or-higher data reviewed had no lab or test line on the claim.")
    else:
        out.append("No records have been requested for this provider, so nothing here checks the billed level against documentation.")
    return out


def _cards(packet):
    cards = {}
    for key in (LOW_KEY, HIGH_KEY, COMPARE_KEY):
        for c in packet.get(key, []):
            cards[c["claim_id"]] = c
    return cards


def pick_citations(packet, leaning):
    """Claim IDs to cite, chosen by code from the packet's sample lists."""
    d = packet.get("documentation_review") or {}
    below = [e["claim_id"] for e in d.get("examples_documentation_below_billed_level", []) if e["billed_cpt"] == "99215"]
    below = below or [e["claim_id"] for e in d.get("examples_documentation_below_billed_level", [])]
    supports = [e["claim_id"] for e in d.get("examples_99215_documentation_supports", [])]
    low = [c["claim_id"] for c in packet.get(LOW_KEY, [])]
    high = [c["claim_id"] for c in packet.get(HIGH_KEY, [])]
    if leaning == UPCODING:
        picks = below[:3] + low[:3]
    elif leaning == HIGH_ACUITY:
        picks = supports[:3] + high[:2]
    else:
        picks = below[:2] + low[:2]
    if not picks:                                    # always cite something from the packet's own samples
        picks = [c["claim_id"] for key in (LOW_KEY, HIGH_KEY, COMPARE_KEY) for c in packet.get(key, [])[:2]]
    seen, out = set(), []
    for c in picks:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def evidence_lines(packet, ids):
    d = packet.get("documentation_review") or {}
    docs = {e["claim_id"]: e for e in d.get("examples_documentation_below_billed_level", []) + d.get("examples_99215_documentation_supports", [])}
    cards = _cards(packet)
    lines = []
    for cid in ids:
        bits = []
        if cid in cards:
            c = cards[cid]
            bits.append(f"billed {c['cpt']}, patient aged {c['age']} with {c['chronic_conditions']} chronic condition(s)"
                        + (f" ({c['conditions']})" if c["conditions"] else ""))
        if cid in docs:
            e = docs[cid]
            if not cards.get(cid):
                bits.append(f"billed {e['billed_cpt']}")
            bits.append(f"documented MDM level {e['documented_mdm_level']}, {e['documented_minutes']} minutes"
                        if e["documented_minutes"] != "not recorded" else f"documented MDM level {e['documented_mdm_level']}, minutes not recorded")
        lines.append(f"{cid}: " + "; ".join(bits) + ".")
    return lines


NEXT_STEPS = {
    UPCODING: [
        "Request the full records for the cited claims and have a certified coder re-score each against current E/M documentation rules (medical decision making or total time).",
        "If the re-scoring confirms the pattern, use the sampling plan in the recovery packet to review a statistical sample of this provider's 99215 claims.",
        "Check whether notes for the cited claims look copied forward, and whether documented minutes repeat from visit to visit.",
    ],
    HIGH_ACUITY: [
        "Do not pursue recovery on this evidence: the documentation returned supports the level billed.",
        "Revisit if the provider's 99215 share keeps rising against peers, or if a larger records sample shows unsupported claims.",
    ],
    INCONCLUSIVE: [
        "Request records for a larger sample of this provider's 99214 and 99215 claims; what came back is too thin to judge.",
        "Re-screen the provider once the records arrive.",
    ],
}
CLOSING = {
    UPCODING: "This pattern is consistent with upcoding. It is a reason to review the records, not a finding.",
    HIGH_ACUITY: "This pattern is consistent with a high-acuity panel. The sampled documentation supports the billed level.",
    INCONCLUSIVE: "The evidence does not support a call either way yet.",
}


def _rule_headline(packet, leaning):
    pid, row = packet["provider_id"], _row_99215(packet)
    if leaning == INCONCLUSIVE:
        return f"{pid}: too few returned records to judge"
    if leaning == UPCODING:
        if row and row["documented_claims"] >= MIN_DOCS_99215:
            return (f"{pid}: {row['documentation_does_not_support_billed_level']} of {row['documented_claims']} documented 99215 claims "
                    f"({row['unsupported_rate']:.0%}) are documented below the billed level")
        rows = [r for r in (packet.get("documentation_review") or {}).get("by_billed_level", []) if r["billed_cpt"] in ("99214", "99215")]
        n, k = sum(r["documented_claims"] for r in rows), sum(r["documentation_does_not_support_billed_level"] for r in rows)
        return f"{pid}: {k} of {n} documented 99214 and 99215 claims ({k / n:.0%}) are documented below the billed level" if n else f"{pid}: documentation below the billed level"
    if row:
        return f"{pid}: documented 99215 claims mostly support the level billed ({row['unsupported_rate']:.0%} below)"
    return f"{pid}: documentation supports the level billed"


def next_steps_21(packet, leaning, ids):
    """Next steps that depend on what records exist and name the claims and counts (issue 63). Version 2.1 and later."""
    d = packet.get("documentation_review")
    n = doc_total(packet)
    shown = ", ".join(ids[:3]) if ids else "the sampled claims"
    ns = (d or {}).get("note_signals") or {}
    if leaning == UPCODING:
        steps = [f"Request the full charts for {shown} and have a certified coder re-score each against the current E/M rules (medical decision making or total time).",
                 "If the re-scoring confirms the pattern, review the random sample in the recovery packet's sampling plan before any overpayment estimate; do not extrapolate from a targeted sample."]
        r = ns.get("rates") or {}
        if ns.get("notes", 0) >= MIN_NOTES_SIGNALS:
            steps.append(f"Look at the notes themselves: {r.get('problems', 0):.0%} address fewer problems than their level implies and {r.get('late', 0):.0%} were signed late; request the audit trail for {shown}.")
        return steps
    if leaning == HIGH_ACUITY:
        if n >= 5:
            row = _row_99215(packet)
            u = f" ({row['documentation_does_not_support_billed_level']} of {row['documented_claims']} documented 99215 claims below the billed level)" if row else ""
            return [f"Do not pursue recovery on this evidence: {n} charts came back and they support the level billed{u}.",
                    "Revisit if the 99215 share keeps rising against peers or a larger sample shows unsupported claims."]
        return [f"The case for a sicker panel is thin ({n} charts came back): request charts for {shown} before ruling out upcoding."]
    if d is None or n == 0:
        return [f"No usable charts yet: request a random sample of 30 charts, then a targeted sample of 99215s for {shown}.",
                "If the practice does not respond, record that non-response is not evidence of upcoding and decide whether the claims signal alone warrants more."]
    if n < 5:
        return [f"Only {n} charts came back: request a larger or targeted sample (for example {shown}) and follow up on any deficiency the practice reported."]
    return [f"{n} charts came back but do not settle it: request a targeted sample of 99215 charts, starting with {shown}.",
            "Re-check after the targeted charts arrive; do not call upcoding or a sicker panel on this evidence alone."]


def assemble(packet, leaning, headline=None, interpretation=None, version="2.0"):
    """Build the final summary dict (the five schema keys). headline and interpretation come from the model for ambiguous
    cases, else from code."""
    ids = pick_citations(packet, leaning)
    parts = facts(packet)
    parts.append(interpretation.strip() if interpretation else CLOSING[leaning])
    if ids:
        parts.append("Examples: " + " ".join(evidence_lines(packet, ids)))
    steps = next_steps_21(packet, leaning, ids) if version == "2.1" else NEXT_STEPS[leaning]
    return {"headline": headline or _rule_headline(packet, leaning), "leaning": leaning,
            "rationale": " ".join(parts), "cited_claim_ids": ids, "next_steps": steps}


# ---- compact card -------------------------------------------------------------------------------------------------

def _table(cols, rows):
    return {"cols": cols, "rows": rows}


def to_card(packet):
    """Compact, derived-numbers-first card for the model. Tables are {cols, rows}; keys are not repeated per row."""
    n, share = packet["n_claims"], packet["share_99215"]
    exp = packet["expected_share_given_patient_complexity"]
    card = {"provider": packet["provider_id"], "claims": n, "patients": packet["n_patients"], "mix": packet["billed_mix"],
            "share_99215": round(share, 4), "expected_share": round(exp, 4),
            "excess_99215_claims": round(share * n - exp * n, 1), "ratio_to_expected": round(share / exp, 2) if exp else None,
            "risk_adjusted_score": packet["risk_adjusted_score"], "z_vs_peers": packet["z_vs_peers"],
            "low_complexity_share_of_99215": (round(low_complexity_share_of_99215(packet), 3)
                                              if low_complexity_share_of_99215(packet) is not None else None),
            "by_complexity": _table(["conditions", "visits", "n_99215", "share", "all_provider_share"],
                                    [[r["chronic_conditions"], r["visits"], r["n_99215"], r["provider_99215_share"],
                                      r["all_provider_99215_share"]] for r in packet["99215_share_by_patient_complexity"]])}
    cols = ["claim_id", "cpt", "patient", "age", "n_cond", "conditions", "dx"]

    def rows(key):
        return [[c["claim_id"], c["cpt"], c["patient_id"], c["age"], c["chronic_conditions"], c["conditions"],
                 c["diagnosis_codes"]] for c in packet.get(key, [])]
    card["claims_99215_low_complexity"] = _table(cols, rows(LOW_KEY))
    card["claims_99215_high_complexity"] = _table(cols, rows(HIGH_KEY))
    card["claims_other_codes"] = _table(cols, rows(COMPARE_KEY))
    d = packet.get("documentation_review")
    if d:
        card["documentation"] = {
            "documented_claims": d["claims_with_documentation"], "share_documented": d["share_of_claims_documented"],
            "by_billed_level": _table(["billed", "documented", "below_billed", "rate", "all_provider_rate"],
                                      [[r["billed_cpt"], r["documented_claims"], r["documentation_does_not_support_billed_level"],
                                        r["unsupported_rate"], r["all_provider_unsupported_rate"]] for r in d["by_billed_level"]]),
            "examples_below_billed": _table(["claim_id", "billed", "mdm", "minutes"],
                                            [[e["claim_id"], e["billed_cpt"], e["documented_mdm_level"], e["documented_minutes"]]
                                             for e in d["examples_documentation_below_billed_level"]]),
            "examples_99215_supported": _table(["claim_id", "billed", "mdm", "minutes"],
                                               [[e["claim_id"], e["billed_cpt"], e["documented_mdm_level"], e["documented_minutes"]]
                                                for e in d["examples_99215_documentation_supports"]])}
        if d.get("note_signals"):
            card["documentation"]["note_signals"] = d["note_signals"]
        if "documented_data_reviewed_moderate_or_higher" in d:
            card["documentation"]["data_reviewed_moderate_plus"] = d["documented_data_reviewed_moderate_or_higher"]
            card["documentation"]["of_those_no_lab_on_claim"] = d["of_those_with_no_lab_or_test_line_on_the_claim"]
    return card


def card_json(packet):
    return json.dumps(to_card(packet), separators=(",", ":"))
