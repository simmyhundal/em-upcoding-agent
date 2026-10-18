"""Judge j3.3: the deterministic rule judge of release 3 (issue 99). j3.2 (`eval/judge_rules_32.py`) is frozen and unchanged; this file reuses it and changes one thing.

Why a new version: release 3 (workflow v2.3, agent v3.3) can lean upcoding on cloned-notes signs although the returned charts support the billed level. j3.2's
evidence tiers cannot express that case: it sorts it as "charts support billing" and deducts 1.5 ("upcoding leaning although the charts support the billed level")
from every such summary, so the judge penalised the very feature release 3 added (11 of 73 upcoding calls in the release 3 test, 5 of 38 for the workflow).

What j3.3 changes (everything else is j3.2, including the checklist and every other deduction):
1. A new evidence tier, **cloning signs**: at least 8 returned notes, the 99215 share more than 3 times expected, and late signatures at 12% or more or, with an audit
   trail, bulk-created or paste-heavy notes at 8% or more (the same thresholds as rules 2.3, so the tier is not independent of the writer, as j3.2 says of its inflated tier).
   It sits after "charts show upcoding" and before the problems-based "notes look inflated" tier.
2. On that tier an upcoding leaning is supported (no "overstated" deduction), but the text must state the basis (late signatures or the audit-trail signs): otherwise 1.0.
   An inconclusive leaning deducts 1.0 ("understated_leaning", as for charts that show upcoding); a high-acuity leaning deducts 1.5 ("overstated").
Judges never change after use: this ships as j3.3 and results record the version beside each score.

Usage: python eval/judge_rules_33.py DATA_DIR FLAGGED_CSV CHECKED_SUMMARIES_JSONL OUT_JSONL [--run-dir RUN]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
import judge_rules_32 as j32  # noqa: E402
import summary_rules as sr  # noqa: E402

VERSION = "j3.3"
TIERS = j32.TIERS[:2] + ("cloning_signs",) + j32.TIERS[2:]
CHECKLIST = j32.CHECKLIST
BASIS = re.compile(r"signed late|late signature|late[- ]entry|late[- ]sign|audit trail|bulk|paste", re.I)


def has_cloning_signs(packet):
    ns = (packet.get("documentation_review") or {}).get("note_signals")
    if not (ns and ns["notes"] >= sr.MIN_NOTES_SIGNALS and j32.ratio(packet) > sr.MAX_EXCESS_FOR_ACUITY):
        return False
    r = ns["rates"]
    return (r.get("late") or 0) >= sr.INFLATED_LATE or bool(ns.get("audit_trail_received") and ((r.get("bulk_created") or 0) >= sr.INFLATED_AUDIT
                                                                                           or (r.get("paste_heavy") or 0) >= sr.INFLATED_AUDIT))


def evidence_tier(packet):
    tier = _evidence_tier_32(packet)
    if tier in ("notes_look_inflated", "charts_support_billing", "mixed") and has_cloning_signs(packet):
        return "cloning_signs"
    return tier


def strength_problems(sm, packet):
    if evidence_tier(packet) != "cloning_signs":
        return _strength_problems_32(sm, packet)
    out, lean = [], sm["leaning"]
    text = " ".join([sm["headline"], sm["rationale"]])
    if lean == sr.UPCODING:
        if not BASIS.search(text):
            out.append(("basis_not_stated", 1.0, "upcoding leaning on cloning signs, but the text never states the late-signature or audit-trail basis"))
        elif not j32.HEDGE.search(text + " " + " ".join(sm["next_steps"])):
            out.append(("no_hedge", 0.5, "upcoding leaning without hedging language"))
    elif lean == sr.HIGH_ACUITY:
        out.append(("overstated", 1.5, "high-acuity leaning although the notes show cloning signs"))
    elif lean == sr.INCONCLUSIVE:
        out.append(("understated_leaning", 1.0, "inconclusive although the notes show cloning signs"))
    if j32.CERTAIN.search(text):
        out.append(("certainty", 0.5, f"certainty wording ('{j32.CERTAIN.search(text).group(0)}') on cloning signs"))
    return out


_evidence_tier_32, _strength_problems_32 = j32.evidence_tier, j32.strength_problems


class _Patched:
    """j3.2's scoring code looks the tier and the strength check up by module-level name; swap them for the duration of a call."""

    def __enter__(self):
        self.saved = (j32.evidence_tier, j32.strength_problems, j32.VERSION, j32.TIERS)
        j32.evidence_tier, j32.strength_problems, j32.VERSION, j32.TIERS = evidence_tier, strength_problems, VERSION, TIERS

    def __exit__(self, *a):
        j32.evidence_tier, j32.strength_problems, j32.VERSION, j32.TIERS = self.saved


def score_summary(record, packet, evidence="", facts=None, dq_flagged=None):
    with _Patched():
        return j32.score_summary(record, packet, evidence, facts, dq_flagged)


def run(data_dir, flagged_csv, checked_path, out_path, run_dir=None, with_docs=True):
    with _Patched():
        return j32.run(data_dir, flagged_csv, checked_path, out_path, run_dir, with_docs)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    for n in ("data_dir", "flagged_csv", "checked_summaries", "out_jsonl"):
        ap.add_argument(n)
    ap.add_argument("--run-dir")
    ap.add_argument("--no-docs", action="store_true")
    a = ap.parse_args()
    rows = run(a.data_dir, a.flagged_csv, a.checked_summaries, a.out_jsonl, a.run_dir, not a.no_docs)
    sc = [r["score"] for r in rows]
    print(f"{len(rows)} summaries, mean {sum(sc) / len(sc):.2f}, distribution {[sc.count(k) for k in range(1, 6)]}")
